# -*- coding: utf-8 -*-
import floater
import bsGame
import bsUtils
import bsInternal
import random
import bs
import some
import json
from thread import start_new_thread
from bs4 import BeautifulSoup
import bsScoreBoard
import weakref
import bsElimination
import portalObjects
import handle
import DB_Manager as db
import datetime
#import pytz
import mystats
import urllib2
import bsSpaz
import math
import zenpayEvent
from bsSpaz import _PunchHitMessage



topsName = []

#print(help(bsInternal.newActivity))

class CrazyBot(bsSpaz.MelBot):
    character = 'Taobao Mascot'
    throwRate = 4.0
    defaultBombCount = 5

    def handleMessage(self, m):
        super(self.__class__, self).handleMessage(m)
        self._color = bs.Timer(100,
                               bs.WeakCall(self._changeColor),
                               repeat=True)

    def _changeColor(self):
        if self.isAlive():
            self.node.color = (random.random() * 2, random.random() * 2,
                               random.random() * 2)
            self.bombType = random.choice(['ice', 'normal', 'sticky'])


class BugBot(bsSpaz.NinjaBot):
    character = 'Pascal'
    throwiness = 0.4
    defaultBombType = 'tnt'

    def handleMessage(self, m):
        super(self.__class__, self).handleMessage(m)
        self._color = bs.Timer(10, bs.WeakCall(self._bug), repeat=True)

    def _bug(self):
        if self.isAlive():
            if self.run:
                self.node.run = 100


class PascalBot(bsSpaz.SpazBot):
    color = (0, 0, 3)
    highlight = (0.2, 0.2, 1)
    character = 'Pascal'
    bouncy = True
    run = True
    punchiness = 0.8
    throwiness = 0.1
    chargeSpeedMin = 0.3
    chargeSpeedMax = 0.5

    def handleMessage(self, m):
        if isinstance(m, _PunchHitMessage):
            node = bs.getCollisionInfo("opposingNode")
            try:
                node.handleMessage(bs.FreezeMessage())
            except Exception:
                print('Cant freeze')
            bs.playSound(bs.getSound('freeze'))
            super(self.__class__, self).handleMessage(m)
        else:
            super(self.__class__, self).handleMessage(m)



class StarLights(bs.Actor):
    def __init__(
        self,
        scale=0.07,
        bounds=(0,0,0),
        life=3000
    ):
        bs.Actor.__init__(self)
        self.scale = scale
        self.life = life
        model = bs.getModel('flash')
        texture = bs.getTexture('white')

        self.nocollision = bs.Material()
        self.nocollision.addActions(
            actions=("modifyPartCollision", "collide", False))

        self.node = bs.newNode('prop', attrs={
            'position': bounds,
            'model': model,
            'body': 'sphere',
            'bodyScale': 0.0,
            'modelScale': self.scale,
            'colorTexture': texture,
            'gravityScale': - 0.01,
            'reflection': 'soft',
            'reflectionScale': [2.0],
            'shadowSize': 1.0,
            'materials': (self.nocollision,)
        })

        bs.animate(self.node, "modelScale", {
            0: 0,
            self.life/2: self.scale,
            self.life: 0
        }, loop=True)

        self.light = bs.newNode("light", owner=self.node, attrs={
            "color": (0.8, 0.6, 0.2),
            "radius": 0.07,
            "intensity": 1.0,
            "volumeIntensityScale": 10
        })
        self.node.connectAttr("position", self.light, "position")

    def handleMessage(self, m):
        self._handleMessageSanityCheck()
        if isinstance(m, bs.DieMessage):
            if m.immediate:
                if self.node.exists():
                    self.node.delete()
                    #print("delete xd")
            else:
                # Para que no se note que desaparecen de la nada
                # agregamos una animacion donde se aprecie mejor
                # como se marchita...
                if self.node.exists():
                    bs.animate(self.node, "modelScale", {
                        0: self.node.modelScale,
                        self.life: 0
                    })
                    bs.gameTimer(self.life, self.node.delete)
                if self.light.exists():
                    bs.animate(self.light, "intensity", {
                        0: self.light.intensity,
                        self.life: 0
                    })
                    bs.gameTimer(self.life, self.light.delete)
                    #print("nodo eliminado")
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.handleMessage(bs.DieMessage(immediate=True))
        else:
            bs.Actor.handleMessage(self, m)


def Ladeborads(ranks=None):
    global topsName
    save = []
    if ranks is None:
        return
    for rank in ranks:
        url = 'http://bombsquadgame.com/accountquery?id=' + rank
        response = json.loads(urllib2.urlopen(urllib2.Request(url)).read())
        if response is not None:
            try:
                soup = BeautifulSoup(response["name_html"], "html.parser")
                name_html = soup.getText()
            except ValueError:
                save.append('-')
            else:
                save.append(name_html)

    topsName = save

start_new_thread(Ladeborads, (some.ranks[0:10],))


