import bs
from bsMap import Map, registerMap
import bsUtils
import random


# Create Empty Map
class newZizagMap(Map):
    import zigZagLevelDefs as defs
    name = 'ZizagMap Test'
    playTypes = ['test', 'melee']

    @classmethod
    def getPreviewTextureName(cls):
        return 'rampageBGColor'

    @classmethod
    def onPreload(cls):
        data = {}
        data['model'] = bs.getModel('zigZagLevel')
        data['modelBottom'] = bs.getModel('zigZagLevelBottom')
        data['modelBG'] = bs.getModel('thePadBG')
        data['bgVRFillModel'] = bs.getModel('natureBackgroundVRFill')
        data['collideModel'] = bs.getCollideModel('zigZagLevelCollide')
        data['tex'] = bs.getTexture('zigZagLevelColor')
        data['modelBGTex'] = bs.getTexture('eggTex3')
        data['collideBG'] = bs.getCollideModel('natureBackgroundCollide')
        data['railingCollideModel'] = bs.getCollideModel('zigZagLevelBumper')
        data['bgMaterial'] = bs.Material()
        data['bgMaterial'].addActions(actions=('modifyPartCollision',
                                               'friction', 10.0))
        return data

    def __init__(self):
        Map.__init__(self)
        self.locs = []
        self.regions = []
        self.collision = bs.Material()
        self.collision.addActions(
            actions=(('modifyPartCollision', 'collide', True)))

        self.node = bs.newNode('terrain', delegate=self, attrs={
            'collideModel': self.preloadData['collideModel'],
            'model': self.preloadData['model'],
            'colorTexture': self.preloadData['tex'],
            'materials': [bs.getSharedObject('footingMaterial')]})
        self.foo = bs.newNode('terrain', attrs={
            'model': self.preloadData['modelBG'],
            'lighting': False,
            'colorTexture': self.preloadData['modelBGTex']})
        self.bottom = bs.newNode('terrain', attrs={
            'model': self.preloadData['modelBottom'],
            'lighting': False,
            'colorTexture': self.preloadData['tex']})
        bs.newNode('terrain', attrs={
            'model': self.preloadData['bgVRFillModel'],
            'lighting': False,
            'vrOnly': True,
            'background': True,
            'colorTexture': self.preloadData['modelBGTex']})
        self.bgCollide = bs.newNode('terrain', attrs={
            'collideModel': self.preloadData['collideBG'],
            'materials': [bs.getSharedObject('footingMaterial'),
                          self.preloadData['bgMaterial'],
                          bs.getSharedObject('deathMaterial')]})
        self.railing = bs.newNode('terrain', attrs={
            'collideModel': self.preloadData['railingCollideModel'],
            'materials': [bs.getSharedObject('railingMaterial')],
            'bumper': True})

        posDict = [{'pos': (1.35, 2.48, -1.55), 'size': (2, 1, 5.22)},
                   {'pos': (-4.50, 2.48, -1.55), 'size': (2, 1, 5.22)},
                   {'pos': (-1.50, 2.48, -3.55), 'size': (2, 1, 5.22)},
                   ]
        for a, map in enumerate(posDict):
            self.locs.append(bs.newNode('locator',
                                        attrs={'shape': 'box',
                                               'position': posDict[a]['pos'],
                                               'color': (0, 5, 1),
                                               'opacity': 1.0,
                                               'drawBeauty': True,
                                               'size': posDict[a]['size'],
                                               'additive': False}))

            self.regions.append(bs.newNode('region',
                                           attrs={'scale': tuple(posDict[a]['size']),
                                                  'type': 'box',
                                                  'materials': [self.collision, bs.getSharedObject('footingMaterial')]}))
            self.locs[-1].connectAttr('position', self.regions[-1], 'position')

        bsGlobals = bs.getSharedObject('globals')
        bsGlobals.tint = (1.0, 1.15, 1.15)
        bsGlobals.ambientColor = (random.uniform(
            0.3, 3), random.uniform(0.3, 3), random.uniform(0.3, 3))
        bsGlobals.vignetteOuter = (0.57, 0.59, 0.63)
        bsGlobals.vignetteInner = (0.97, 0.95, 0.93)
        bsGlobals.vrCameraOffset = (-1.5, 0, 0)


registerMap(newZizagMap)
