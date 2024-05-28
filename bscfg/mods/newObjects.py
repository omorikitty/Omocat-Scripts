import bs,random,bsUtils,bsMap, bsGame,bsBomb,bsSpaz, bsVector,weakref
from bsUtils import Background,animate

def _haveNewProOptions():
    return True
bsUtils._haveProOptions = _haveNewProOptions

#Maybe in the future, but no for now
#def _haveNewPro():
#    return True
#bsUtils._havePro = _haveNewPro

# def newBackgroundInit(self, fadeTime=500, startFaded=False, showLogo=False):
#         bs.Actor.__init__(self)
#         self._dying = False
#         self.fadeTime=fadeTime
#         session = bs.getSession()
#         self._session = weakref.ref(session)
#         with bs.Context(session):
#             self.node = bs.newNode('image', delegate=self, attrs={
#                 'fillScreen':True,
#                 'texture':bs.getTexture('bg'),
#                 'tiltTranslate':-0.3,
#                 'hasAlphaChannel':False,
#                 'color':(1, 1, 1)})
#             if not startFaded:
#                 animate(self.node, 'opacity',
#                         {0:0, self.fadeTime:1}, loop=False)
#             if showLogo:
#                 logoTexture = bs.getTexture('sMPlogo')#logo
#                 logoModel = bs.getModel('smpLogo') #logo
#                 logoModelTransparent = bs.getModel('smpLogo')#logoTransparent
#                 self.logo = bs.newNode('image', owner=self.node, attrs={
#                     'texture':logoTexture,
#                     'modelOpaque':logoModel,
#                     'modelTransparent':logoModelTransparent,
#                     'scale':(0.7, 0.7),
#                     'vrDepth':-250,
#                     'color':(0.15, 0.15, 0.15),
#                     'position':(0, 0),
#                     'tiltTranslate':-0.05,
#                     'absoluteScale':False})
#                 self.node.connectAttr('opacity', self.logo, 'opacity')
#                 if not bs.getEnvironment()['vrMode']:
#                     self.c = bs.newNode('combine', owner=self.node,
#                                         attrs={'size':2})
#                     for attr in ['input0', 'input1']:
#                         animate(self.c, attr, {0:0.693, 50:0.7, 500:0.693},
#                                 loop=True)
#                     self.c.connectAttr('output', self.logo, 'scale')
#                     c = bs.newNode('combine', owner=self.node, attrs={'size':2})
#                     c.connectAttr('output', self.logo, 'position')
#                     keys = {}
#                     time = 0
#                     for i in range(10):
#                         keys[time] = (random.random()-0.5)*0.0015
#                         time += random.random() * 100
#                     animate(c, "input0", keys, loop=True)
#                     keys = {}
#                     time = 0
#                     for i in range(10):
#                         keys[time] = (random.random()-0.5)*0.0015 + 0.05
#                         time += random.random() * 100
#                     animate(c, "input1", keys, loop=True)
# Background.__init__ = newBackgroundInit

class SpikesFactory(object):
    def __init__(self):
        self.puasModel = bs.getModel('flash')
        
        self.puasTex = bs.getTexture('bg')            
            
        self.impactBlastMaterial = bs.Material()
        self.impactBlastMaterial.addActions(
            conditions=(('weAreOlderThan',200),
                        'and',('theyAreOlderThan',200),
                        'and',('evalColliding',),
                        'and',(('theyHaveMaterial',bs.getSharedObject('footingMaterial')),
                               'or',('theyHaveMaterial',bs.getSharedObject('objectMaterial')))),
            actions=(('message','ourNode','atConnect',ImpactMessage())))
            
        self.bounceMaterial = bs.Material()     
        self.bounceMaterial.addActions(
            conditions=(('theyHaveMaterial',bs.getSharedObject('footingMaterial'))),
            actions=(('modifyPartCollision','collide',True),
                     ('modifyPartCollision','physical',True),
                     ('message','ourNode','atConnect',BounceMessage())))
        self.bounceMaterial.addActions(actions=( ("modifyPartCollision","friction",-2)))

class ImpactMessage(object):
    pass
    
class BounceMessage(object):
    pass