def onTransitionIn(self, music=None):
    """
    Method override; optionally can
    be passed a 'music' string which is the suggested type of
    music to play during the game.
    Note that in some cases music may be overridden by
    the map or other factors, which is why you should pass
    it in here instead of simply playing it yourself.
    """

    bs.Activity.onTransitionIn(self)

    colo = (random.uniform(0.5, 3), random.uniform(0.5,
                                                   3), random.uniform(0.5, 3))
    if some.show_texts:
        m = [
            ("Scripts Made By: Logic\nHosting Provider: {}").format(some.host),
            ("Asking For Adminship Can Get You Kicked"),
            (u"Mail Your Suggestions/Contributions On \n awesomelogix@gmail.com"
             ), (u"All Chats, Name & ID's Are Being Logged..."),
            ("This Party Has An Abusive Filter\nWith Over 600 Filtered Words"),
            ("Stats Get Reset Every Monday!\nPoints Are Not Affected"),
            (u"Join RAGE On Discord To Get Server Address!\nLink: https://bit.ly/awesomelogic"
             ),
            (u"For The Best Gaming Experience,\nNight Mode Will Automatically Turn On At 8PM Till 7AM"
             ),
            ("Swipe From Punch To Jump To Perform A Backflip\nLong Press Bomb Button To Toggle It!"
             ), ("Thanks For Playing!\nHave Fun And Play Ethically!")
        ]
    else:
        m = ['']
    self.myName = bsUtils.Text(
        random.choice(m),
        vAttach='bottom',
        hAlign='center',
        shadow=1.0,
        position=(0, 140) if self.getName() == "Elimination" else
        (0, 100) if self.getName() == "BombSpot" else (0, 50),
        color=colo,
        maxWidth=350)

    po = self.myName.node.position

    obj = bsUtils.Text(bs.getSpecialChar('logoFlat'),
                       position=(po[0] + 325, po[1] + 0),
                       vAttach='bottom',
                       color=colo,
                       hAlign='center',
                       vAlign='center',
                       scale=1.5 if some.show_texts else 0).autoRetain()

    obj1 = bsUtils.Text(bs.getSpecialChar('logoFlat'),
                        position=(po[0] - 325, po[1] + 0),
                        vAttach='bottom',
                        color=colo,
                        hAlign='center',
                        vAlign='center',
                        scale=1.5 if some.show_texts else 0).autoRetain()

    def animate():
        self.myName.node.text = random.choice(m)

    def getcolors():
        """
        esta funcion devulve un
        color aleatorio
        """
        colors = [0, 1, 2]
        return (random.choice(colors),
                random.choice(colors),
                random.choice(colors))


    def cyberPunkLights():
        positionMap = [(-6, 7, -2.5), (6, 7, -2.5), (0, 7, -6), (0, 7, 4), (0, 7, -4), (-6, 7, 3), (6, 7, 3)]
        for pos in positionMap:
            nodeLight = bs.newNode('light',
                                    attrs={
                                        'position': pos,
                                        'color': getcolors(),
                                        'intensity': 0.4 if some.night else 0.01,
                                        'volumeIntensityScale': 1.0 if some.night else 0.5
                                    })
            bs.animate(nodeLight, 'radius', {0:0, 500:0.5})

    bs.gameTimer(
        1000, bs.Call(cyberPunkLights))
    def animate3():
        bs.animate(self.myName.node, 'opacity', {0: 1, 1000: 0, 2000: 1})
        bs.animate(obj.node, 'opacity', {0: 1, 1000: 0, 2000: 1})
        bs.animate(obj1.node, 'opacity', {0: 1, 1000: 0, 2000: 1})
        bs.gameTimer(1000, animate)

    animate3()
    bs.animate(obj.node, 'rotate', {0: 0.0, 3000: 360.0}, loop=True)
    bs.animate(obj1.node, 'rotate', {0: 0.0, 3000: 360.0}, loop=True)
    bs.animate(self.myName.node,
               'scale', {
                   0: 1.25,
                   1000: 1.30,
                   2000: 1.25
               },
               loop=True)
    bs.gameTimer(9000, animate3, repeat=True)

    self.version = bs.NodeActor(
        bs.newNode('text',
                   attrs={
                       'vAttach': 'bottom',
                       'vAlign': 'bottom',
                       'hAttach': 'left',
                       'hAlign': 'left',
                       'flatness': 1.0,
                       'opacity': 1.0,
                       'shadow': 0.5,
                       'color': (0.5, 0.5, 0.5, 0.7),
                       'scale': 0.7,
                       'position': (10, 10),
                       'text': bsUtils._gServerConfig.get('partyName', '') + ('\n' + 'Scripts Available At: https://github.com/Awesome-Logic/') #if some.is_logic else ''
                   }))
    self.version2 = bs.NodeActor(
        bs.newNode('text',
                   attrs={
                       'vAttach': 'bottom',
                       'vAlign': 'bottom',
                       'hAttach': 'right',
                       'hAlign': 'right',
                       'flatness': 1.0,
                       'opacity': 1.0,
                       'shadow': 0.5,
                       'color': (0.5, 0.5, 0.5, 0.7),
                       'scale': 0.7,
                       'position': (-10, 10),
                       'text':
                       '{}\nScripts By: Awesome-Logic\nHosting By: {}'.format(
                        datetime.datetime.now().strftime("%d-%m-%Y"), some.host)
                   }))



    # txt = '\n'.join(open(some.flyfile).read().split('\n'))
    # animateText = bsUtils.Text('/torneo',
    #    position=(0, 285),
    #    hAlign='center',
    #    vAlign='top',
    #    flatness=1.0,
    #    maxWidth=180,
    #    color=colo,
    #    transition='inLeft',
    #    scale=1.0,
    #    #transitionOutDelay=8000,
    #    shadow=1.0,
    #    transitionDelay=1000).autoRetain()


    # Para hacerlo un poco mas flexible...
    showRanks = 3
    if len(topsName) >= showRanks:
        pos = (-600, -115)
        positionOffset = [(0, -35*i) for i in range(showRanks)]
        for i in range(showRanks):
            topsText = bs.getSpecialChar('trophy1')+"#"+str(i + 1)+ topsName[i]
            top = bsUtils.Text(topsText,
                position=(pos[0] + positionOffset[i][0], pos[1] + positionOffset[i][1]),
                hAlign='left',
                vAttach='top',
                scale=0.6,
                color=(2,2,0),
                vAlign='bottom').autoRetain()



    # make our map
    self._map = self._mapType()

    # give our map a chance to override the music
    # (for happy-thoughts and other such themed maps)
    overrideMusic = self._mapType.getMusicType()
    if overrideMusic is not None:
        music = overrideMusic

    if music is not None:
        bs.playMusic(music)


