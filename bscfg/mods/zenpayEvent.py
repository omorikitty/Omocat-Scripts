import bs
import random
import bsGame
import bsInternal
import bsUtils
import bsSpaz
import newObjects
import portalObjects
import quakeBall
import weakref

# Tome la idea del sistema de eventos del modpack explodinary solo que el mio es mas basico :p


zenEvents = {}


def add_event(event):
    """Agrega los eventos que deseemos."""
    zenEvents[event.name] = event


class zenpayEvents(bs.Actor):
    def __init__(self, update=25):
        bs.Actor.__init__(self)
        self.update = update  # Ajusta la frecuencia de cada evento
        self.current_event = None
        self.event_timer = None
        self.currentEvents = []
        self._events_available = list(zenEvents.keys())

    def start(self):
        """Inicia los eventos."""
        self.event_timer = bs.Timer(
            self.update * 1000, bs.WeakCall(self.zen_event), repeat=True
        )

    def stop_event(self):
        """Detiene el evento actual."""
        if self.current_event is not None:
            self.current_event.stop()
            try:
                self.currentEvents.remove(self.current_event)
            except ValueError:
                pass
            self.current_event = None

    def _stop(self):
        """Detiene el temporizador."""
        if self.event_timer is not None:
            self.event_timer = None

    def all_events(self):
        """Retorna una lista con los eventos disponibles."""
        bsInternal._chatMessage(
            "Available Events | Currents: {}".format(len(self.currentEvents))
        )
        for i, name in enumerate(zenEvents):
            bsInternal._chatMessage("{}: {}\n".format(str(i), name))

    def stop_all_events(self):
        """Interrumpe todos los eventos en curso."""
        try:
            allEvents = list(self.currentEvents)
            for event in allEvents:
                event().stop()
                self.currentEvents.remove(event)
            bs.screenMessage(
                "All Events Have Been Stopped", transient=True, color=(1, 1, 0)
            )
        except:
            self.currentEvents = []
            bs.screenMessage(
                "All Events Have Been Stopped", transient=True, color=(1, 1, 0)
            )

    def run_event(self, ev):
        """Inicia un evento."""
        if not isinstance(ev, int):
            return
        try:
            choose = self._events_available[ev]
        except IndexError:
            bs.screenMessage(
                "This event is not available", color=(1, 0, 0), transient=True
            )
            return

        event = zenEvents[choose]
        if not event in self.currentEvents:
            self.anunciar(choose)
            self.currentEvents.append(event)
            bs.screenMessage("Starting event...", transient=True, color=(1, 1, 0))
            self.current_event = event().run()
        else:
            bs.screenMessage("That Event is Ongoing", transient=True, color=(1, 0, 0))

    def zen_event(self):
        """Escoge un evento aleatorio."""
        if zenEvents:
            choice = random.choice(list(zenEvents.keys()))
            self.anunciar(choice)
            event = zenEvents[choice]
            self.stop_event()  
            self.current_event = event().run()
            self.currentEvents.append(event)

    def anunciar(self, event):
        bs.gameTimer(10, lambda: bs.playSound(bs.getSound("scoreHit01")))
        bsUtils.ZoomText(
            event,
            lifespan=1000,
            jitter=2.0,
            position=(0, -230 - 1 * 20),
            scale=0.5,
            maxWidth=800,
            trail=True,
            color=(0.7, 1.1, 0.95),
        ).autoRetain()

    def cleanup(self):
        print("Deteniendo los eventos...")
        self.stop_all_events()

    def onFinalize(self):
        bs.Actor.onFinalize(self)
        self.cleanup()

    def handleMessage(self, m):
        self._handleMessageSanityCheck()
        if isinstance(m, bs.DieMessage):
            self.cleanup()
        else:
            bs.Actor.handleMessage(self, m)


class zenEvent:
    def __init__(self):
        self.activity = bs.getActivity
        self.session = bs.getSession

    def run(self):
        """Las acciones de tu evento"""

    def stop(self):
        """Detiene El Evento En curso"""

    def get_players(self):
        return [p for p in self.activity().players if p.exists()]

    def get_players_actor(self):
        """return all players"""
        return [p.actor for p in self.activity().players if p.actor.exists()]


class BackFlip(zenEvent):
    name = "BackFlip"

    def run(self):
        bsSpaz.Spaz.backflip = True
        bsSpaz.Spaz.backflipPresent = True

    def stop(self):
        bsSpaz.Spaz.backflip = False
        bsSpaz.Spaz.backflipPresent = False


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
        self.activity()._firework_time = bs.Timer(500, bs.Call(self.doFireWork), True)

    def stop(self):
        self.activity()._firework_time = None

    def doFireWork(self):
        bounds = self.activity()._map.getDefBoundBox("levelBounds")
        pos = (
            random.uniform(
                bounds[0],
                bounds[3],
            ),
            random.uniform(
                bounds[1],
                bounds[4],
            ),
            random.uniform(
                bounds[2],
                bounds[5],
            ),
        )
        newObjects.Firework(pos=pos, sound=False).autoRetain()


add_event(Fire_Work)


class ShowerBombs(zenEvent):
    name = "Meteor Shower"

    def run(self):
        self.activity()._shower_time = bs.Timer(500, bs.Call(self.doShowerBomb), True)

    def stop(self):
        self.activity()._shower_time = None

    def doShowerBomb(self):
        bounds = self.activity()._map.getDefBoundBox("levelBounds")
        pos = (
            random.uniform(
                bounds[0],
                bounds[3],
            )
            * 0.9,
            random.uniform(
                bounds[4],
                bounds[4],
            ),
            random.uniform(
                bounds[2],
                bounds[5],
            )
            * 0.9,
        )

        vel = (
            (-5.0 + random.random() * 15.0)
            * -((pos[0] - (bounds[0] + bounds[3]) / 2) / 4),
            random.uniform(-3.066, -4.12),
            (-5.0 + random.random() * 15.0)
            * -((pos[2] - (bounds[2] + bounds[5]) / 2) / 4),
        )
        bombTypes = ["normal", "tnt", "cluster"]
        bs.Bomb(
            position=pos, velocity=vel, bombType=random.choice(bombTypes)
        ).autoRetain()


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
        bsSpaz.Spaz.quakeLaser = True

    def stop(self):
        bsSpaz.Spaz.quakeLaser = False


add_event(partyLaser)


class GodSpeed(zenEvent):
    name = "God Speed"

    def run(self):
        try:
            for i in self.get_players_actor():
                if i.node.exists():
                    i.node.hockey = True
        except:
            pass

    def stop(self):
        try:
            for i in self.get_players_actor():
                if i.node.exists():
                    i.node.hockey = False
        except:
            pass


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
        for node in bsInternal.getNodes():
            if node.exists() and node.getNodeType() == "spaz":
                node.handleMessage(
                    "impulse",
                    node.position[0],
                    node.position[1],
                    node.position[2],
                    0,
                    25,
                    0,
                    32,
                    0.05,
                    0,
                    0,
                    0,
                    0.8,
                    0,
                )


add_event(lowGravity)


class TurretEvent(zenEvent):
    name = "Turret"

    def run(self):
        points = self.activity().getMap().flagPointDefault
        self.activity()._turret = portalObjects.zenTurret(position=points, rangeZone=10).autoRetain()

    def stop(self):
        self.activity()._turret.handleMessage(bs.DieMessage())
        #self.activity()._turret = None


add_event(TurretEvent)