class FlyBot(bs.Actor):

    def __init__(self, pos = (0,4,0), vel = (0,0,0)):
        bs.Actor.__init__(self)
        
        self.speedMul = 1.0
        self.hp = 100
        self.x, self.y, self.z = pos
        # Our 'base'
        self.touchedSound = bs.getSound('error')
        # DON'T TOUCH THE CHILD!!!!!1!!!1!!11!!
        self.tex1 = bs.getTexture('landMine')
        self.tex2 = bs.getTexture('landMineLit')

        self.node = bs.newNode('prop',
                               delegate = self,
                               attrs={
                                   'position':pos,
                                   'velocity':vel,
                                   'body':'sphere',
                                   'model':bs.getModel('bomb'),
                                   'shadowSize':0.3,
                                   'colorTexture':self.tex1,
                                   'materials':[bs.getSharedObject('objectMaterial')],
                                   'extraAcceleration':(0,20,0)})

        bs.gameTimer(1000, bs.Call(self._update), True)
        self.textureSequence = \
                bs.newNode('textureSequence', owner=self.node, attrs={
                    'rate':100,
                    'inputTextures':(self.tex1, self.tex2)})
        
        
    def _update(self):
        if not self.node.exists(): return
        xv, yv, zv = (0,20,0)

        if self.x < self.node.position[0]:
            xv -= 5 * self.speedMul
        if self.x > self.node.position[0]:
            xv += 5 * self.speedMul
        if self.y < self.node.position[1]:
            yv -= 5 * self.speedMul
        if self.y > self.node.position[1]:
            yv += 5 * self.speedMul 
        if self.z < self.node.position[2]:
            xv -= 5 * self.speedMul 
        if self.z > self.node.position[2]:
            zv += 5 * self.speedMul

        self.node.extraAcceleration = (xv, yv, zv)

    def handleMessage(self, m):
        if not self.node.exists(): return
        if isinstance(m, bs.OutOfBoundsMessage):
            self.node.delete()
        elif isinstance(m, bs.DieMessage):
            self.node.delete()

        # TODO - add functoional for speed-up on picked up
        elif isinstance(m, bs.PickedUpMessage):
            bs.Blast(position = self.node.position, blastType = 'impact',
                     blastRadius = 0.8).autoRetain()
            bs.playSound(self.touchedSound, position = self.node.position,
                         volume = 4)
            self.x, self.y, self.z = m.node.position
            # I SAID DON'T TOUCH!
            self.speedMul = 3.0
            self.hp -= 10 + random.randint(-3,3)
            if self.hp < 0:
                bs.Blast(position = self.node.position, blastRadius = 0.5,
                         blastType = 'tnt')
                self.handleMessage(bs.DieMessage())
        elif isinstance(m, bs.DroppedMessage):
            self.speedMul = 1.0
        else:
            bs.Actor.handleMessage(self, m)     