def starGenerator(self, maxStar=10):
    """Genera las particulas de estrella"""

    # Cuando las estrellas sobren
    # Borralas!!
    if len(self.stars) > maxStar:
        for i in self.stars:
            if i.exists():
                i.handleMessage(bs.DieMessage(immediate=False))
        self.stars = []
    else:
        for _ in xrange(maxStar):
            bounds = self.getMap().getDefBoundBox("levelBounds")
            position = (
                random.uniform(bounds[0], bounds[3])*0.9,
                random.uniform(bounds[1], bounds[4]),
                random.uniform(bounds[2], bounds[5])*0.9
            )
            star = StarLights(bounds=position, scale=0.09).autoRetain()
            self.stars.append(star)

def onTransitionOut(self):
    bs.Activity.onTransitionOut(self)
    # self.star.stop()
    # self.star=None
    self.starTime = None


bsGame.GameActivity.lastBountyPlayerName = None
def getBounty(self):
    """Escoge una victima al azar"""
    players = []
    for p in self.players:
        players.append(p)
    bounty = random.choice(players)
    return bounty

def _chooseAnimatePlayer(self):
    player = self.getBounty()
    icon = player.getIcon()
    outlineTex = bs.getTexture('characterIconMask')
    texture = icon['texture']
    self._image = bs.NodeActor(bs.newNode('image',
                   attrs={'texture':texture,
                   'tintTexture':icon['tintTexture'],
                   'tintColor':icon['tintColor'],
                   'tint2Color':icon['tint2Color'],
                   'maskTexture':outlineTex,
                   'position':(70,80),'rotate':0,
                   'scale':(80,80), 'opacity':1.0,
                   'absoluteScale':True,'attach':'bottomLeft'}))
    if self._choseText.exists():
        self._choseText.text = player.getName()
        self._choseText.color = player.highlight
    #if self._rewardText.exists(): self._rewardText.text = "Reward:  " + str(reward)
    return player

def stopChoose(self):
    try:
        self._chooseSound = None
        self._chooseTime = None
        self._alarmSound = None
        player = self._chooseAnimatePlayer()
        if player.isAlive() and player.actor:
            if self.lastBountyPlayerName is None:
                reward = random.randint(50, 1000)
                self.lastBountyPlayerName = (player, reward)
            light = bs.newNode(
                    'light',
                    owner=player.actor.node,
                    attrs={"intensity": 0.6,
                           "heightAttenuated": False,
                           "volumeIntensityScale": 0.1, "radius":
                           0.13, "color": bs.getNormalizedColor(player.highlight)})

            bs.animate(light, 'intensity',
                       {0: 1.0, 200: 0.4, 400: 1.0},
                       loop=True)
            player.actor.node.connectAttr(
                'position', light, 'position')
            #_chooseLight(player)
            bs.playSound(bs.getSound("cashRegister"))
            bs.screenMessage(
                u"ALERT!!!: {} Has Been Choosen".format(player.getName()),
                color=(2, 2, 0),
                transient=True)
            bs.screenMessage(
                u"A Reward For {}\ue01f Tickets.".format(str(reward)),
                color=(2, 2, 0),
                transient=True)
        else:
            self.startChoose()
    except Exception:
        bs.printException()


def startChoose(self):
    self._chooseSound =  bs.NodeActor(
        bs.newNode(
            'sound',attrs={'sound':bs.playSound(bs.getSound("warnBeep")),
            'volume':1.0
        }
    ))
    self._chooseTime = bs.Timer(80, bs.WeakCall(self._chooseAnimatePlayer), repeat=True)
    bs.gameTimer(2000, self.stopChoose)

def announceBounty(self):
    """Anuncia la victima"""
    if self.hasEnded(): return
    try:
        bs.playSound(bs.getSound("ding"))
        bs.screenMessage(
            u"Bounty Hunt Alert!",
            color=(2, 2, 0),
            transient=True)
        self._alarmSound = bs.NodeActor(
            bs.newNode(
                'sound',attrs={'sound':bs.playSound(bs.getSound("alarm")),
                'volume':1.0
            }
        ))
        self.startChoose()

    except Exception, e:
        print e


bsGame.GameActivity.getBounty = getBounty
bsGame.GameActivity.announceBounty = announceBounty
bsGame.GameActivity._chooseAnimatePlayer = _chooseAnimatePlayer
bsGame.GameActivity.stopChoose = stopChoose
bsGame.GameActivity.startChoose = startChoose


