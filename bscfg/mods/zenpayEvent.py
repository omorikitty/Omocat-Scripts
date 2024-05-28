import bs
import random
import bsGame
import bsInternal
import bsUtils
import bsSpaz
import newObjects
import quakeBall
import weakref

# Tome la idea del sistema de eventos del modpack explodinary solo que el mio es mas basico :p


zenEvents = {}
inCurrent = []
#print(len(inCurrent))

def add_event(event):
    """agrega los eventos que deseemos :>"""
    zenEvents[event.name] = event


class zenpayEvent:
    def __init__(self, update=25):
        self.update = update # ajusta la frecuenzia de cada evento
        self.current_event = None
        self.event_timer =  None
        self._events_available = list(zenEvents.keys())

    def start(self):
        """inicia los eventos"""
        self.event_timer = bs.Timer(self.update * 1000, bs.WeakCall(self.zen_event), repeat=True)

    def stop_event(self):
        """detiene el evento actual"""
        if self.current_event is not None:
            self.current_event.stop()
            inCurrent.remove(self.current_event)
            self.current_event = None

        
    def _stop(self):
        """detiene el temporizador"""
        if self.event_timer is not None: 
            self.event_timer = None

    def all_events(self):
        """Retorna una lista con los eventos disponibles"""
        bsInternal._chatMessage("Available Events | Currents: {}".format(len(inCurrent)))
        for i, name in enumerate(zenEvents):
            bsInternal._chatMessage('{}: {}\n'.format(str(i), name))


    def stop_all_events(self):
        """Interrumpe todos los eventos y los que estan en transcurso"""
        try:
            for event in inCurrent:
                event.stop()
                inCurrent.remove(event)
            bs.screenMessage(
                "All Events Have Been Stopped", 
                transient=True, 
                color=(1, 1, 0)
            )
        except Exception as e:
            print(e)
            #raise e
    def run_event(self, ev):
        """Inicia un evento"""
        if not isinstance(ev, int):
            return
        try:
            choose = self._events_available[ev]
            #self.onEventInCurrent(choose)
        except IndexError:
            bs.screenMessage(
                "This event is not available", color=(1, 0, 0), transient=True)
            return
        else:
            event = zenEvents[choose]()
            bs.screenMessage(
                "Starting event...",  
                transient=True, 
                color=(0, 1, 0)
            )
            self.anunciar(choose)
            event.run()
            inCurrent.append(event)
            #print(str(inCurrent))

    def zen_event(self):
        """escoge un evento aleatorio"""
        if zenEvents:
            choice = random.choice(list(zenEvents.keys()))
            self.anunciar(choice)
            event = zenEvents[choice]()
            self.stop_event()
            event.run()
            self.current_event = event
            inCurrent.append(event)


    def anunciar(self, event):
        self.animateText = bsUtils.Text(event,
           position=(0, 285),
           hAlign='center',
           vAlign='top',
           flatness=1.0,
           maxWidth=180,
           color=(1,1,0),
           transition='inLeft',
           scale=1.0,
           transitionOutDelay=1000,
           shadow=1.0,
           transitionDelay=0).autoRetain()
        if self.animateText is not None:
            if self.animateText.node.exists():
                bs.gameTimer(1000, self.animateText.node.delete)

class zenEvent:
    name = "event test"
    def __init__(self):
        self.activity = bs.getActivity
        self.session = bs.getSession

    def run(self):
        """Las acciones de tu evento"""
        pass


    def stop(self):
        """Detiene El Evento En curso"""
        pass

    def get_players(self):
        myPlayers = []
        for player in self.activity().players:
            if player.exists():
                myPlayers.append(player)
        return myPlayers if myPlayers is not None else None

    def get_players_actor(self):
        """return all players"""
        all_player = []
        for player in self.activity().players:
            if player.actor:
                all_player.append(player.actor)
        return all_player if all_player is not None else None



class BackFlip(zenEvent):
    name = "BackFlip"
    def run(self):
        bsSpaz.Spaz.backflip=True
        bsSpaz.Spaz.backflipPresent=True

    def stop(self):
        bsSpaz.Spaz.backflip=False
        bsSpaz.Spaz.backflipPresent=False

add_event(BackFlip)