class Puas(bs.Actor):
    def __init__(self,position=(0,0,0),velocity = (0,0,0),owner = None,sourcePlayer = None,expire = True,hit = True):
    
        bs.Actor.__init__(self)
        
        factory = self.getFactory()

        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={'position':position,
                                      'velocity':velocity,
                                      'model':factory.puasModel,
                                      'lightModel':factory.puasModel,
                                      'body':'crate',
                                      'modelScale':0.35,
                                      'shadowSize':0.2,                                       
                                      'colorTexture':factory.puasTex,
                                      'materials':(factory.impactBlastMaterial,bs.getSharedObject('objectMaterial'))})
                                      
        if owner is None: owner = bs.Node(None)

        self.hit = hit
        self.owner = owner
        self.expire = expire
                                      
    @classmethod
    def getFactory(cls):
        activity = bs.getActivity()
        try: return activity._sharedSpikesFactory
        except Exception:
            f = activity._sharedSpikesFactory = SpikesFactory()
            return f

            
    def handleMessage(self,m):
        if isinstance(m,bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        if isinstance(m,bs.OutOfBoundsMessage):
            if self.node.exists():
                self.node.delete()
        if isinstance(m,ImpactMessage):
            node = bs.getCollisionInfo("opposingNode")
            if self.hit == True and not node is self.owner:
                bs.Blast(position = self.node.position,hitType = 'punch',blastRadius = 1).autoRetain()
            if self.expire == True:
                if self.node.exists():
                    self._lifeTime = bs.Timer(20000,bs.WeakCall(self.animBR))
                    self._clrTime = bs.Timer(20310,bs.WeakCall(self.clrBR))
            
    def animBR(self):
        if self.node.exists():
            bs.animate(self.node,"modelScale",{0:1,200:0})
        
    def clrBR(self):
        if self.node.exists():
            self.node.delete()
        
class MagneticZone(bs.Actor):
    def __init__(self,position = (0,1,0),scale = 10,infinity = False,owner = None):
        bs.Actor.__init__(self)
        self.shields = []
        
        self.position = (position[0],position[1],position[2])
        self.scale = scale
        self.suckObjects = []
        self.owner = owner
        
        self.blackHoleMaterial = bs.Material()
        self.suckMaterial = bs.Material()
                                                  
        self.suckMaterial.addActions(conditions=(('theyHaveMaterial', bs.getSharedObject('objectMaterial'))),
                                                      actions=(("modifyPartCollision","collide",True),
                                                      ("modifyPartCollision","physical",False),
                                                      ("call","atConnect", self.touchedObjSuck)))
                              
        self.suckRadius = bs.newNode('region',
                       attrs={'position':(self.position[0],self.position[1],self.position[2]),
                              'scale':(scale,scale,scale),
                              'type':'sphere',
                              'materials':[self.suckMaterial]})
                              
        
        if not infinity: self._dieTimer = bs.Timer(20000,bs.WeakCall(self.finish))
        bsUtils.animateArray(self.suckRadius,"scale",3,{0:(0,0,0),300:(self.scale*8,self.scale*8,self.scale*8)},True)
        
    def finish(self):
        self.suckRadius.delete()
        self.suckRadius.handleMessage(bs.DieMessage())
        for i in self.suckObjects:
            if i.exists(): i.extraAcceleration = (0,0,0)
        
    def touchedObjSuck(self):
        node = bs.getCollisionInfo('opposingNode')
        if node.getNodeType() in ['prop']:#,'bomb']:
            self.suckObjects.append(node)

        if self.owner.exists():
            for i in self.suckObjects:
                if i.exists(): i.extraAcceleration = ((self.owner.position[0] - i.position[0])*6,(self.owner.position[1] - i.position[1])*6,(self.owner.position[2] - i.position[2])*6)
        else: self.finish()
                               
class VolcanoEruption(bs.Actor):
    def __init__(self, position=(0,0,0)):
        bs.Actor.__init__(self)

        self.position = position
        bs.gameTimer((random.randrange(20000,40000)),self.startEruption)
        
    def startEruption(self):
        bs.playSound(bs.getSound('alarm'))
        bsUtils.animateArray(bs.getSharedObject('globals'),'tint',3,{0:bs.getSharedObject('globals').tint,500:(1,0,0),1000:bs.getSharedObject('globals').tint,
                                                                     1500:bs.getSharedObject('globals').tint,2000:(1,0,0),2500:bs.getSharedObject('globals').tint,
                                                                     3000:bs.getSharedObject('globals').tint,3500:(1,0,0),4000:bs.getSharedObject('globals').tint})
        self.rain = bs.Timer(200,bs.WeakCall(self.dropB),repeat = True)
        bs.gameTimer(20000,self.endEruption)
        
    def endEruption(self):
        self.rain = None
        bs.gameTimer((random.randrange(20000,40000)),self.startEruption)

    def dropB(self):
        vel = ((random.randrange(-8,8)),(random.randrange(10,13)),(random.randrange(-6,6)))
        bs.Bomb(position=self.position,velocity=vel,bombType = 'lava').autoRetain()

class Portal(bs.Actor):
    def __init__(self, pos=(0,0,0),pos2=(0,0,0),size=1):
        bs.Actor.__init__(self)

        self.pos = pos
        self.pos2 =(pos2[0],pos2[1]-0.56,pos2[2])
        self.size = (size,size,size)
        
        self.playMaterial = bs.Material()
        self.playMaterial.addActions(
            conditions=("theyHaveMaterial",bs.getSharedObject('playerMaterial')),
            actions=(("modifyPartCollision","collide",True),
                     ("modifyPartCollision","physical",False),
                     ("call","atConnect",self.teleport)))
                     
        self.portal = bs.NodeActor(bs.newNode('region',attrs={'position':self.pos,
                      'scale':self.size, 'type': 'sphere',
                      'materials':(self.playMaterial,)}))
        
    def teleport(self):
        playerNode = bs.getCollisionInfo('opposingNode')
        try: player = playerNode.getDelegate().getPlayer()
        except Exception: player = None
        if player.exists():
            player.actor.node.handleMessage(bs.StandMessage(position = self.pos2))
        
class FireZone(bs.Actor):
    def __init__(self, position=(0,0,0),end=True,scale=1,owner=None):
        bs.Actor.__init__(self)
        
        self.scale = scale
        self.position = position
        self.end = end
        self.owner = owner
        
        self.fireMaterial = bs.Material()
        self.fireMaterial.addActions(conditions=(('theyHaveMaterial', bs.getSharedObject('objectMaterial'))),
                                                      actions=(("modifyPartCollision","collide",True),
                                                      ("modifyPartCollision","physical",False),
                                                      ("call","atConnect",self.burn)))
        
        self.node = bs.newNode('region',
                       attrs={'position':self.position,
                              'scale':(scale,scale,scale),
                              'type':'sphere',
                              'materials':[self.fireMaterial],})
        self.startFire()
                              
    def startFire(self):
        self.flames = bs.Timer(100,bs.WeakCall(self.setFlame),repeat = True)
        if self.end: bs.gameTimer(10000,self.endFire)
        
    def setFlame(self):
        if self.node.exists():
            bs.emitBGDynamics(position=self.position,velocity=(0,5,0),count=100,spread=self.scale*0.4,scale=3,chunkType='sweat');
        
    def endFire(self):
        self.flames = None
        if self.node.exists(): self.node.delete()
        
    def burn(self):
        node = bs.getCollisionInfo("opposingNode")
        t = self.node.position
        mag = 0.6
        node.handleMessage(bs.HitMessage(pos=t, velocity=(0,0,0),
                                        magnitude=mag,   hitType='punch',
                                        hitSubType='superPunch', radius=self.scale*0.4,
                                        sourcePlayer=self.owner))
                                        
class Firework(bs.Actor):
    def __init__(self,pos=(0,0,0),vel = (0,0,0),time=1500,spread=1.0,sound=False,color=None):
    
        bs.Actor.__init__(self)
        self.tex = bs.getTexture('white')
        self.model = bs.getModel('flash')
        self.upSound = bs.getSound('frostyFall')
        self.explodeSounds = (bs.getSound('explosion01'),
                              bs.getSound('explosion02'),
                              bs.getSound('explosion03'),
                              bs.getSound('explosion04'),
                              bs.getSound('explosion05'))
        self.spread = spread
        if not color is None: self._color = color
        else: self.color = (random.random()*2,random.random()*2,random.random()*2)

        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={'position':pos,
                                      'velocity':vel,
                                      'model':self.model,
                                      'body':'sphere',
                                      'modelScale':0.1,
                                      'shadowSize':0.2,
                                      'gravityScale':-1,
                                      'colorTexture':self.tex,
                                      'materials':[bs.getSharedObject('objectMaterial')]})
        self._trailTimer = bs.Timer(10,bs.WeakCall(self.addTrail),repeat=True)
        if sound:
            self._sound = bs.newNode('sound',attrs={'sound':self.upSound,'volume':1.0})
            self.node.connectAttr('position',self._sound,'position')
        else: self._sound = None
        bs.gameTimer(int(time),self.doFireworks)
        
    def addTrail(self):
        if self.node.exists():
            bs.emitBGDynamics(position=self.node.position,velocity=(0,1,0),count=random.randint(1,5),spread=0.05,scale=0.5,chunkType='spark')

    def doFireworks(self):
        if self.node.exists(): 
            bs.emitBGDynamics(position=self.node.position,velocity=(0,0,0),count=random.randint(1,5),spread=self.spread,scale=0.5,chunkType='spark')
        
            explosion = bs.newNode("explosion", attrs={'position':self.node.position,
                                   'velocity':(0,0,0), 'radius':self.spread*1,'big':True,})
            explosion.color = self.color
        
            light = bs.newNode('light', attrs={
                'position':self.node.position,
                'volumeIntensityScale': 10.0,
                'color': self.color})
            iScale = 1.6
            lightRadius = self.spread
            s = random.uniform(0.6,0.9)
            bsUtils.animate(light,"intensity", {
                0:2.0*iScale, int(s*20):0.1*iScale,
                int(s*25):0.2*iScale, int(s*50):17.0*iScale, int(s*60):5.0*iScale,
                int(s*80):4.0*iScale, int(s*200):0.6*iScale,
                int(s*2000):0.00*iScale, int(s*3000):0.0})
            bsUtils.animate(light,"radius", {
                0:lightRadius*0.2, int(s*50):lightRadius*0.55,
                int(s*100):lightRadius*0.3, int(s*300):lightRadius*0.15,
                int(s*1000):lightRadius*0.05})
            bs.gameTimer(int(s*3000),light.delete)
            bs.gameTimer(2000,light.delete)
            
            bs.shakeCamera(intensity=0)
            
            bs.gameTimer(1000,explosion.delete)
            self._sound = None
            self.node.delete()
            ambientColors = {
                0: (1.06, 1.04, 1.03), 120: (8, 8, 8),
                280+random.randint(50, 220): (1.06, 1.04, 1.03)
            }

            bs.animateArray(
                bs.getSharedObject('globals'), 'ambientColor',
                3, ambientColors)

    def handleMessage(self,m):
        if isinstance(m,bs.OutOfBoundsMessage):
            if self.node.exists():
                self.node.delete()