def onBegin(self):
    bs.Activity.onBegin(self)

    self._choseText = bs.newNode('text',
                     attrs={'vAttach':'bottom', 'hAttach':'left',
                     'text':' ','opacity':1.0,
                     'maxWidth':150,  'hAlign':'center',
                     'vAlign':'center', 'shadow':1.0,
                     'flatness':1.0, 'color':(1,1,1),
                     'scale':1,'position':(70,155)})
    # self._rewardText = bs.newNode('text',
    #      attrs={'vAttach':'top', 'hAttach':'center',
    #      'text':' ','opacity':1.0,
    #      'maxWidth':150,  'hAlign':'center',
    #      'vAlign':'center', 'shadow':1.0,
    #      'flatness':1.0, 'color':(1,1,1),
    #      'scale':1,'position':(-10,-80)})

    # player_bounty = getBounty(self.players).getName(icon=True, full=True)
    if not self.getMap().getName() == "Football Stadium": self.bounty = bs.Timer(10 * 1000, bs.Call(self.announceBounty))
    if self.getMap().getName() == "Football Stadium":
        import Bally
        Bally.StickyBall(position=self.getMap().getDefPoint("flagDefault")).autoRetain()

    if some.zenpay_event:
        self.zenpay = zenpayEvent.zenpayEvent()
        self.zenpay.start()
    self.stars = []
    if not hasattr(self, "_standardTimeLimitTime") or not hasattr(
        self, "_standardTimeLimitTimer"):
        self.setupStandardTimeLimit()
    if some.floating_landmine: self.flo = floater.Floater(self._mapType())
    # if some.night:
    #     bs.getSharedObject('globals').tint = (0.5, 0.7, 1)
    MapBounds = self.getMap().getDefBoundBox("levelBounds")
    import EndVote
    import time
    EndVote.voters = []
    EndVote.game_started_on = time.time()

    def snowfall():
        for i in range(5):
            pos = (random.uniform(MapBounds[0], MapBounds[3]),
                   MapBounds[4] - random.uniform(0, 0.3),
                   random.uniform(MapBounds[2], MapBounds[5]))
            #vel2 = (random.uniform(-2,2),0,random.uniform(-2,2))
            #color = (random.uniform(.5,1),random.uniform(0.5,1),random.uniform(.5,1))
            # portalObjects.Bubble(position=pos,velocity=vel2,thrust=0,color=color)
            vel = (0, 0, 0)  # (random.uniform(-2,2),0,random.uniform(-2,2))
            bs.emitBGDynamics(position=pos,
                              velocity=vel,
                              count=5,
                              scale=0.5,
                              spread=0.2,
                              chunkType="ice")

    if some.snowfall:
        bs.gameTimer(100, snowfall, True)

    def light():
        abc = bs.newNode('light',
                         attrs={
                             'position': (0, 10, 0),
                             'color': (0.2, 0.2, 0.4),
                             'volumeIntensityScale': 1.0,
                             'radius': 10
                         })
        bsUtils.animate(abc, "intensity", {
            0: 1,
            50: 10,
            150: 5,
            250: 0,
            260: 10,
            410: 5,
            510: 0
        })
        ho = random.random() * 20000
        from random import randint
        ho = (randint(5, 20) * 1000)
        bs.gameTimer(int(ho), light)

    key = {
        0: (0.9, 0.5, 0),
        1000 * 2: (0, 0, 0.9),
        2000 * 3: (0, 0.9, 0),
        3000 * 4: (0.9, 0.5, 0),
        4000 * 5: (0, 0.9, 0.9),
        5000 * 6: (0.9, 0, 0.9),
        6000 * 7: (0.9, 0.5, 0)
    }
    #bs.animateArray(bs.getSharedObject("globals"), "tint", 3, key, loop=True)
    bs.animateArray(bs.getSharedObject("globals"), "vignetteOuter", 3, key, loop=True)
    try:
        bs.animateArray(self.getMap().node, "color", 3, key, loop=True)
        bs.animateArray(self.getMap().floor, "color", 3, key, loop=True)
    except:
        pass

    try:
        self.getMap().node.materials = [bs.getSharedObject('footingMaterial')]
        self.getMap().floor.materials = [bs.getSharedObject('footingMaterial')]
        self.getMap().isHockey = False
    except:
        pass
    s = self.getSession()

    try:
        self._bots = bs.BotSet()
        self.botTypes = [
            bs.BomberBot, bs.BomberBotPro, bs.BomberBotProShielded,
            bs.ToughGuyBot, bs.ToughGuyBotPro, bs.ToughGuyBotProShielded,
            bs.ChickBot, bs.ChickBotPro, bs.ChickBotProShielded, bs.NinjaBot,
            bs.MelBot, bs.PirateBot
        ]
        def btspawn():
            if len(self.players) == 1:
                try:
                    if not self._bots.haveLivingBots():
                        pt = (self.players[0].actor.node.position[0],
                              self.players[0].actor.node.position[1] + 2,
                              self.players[0].actor.node.position[2])
                        self._bots.spawnBot(random.choice(self.botTypes),
                                            pos=pt,
                                            spawnTime=500)
                except:
                    pass
            else:
                self.botTimer = None


        self.botTimer = bs.gameTimer(1000,btspawn,True)
        self.starTime = bs.gameTimer(3010, bs.WeakCall(self.starGenerator), repeat=True)
        if isinstance(s, bs.CoopSession):
            import bsUI
            bsInternal._setAnalyticsScreen(
                'Coop Game: ' + s._campaign.getName() + ' ' +
                s._campaign.getLevel(bsUI.gCoopSessionArgs['level']).getName())
            bsInternal._incrementAnalyticsCount('Co-op round start')
            if len(self.players) == 1:
                bs.screenMessage(
                    'No Human Player Available, Push Your Rank With Bots Until Someone Comes!'
                )
                bsInternal._incrementAnalyticsCount(
                    'Co-op round start 1 human player')
            elif len(self.players) == 2:
                bsInternal._incrementAnalyticsCount(
                    'Co-op round start 2 human players')
            elif len(self.players) == 3:
                bsInternal._incrementAnalyticsCount(
                    'Co-op round start 3 human players')
            elif len(self.players) >= 4:
                bsInternal._incrementAnalyticsCount(
                    'Co-op round start 4+ human players')
        elif isinstance(s, bs.TeamsSession):
            bsInternal._setAnalyticsScreen('Teams Game: ' + self.getName())
            bsInternal._incrementAnalyticsCount('Teams round start')
            if len(self.players) == 1:
                bsInternal._incrementAnalyticsCount(
                    'Teams round start 1 human player')
            elif len(self.players) > 1 and len(self.players) < 8:
                bsInternal._incrementAnalyticsCount('Teams round start ' +
                                                    str(len(self.players)) +
                                                    ' human players')
            elif len(self.players) >= 8:
                bsInternal._incrementAnalyticsCount(
                    'Teams round start 8+ human players')
        elif isinstance(s, bs.FreeForAllSession):
            bsInternal._setAnalyticsScreen('FreeForAll Game: ' +
                                           self.getName())
            bsInternal._incrementAnalyticsCount('Free-for-all round start')
            if len(self.players) == 1:
                bs.screenMessage(
                    'No Human Player Available, Push Your Rank With Bots Until Someone Comes!'
                )
                bsInternal._incrementAnalyticsCount(
                    'Free-for-all round start 1 human player')
            elif len(self.players) > 1 and len(self.players) < 8:
                bsInternal._incrementAnalyticsCount(
                    'Free-for-all round start ' + str(len(self.players)) +
                    ' human players')
            elif len(self.players) >= 8:
                bsInternal._incrementAnalyticsCount(
                    'Free-for-all round start 8+ human players')
    except Exception:
        bs.printException("error setting analytics screen")

    # for some analytics tracking on the c layer..
    bsInternal._resetGameActivityTracking()

    # we dont do this in onTransitionIn because it may depend on
    # players/teams which arent available until now
    bs.gameTimer(1, bs.WeakCall(self.showScoreBoardInfo))
    bs.gameTimer(1000, bs.WeakCall(self.showInfo))
    bs.gameTimer(2500, bs.WeakCall(self._showTip))

    # store some basic info about players present at start time
    self.initialPlayerInfo = [{
        'name': p.getName(full=True),
        'character': p.character
    } for p in self.players]

    # sort this by name so high score lists/etc will be consistent
    # regardless of player join order..
    self.initialPlayerInfo.sort(key=lambda x: x['name'])

    # if this is a tournament, query info about it such as how much
    # time is left
    try:
        tournamentID = self.getSession()._tournamentID
    except Exception:
        tournamentID = None

    if tournamentID is not None:
        bsInternal._tournamentQuery(args={
            'tournamentIDs': [tournamentID],
            'source': 'in-game time remaining query'
        },
                                    callback=bs.WeakCall(
                                        self._onTournamentQueryResponse))