class Dash(zenEvent):
    name = "Dash Event"
    def run(self):
        # bsSpaz.Spaz.dash_enable = True
        # for spaz in self.get_players():
        #     spaz.assignInputCall("punchRelease", bs.Call(self.dash, spaz.actor))
        bsSpaz.Spaz.dashEnable = True
    def stop(self):
        # bsSpaz.Spaz.dash_enable = False
        # for spaz in self.get_players():
        #     spaz.assignInputCall("punchRelease", bs.Call(bsSpaz.Spaz.onPunchRelease, spaz.actor))
        bsSpaz.Spaz.dashEnable = False
    

add_event(Dash)

class Fire_Work(zenEvent):
    name = "Fire Works"
    def run(self):
        self.activity()._firework_time = bs.Timer(1000, bs.Call(self.doFireWork), True)
    def stop(self):
        self.activity()._firework_time = None
    def doFireWork(self):
        bounds = self.activity()._map.getDefBoundBox("levelBounds")
        pos = (
            random.uniform(bounds[0], bounds[3],),
            random.uniform(bounds[1], bounds[4],),
            random.uniform(bounds[2], bounds[5],),
        )
        newObjects.Firework(pos=pos, sound=False).autoRetain()


add_event(Fire_Work)


class ShowerBombs(zenEvent):
    name = "Meteor Shower"
    def run(self):
        self.activity()._shower_time = bs.Timer(300, bs.Call(self.doShowerBomb), True)
    def stop(self):
        self.activity()._shower_time = None

    def doShowerBomb(self):
        bounds = self.activity()._map.getDefBoundBox("levelBounds")
        pos = (
            random.uniform(bounds[0], bounds[3],)*0.9,
            random.uniform(bounds[4], bounds[4],),
            random.uniform(bounds[2], bounds[5],)*0.9,
               )

        vel = (
            (-5.0 + random.random() * 15.0) * -( ( pos[0] - ( bounds[0] + bounds[3] ) / 2 ) / 4 ),
            random.uniform(-3.066, -4.12),
            (-5.0 + random.random() * 15.0) * -( ( pos[2] - ( bounds[2] + bounds[5] ) / 2 ) / 4 ),
        )

        bs.Bomb(position=pos, velocity=vel, bombType="normal").autoRetain()


add_event(ShowerBombs)


class jumpfly(zenEvent):
    name = "Jump Fly"
    def run(self):
        # for i in self.get_players():
        #     i.assignInputCall("jumpRelease", bs.Call(self.onJumpFly, i.actor))
        bsSpaz.Spaz.jumpFly3D = True
        bs.screenMessage("Fly!")

    def stop(self):
        bsSpaz.Spaz.jumpFly3D = False
        # for i in self.get_players():
        #     i.assignInputCall("jumpRelease", bs.Call(bsSpaz.Spaz.onJumpRelease, i.actor))

    

add_event(jumpfly)

class partyLaser(zenEvent):
    name = "Party Laser"
    def run(self):
        bsSpaz.Spaz.quakeLaser=True

    def stop(self):
        bsSpaz.Spaz.quakeLaser=False
        


add_event(partyLaser)

class GodSpeed(zenEvent):
    name = "God Speed"
    def run(self):
        for i in self.get_players_actor():
            if i.node.exists():
                setattr(i.node, "hockey", True)

    def stop(self):
        for i in self.get_players_actor():
            if i.node.exists():
                setattr(i.node, "hockey", False)

add_event(GodSpeed)


class Healing(zenEvent):
    name = "Healing Players"
    def run(self):
        for i in self.get_players_actor():
            i.node.handleMessage(bs.PowerupMessage(powerupType="health"))
        bs.screenMessage("I feel Good!")

add_event(Healing)


class lowGravity(zenEvent):
    name = "Low Gravity"
    def run(self):
        self.activity()._gravity_time = bs.Timer(150, bs.Call(self.gravity), True)
    def stop(self):
        self.activity()._gravity_time = None
                
    def gravity(self):
        for node in bs.getNodes():
            if node.exists() and node.getNodeType() in ["spaz"]:
                node.handleMessage('impulse',
                                   node.position[0], node.position[1], node.position[2],
                                   0, 25, 0,
                                   32, 0.05, 0, 0,
                                   0, 0.8, 0)


add_event(lowGravity)
