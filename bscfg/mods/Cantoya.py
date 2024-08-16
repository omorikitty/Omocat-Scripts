# coding: utf-8
import bsInternal
import bs
import random
import bsGame


class CantoyaFactory(object):
    def __init__(self):
        """
        Instantiate a factory object.
        """

        self.model = bs.getModel("frostyPelvis")
        self.texture = bs.getTexture("white")
        self.body = "box"

        self.cantoya_material = bs.Material()
        self.cantoya_material.addActions(
            actions=(('modifyPartCollision', 'collide', False),)
        )


class CantoyaBalloon(bs.Actor):
    pool = []

    def __init__(self, factory, bounds):
        bs.Actor.__init__(self)
        self.factory = factory
        self.bounds = bounds

        self.node = bs.newNode('prop', delegate=self, attrs={
            'model': self.factory.model,
            'lightModel': bs.getModel("shield"),
            'body': self.factory.body,
            'bodyScale': 0,
            'modelScale': 0.04,
            'shadowSize': 0,
            'colorTexture': self.factory.texture,
            'reflection': 'soft',
            'reflectionScale': [1.0],
            'materials': [self.factory.cantoya_material, bs.getSharedObject('objectMaterial')],
            'gravityScale': -0.1, # para que floten hacia arriba
            'damping': 0.01, # damping ligero para que emergan lentamente
            'density': 0.1, # esto le dara ligeresa..
        })

        self.light = bs.newNode('light', attrs={
            'color': (1, 1, 0),
            'radius': 0.02,
            'volumeIntensityScale': 0.5},
            owner=self.node)

        self.node.connectAttr('position', self.light, 'position')
        bs.animate(self.light, "intensity", {0: 0, 1500: 0.5}, loop=False)
        self.setPosition()

    def onFinalize(self):
        """Limpia la lista con las instancias de de este actor"""
        bs.Actor.onFinalize(self)
        self.getActivity().cantoya_particles = []

    def setPosition(self):
        """Simplemente establece una Posicion Aleatoria en el Mapa"""
        offset = 4
        scale = self.node.modelScale
        if self.node.exists():
            bs.animate(self.node, "modelScale", {0: 0, 1000: scale + random.uniform(0.001, 0.02)})
            mid_x = (self.bounds[0] + self.bounds[3]) / 2
            mid_y = (self.bounds[1] + self.bounds[4]) / 2
            mid_z = (self.bounds[2] + self.bounds[5]) / 2

            range_x = (self.bounds[3] - self.bounds[0]) / 2
            range_y = (self.bounds[4] - self.bounds[1]) / 2
            range_z = (self.bounds[5] - self.bounds[2]) / 2

            x = mid_x + random.uniform(-range_x, range_x)
            y = mid_y + random.uniform(-range_y, range_y)
            z = mid_z + random.uniform(-range_z, range_z)

            self.node.position = (x, y - offset, z)

    def handleMessage(self, m):
        if isinstance(m, bs.OutOfBoundsMessage):
            """En lugar de destruir los nodos mejor reciclamos los que ya estan cambiando su posicion nuevamente"""
            self.setPosition()

        else:
            bs.Actor.handleMessage(self, m)


def cantoyaGenerator(activity, num_particles=50):
    """Genera las particulas que desees"""
    factory = CantoyaFactory()
    map_bounds = activity.getMap().getDefBoundBox('areaOfInterestBounds')
    particles = [CantoyaBalloon(factory, map_bounds) for _ in range(num_particles)]
    activity._cantoya_particles = particles


bsGame.Activity.cantoyaGenerator = cantoyaGenerator