msg = [
    "Comando /rule en el Chat Para Ver Las Reglas",
    "Comando /help Para Mas Informacion",
    "Comando /bet  Para Apostar",
    "Comando /redeem Para Canjear Codigos",
    "Comando /spawn Para Spawnear si no Quieres Esperar.",
    "Comando /report Para Reportar Abusos o Jugadores Molestos."
]


def onBeginstats(self, customContinueMessage=None):
    global msg
    bs.Activity.onBegin(self)
    color = (random.random(), random.random(), random.random())
    bs.screenMessage(random.choice(msg), color = color)
    start_new_thread(mystats.update,(self.scoreSet,))
    # start_new_thread(mystats.update,(self.scoreSet,))
    # pop up a 'press any button to continue' statement after our
    # min-view-time show a 'press any button to continue..'
    # thing after a bit..
    if bs.getEnvironment()['interfaceType'] == 'large':
        # FIXME - need a better way to determine whether we've probably
        # got a keyboard
        s = bs.Lstr(resource='pressAnyKeyButtonText')
    else:
        s = bs.Lstr(resource='pressAnyButtonText')


    bsUtils.Text(s,
                 vAttach='bottom',
                 hAlign='center',
                 flash=True,
                 vrDepth=50,
                 position=(0, 10),
                 scale=0.8,
                 color=(0.5, 0.7, 0.5, 0.5),
                 transition='inBottomSlow',
                 transitionDelay=self._minViewTime).autoRetain()
bsGame.ScoreScreenActivity.onBegin = onBeginstats

