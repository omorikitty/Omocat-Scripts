# by:
# Patron-Modz
import bs
import bsBomb
from bsBomb import (BombFactory, ImpactMessage)
class StickyBall(bs.Actor):
    def __init__(self,
                 scale = 1.0,
                 position = (0.0, 1.0, 0.0)):
        bs.Actor.__init__(self)
    
        self.scale = scale
        bomb = BombFactory()
        materials = [bs.getSharedObject('objectMaterial'),
                     bomb.impactBlastMaterial]
        
        model = bs.getModel('frostyPelvis')
        tex = bs.getTexture('star')
        
        self.bounce = False
        self.old_pos = position
        self.position = (position[0], position[1]+2, position[2])
        
        self.node = bs.newNode('prop', delegate=self,
            attrs={'position': self.position,
                   'body': 'sphere',
                   'bodyScale': self.scale,
                   'model': model,
                   'shadowSize': 0.3,
                   'colorTexture': tex,
                   'sticky': True,
                   'reflection': 'soft',
                   'reflectionScale': [1.5],
                   'isAreaOfInterest':True,
                   'materials': materials})
        bs.animate(self.node, 'modelScale',
            {0: 0, 20: 1.3 * self.scale, 26: self.scale})

    def handleMessage(self, msg):
        if isinstance(msg, ImpactMessage):
            if self.bounce:
                self.node.handleMessage(
                        'impulse', self.node.position[0], self.node.position[1],
                        self.node.position[2], -self.node.velocity[0]*2,
                        self.node.velocity[1]+10, -self.node.velocity[2]*2,
                        -50, -50, 0, 0, -self.node.velocity[0]*2,
                        self.node.velocity[1]+10, -self.node.velocity[2]*2)
                bs.playSound(bs.getSound('bunnyJump'),position=self.node.position)
                
        elif isinstance(msg, bs.HitMessage):
            self.node.handleMessage('impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                msg.velocity[0], msg.velocity[1], msg.velocity[2], msg.magnitude,
                msg.velocityMagnitude, msg.radius, 0,
                msg.velocity[0], msg.velocity[1], msg.velocity[2])
        elif isinstance(msg, bs.OutOfBoundsMessage):
            if self.node:
                self.node.delete()
            # StickyBall(scale=self.scale,
            #            position=self.old_pos).autoRetain()
        elif isinstance(msg, bs.PickedUpMessage):
            self.bounce = False
            self.node.sticky = False
        elif isinstance(msg, bs.DroppedMessage):
            self.bounce = True
            self.node.sticky = False
        elif isinstance(msg, bs.DieMessage):
            if self.node:
                self.node.delete()
        else:
            bs.Actor.handleMessage(self, msg)