def gameAct_handleMessage(self, msg):

    m = msg

    if isinstance(msg, bs.PlayerSpazDeathMessage):

        player = msg.spaz.getPlayer()
        killer = msg.killerPlayer
        killerid = killer.get_account_id()
        stats = db.getData(killerid)
        #print("player: " + player.getName() + " Killer: " + killer.getName() + " killed: " + str(msg.killed))
        if self.lastBountyPlayerName is not None:
            if player.getName() == self.lastBountyPlayerName[0].getName() and not killer.getName() == self.lastBountyPlayerName[0].getName():
                if self._choseText.exists():
                    self._choseText.text = "Captured!"
                    self._choseText.color = (2, 0, 0)
                bs.playSound(bs.getSound("dingSmall"))
                bs.playSound(bs.getSound("achievement"))
                bs.screenMessage(
                    u"Bounty Captured! 🏆 {} has been captured by {}! 🎉".format(player.getName(), killer.getName()),
                    color=(0, 1, 0),
                    transient=True)
                bs.screenMessage(
                    u"🎉 Congratulations {}! You've claimed a bounty of {} points by eliminating {}. Keep up the good work! 🏆".format(killer.getName(), self.lastBountyPlayerName[1], player.getName()),
                    color=(0, 1, 0),
                    transient=True,
                    clients=[killer.getInputDevice().getClientID()])
                stats['p'] += self.lastBountyPlayerName[1]
                db.saveData(killerid, stats)
                self.lastBountyPlayerName = None

        # inform our score-set of the demise
        self.scoreSet.playerLostSpaz(player, killed=msg.killed, killer=killer)

        # award the killer points if he's on a different team
        if killer is not None and killer.getTeam() is not player.getTeam():
            pts, importance = msg.spaz.getDeathPoints(msg.how)
            if not self.hasEnded():
                self.scoreSet.playerScored(killer,
                                           pts,
                                           kill=True,
                                           victimPlayer=player,
                                           importance=importance,
                                           showPoints=self._showKillPoints)

    elif isinstance(m, bs.SpazBotDeathMessage):
        pts, importance = m.badGuy.getDeathPoints(m.how)
        if m.killerPlayer is not None and m.killerPlayer.exists():
            try:
                target = m.badGuy.node.position
            except Exception:
                target = None
            try:
                self.scoreSet.playerScored(m.killerPlayer,
                                           pts * 2,
                                           target=target,
                                           kill=True,
                                           screenMessage=False,
                                           importance=importance)
                self._dingSound = bs.getSound('dingSmall')
                self._dingSoundHigh = bs.getSound('dingSmallHigh')
                bs.playSound(self._dingSound
                             if importance == 1 else self._dingSoundHigh,
                             volume=0.6)
            except Exception as e:
                print 'EXC on last-stand SpazBotDeathMessage', e


def elim_update(self):

    if self._soloMode:
        # for both teams, find the first player on the spawn order
        # list with lives remaining and spawn them if they're not alive
        for team in self.teams:
            # prune dead players from the spawn order
            team.gameData['spawnOrder'] = [
                p for p in team.gameData['spawnOrder'] if p.exists()
            ]
            for player in team.gameData['spawnOrder']:
                if player.gameData['lives'] > 0:
                    if not player.isAlive():
                        self.spawnPlayer(player)
                        self._updateIcons()
                    break

    # if we're down to 1 or fewer living teams, start a timer to end
    # the game (allows the dust to settle and draws to occur if deaths
    # are close enough)
    if len(self._getLivingTeams()) < 2:
        if len(self.players) == 1 and self.players[0].gameData['lives'] > 0:
            return
        self._roundEndTimer = bs.Timer(500, self.endGame)


defaultlimit = bsGame.GameActivity.setupStandardTimeLimit


def _setupStandardTimeLimit(func):
    def deco(*args):
        if len(args) > 1:
            duration = args[1]
            if duration <= 0:
                try:
                    duration = int(some.default_game_time_limit) * 60
                except:
                    pass
            return func(*args)

    return deco



bsGame.GameActivity.setupStandardTimeLimit = _setupStandardTimeLimit(defaultlimit)
bsGame.GameActivity.onBegin = onBegin
bsGame.GameActivity.starGenerator = starGenerator
bsGame.GameActivity.onTransitionIn = onTransitionIn
bsGame.GameActivity.onTransitionOut = onTransitionOut
bsGame.GameActivity.handleMessage = gameAct_handleMessage
bsElimination.EliminationGame._update = elim_update


rejoin_cooldown = 10 * 1000
bsGame.Session.players_on_wait = {}
bsGame.Session.players_req_identifiers = {}
bsGame.Session.waitlist_timers = {}
def _Modify_Session_onPlayerRequest(self, player):
    global rejoin_cooldown
    """
    Called when a new bs.Player wants to join;
    should return True or False to accept/reject.
    """
    # limit player counts based on pro purchase/etc *unless* we"re in a
    # stress test
    count = 0
    # if bsUtils._gStressTestResetTimer is None:

    #     if len(self.players) >= self._maxPlayers:

    #         # print a rejection message *only* to the client trying to join
    #         # (prevents spamming everyone else in the game)
    #         bs.playSound(bs.getSound("error"))
    #         bs.screenMessage(
    #             bs.Lstr(
    #                 resource="playerLimitReachedText",
    #                 subs=[("${COUNT}", str(self._maxPlayers))]),
    #             color=(0.8, 0.0, 0.0),
    #             clients=[player.getInputDevice().getClientID()],
    #             transient=True)
    #         return False
    # rejoin cooldown
    pid = player.get_account_id()
    #print(help(player.setName))
    #print(dir(bsInternal))
    import math
    if pid:
        leave_time = self.players_on_wait.get(pid)
        if leave_time:
            diff = str(
                int((rejoin_cooldown - bs.getRealTime() + leave_time) / 1000)
            )
            bs.screenMessage(
                "You Can Join in {} Seconds.".format(diff),
                clients=[player.getInputDevice().getClientID()],
                transient=True)
            return False
        self.players_req_identifiers[player.getID()] = pid

    if pid in self.players_req_identifiers:
        bs.screenMessage("Welcome Back!", clients=[pid.getInputDevice().getClientID()], transient=True)

    if player.get_account_id() is None:
        bs.screenMessage('Loading; try again in a moment......',color=(1,1,0),transient=True,clients=[player.getInputDevice().getClientID()])
        return False
    #handle.join(player)
    if not player.get_account_id() in db.cache:
        if not player.get_account_id() in handle.queue: handle.queue.append(player.get_account_id()) ; start_new_thread(handle.join, (player.get_account_id(),player.getInputDevice().getClientID()))
        bs.screenMessage('Loading; try again in a moment......',color=(1,1,0),transient=True,clients=[player.getInputDevice().getClientID()])
        return False

    for current in self.players:
        if current.get_account_id() == player.get_account_id():
            count += 1

    if not db.getAdmin(player.get_account_id()):
        if count >= 1:
            bs.screenMessage("No se permiten bots!",
                clients=[player.getInputDevice().getClientID()], transient=True)
            bs.playSound(bs.getSound("error"))
            return False

    bs.playSound(bs.getSound("pop01"))
    return True




def Modify_onPlayerLeave(self, player):
    global rejoin_cooldown
    """
    Called when a previously-accepted bs.Player leaves the session.
    """
    # remove them from the game rosters
    def delete_player_on_wait(pid):
        try:
            self.players_on_wait.pop(pid)
        except KeyError:
            pass
    pid = player.get_account_id()

    if pid is None:
        idset = {
            p.get_account_id()
            for p in self.players if p.get_account_id() is not None
        }
        diff = list(set(db.cache.keys()) - idset)
    else:
        diff = [pid]

    #if len(diff) > 1: print 'more than one diff:', diff

    for i in diff:
        db.playerLeave(i)

    identifier = self.players_req_identifiers.get(player.getID())
    if identifier:
        self.players_on_wait[identifier] = bs.getRealTime()
        with bs.Context('UI'):
            self.waitlist_timers[identifier] = bs.realTimer(
                rejoin_cooldown, bs.Call(delete_player_on_wait, identifier))

    if player in self.players:
        bs.playSound(bs.getSound('corkPop'))
        #bs.screenMessage("Adios nos Vemos! :>", clients=[player.getInputDevice().getClientID()], transient=True)
        # this will be None if the player is still in the chooser
        team = player.getTeam()

        activity = self._activityWeak()


        # if he had no team, he's in the lobby
        # if we have a current activity with a lobby, ask them to remove him
        if team is None:
            with bs.Context(self):
                try:
                    self._lobby.removeChooser(player)
                except Exception:
                    bs.printException(
                        'Error: exception in Lobby.removeChooser()')

        # *if* he was actually in the game, announce his departure
        if team is not None and len(activity.players) <= 3:
            bs.screenMessage(
                bs.Lstr(resource='playerLeftText',
                        subs=[('${PLAYER}', player.getName(full=True))]))

        # remove him from his team and session lists
        # (he may not be on the team list since player are re-added to
        # team lists every activity)
        if team is not None and player in team.players:

            # testing.. can remove this eventually
            if isinstance(self, bs.FreeForAllSession):
                if len(team.players) != 1:
                    bs.printError("expected 1 player in FFA team")
            team.players.remove(player)

        # remove player from any current activity
        if activity is not None and player in activity.players:
            activity.players.remove(player)

            # run the activity callback unless its been finalized
            if not activity.isFinalized():
                try:
                    with bs.Context(activity):
                        activity.onPlayerLeave(player)
                except Exception:
                    bs.printException(
                        'exception in onPlayerLeave for activity', activity)
            else:
                bs.printError(
                    "finalized activity in onPlayerLeave; shouldn't happen")

            player._setActivity(None)

            # reset the player - this will remove its actor-ref and clear
            # its calls/etc
            try:
                with bs.Context(activity):
                    player._reset()
            except Exception:
                bs.printException(
                    'exception in player._reset in'
                    ' onPlayerLeave for player', player)

        # if we're a non-team session, remove the player's team completely
        if not self._useTeams and team is not None:

            # if the team's in an activity, call its onTeamLeave callback
            if activity is not None and team in activity.teams:
                activity.teams.remove(team)

                if not activity.isFinalized():
                    try:
                        with bs.Context(activity):
                            activity.onTeamLeave(team)
                    except Exception:
                        bs.printException(
                            'exception in onTeamLeave for activity', activity)
                else:
                    bs.printError("finalized activity in onPlayerLeave p2"
                                  "; shouldn't happen")

                # clear the team's game-data (so dying stuff will
                # have proper context)
                try:
                    with bs.Context(activity):
                        team._resetGameData()
                except Exception:
                    bs.printException('exception clearing gameData for team:',
                                      team, 'for player:', player,
                                      'in activity:', activity)

            # remove the team from the session
            self.teams.remove(team)
            try:
                with bs.Context(self):
                    self.onTeamLeave(team)
            except Exception:
                bs.printException('exception in onTeamLeave for session', self)
            # clear the team's session-data (so dying stuff will
            # have proper context)
            try:
                with bs.Context(self):
                    team._resetSessionData()
            except Exception:
                bs.printException('exception clearing sessionData for team:',
                                  team, 'in session:', self)

        # now remove them from the session list
        self.players.remove(player)

    else:
        print('ERROR: Session.onPlayerLeave called'
              ' for player not in our list.')


bsGame.Session.onPlayerRequest = _Modify_Session_onPlayerRequest
bsGame.Session.onPlayerLeave = Modify_onPlayerLeave


def bsScoreBoardinit(self, scoreboard, team, doCover, scale, label,
                     flashLength):

    self._scoreboard = weakref.ref(scoreboard)
    self._doCover = False
    self._scale = scale
    self._flashLength = flashLength
    self._width = 140.0 * self._scale
    self._height = 32.0 * self._scale
    self._barWidth = 2.0 * self._scale
    self._barHeight = 32.0 * self._scale
    self._barTex = self._backingTex = bs.getTexture('bar')
    self._coverTex = bs.getTexture('uiAtlas')
    self._model = bs.getModel('meterTransparent')

    safeTeamColor = bs.getSafeColor(team.color, targetIntensity=1.0)

    vr = bs.getEnvironment()['vrMode']

    if self._doCover:
        if vr:
            self._backingColor = [0.1 + c * 0.1 for c in safeTeamColor]
        else:
            self._backingColor = [0.05 + c * 0.17 for c in safeTeamColor]
    else:
        self._backingColor = [0.05 + c * 0.1 for c in safeTeamColor]

    self._backing = bs.NodeActor(
        bs.newNode('image',
                   attrs={
                       'scale': (self._width, self._height),
                       'opacity':
                       (0.8 if vr else 0.8) if self._doCover else 0.5,
                       'color': self._backingColor,
                       'vrDepth': -3,
                       'attach': 'topLeft',
                       'texture': self._backingTex
                   }))

    self._barColor = safeTeamColor
    self._bar = bs.NodeActor(
        bs.newNode('image',
                   attrs={
                       'opacity': 0.7,
                       'color': self._barColor,
                       'attach': 'topLeft',
                       'texture': self._barTex
                   }))

    self._barScale = bs.newNode('combine',
                                owner=self._bar.node,
                                attrs={
                                    'size': 2,
                                    'input0': self._barWidth,
                                    'input1': self._barHeight
                                })

    self._barScale.connectAttr('output', self._bar.node, 'scale')

    self._barPosition = bs.newNode('combine',
                                   owner=self._bar.node,
                                   attrs={
                                       'size': 2,
                                       'input0': 0,
                                       'input1': 0
                                   })

    self._barPosition.connectAttr('output', self._bar.node, 'position')

    self._coverColor = safeTeamColor

    if self._doCover:
        self._cover = bs.NodeActor(
            bs.newNode('image',
                       attrs={
                           'scale': (self._width * 1.15, self._height * 1.6),
                           'opacity': 1.0,
                           'color': self._coverColor,
                           'vrDepth': 2,
                           'attach': 'topLeft',
                           'texture': self._coverTex,
                           'modelTransparent': self._model
                       }))

    c = safeTeamColor
    self._scoreText = bs.NodeActor(
        bs.newNode('text',
                   attrs={
                       'hAttach': 'left',
                       'vAttach': 'top',
                       'hAlign': 'right',
                       'vAlign': 'center',
                       'maxWidth': 130.0 * (1.0 - scoreboard._scoreSplit),
                       'vrDepth': 2,
                       'scale': self._scale * 0.9,
                       'text': '',
                       'shadow': 1.0 if vr else 0.5,
                       'flatness':
                       (1.0 if vr else 0.5) if self._doCover else 1.0,
                       'color': c
                   }))

    c = safeTeamColor

    if label is not None:
        teamNameLabel = label
    else:
        teamNameLabel = team.name

        # we do our own clipping here; should probably try to tap into some
        # existing functionality
        if type(teamNameLabel) is bs.Lstr:

            # hmmm; if the team-name is a non-translatable value lets go
            # ahead and clip it otherwise we leave it as-is so
            # translation can occur..
            if teamNameLabel.isFlatValue():
                v = teamNameLabel.evaluate()
                # in python < 3.5 some unicode chars can have length 2,
                # so we need to convert to raw int vals for safer trimming
                vChars = bs.uniToInts(v)
                if len(vChars) > 10:
                    teamNameLabel = bs.Lstr(value=bs.uniFromInts(vChars[:10]) +
                                            '...')
        else:
            # in python < 3.5 some unicode chars can have length 2,
            # so we need to convert to raw int vals for safe trimming
            teamNameLabelChars = bs.uniToInts(teamNameLabel)
            if len(teamNameLabelChars) > 10:
                teamNameLabel = bs.uniFromInts(teamNameLabelChars[:10]) + '...'
            teamNameLabel = bs.Lstr(value=teamNameLabel)

    self._nameText = bs.NodeActor(
        bs.newNode('text',
                   attrs={
                       'hAttach': 'left',
                       'vAttach': 'top',
                       'hAlign': 'left',
                       'vAlign': 'center',
                       'vrDepth': 2,
                       'scale': self._scale * 0.9,
                       'shadow': 1.0 if vr else 0.5,
                       'flatness':
                       (1.0 if vr else 0.5) if self._doCover else 1.0,
                       'maxWidth': 130 * scoreboard._scoreSplit,
                       'text': teamNameLabel,
                       'color': c + (1.0, )
                   }))

    self._score = None


bsScoreBoard._Entry.__init__ = bsScoreBoardinit
