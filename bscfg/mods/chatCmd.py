# -*- coding: utf-8 -*-
import json
import bs
import bsInternal
import bsPowerup
import bsUtils
import random
import some
import threading
import handle
import DB_Manager as db
import kicker
import re
import datetime
import bsSpaz
import portalObjects
import quake
from bsSpaz import *
import zenpayEvent

reply = None
succes = False
costs = {
    'nv': 10,
    'heal': 20,
    'thaw': 5,
    'gp': 50,
    'reflections': 200,
    'end': 200,
}
#costs = {'nv':10,'heal':20,'thaw':5,'sm':50,'gp':2,'reflections':20}

admincommands = [
    'except', 'cm', 'take', 'unmute', 'mute', 'maxPlayers', 'ac', 'cameraMode',
    'admin', 'kill', 'kick', 'gm', 'floater', 'curse', 'freeze', 'shatter',
    'end', 'log', 'removetag', 'remove', 'pause', 'kick', 'fly', 'ban', 'hug',
    'freeze', 'quit', 'box', 'tint', 'icy', 'lm', 'permaban', 'warn', 'unwarn',
    'rt', 'laser', 'fireman', 'count', 'reflections', 'sm', 'nuke', 'speed',
    'playSound', 'addcoin', 'addtag', 'restart', 'vip', 'spaz', 'private',
    'flo', '3d', 'torneo', '3dfly', 'reload', 'newfly', 'count', 'mapop', 'colormap',
    'colorful', 'count', 'cooldown', 'event', 'anounce', 'colorname', 'cn', 'evilname',
    'dance', 'say', 'nodes'
]

restrictAdminCommands = ["admin", "vip"]

vipcmd = [
    'box', 'reflections', 'sm', 'count', 'icy', 'end', 'ac', 'magicbox',
    'cameraMode', 'rt', 'cc', 'cn', 'ooh', 'nv', 'heal',
    'thaw', 'sm', 'freeze', 'hug', 'playSound', 'curse', 'shatter',
    'spaz', 'laser', 'icy', 'gp', 'flo', 'fly', 'cm', 'tint', 'lm',
    'newfly', '3dfly', 'count', 'colorname'
]


def find_players_and_bots():
    result = []
    for i in bsInternal.getNodes():
        if hasattr(i, "getNodeType") and str(i.getNodeType()) == "spaz":
            i = i.getDelegate()
            if isinstance(i, bsSpaz.PlayerSpaz):
                result.append(i)
    return result


class chatOptions(object):
    def __init__(self):
        self.eventSystem = None
        self.all = True  # just in case
        self.tint = (0.9, 0.9, 0.9)  # needs for /nv
        self.availableColor = {
            "red": (1, 0, 0),
            "green": (0, 1, 0),
            "blue": (0, 0, 1),
            "purple": (1, 0, 1),
            "cyan": (0, 1, 1),
            "yellow": (1, 1, 0),
            "black": (0, 0, 0),
            "white": (1, 1, 1)
        }
        self._active_timers = []

    def getActorNode(self, clientID, activity):
        clientID = int(clientID)
        for player in activity.players:
            if player.getInputDevice().getClientID() == clientID:
                return player.actor

        if clientID < len(activity.players):
            player = activity.players[clientID]
            return player.actor

    def getEvents(self):
        if self.eventSystem is None:
            self.eventSystem = zenpayEvent.zenpayEvents().autoRetain()
        return self.eventSystem

    def _safeSetAttr(self, node, attr, val):
        if node is None:
            return
        if node.exists():
            setattr(node, attr, val)

    def checkDevice(self, clientID, msg):
        global reply
        for i in bsInternal._getForegroundHostActivity().players:
            if i.getInputDevice().getClientID() == clientID:
                player = i
                break
        else:
            return None
        m = handle.extract_command(msg)
        n = player.get_account_id()
        if db.getAdmin(n):
            if m in restrictAdminCommands:
                reply = "Restricted Command"
                return False
            reply = "Command Succes"
            return True
        if n in some.ownerid:
            reply = "Command Succes"
            return True
        if db.getVip(n) and m in vipcmd:
            reply = "Command Succes"
            return True
        else:
            return False

    def Vip(self, nick):
        i = handle.getPlayerFromNick(nick)
        if i is None:
            bs.screenMessage('Error Finding Player')
            return
        n = i.get_account_id()
        print(i.getName(True, False))
        try:
            db.makeVip(n, i.getName(True, False))
            bs.screenMessage(u'{}\n Ahora Es Vip!'.format(
                i.getName(True)),
                color=(0.5, 0.5, 2.0))
        except Exception, e:
            print(e)
        # i.removeFromGame()

    def tran(self, clientID, cost):
        cost = int(cost)
        for i in bsInternal._getForegroundHostActivity().players:
            if i.getInputDevice().getClientID() == clientID:
                n1 = i.get_account_id()
                clid = i.getInputDevice().getClientID()

        stats = db.getData(n1)

        coins = stats['p']
        if coins >= cost:
            coins -= cost
            stats['p'] = coins
            msgg = (u"This Command Cost " + str(cost) +
                    u" \ue01f. Player Now Has " + str(coins) + u' \ue01f')
            bs.screenMessage(msgg, clients=[clid], transient=True)
            db.saveData(n1, stats)
            return True
        else:
            msgg = 'The Command Costs: ' + \
                str(cost) + u'\ue01f. You Only Have: ' + str(coins) + u'\ue01f'
            bs.screenMessage(msgg, clients=[clid], transient=True)
            db.saveData(n1, stats)
            return False

    def admin(self, nick):
        i = handle.getPlayerFromNick(nick)
        if i is None:
            bs.screenMessage('Error Finding Player')
            return
        n = i.get_account_id()
        print(i.getName(True, False))
        try:
            db.makeAdmin(n, i.getName(True, False))
            bs.screenMessage(u'{}\n Ahora Es Admin!'.format(
                i.getName(True)),
                color=(0.5, 0.5, 2.0))
        except Exception, e:
            print(e)
        # i.removeFromGame()

    def deletedmin(self, nick):
        i = handle.getPlayerFromNick(nick)
        if i is None:
            bs.screenMessage('Error Finding Player')
            return
        n = i.get_account_id()
        print(i.getName(True, False))
        try:
            db.deleteAdmin(n, i.getName(True, False))
            bs.screenMessage('Admin Removido\nExitosamente!',
                             color=(1, 0.5, 0.5))
        except Exception, e:
            print(e)
        # i.removeFromGame()

    def deletevip(self, nick):
        i = handle.getPlayerFromNick(nick)
        if i is None:
            bs.screenMessage('Error Finding Player')
            return
        n = i.get_account_id()
        print(i.getName(True, False))
        try:
            db.deleteVip(n, i.getName(True, False))
            bs.screenMessage('Vip Removido\nExitosamente!',
                             color=(1, 0.5, 0.5))
        except Exception, e:
            print(e)
        # i.removeFromGame()

    def permaban(self, nick, reason):
        try:
            p = handle.getPlayerFromNick(nick)
            n = p.get_account_id()
            if n is not None:
                db.permaUser(n, reason)
                ac_names = handle.getAccountNamesFromAccountID(n)
                some.permabanned.extend(ac_names)
                bs.screenMessage(
                    u'{} has been permabanned!'.format(p.getName().encode('utf-8')),
                    color=(1, 0, 0))
                return
            else:
                for i in bsInternal._getGameRoster():
                    # print i
                    try:
                        if bs.utf8(i['displayString']).lower().find(
                                nick.encode('utf-8').lower()) != -1 or str(
                                    i['clientID']) == nick:
                            n = handle.getAccountIDFromAccountName(
                                i['displayString'].decode('utf-8').encode(
                                    'unicode_escape'))
                            n2 = handle.getAccountNamesFromAccountID(n)
                            db.permaUser(n)
                            some.permabanned.extend(n2)
                            bs.screenMessage(
                                u'{} has been permabanned'.format(n2),
                                color=(1, 0, 0))
                            return
                    except Exception as e:
                        print(e)
        except Exception as e:
            bs.printException()

    def count_down_timer(self, time):
        def show_time_remaining(t):
            if t > 0:
                bs.screenMessage(str(t) + 's', color=(0.5, 1.0, 0.5))
            else:
                bs.screenMessage('Tiempo agotado', color=(1.0, 0.5, 0.5))

        for i in range(time, -1, -1):
            bs.gameTimer((time - i) * 1000, bs.Call(show_time_remaining, i))

    def dickTula(self, nick):
        i = nick
        if i is None:
            bs.screenMessage('Error Finding Player')
            return
        size = random.randint(1, 1000)
        bsInternal._chatMessage(u'A {} le mide su tula {}cm'.format(
            i.getName(True, True), size))

    def booba(self, nick):
        i = nick
        if i is None:
            bs.screenMessage('Error Finding Player')
            return
        size = random.randint(1, 1000)
        bsInternal._chatMessage(u'A {} le Mide {}cm Cada Teta Noway.'.format(
            i.getName(True, True), size))

    def butty(self, nick):
        i = nick
        if i is None:
            bs.screenMessage('Error Finding Player')
            return
        size = random.randint(1, 1000)
        bsInternal._chatMessage(u'A {} le Mide {} Cada Nalga Noway.'.format(
            i.getName(True, True), size))

    def PorcentajeDeFacha(self, nick):
        i = nick
        if i is None:
            bs.screenMessage('Error Finding Player')
            return
        porcentaje = random.randint(1, 100)
        bsInternal._chatMessage(u'{} Tiene un nivel de facha del {}%'.format(
            i.getName(True, True), porcentaje))

    def fireMan(self, node):
        if node is None or not node.exists():
            self._active_timers = []
            return
        bs.emitBGDynamics(
            position = tuple([pos + random.uniform(-0.3, 0.3) for pos in node.position]),
            velocity=(0, 0, 0),
            count=10,
            scale=0.985 + random.uniform(-0.2, 0.2),
            spread=0.05,
            chunkType='sweat')
        self._active_timers = [bs.Timer(10, bs.Call(self.fireMan, node), True)]

    def ban(self, nick, secs, reason):
        try:
            p = handle.getPlayerFromNick(nick)
            n = p.get_account_id()
            if n is not None:
                db.banUser(n, secs, reason)
                ac_names = handle.getAccountNamesFromAccountID(n)
                some.banned.extend(ac_names)
                for i in ac_names:
                    with bs.Context('UI'):
                        bs.realTimer(secs * 1000,
                                     bs.Call(some.banned.remove, i))
                bs.screenMessage(
                    u'{} has been banned | Reason: {} | Expires on: {}'.format(
                        p.getName(), reason,
                        (datetime.datetime.now() + datetime.timedelta(
                            seconds=secs)).strftime('%d/%m/%Y, %H:%M:%S')))
                return
            else:
                for i in bsInternal._getGameRoster():
                    # print i
                    try:
                        if bs.utf8(i['displayString']).lower().find(
                                nick.encode('utf-8').lower()) != -1 or str(
                                    i['clientID']) == nick:
                            n = handle.getAccountIDFromAccountName(
                                i['displayString'].decode('utf-8').encode(
                                    'unicode_escape'))
                            n2 = handle.getAccountNamesFromAccountID(n)
                            db.banUser(n, secs, reason)
                            bs.screenMessage(
                                u'{} has been banned | Reason: {} | Expires on: {}'
                                .format(n, reason,
                                        (datetime.datetime.now() +
                                         datetime.timedelta(seconds=secs)
                                         ).strftime('%d/%m/%Y, %H:%M:%S')))
                            some.banned.extend(n2)
                            for i in n2:
                                with bs.Context('UI'):
                                    bs.realTimer(
                                        secs * 1000,
                                        bs.Call(some.banned.remove, i))
                            return
                    except Exception as e:
                        print(e)
            #some.permabanned = open(some.banfile).read().split('\n')
        except Exception as e:
            bs.printException()

    def anounceText(self, t):
        activity = bsInternal._getForegroundHostActivity()
        try:
            exists = activity._anounce_text.exists()
        except Exception:
            exists = False
        if not exists:
            activity._anounce_text = bs.newNode('text',
                                                attrs={'text': t,
                                                       'scale': 2,
                                                       'maxWidth': 115.0,
                                                       'position': (0, 0),
                                                       'shadow': 1.3,
                                                       'flatness': 1.0,
                                                       'color': (1, 1, 1),
                                                       'hAlign': 'center',
                                                       'vAttach': 'center'})
        else:
            activity._anounce_text.text = str(t)
        bs.gameTimer(10000, activity._anounce_text.delete)

    def kickByNick(self, nick, reason='Admin Used Kick Command'):
        kicker.kick(nick, reason)

    def colormap(self, activity, color):
        try:
            activity._map.node.color = color
            activity._map.floor.color = color
            activity._map.bottom.color = color
            activity._map.railing.color = color
            activity._map.bgCollide.color = color
        except:
            return

    def opt(self, clientID, msg):
        global succes
        try:
            activity = bsInternal._getForegroundHostActivity()
            with bs.Context(activity):
                checkdev = self.checkDevice(clientID, msg)
                m = handle.extract_command(msg)
                if m in admincommands and checkdev != True:
                    bs.screenMessage("You are not an admin",
                                     transient=True,
                                     clients=[clientID])
                    return
                else:
                    for i in bsInternal._getForegroundHostActivity().players:
                        if i.getInputDevice().getClientID() == clientID:
                            n = i.get_account_id()
                            player = i 
                            break
                    else:
                        return
                    if m in costs and checkdev != True:
                        cost = costs[m]
                        if self.tran(clientID, cost) == False:
                            return
                    if not 'player' in locals():
                        return
                    if player is None:
                        return
                    m = handle.extract_command(msg)
                    a = msg.split(' ')[1:]  # arguments
                    if m == 'ban':
                        if len(a) < 3:
                            bs.screenMessage(
                                "Usage: /ban <name/id/clientid> <time [1m,5h,1d,etc.]> <reason>"
                            )
                        else:
                            seconds_per_unit = {
                                "s": 1,
                                "m": 60,
                                "h": 3600,
                                "d": 86400,
                                "w": 604800
                            }

                            def cts(s):
                                return int(s[:-1]) * seconds_per_unit[s[-1]]
                            self.ban(a[0], cts(a[1].lower()),
                                     (' '.join(a[2:])))

                            succes = True

                    elif m == 'anounce':
                        if a == []:
                            bs.screenMessage("Format: /anounce <message>", clients=[clientID], transient=True)
                        else:
                            self.anounceText(' '.join(a[0:]).encode('utf-8'))
                            succes = True
                    elif m == "evilname":
                        if player.get_account_id() not in some.effectid:
                            some.effectid.append(player.get_account_id())
                    elif m == "fireman":
                        if a == []:
                            self.fireMan(player.actor.node)
                        else:
                            self.fireMan(self.getActorNode(a[0], activity).node)
                    elif m == 'say':
                        send = ' '.join(a[0:]).encode('utf-8')
                        bs.pushCall(bs.Call(bsInternal._chatMessage, send))

                    elif m == 'nodes':
                        bsInternal._chatMessage(bs.printNodes())

                    elif m == 'neon':
                        if a == []:
                            bs.screenMessage(
                                "Format: /neon <purple, green, blue, etc..> <intensity(max 3)>", clients=[clientID], transient=True)
                            c = [c for c in self.availableColor.keys()]
                            bs.screenMessage(
                                "\n".join(c),
                                clients=[clientID],
                                transient=True
                            )
                        elif len(a) >= 3:
                            try:
                                color = (float(a[0]), float(a[1]), float(a[2]))
                                self._safeSetAttr(player.actor.node, "color", color)
                                self._safeSetAttr(player.actor.node, "highlight", color)

                            except Exception, e:
                                print(e)

                        else:
                            intensity = 2 if len(a) <= 1 else int(a[1])
                            if intensity > 3:
                                return
                            color = None if not a[0] in self.availableColor else self.availableColor[a[0]]
                            glow = (color[0] * intensity, color[1] * intensity, color[2] * intensity)
                            if color is None:
                                bs.screenMessage('not Available Color', clients=[clientID], transient=True)
                                return

                            self._safeSetAttr(player.actor.node, "color", glow)
                            self._safeSetAttr(player.actor.node, "highlight", glow)

                    elif m == 'event':
                        # Esto tiene que ver con el sistema de eventos zeenppay
                        # Permite llamar un evento
                        if a == []:
                            self.getEvents().all_events()
                            # succes=True
                        else:
                            if a[0] != "stop":
                                try:
                                    self.getEvents().run_event(int(a[0]))
                                    # succes=True
                                except Exception as e:
                                    print e
                            else:
                                self.getEvents().stop_all_events()
                                # succes=True
                    elif m == "colorname":
                        # print(dir(player.actor.node))
                        if a == []:
                            c = random.choice(list(self.availableColor.keys()))
                            self._safeSetAttr(player.actor.node, "nameColor", self.availableColor[c])
                        else:
                            if len(a) == 3:
                                color = (float(a[0]), float(a[1]), float(a[2]))
                                self._safeSetAttr(player.actor.node, "nameColor", color) 
                                succes = True

                    elif m == "rule":
                        ms = [
                            '== Rules ==',
                            '1. No Pedir Admin',
                            '2. No Pedir nada al Onwer cuando este presente',
                            '2. No Spamm',
                            '3. No Molestar a otros jugadores 0 Toxicidad'
                        ]
                        bs.screenMessage('\n'.join(ms),
                                         transient=True,
                                         clients=[clientID]
                                         )
                    elif m == 'help':
                        try:
                            if a == []:
                                page_list = [
                                    "commands",
                                    "shop",
                                    "stats",
                                    "redeem",
                                    "admin",
                                    "vip"
                                ]
                                bs.screenMessage("Pages: [{}]".format(" | ".join(page_list)), transient=True, clients=[clientID])
                            else:
                                import ChatManager
                                ChatManager.Helper(a[0], clientID)
                        except Exception as e:
                            print e
                    elif m == 'mapop':
                        try:
                            activity._map.node.opacity = 0.5 if a == [] else float(a[0])
                            activity._map.foo.opacity = 0.5 if a == [] else float(a[0])
                            succes = True
                        except:
                            return

                    elif m == 'colormap':
                        if a == []:
                            bs.screenMessage("Use: /colormap {} or custom (0, 1, 0)".format(" ".join(self.availableColor.keys())))
                        elif a[0] in self.availableColor and not a[0].isdigit():
                            try:
                                self.colormap(activity, self.availableColor[a[0]])
                                succes = True
                            except:
                                return
                        else:
                            try:
                                if len(a) < 3:
                                    return
                                r = float(a[0])
                                g = float(a[1])
                                b = float(a[2])
                                color = (r, g, b)
                                self.colormap(activity, color)
                                succes = True
                            except:
                                return

                    elif m == '/log':
                        open(some.logfile,
                             'a+').write('\n' * 5 +
                                         str(bsInternal._getGameRoster()) +
                                         '\n' +
                                         str(bsInternal._getChatMessages()))

                    elif m == 'cn':
                        if a == []:
                            bs.screenMessage(
                                'Use: /cn <clientID> For Change Name Players')
                        else:
                            spaz = self.getActorNode(a[0], activity).node
                            if spaz.exists():
                                spaz.name = ' '.join(a[1:])
                                succes = True
                    elif m == 'booba':
                        self.booba(player)
                    elif m == 'butty':
                        self.butty(player)
                    elif m == 'spawn':
                        if a == []:
                            if player.isAlive() or player.actor:
                                bs.screenMessage("Ya estas Jugando...", transient=True, clients=[clientID])
                            else:
                                if activity.hasBegun():
                                    activity.spawnPlayer(player)

                    elif m == 'cooldown':
                        # Its purpose is to add a new command to the list of commands with Cooldown,
                        # this in case players think of spamming a single command XD
                        if a == []:
                            bs.screenMessage(
                                "Format: /cooldown <command> <time cooldown>",
                                transient=True,
                                clients=[clientID])

                        else:
                            current = []
                            try:
                                command = a[0]  # comand
                                time = int(a[1])  # time to cooldown
                                import ChatManager
                                if command in admincommands:
                                    # mantegamos un log de los comandos que fueron agregados recientemente
                                    current.append(command)

                                if command != "clean":
                                    ChatManager.add_cmd_cooldown(command, time)
                                    succes = True
                                else:
                                    # clean...
                                    for i in current:
                                        ChatManager.delete_timeout(i)
                                    succes = True
                            except Exception as e:
                                print e

                    elif m == 'laser':
                        import quakeBall

                        def addShot(spaz):
                            if spaz.isAlive() and spaz.node.exists():
                                quakeBall.QuakeBallFactory().give(spaz)

                        if a == []:
                            addShot(player.actor)
                            succes = True
                        elif a[0] == "all":
                            for i in bs.getSession().players:
                                addShot(i.actor)
                                succes = True
                        else:
                            try:
                                spaz = self.getActorNode(a[0], activity)
                                addShot(spaz)
                                succes = True
                            except:
                                return

                    elif m == 'whitelist':
                        if a[0] == 'off':
                            some.enableWithelist = False
                            bs.screenMessage('Withelist Disable')
                            succes = True
                        else:
                            bs.screenMessage('Whitelist Enable')
                            some.enableWithelist = True
                            succes = True

                    elif m == 'report':
                        if a == []:
                            bs.screenMessage(
                                'Write You Reasons Pls!\nUse: /report <clientID/playerid/name> <reason>')
                        elif a[0] == 'view':
                            with open(some.reportfile) as f:
                                for i in f.read().split('\n'):
                                    if i != "":
                                        bs.screenMessage(i, clients=[clientID], transient=True)

                        else:
                            to = handle.getPlayerFromNick(a[0])
                            reason = ' '.join(a[1:])
                            if reason == '' or reason == ' ':
                                bs.screenMessage(
                                    'Write You Reasons Pls!\nUse: /report <clientID/playerid/name> <reason>')
                                return
                            open(some.reportfile,
                                 'a+').write(time.strftime("%Y-%m-%d %H:%M:%S") + '  -  ' + player.getName() + '  -  '
                                             + to.getName() + '  -  reason: ' + reason + '  -  ' + to.get_account_id() + '\n')
                            bs.screenMessage(
                                'Su reporte ha sido Enviado!', color=(0, 1, 0), clients=[clientID], transient=True)

                    elif m == 'newfly':
                        import portalObjects
                        if a == []:
                            portalObjects.NewFly(player)
                            succes = True
                        elif a[0] == 'all':
                            for i in activity.players:
                                if i.exists() and i.isAlive():
                                    portalObjects.NewFly(i)
                                    succes = True
                        else:
                            try:
                                n = handle.getPlayerFromNick(a[0])
                                portalObjects.NewFly(n)
                                succes = True
                            except:
                                return

                    elif m == 'colorful':
                        key = {
                            0: (1, 0, 0),
                            1000 * 2: (0, 0, 1),
                            2000 * 3: (0, 1, 0),
                            3000 * 4: (1, 0, 0)
                        }

                        def switch():
                            try:
                                bs.animateArray(activity._map.node, "color", 3, key, loop=True)
                            except:
                                pass
                        bs.gameTimer(100, switch)
                        succes = True
                    elif m == '3dfly':
                        def onJump(i):
                            if not i.exists() or i.node.knockout > 0.0:
                                return
                            i.node.handleMessage(
                                "impulse",
                                i.node.position[0],
                                i.node.position[1],
                                i.node.position[2],
                                i.node.moveLeftRight * 10,
                                i.node.position[1] + 32,
                                i.node.moveUpDown * -10,
                                5, 5, 0, 0,
                                i.node.moveLeftRight * 10,
                                i.node.position[1] + 32,
                                i.node.moveUpDown * -10
                            )

                        if a == []:
                            player.assignInputCall('jumpPress', bs.Call(onJump, player.actor))
                            succes = True
                        elif a[0] == "all":
                            for i in bs.getSession().players:
                                i.assignInputCall('jumpPress', bs.Call(onJump, i.actor))
                                succes = True
                        else:
                            try:
                                i = handle.getPlayerFromNick(a[0])
                                i.assignInputCall('jumpPress', bs.Call(onJump, i.actor))
                                succes = True
                            except:
                                return
                    elif m == 'private':
                        if a == []:
                            bsInternal._setPublicPartyEnabled(False)
                            bs.screenMessage(
                                'El servidor se encuentra en Privado!', color=(2, 2, 0))
                        else:
                            if a[0] == 'off':
                                bsInternal._setPublicPartyEnabled(True)
                                bs.screenMessage(
                                    'El servidor ahora es publico!', color=(2, 2, 0))

                    elif m == 'magicbox':
                        pos = player.actor.node.position
                        FlyBox(position=(pos[0], pos[1] + 0.5, pos[2])).autoRetain()
                        succes = True
                    elif m == 'unperma':
                        some.permabanned = []
                        succes = True
                    elif m == 'addcoin':
                        try:
                            n = player.get_account_id()
                            if n is None:
                                return
                            stats = db.getData(n)
                            amount = int(a[0])
                            if amount >= 99999:
                                bs.screenMessage('Esa cantidad es exagerada!')
                                return

                            stats['p'] += amount
                            msg = (u"Ok admin, Se Han Transferido " + str(amount) +
                                   u"\ue01f Ha su Cuenta!")
                            bs.screenMessage(msg, color=(0, 1, 0))
                            bs.playSound(bs.getSound('cashRegister'))
                            db.saveData(n, stats)
                            #succes = True
                        except Exception as e:
                            pass
                    elif m == 'speed':
                        try:
                            if a == []:
                                bsInternal._chatMessage(
                                    'usage: /speed all or clientid')
                                self._safeSetAttr(player.actor.node, "hockey", True)
                                succes = True
                            else:
                                if a[0] == 'all':
                                    for node in bs.getNodes():
                                        if node.getNodeType() == "spaz":
                                            self._safeSetAttr(player.actor.node, "hockey", True)
                                            succes = True
                                else:
                                    try:
                                        spaz = self.getActorNode(a[0], activity).node
                                        self._safeSetAttr(spaz, "hockey", True)
                                        succes = True
                                    except:
                                        return

                        except:
                            pass

                    elif m == 'rainbow':
                        def _doRainbow(player):
                            if player.actor:
                                bs.animateArray(player.actor.node, 'color', 3, {
                                    0: (2, 0, 2),
                                    250: (2, 0, 0),
                                    250 * 2: (2, 2, 0),
                                    250 * 3: (0, 2, 2),
                                    250 * 4: (2, 0, 2)}, loop=True)
                                bs.animateArray(player.actor.node, 'highlight', 3, {
                                    0: (2, 0, 2),
                                    250: (2, 0, 0),
                                    250 * 2: (2, 2, 0),
                                    250 * 3: (0, 2, 2),
                                    250 * 4: (2, 0, 2)}, loop=True)
                        if a == []:
                            bs.screenMessage(
                                "Format: /rainbow all or clientid")
                            _doRainbow(player)
                            succes = True
                        elif a[0] == 'all':
                            for i in bs.getSession().players:
                                _doRainbow(i)
                                succes = True
                        else:
                            try:
                                playeractor = handle.getPlayerFromNick(a[0])
                                _doRainbow(playeractor)
                                succes = True
                            except:
                                return

                    elif m == 'nuke':
                        if a == []:
                            position = (player.actor.node.position[0],
                                        10,
                                        player.actor.node.position[2])
                            import portalObjects
                            portalObjects.Nuke(position=position).autoRetain()
                            succes = True

                    elif m == 'dance':
                        def dance(actor=None):
                            def work(node=None):
                                if node is not None and node.exists():
                                    pos = (node.position[0], node.position[1] + 0.5, node.position[2])
                                    node.handleMessage("impulse", pos[0], pos[1], pos[2], 0, -2, 0, 2000, 0, 1, 0, 0, -2, 0)
                            if actor is not None and actor.exists():
                                if not hasattr(actor, '_dance') or (hasattr(actor, '_dance') and actor._dance is None):
                                    actor._dance = bs.Timer(100, bs.Call(work, actor.node), repeat=True)
                                    work(node=actor.node)
                                else:
                                    actor._dance = None
                        if a[0] == 'all':
                            for i in find_players_and_bots():
                                dance(i)
                        else:
                            if int(a[0]) < len(activity.players):
                                dance(activity.players[int(a[0])].actor)
                    elif m == 'count':
                        if a == []:
                            bs.screenMessage(
                                'Use: /count <seconds>')
                        else:
                            t = int(a[0])
                            self.count_down_timer(t)
                    elif m == 'tula':
                        self.dickTula(player)
                    elif m == 'facha':
                        self.PorcentajeDeFacha(player)
                    elif m == 'pito':
                        try:
                            handle.pito(player, a[0])
                        except Exception as e:
                            print e.message
                            return
                    elif m == 'give' or m == 'donate':
                        if len(a) < 2:
                            bsInternal._chatMessage(
                                'usage: /give player_name amount')
                        else:
                            try:
                                handle.give(player, a[0], a[1],
                                            ' '.join(a[2:]))
                                bs.playSound(bs.getSound('cashRegister'))
                            except Exception as e:
                                print e.message
                    elif m == 'take':
                        if len(a) < 2:
                            bsInternal._chatMessage(
                                'usage: /take player_name amount')
                        else:
                            try:
                                handle.take(player, a[0], a[1],
                                            ' '.join(a[2:]))
                            except Exception as e:
                                print e.message
                    elif m == 'reload':
                        import autoreload
                        autoreload.update()
                        bs.reloadMedia()
                    elif m == 'redeem':
                        import json
                        codes = json.load(open(some.codefile))
                        if a[0] == []:
                            return
                        elif a[0] in codes:
                            if codes[a[0]]['s'] is None:
                                stats = db.getData(player.get_account_id())
                                stats['p'] += int(codes[a[0]]['t'])
                                db.saveData(player.get_account_id(), stats)
                                bs.screenMessage(
                                    'Congrats! You have successfully redeemed {} tickets! Join Discord for codes every 30 mins :)'
                                    .format(codes[a[0]]['t']),
                                    color=(0.5, 1, 0.5))
                                codes[a[0]]['s'] = player.getName(True)
                                open(some.codefile,
                                     'w+').write(json.dumps(codes, indent=4))
                            else:
                                bs.screenMessage(
                                    u'Lol the code has already been used by {}. Sucks to be u. Join Discord for codes every 30 mins! :)'
                                    .format(codes[a[0]]['s']),
                                    color=(1, .5, .5))
                        else:
                            bs.screenMessage(
                                'No such code exists. Learn to copy stuff, dumb butt. Join Discord for codes every 30 mins :)',
                                color=(1, .5, .5))
                    elif m == 'except':
                        if len(a) >= 1:
                            if not ' '.join(a[0:]).lower() in some.trans:
                                some.trans.append((' '.join(a[0:])).lower())
                                open(some.transfile,
                                     'a').write(' '.join(a[0:]).lower() + '\n')
                                bs.screenMessage('Exception Added')
                            else:
                                bs.screenMessage(
                                    'Exception is already present')
                    elif m == 'floater':
                        playerlist = bsInternal._getForegroundHostActivity(
                        ).players
                        if not hasattr(bsInternal._getForegroundHostActivity(),
                                       'flo'):
                            import floater
                            bsInternal._getForegroundHostActivity().flo = floater.Floater(bsInternal._getForegroundHostActivity()._mapType())
                        floater = bsInternal._getForegroundHostActivity().flo
                        if floater.controlled:
                            bs.screenMessage(
                                'Floater is already being controlled',
                                color=(1, 0, 0))
                            return
                        for i in playerlist:
                            if i.getInputDevice().getClientID() == clientID:
                                clientID = i.getInputDevice().getClientID()
                                bs.screenMessage(
                                    'You\'ve Gained Control Over The Floater!\nPress Bomb to Throw Bombs and Punch to leave!\nYou will automatically get released after some time!',
                                    clients=[clientID],
                                    transient=True,
                                    color=(0, 1, 1))

                                def dis(i, floater):
                                    i.actor.node.invincible = False
                                    i.resetInput()
                                    i.actor.connectControlsToPlayer()
                                    floater.dis()

                                # bs.gameTimer(15000,bs.Call(dis,i,floater))
                                ps = i.actor.node.position
                                i.actor.node.invincible = True
                                floater.node.position = (ps[0], ps[1] + 1.5,
                                                         ps[2])
                                i.actor.node.holdNode = bs.Node(None)
                                i.actor.node.holdNode = floater.node2
                                i.actor.disconnectControlsFromPlayer()
                                i.resetInput()
                                floater.sourcePlayer = i
                                floater.con()
                                i.assignInputCall('pickUpPress', floater.up)
                                i.assignInputCall('pickUpRelease', floater.upR)
                                i.assignInputCall('jumpPress', floater.down)
                                i.assignInputCall('jumpRelease', floater.downR)
                                i.assignInputCall('bombPress', floater.drop)
                                i.assignInputCall('punchPress',
                                                  bs.Call(dis, i, floater))
                                i.assignInputCall('upDown', floater.updown)
                                i.assignInputCall('leftRight',
                                                  floater.leftright)
                                i.actor.afk_checker = None

                    elif m == 'mute':
                        if a == []:
                            bsInternal._chatMessage('Admin Muted The Chat')

                            def unmute():
                                if some.chatMuted:
                                    some.chatMuted = False
                                    bs.screenMessage('ChatMute Timed-Out',
                                                     transient=True,
                                                     color=(0.5, 0.5, 1))

                            with bs.Context('UI'):
                                bs.realTimer(120000, unmute)
                            some.chatMuted = True
                            succes = True
                        else:
                            kicker.kick(a[0],
                                        reason=' '.join(a[1:]),
                                        mute=True,
                                        warn=True)
                            succes = True
                    elif m == 'unmute':
                        bsInternal._chatMessage('Admin UnMuted The Chat')
                        some.chatMuted = False
                        import ChatManager
                        ChatManager.mutedIDs = []
                        succes = True
                    elif m == 'contact':
                        bsInternal._chatMessage('Discord: hollownest')
                    elif m == 'log':
                        open(some.logfile,
                             'a+').write('\n' * 5 +
                                         str(bsInternal._getGameRoster()) +
                                         '\n' +
                                         str(bsInternal._getChatMessages()))
                    elif m == 'whois':
                        if a == []:
                            bs.screenMessage('No Rank Provided')
                        elif not a[0].isdigit():
                            bs.screenMessage('Not A Valid Rank')
                        else:
                            handle.me(db.getUserFromRank(int(a[0])))
                    elif m == 'ip':
                        import reboot
                        bsInternal._chatMessage('IP: {} | Port: {}'.format(
                            reboot.ip, reboot.port))
                    elif m == 'me' or m == 'stats' or m == 'rank' or m == 'myself' or m == 'ranks':
                        if a == []:
                            handle.me(player)
                        else:
                            handle.me(handle.getPlayerFromNick(a[0]))
                    elif m in ['inv', 'inventory', 'items']:
                        if a == []:
                            handle.inv(player)
                        else:
                            handle.inv(handle.getPlayerFromNick(a[0]))
                    elif m == 'shop':
                        if len(a) > 0:
                            if a[0] == "hit-effect":
                                bsInternal._chatMessage('==========SMASH EFFECTS=========')
                                for i, k in some.hit_effect_prices.items():
                                    bsInternal._chatMessage(
                                        u"Name: {} {} Details: {} {} Cost: {} \ue01f/Day"
                                        .format(i.capitalize(), (' ' * (20 - len(i))),
                                                k['d'], (' ' * (20 - len(i))),
                                                str(k['c'])))
                                bs.screenMessage('\n' * 1000)
                        else:
                            bsInternal._chatMessage("You can buy these:")
                            bsInternal._chatMessage(
                                "Use /buy <name_of_perk> <no_of_days>")
                            bsInternal._chatMessage('==========COMMANDS=========')
                            for i, k in costs.items():
                                bsInternal._chatMessage(
                                    u"Command: /{} {} Cost: {} \ue01f".format(
                                        i, ' ' * (20 - len(i)), str(k)))

                            bsInternal._chatMessage('==========PERKS=========')
                            for i, k in some.prices.items():
                                bsInternal._chatMessage(
                                    u"Name: {} {} Details: {} {} Cost: {} \ue01f/Day"
                                    .format(i.capitalize(), (' ' * (20 - len(i))),
                                            k['d'], (' ' * (20 - len(i))),
                                            str(k['c'])))
                            bsInternal._chatMessage("New Effects Available Use: /shop hit-effect")
                            bs.screenMessage('\n' * 1000)
                    elif m == 'removetag':
                        n = handle.getPlayerFromNick(a[0]).get_account_id()
                        stats = db.getData(n)
                        stats['t'] = ''
                        bs.screenMessage('Tag Removed')
                        db.saveData(n, stats)
                        succes = True
                    elif m == 'addtag':
                        n = handle.getPlayerFromNick(a[0]).get_account_id()
                        stats = db.getData(n)
                        tag = ' '.join(a[1:])
                        if stats['t'] == '' or stats['t'] != '':
                            if len(tag) > 20:
                                return
                            tag = bs.uni(tag).replace(
                                '/c', u'\ue043').replace(
                                    '/d', u'\ue048')
                            stats['t'] = tag
                            bs.screenMessage('Tag Added')
                            db.saveData(n, stats)
                            succes = True
                    elif m == 'throw':
                        if a == []:
                            bs.screenMessage('No Item Specified')
                        else:
                            item = a[0]
                            import json
                            for i in bsInternal._getForegroundHostActivity(
                            ).players:
                                if i.getInputDevice().getClientID(
                                ) == clientID:
                                    n = i.get_account_id()
                                    break
                            else:
                                return
                            if True:
                                try:
                                    stats = db.getData(n)
                                    if item in stats['i']:
                                        stats['i'].pop(item)
                                        bs.screenMessage('Item Thrown Away')
                                    db.saveData(n, stats)
                                except Exception as e:
                                    print e
                                    return
                    elif m == 'id':
                        i = player
                        if i is not None:
                            n = i.get_account_id()
                            n2 = i.getInputDevice().getClientID()
                            bsInternal._chatMessage(
                                'Unique ID For Player %s : %s' %
                                (i.getName(True), n))
                        else:
                            #bs.screenMessage("Join Game First")
                            return
                    elif m == 'convert':
                        if len(a) == 1:
                            handle.convert(player, a[0])
                        else:
                            bsInternal._chatMessage('Usage: /convert amount')
                    elif m == 'bet' or m == 'gamble':
                        if a == []:
                            bs.screenMessage(
                                'You also need to enter the amount. Fool.',
                                color=(1, .5, .5))
                            bsInternal._chatMessage(
                                'Usage: /bet [amount/all/half]')
                        else:
                            handle.bet(player, a[0])
                    elif m == 'beg':
                        handle.beg(player)
                    elif m == 'daily':
                        try:
                            handle.daily(clientID)
                        except Exception as e:
                            print e
                    elif m == 'buy':
                        if a == []:
                            bsInternal._chatMessage(
                                'Item name not provided. Use /shop to get a list.'
                            )
                        else:
                            a[0] = bs.utf8(a[0]).lower()
                            if a[0] in some.all_prices:
                                import json
                                for i in bsInternal._getForegroundHostActivity(
                                ).players:
                                    if i.getInputDevice().getClientID(
                                    ) == clientID:
                                        n = i.get_account_id()
                                        break
                                else:
                                    return
                                if True:
                                    try:
                                        stats = {}
                                        stats = db.getData(n)
                                    except Exception as e:
                                        print e, '/buy get error'
                                        return
                                if a[0] in stats['i'] and a[0] not in ['tag', 'color-burst', 'damage-count']:
                                    bs.screenMessage(
                                        'You Already Have This Item!')
                                    return
                                if ('backflip' in stats['i'] and a[0] == 'backflip-protection') or 'backflip-protection' in stats['i'] and a[0] == 'backflip':
                                    bs.screenMessage(
                                        'You can\'t have both backflip and backflip-protection!')
                                    return
                                if a[0] != 'tag':
                                    try:
                                        limitDay = int(a[1])
                                        a[1] = int(a[1])
                                    except:
                                        limitDay = 1
                                else:
                                    limitDay = 9999
                                try:
                                    if stats['p'] >= (some.all_prices[a[0]]['c'] *
                                                      limitDay):
                                        stats['p'] -= (some.all_prices[a[0]]['c'] *
                                                       limitDay)
                                        import datetime
                                        expire_time = long(
                                            (datetime.datetime.now() +
                                             datetime.timedelta(days=limitDay)
                                             ).strftime("%Y%m%d%H%M")
                                        )  # (str(7*(len(History)//3)),"%d")
                                        if a[0] in list(some.hit_effect_prices.keys()):
                                            if len(a) > 1:
                                                if a[1] in self.availableColor:
                                                    stats['color'] = tuple(c * 10 for c in self.availableColor[a[1]])
                                                elif a[1] == "myself":
                                                    stats['color'] = tuple(c * 10 for c in player.color)
                                                else:
                                                    bsInternal._chatMessage("Elige un color Valido.")
                                                    bsInternal._chatMessage("ex: /buy color-burst <red/blue/green>")
                                                    return
                                            else:
                                                rand = random.choice(list(self.availableColor.values()))
                                                stats['color'] = tuple(c * 10 for c in rand)

                                        if a[0] == 'tag':
                                            tag = ' '.join(a[1:])
                                            if len(tag) > 20:
                                                return
                                            tag = bs.uni(tag).replace(
                                                '/c', u'\ue043').replace(
                                                    '/d', u'\ue048')
                                            if not any(i in re.sub(
                                                    '[^A-Za-z0-9]+', '',
                                                    tag.lower()) for i in [
                                                        'moderator', 'admin',
                                                        'owner'
                                            ]) and not tag.startswith(
                                                    u'\ue048#'):
                                                stats['t'] = tag
                                            else:
                                                return
                                        stats['i'].update({a[0]: expire_time})
                                        bs.playSound(bs.getSound('ding'))
                                        bs.screenMessage(
                                            'Purchase Successful! Expires on: {} | Use /throw {} to remove it'
                                            .format(
                                                (datetime.datetime.strptime(
                                                    str(expire_time),
                                                    "%Y%m%d%H%M").strftime(
                                                        "%d-%m-%Y %H:%M:%S")),
                                                a[0]))
                                        db.saveData(n, stats)
                                    else:
                                        bs.screenMessage(u'Not Enough \ue01f')
                                except Exception as e:
                                    print e
                            else:
                                bs.screenMessage("No Such Item Exists!")
                    if m == 'unban':
                        some.banned = []
                    if m == 'kick':
                        if a == []:
                            bsInternal._chatMessage(
                                'Using: /kick name or number of list')
                        else:
                            reason = ' '.join(
                                a[1:]) if ' '.join(a[1:]) != '' else None
                            self.kickByNick(a[0], reason=reason)
                            succes = True
                    if m == 'unwarn':
                        some.warn = {}
                        bs.screenMessage('All warns have been reset')
                        succes = True
                    if m == 'warn':
                        if a == []:
                            bsInternal._chatMessage(
                                'Using: /warn name or number of list')
                        else:
                            reason = ' '.join(
                                a[1:]) if ' '.join(a[1:]) != '' else None
                            kicker.kick(a[0], reason=reason, warn=True)
                            succes = True
                    elif m == 'list':
                        if len(a) > 0:
                            if a[0] == "admin":
                                bsInternal._chatMessage(
                                    "======== ADMIN LIST ========")
                                for id, name in db.getAllAdmins().items():
                                    bsInternal._chatMessage(
                                        name + "   |   id: " + id)
                            elif a[0] == "vip":
                                bsInternal._chatMessage(
                                    "======== VIP LIST ========")
                                for id, name in db.getAllVips().items():
                                    bsInternal._chatMessage(
                                        name + "   |   id: " + id)

                        else:
                            bsInternal._chatMessage(
                                "======== FOR /kick ONLY: ========")
                            for i in bsInternal._getGameRoster():
                                try:
                                    bsInternal._chatMessage(
                                        i['players'][0]['nameFull'] +
                                        "     (/kick " + str(i['clientID']) + ")")
                                except:
                                    bsInternal._chatMessage(i['displayString'] +
                                                            "     (/kick " +
                                                            str(i['clientID']) +
                                                            ")")
                            bsInternal._chatMessage(
                                "==================================")
                            bsInternal._chatMessage(
                                "======= For other commands: =======")
                            for s in bsInternal._getForegroundHostSession(
                            ).players:
                                bsInternal._chatMessage(
                                    s.getName() + "     " +
                                    str(bsInternal._getForegroundHostSession().
                                        players.index(s)))
                            bs.screenMessage('\n' * 1000)
                    elif m == 'ooh':
                        if a is not None and len(a) > 0:
                            s = int(a[0])

                            def oohRecurce(c):
                                bs.playSound(bs.getSound('ooh'), volume=2)
                                c -= 1
                                if c > 0:
                                    bs.gameTimer(
                                        int(a[1]) if len(a) > 1
                                        and a[1] is not None else 1000,
                                        bs.Call(oohRecurce, c=c))

                            oohRecurce(c=s)
                            succes = True
                        else:
                            bs.playSound(bs.getSound('ooh'), volume=2)
                            succes = True
                    elif m == 'playSound':
                        if a is not None and len(a) > 1:
                            s = int(a[1])

                            def oohRecurce(c):
                                bs.playSound(bs.getSound(str(a[0])), volume=2)
                                c -= 1
                                if c > 0:
                                    bs.gameTimer(
                                        int(a[2]) if len(a) > 2
                                        and a[2] is not None else 1000,
                                        bs.Call(oohRecurce, c=c))

                            oohRecurce(c=s)
                            succes = True
                        else:
                            bs.playSound(bs.getSound(str(a[0])), volume=2)
                            succes = True
                    elif m == 'quit' or m == 'restart':
                        bs.screenMessage(bs.Lstr(resource='internal.serverRestartingText'), transient=True)
                        bs.pushCall(bs.Call(bs.quit))
                        succes = True

                    elif m == 'nv':
                        if self.tint is None:
                            self.tint = bs.getSharedObject('globals').tint
                        bs.getSharedObject('globals').tint = (
                            0.5, 0.7,
                            1) if a == [] or not a[0] == u'off' else self.tint
                        succes = True

                    elif m == 'admin':
                        if a == []:
                            bs.screenMessage(
                                'usage: /admin add/remove <clientid>')
                        else:
                            if a[0] == 'add':
                                self.admin(a[1])
                            elif a[0] == 'remove':
                                self.deletedmin(a[1])
                    elif m == 'vip':
                        if a == []:
                            bs.screenMessage(
                                'usage: /vip add/remove <clientid>')
                        else:
                            if a[0] == 'add':
                                self.Vip(a[1])
                            elif a[0] == 'remove':
                                self.deletevip(a[1])

                    elif m == 'permaban':
                        if len(a) < 2:
                            bs.screenMessage("Format: /permaban <id/name/clientid> <rease>", clients=[clientID], transient=True)
                        else:
                            n = a[0]
                            reason = ' '.join(a[1:])
                            self.permaban(n, reason)
                            succes = True
                    elif m == 'freeze':
                        if a == []:
                            bsInternal._chatMessage(
                                'Using: /freeze all or number of list')
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(
                                            bs.FreezeMessage())
                                        succes = True
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(
                                    a[0])].actor.node.handleMessage(
                                        bs.FreezeMessage())
                                succes = True
                    elif m == 'thaw':
                        if a == []:
                            for i in range(len(activity.players)):
                                if activity.players[i].getInputDevice(
                                ).getClientID() == clientID:
                                    bsInternal._getForegroundHostActivity(
                                    ).players[i].actor.node.handleMessage(
                                        bs.ThawMessage())
                                    succes = True
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(
                                            bs.ThawMessage())
                                        succes = True
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(
                                    a[0])].actor.node.handleMessage(
                                        bs.ThawMessage())
                                succes = True
                    elif m == 'kill':
                        if a == []:
                            bsInternal._chatMessage(
                                'Using: /kill all or number of list')
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(
                                            bs.DieMessage())
                                        succes = True
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(
                                    a[0])].actor.node.handleMessage(
                                        bs.DieMessage())
                    elif m == 'curse':
                        if a == []:
                            bsInternal._chatMessage(
                                'Using: /curse all or number of list')
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.curse()
                                        succes = True
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(
                                    a[0])].actor.curse()
                                succes = True

                    elif m == 'spaz':
                        try:
                            if a == []:
                                bsInternal._chatMessage('Failed!! Usage: /spazall or /spaz number of list')
                            else:
                                if a[0] == 'all':
                                    for i in bs.getSession().players:
                                        # a.append(a[0])
                                        t = i.actor.node
                                        try:
                                            if a[1] in ['ali', 'neoSpaz', 'wizard', 'cyborg', 'penguin', 'agent', 'pixie', 'bear', 'bunny', 'zoe']:
                                                t.colorTexture = bs.getTexture(a[1] + 'Color')
                                                t.colorMaskTexture = bs.getTexture(a[1] + 'ColorMask')
                                                t.headModel = bs.getModel(a[1] + 'Head')
                                                t.torsoModel = bs.getModel(a[1] + 'Torso')
                                                t.pelvisModel = bs.getModel(a[1] + 'Pelvis')
                                                t.upperArmModel = bs.getModel(a[1] + 'UpperArm')
                                                t.foreArmModel = bs.getModel(a[1] + 'ForeArm')
                                                t.handModel = bs.getModel(a[1] + 'Hand')
                                                t.upperLegModel = bs.getModel(a[1] + 'UpperLeg')
                                                t.lowerLegModel = bs.getModel(a[1] + 'LowerLeg')
                                                t.toesModel = bs.getModel(a[1] + 'Toes')
                                                t.style = 'female' if a[1] == 'zoe' else a[1]
                                                succes = True
                                        except:
                                            print 'error'
                                    bs.screenMessage('All skin change!')
                                else:
                                    try:
                                        if a[1] in ['ali', 'neoSpaz', 'wizard', 'cyborg', 'penguin', 'agent', 'pixie', 'bear', 'bunny', 'zoe']:
                                            n = int(a[0])
                                            t = bs.getSession().players[n].actor.node
                                            t.colorTexture = bs.getTexture(a[1] + 'Color')
                                            t.colorMaskTexture = bs.getTexture(a[1] + 'ColorMask')
                                            t.headModel = bs.getModel(a[1] + 'Head')
                                            t.torsoModel = bs.getModel(a[1] + 'Torso')
                                            t.pelvisModel = bs.getModel(a[1] + 'Pelvis')
                                            t.upperArmModel = bs.getModel(a[1] + 'UpperArm')
                                            t.foreArmModel = bs.getModel(a[1] + 'ForeArm')
                                            t.handModel = bs.getModel(a[1] + 'Hand')
                                            t.upperLegModel = bs.getModel(a[1] + 'UpperLeg')
                                            t.lowerLegModel = bs.getModel(a[1] + 'LowerLeg')
                                            t.toesModel = bs.getModel(a[1] + 'Toes')
                                            t.style = 'female' if a[1] == 'zoe' else a[1]
                                            bs.screenMessage('Player skin change!')
                                            succes = True

                                    except:
                                        bsInternal._chatMessage('Failed!! Usage: /spazall or /spaz number of list')

                        except:
                            bs.screenMessage('error', color=(1, 0, 0))
                    elif m == 'box':
                        if a == []:
                            bsInternal._chatMessage(
                                'Using: /box all or number of list')
                        else:
                            try:
                                if a[0] == 'all':
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.torsoModel = bs.getModel(
                                                "tnt")
                                        except:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.colorMaskTexture = bs.getTexture(
                                                "tnt")
                                        except:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.colorTexture = bs.getTexture(
                                                "tnt")
                                        except:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.highlight = (1, 1, 1)
                                        except:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.color = (1, 1, 1)
                                        except:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.headModel = None
                                        except:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.style = "cyborg"
                                        except:
                                            pass
                                    succes = True
                                else:
                                    n = int(a[0])
                                    bs.getSession().players[
                                        n].actor.node.torsoModel = bs.getModel(
                                            "tnt")
                                    bs.getSession().players[
                                        n].actor.node.colorMaskTexture = bs.getTexture(
                                            "tnt")
                                    bs.getSession().players[
                                        n].actor.node.colorTexture = bs.getTexture(
                                            "tnt")
                                    bs.getSession(
                                    ).players[n].actor.node.highlight = (1, 1,
                                                                         1)
                                    bs.getSession(
                                    ).players[n].actor.node.color = (1, 1, 1)
                                    bs.getSession(
                                    ).players[n].actor.node.headModel = None
                                    bs.getSession(
                                    ).players[n].actor.node.style = "cyborg"
                                    succes = True
                            except:
                                bs.screenMessage('Error!', color=(1, 0, 0))
                    elif m == 'remove':
                        if a == []:
                            bsInternal._chatMessage(
                                'Using: /remove all or number of list')
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.removeFromGame()
                                        succes = True
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(
                                    a[0])].removeFromGame()
                                succes = True
                    elif m == 'end':
                        try:
                            bsInternal._getForegroundHostActivity().endGame()
                            bs.screenMessage(
                                "Finalizando Partida\nWait a minute..", color=(0.5, 0.5, 1))
                        except:
                            bs.screenMessage(
                                "Ya se Finalizo\nLa Partida", color=(1, 0.5, 0.5))
                    elif m == 'hug':
                        if a == []:
                            bsInternal._chatMessage(
                                'Using: /hug all or number of list')
                        else:
                            try:
                                if a[0] == 'all':
                                    try:
                                        bsInternal._getForegroundHostActivity(
                                        ).players[
                                            0].actor.node.holdNode = bsInternal._getForegroundHostActivity(
                                        ).players[1].actor.node
                                    except:
                                        pass
                                    try:
                                        bsInternal._getForegroundHostActivity(
                                        ).players[
                                            1].actor.node.holdNode = bsInternal._getForegroundHostActivity(
                                        ).players[0].actor.node
                                    except:
                                        pass
                                    try:
                                        bsInternal._getForegroundHostActivity(
                                        ).players[
                                            3].actor.node.holdNode = bsInternal._getForegroundHostActivity(
                                        ).players[2].actor.node
                                    except:
                                        pass
                                    try:
                                        bsInternal._getForegroundHostActivity(
                                        ).players[
                                            4].actor.node.holdNode = bsInternal._getForegroundHostActivity(
                                        ).players[3].actor.node
                                    except:
                                        pass
                                    try:
                                        bsInternal._getForegroundHostActivity(
                                        ).players[
                                            5].actor.node.holdNode = bsInternal._getForegroundHostActivity(
                                        ).players[6].actor.node
                                    except:
                                        pass
                                    try:
                                        bsInternal._getForegroundHostActivity(
                                        ).players[
                                            6].actor.node.holdNode = bsInternal._getForegroundHostActivity(
                                        ).players[7].actor.node
                                    except:
                                        pass
                                    succes = True
                                else:
                                    bsInternal._getForegroundHostActivity(
                                    ).players[int(
                                        a[0]
                                    )].actor.node.holdNode = bsInternal._getForegroundHostActivity(
                                    ).players[int(a[1])].actor.node
                                    succes = True
                            except:
                                bs.screenMessage('Error!', color=(1, 0, 0))
                    elif m == 'gm':
                        if a == []:
                            for i in range(len(activity.players)):
                                if activity.players[i].getInputDevice(
                                ).getClientID() == clientID:
                                    activity.players[
                                        i].actor.node.hockey = activity.players[
                                            i].actor.node.hockey == False
                                    activity.players[
                                        i].actor.node.invincible = activity.players[
                                            i].actor.node.invincible == False
                                    activity.players[
                                        i].actor._punchPowerScale = 5 if activity.players[
                                            i].actor._punchPowerScale == 1.2 else 1.2
                                    succes = True
                        else:
                            activity.players[int(
                                a[0])].actor.node.hockey = activity.players[
                                    int(a[0])].actor.node.hockey == False
                            activity.players[int(
                                a[0]
                            )].actor.node.invincible = activity.players[int(
                                a[0])].actor.node.invincible == False
                            activity.players[int(
                                a[0]
                            )].actor._punchPowerScale = 5 if activity.players[
                                int(a[0]
                                    )].actor._punchPowerScale == 1.2 else 1.2
                            succes = True
                    elif m == 'tint':
                        if a == []:
                            bsInternal._chatMessage('Using: /tint R G B')
                            bsInternal._chatMessage('OR')
                            bsInternal._chatMessage(
                                'Using: /tint r bright speed')
                        else:
                            if a[0] == 'r':
                                m = 1.3 if a[1] is None else float(a[1])
                                s = 1000 if a[2] is None else float(a[2])
                                bsUtils.animateArray(
                                    bs.getSharedObject('globals'), 'tint', 3, {
                                        0: (1 * m, 0, 0),
                                        s: (0, 1 * m, 0),
                                        s * 2: (0, 0, 1 * m),
                                        s * 3: (1 * m, 0, 0)
                                    }, True)
                                succes = True
                            else:
                                try:
                                    if a[1] is not None:
                                        bs.getSharedObject('globals').tint = (
                                            float(a[0]), float(a[1]),
                                            float(a[2]))
                                        succes = True
                                    else:
                                        bs.screenMessage('Error!',
                                                         color=(1, 0, 0))
                                except:
                                    bs.screenMessage('Error!', color=(1, 0, 0))
                    elif m == 'pause':
                        bs.getSharedObject(
                            'globals').paused = bs.getSharedObject(
                                'globals').paused == False
                        succes = True
                    elif m == 'sm':
                        bs.getSharedObject(
                            'globals').slowMotion = bs.getSharedObject(
                                'globals').slowMotion == False
                        succes = True
                    # elif m == '/bunny':
                    #     if a == []:
                    #         bsInternal._chatMessage('Using: /bunny count owner(number of list)')
                    #     import BuddyBunny
                    #     for i in range(int(a[0])):
                    #         p=bs.getSession().players[int(a[1])]
                    #         if not 'bunnies' in p.gameData:
                    #             p.gameData['bunnies'] = BuddyBunny.BunnyBotSet(p)
                    #         p.gameData['bunnies'].doBunny()
                    elif m == 'cameraMode':
                        try:
                            if bs.getSharedObject(
                                    'globals').cameraMode == 'follow':
                                bs.getSharedObject(
                                    'globals').cameraMode = 'rotate'
                                succes = True
                            else:
                                bs.getSharedObject(
                                    'globals').cameraMode = 'follow'
                                succes = True
                        except:
                            pass
                    elif m == 'lm':
                        arr = []
                        for i in range(100):
                            try:
                                arr.append(bsInternal._getChatMessages()[-1 -
                                                                         i])
                                succes = True
                            except:
                                pass
                        arr.reverse()
                        for i in arr:
                            if not 'Server67323: ' in i:
                                bsInternal._chatMessage(i)
                    elif m == 'gp':
                        if a == []:
                            bsInternal._chatMessage(
                                'Using: /gp number of list')
                        else:
                            s = bsInternal._getForegroundHostSession()
                            for i in s.players[int(a[0])].getInputDevice(
                            )._getPlayerProfiles():
                                try:
                                    bsInternal._chatMessage(i)
                                    succes = True
                                except:
                                    pass
                            bs.screenMessage('\n' * 1000)
                    elif m == 'joke':
                        threading.Thread(target=handle.joke,
                                         args=(player.getName(
                                             True, False), )).start()
                        succes = True

                    elif m == 'icy':
                        bsInternal._getForegroundHostActivity().players[int(
                            a[0]
                        )].actor.node = bsInternal._getForegroundHostActivity(
                        ).players[int(a[1])].actor.node
                        succes = True
                    elif m == 'fly':
                        if a == []:
                            bsInternal._chatMessage(
                                'Using: /fly all or number of list')
                        else:
                            if a[0] == 'all':
                                for i in bsInternal._getForegroundHostActivity(
                                ).players:
                                    i.actor.node.fly = True
                                    succes = True
                            else:
                                bsInternal._getForegroundHostActivity(
                                ).players[int(
                                    a[0]
                                )].actor.node.fly = bsInternal._getForegroundHostActivity(
                                ).players[int(a[0])].actor.node.fly == False
                                succes = True
                    elif m == 'floorReflection':
                        bs.getSharedObject(
                            'globals').floorReflection = bs.getSharedObject(
                                'globals').floorReflection == False
                        succes = True
                    elif m == 'ac':
                        if a == []:
                            bsInternal._chatMessage('Using: /ac R G B')
                            bsInternal._chatMessage('OR')
                            bsInternal._chatMessage(
                                'Using: /ac r bright speed')
                        else:
                            if a[0] == 'r':
                                m = 1.3 if a[1] is None else float(a[1])
                                s = 1000 if a[2] is None else float(a[2])
                                bsUtils.animateArray(
                                    bs.getSharedObject('globals'),
                                    'ambientColor', 3, {
                                        0: (1 * m, 0, 0),
                                        s: (0, 1 * m, 0),
                                        s * 2: (0, 0, 1 * m),
                                        s * 3: (1 * m, 0, 0)
                                    }, True)
                                succes = True
                            else:
                                try:
                                    if a[1] is not None:
                                        bs.getSharedObject(
                                            'globals').ambientColor = (float(
                                                a[0]), float(a[1]), float(
                                                    a[2]))
                                        succes = True
                                    else:
                                        bs.screenMessage('Error!',
                                                         color=(1, 0, 0))
                                except:
                                    bs.screenMessage('Error!', color=(1, 0, 0))
                    elif m == 'rt':
                        global times
                        if a == []:
                            choice = 1
                        else:
                            choice = int(a[0])
                        times = 1
                        defdict = {}

                        def fix():
                            for i, k in defdict.items():
                                try:
                                    i.colorTexture = k
                                except:
                                    pass

                        def asset():
                            global times
                            nodes = bs.getNodes()
                            times += 1
                            assets = []
                            models = []
                            assetnames = [
                                'achievementBoxer', 'achievementCrossHair',
                                'achievementDualWielding', 'achievementEmpty',
                                'achievementFlawlessVictory',
                                'achievementFootballShutout',
                                'achievementFootballVictory',
                                'achievementFreeLoader',
                                'achievementGotTheMoves',
                                'achievementInControl',
                                'achievementMedalLarge',
                                'achievementMedalMedium',
                                'achievementMedalSmall', 'achievementMine',
                                'achievementOffYouGo', 'achievementOnslaught',
                                'achievementOutline', 'achievementRunaround',
                                'achievementSharingIsCaring',
                                'achievementStayinAlive',
                                'achievementSuperPunch', 'achievementTNT',
                                'achievementTeamPlayer', 'achievementWall',
                                'achievementsIcon', 'actionButtons',
                                'actionHeroColor', 'actionHeroColorMask',
                                'actionHeroIcon', 'actionHeroIconColorMask',
                                'advancedIcon', 'agentColor', 'agentColorMask',
                                'agentIcon', 'agentIconColorMask',
                                'aliBSRemoteIOSQR', 'aliColor', 'aliColorMask',
                                'aliControllerQR', 'aliIcon',
                                'aliIconColorMask', 'aliSplash', 'alienColor',
                                'alienColorMask', 'alienIcon',
                                'alienIconColorMask', 'alwaysLandBGColor',
                                'alwaysLandLevelColor', 'alwaysLandPreview',
                                'analogStick', 'arrow', 'assassinColor',
                                'assassinColorMask', 'assassinIcon',
                                'assassinIconColorMask', 'audioIcon',
                                'backIcon', 'bar', 'bearColor',
                                'bearColorMask', 'bearIcon',
                                'bearIconColorMask', 'bg', 'bigG',
                                'bigGPreview', 'black', 'bombButton',
                                'bombColor', 'bombColorIce', 'bombStickyColor',
                                'bonesColor', 'bonesColorMask', 'bonesIcon',
                                'bonesIconColorMask', 'boxingGlovesColor',
                                'bridgitLevelColor', 'bridgitPreview',
                                'bunnyColor', 'bunnyColorMask', 'bunnyIcon',
                                'bunnyIconColorMask', 'buttonBomb',
                                'buttonJump', 'buttonPickUp', 'buttonPunch',
                                'buttonSquare', 'chTitleChar1', 'chTitleChar2',
                                'chTitleChar3', 'chTitleChar4', 'chTitleChar5',
                                'characterIconMask', 'chestIcon',
                                'chestIconEmpty', 'chestIconMulti',
                                'chestOpenIcon', 'circle', 'circleNoAlpha',
                                'circleOutline', 'circleOutlineNoAlpha',
                                'circleShadow', 'circleZigZag', 'coin',
                                'controllerIcon', 'courtyardLevelColor',
                                'courtyardPreview', 'cowboyColor',
                                'cowboyColorMask', 'cowboyIcon',
                                'cowboyIconColorMask', 'cragCastleLevelColor',
                                'cragCastlePreview', 'crossOut',
                                'crossOutMask', 'cursor', 'cuteSpaz',
                                'cyborgColor', 'cyborgColorMask', 'cyborgIcon',
                                'cyborgIconColorMask', 'doomShroomBGColor',
                                'doomShroomLevelColor', 'doomShroomPreview',
                                'downButton', 'egg1', 'egg2', 'egg3', 'egg4',
                                'eggTex1', 'eggTex2', 'eggTex3', 'empty',
                                'explosion', 'eyeColor', 'eyeColorTintMask',
                                'file', 'flagColor', 'flagPoleColor', 'folder',
                                'fontBig', 'fontExtras', 'fontExtras2',
                                'fontExtras3', 'fontExtras4', 'fontSmall0',
                                'fontSmall1', 'fontSmall2', 'fontSmall3',
                                'fontSmall4', 'fontSmall5', 'fontSmall6',
                                'fontSmall7', 'footballStadium',
                                'footballStadiumPreview', 'frameInset',
                                'frostyColor', 'frostyColorMask', 'frostyIcon',
                                'frostyIconColorMask', 'fuse',
                                'gameCenterIcon', 'gameCircleIcon',
                                'gladiatorColor', 'gladiatorColorMask',
                                'gladiatorIcon', 'gladiatorIconColorMask',
                                'glow', 'googlePlayAchievementsIcon',
                                'googlePlayGamesIcon',
                                'googlePlayLeaderboardsIcon', 'googlePlusIcon',
                                'googlePlusSignInButton', 'graphicsIcon',
                                'heart', 'hockeyStadium',
                                'hockeyStadiumPreview', 'iconOnslaught',
                                'iconRunaround', 'impactBombColor',
                                'impactBombColorLit', 'inventoryIcon',
                                'jackColor', 'jackColorMask', 'jackIcon',
                                'jackIconColorMask', 'jumpsuitColor',
                                'jumpsuitColorMask', 'jumpsuitIcon',
                                'jumpsuitIconColorMask', 'kronk',
                                'kronkColorMask', 'kronkIcon',
                                'kronkIconColorMask', 'lakeFrigid',
                                'lakeFrigidPreview', 'lakeFrigidReflections',
                                'landMine', 'landMineLit', 'leaderboardsIcon',
                                'leftButton', 'levelIcon', 'light',
                                'lightSharp', 'lightSoft', 'lock', 'logIcon',
                                'logo', 'logoEaster', 'mapPreviewMask',
                                'medalBronze', 'medalComplete', 'medalGold',
                                'medalSilver', 'melColor', 'melColorMask',
                                'melIcon', 'melIconColorMask', 'menuBG',
                                'menuButton', 'menuIcon', 'meter',
                                'monkeyFaceLevelColor', 'monkeyFacePreview',
                                'multiplayerExamples', 'natureBackgroundColor',
                                'neoSpazColor', 'neoSpazColorMask',
                                'neoSpazIcon', 'neoSpazIconColorMask',
                                'nextLevelIcon', 'ninjaColor',
                                'ninjaColorMask', 'ninjaIcon',
                                'ninjaIconColorMask', 'nub', 'null',
                                'oldLadyColor', 'oldLadyColorMask',
                                'oldLadyIcon', 'oldLadyIconColorMask',
                                'operaSingerColor', 'operaSingerColorMask',
                                'operaSingerIcon', 'operaSingerIconColorMask',
                                'ouyaAButton', 'ouyaIcon', 'ouyaOButton',
                                'ouyaUButton', 'ouyaYButton', 'penguinColor',
                                'penguinColorMask', 'penguinIcon',
                                'penguinIconColorMask', 'pixieColor',
                                'pixieColorMask', 'pixieIcon',
                                'pixieIconColorMask', 'playerLineup',
                                'powerupBomb', 'powerupCurse', 'powerupHealth',
                                'powerupIceBombs', 'powerupImpactBombs',
                                'powerupLandMines', 'powerupPunch',
                                'powerupShield', 'powerupSpeed',
                                'powerupStickyBombs', 'puckColor',
                                'rampageBGColor', 'rampageBGColor2',
                                'rampageLevelColor', 'rampagePreview',
                                'reflectionChar_+x', 'reflectionChar_+y',
                                'reflectionChar_+z', 'reflectionChar_-x',
                                'reflectionChar_-y', 'reflectionChar_-z',
                                'reflectionPowerup_+x', 'reflectionPowerup_+y',
                                'reflectionPowerup_+z', 'reflectionPowerup_-x',
                                'reflectionPowerup_-y', 'reflectionPowerup_-z',
                                'reflectionSharp_+x', 'reflectionSharp_+y',
                                'reflectionSharp_+z', 'reflectionSharp_-x',
                                'reflectionSharp_-y', 'reflectionSharp_-z',
                                'reflectionSharper_+x', 'reflectionSharper_+y',
                                'reflectionSharper_+z', 'reflectionSharper_-x',
                                'reflectionSharper_-y', 'reflectionSharper_-z',
                                'reflectionSharpest_+x',
                                'reflectionSharpest_+y',
                                'reflectionSharpest_+z',
                                'reflectionSharpest_-x',
                                'reflectionSharpest_-y',
                                'reflectionSharpest_-z', 'reflectionSoft_+x',
                                'reflectionSoft_+y', 'reflectionSoft_+z',
                                'reflectionSoft_-x', 'reflectionSoft_-y',
                                'reflectionSoft_-z', 'replayIcon',
                                'rgbStripes', 'rightButton', 'robotColor',
                                'robotColorMask', 'robotIcon',
                                'robotIconColorMask', 'roundaboutLevelColor',
                                'roundaboutPreview', 'santaColor',
                                'santaColorMask', 'santaIcon',
                                'santaIconColorMask', 'scorch', 'scorchBig',
                                'scrollWidget', 'scrollWidgetGlow',
                                'settingsIcon', 'shadow', 'shadowSharp',
                                'shadowSoft', 'shield', 'shrapnel1Color',
                                'slash', 'smoke', 'softRect', 'softRect2',
                                'softRectVertical', 'sparks', 'star',
                                'startButton', 'stepRightUpLevelColor',
                                'stepRightUpPreview', 'storeCharacter',
                                'storeCharacterEaster', 'storeCharacterXmas',
                                'storeIcon', 'superheroColor',
                                'superheroColorMask', 'superheroIcon',
                                'superheroIconColorMask', 'textClearButton',
                                'thePadLevelColor', 'thePadPreview',
                                'ticketRoll', 'ticketRollBig', 'ticketRolls',
                                'tickets', 'ticketsMore', 'tipTopBGColor',
                                'tipTopLevelColor', 'tipTopPreview', 'tnt',
                                'touchArrows', 'touchArrowsActions',
                                'towerDLevelColor', 'towerDPreview',
                                'treesColor', 'trophy', 'tv', 'uiAtlas',
                                'uiAtlas2', 'upButton', 'usersButton',
                                'vrFillMound', 'warriorColor',
                                'warriorColorMask', 'warriorIcon',
                                'warriorIconColorMask', 'white',
                                'windowHSmallVMed', 'windowHSmallVSmall',
                                'wings', 'witchColor', 'witchColorMask',
                                'witchIcon', 'witchIconColorMask',
                                'wizardColor', 'wizardColorMask', 'wizardIcon',
                                'wizardIconColorMask', 'wrestlerColor',
                                'wrestlerColorMask', 'wrestlerIcon',
                                'wrestlerIconColorMask', 'zigZagLevelColor',
                                'zigzagPreview', 'zoeColor', 'zoeColorMask',
                                'zoeIcon', 'zoeIconColorMask'
                            ]
                            for i in assetnames:
                                assets.append(bs.getTexture(i))
                            # for i in nodes:
                            # if hasattr(i,'colorTexture'):
                            #if i.colorTexture not in assets:assets.append(i.colorTexture)
                            # if hasattr(i,'model'):
                            #   if i.model not in models:models.append(i.model)
                            for i in nodes:
                                if hasattr(i, 'colorTexture'):
                                    if i not in defdict:
                                        defdict.update({i: i.colorTexture})
                                    i.colorTexture = random.choice(assets)
                                # if hasattr(i,'model'):
                                #   i.model = random.choice(models)
                            if times <= choice:
                                bs.gameTimer(1000, asset)
                            else:
                                bs.gameTimer(1000, fix)

                        asset()
                        succes = True
                    elif m == 'iceOff':
                        try:
                            activity.getMap().node.materials = [
                                bs.getSharedObject('footingMaterial')
                            ]
                            activity.getMap().isHockey = False
                        except:
                            pass
                        try:
                            activity.getMap().floor.materials = [
                                bs.getSharedObject('footingMaterial')
                            ]
                            activity.getMap().isHockey = False
                        except:
                            pass
                        for i in activity.players:
                            i.actor.node.hockey = False
                        succes = True
                    elif m == 'maxPlayers':
                        if a == []:
                            bsInternal._chatMessage(
                                'Using: /maxPlayers count of players')
                        else:
                            try:
                                #bsInternal._getForegroundHostSession()._maxPlayers = int(a[0])
                                import detect
                                detect.maxPlayers = int(a[0])
                                bsInternal._setPublicPartyMaxSize(int(a[0]))
                                bsInternal._chatMessage(
                                    'Players limit set to ' + str(int(a[0])))
                                succes = True
                            except:
                                bs.screenMessage('Error!', color=(1, 0, 0))
                    elif m == 'heal':
                        if a == []:
                            for i in range(len(activity.players)):
                                if activity.players[i].getInputDevice(
                                ).getClientID() == clientID:
                                    bsInternal._getForegroundHostActivity(
                                    ).players[i].actor.node.handleMessage(
                                        bs.PowerupMessage(
                                            powerupType='health'))
                                    succes = True
                        elif a[0] == 'all':
                            for i in activity.players:
                                if i.exists() and i.actor.node.exists():
                                    i.actor.node.handleMessage(
                                        bs.PowerupMessage(
                                            powerupType='health'))
                                    succes = True
                        else:
                            try:
                                bsInternal._getForegroundHostActivity(
                                ).players[int(a[0])].actor.node.handleMessage(
                                    bs.PowerupMessage(powerupType='health'))
                                succes = True
                            except:
                                bs.screenMessage('Error!', color=(1, 0, 0))
                    elif m == 'reflections':
                        if a == [] or len(a) < 2:
                            bsInternal._chatMessage(
                                'Using: /reflections type(1/0) scale')
                        else:
                            rs = [int(a[1])]
                            type = 'soft' if int(a[0]) == 0 else 'powerup'
                            try:
                                bsInternal._getForegroundHostActivity().getMap(
                                ).node.reflection = type
                                bsInternal._getForegroundHostActivity().getMap(
                                ).node.reflectionScale = rs
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap(
                                ).bg.reflection = type
                                bsInternal._getForegroundHostActivity().getMap(
                                ).bg.reflectionScale = rs
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap(
                                ).floor.reflection = type
                                bsInternal._getForegroundHostActivity().getMap(
                                ).floor.reflectionScale = rs
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap(
                                ).center.reflection = type
                                bsInternal._getForegroundHostActivity().getMap(
                                ).center.reflectionScale = rs
                            except:
                                pass
                            succes = True
                    elif m == 'shatter':
                        if a == []:
                            bsInternal._chatMessage(
                                'Using: /shatter all or number of list')
                        else:
                            if a[0] == 'all':
                                for i in bsInternal._getForegroundHostActivity(
                                ).players:
                                    i.actor.node.shattered = int(a[1])
                                    succes = True
                            else:
                                bsInternal._getForegroundHostActivity(
                                ).players[int(
                                    a[0])].actor.node.shattered = int(a[1])
                                succes = True
                    elif m == 'cm':
                        if a == []:
                            time = 8000
                            succes = True
                        else:
                            time = int(a[0])

                            op = 0.08
                            std = bs.getSharedObject('globals').vignetteOuter
                            bsUtils.animateArray(
                                bs.getSharedObject('globals'), 'vignetteOuter',
                                3, {
                                    0: bs.getSharedObject(
                                        'globals').vignetteOuter,
                                    17000: (0, 1, 0)
                                })
                            succes = True
                        try:
                            bsInternal._getForegroundHostActivity().getMap(
                            ).node.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap(
                            ).bg.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap(
                            ).bg.node.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap(
                            ).node1.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap(
                            ).node2.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap(
                            ).node3.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap(
                            ).steps.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap(
                            ).floor.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap(
                            ).center.opacity = op
                        except:
                            pass

                        def off():
                            op = 1
                            try:
                                bsInternal._getForegroundHostActivity().getMap(
                                ).node.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap(
                                ).bg.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap(
                                ).bg.node.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap(
                                ).node1.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap(
                                ).node2.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap(
                                ).node3.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap(
                                ).steps.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap(
                                ).floor.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap(
                                ).center.opacity = op
                            except:
                                pass
                            bsUtils.animateArray(
                                bs.getSharedObject('globals'), 'vignetteOuter',
                                3, {
                                    0: bs.getSharedObject(
                                        'globals').vignetteOuter,
                                    100: std
                                })

                        bs.gameTimer(time, bs.Call(off))

                    # elif m == '/help':
                    #     with open(some.helpfile) as f:
                    #         for i in f.read().split('\n'):
                    #             if i != "":
                    #                 bsInternal._chatMessage(i)
                    #     bs.screenMessage('\n' * 1000)

        except:
            reply = "An Error Has Occurred"
            # bs.printException()
            return


c = chatOptions()


def cmd(v):
    global reply
    global succes
    c.opt(v[0], v[1])
    if succes and reply is not None:
        with bs.Context('UI'):
            bs.screenMessage(reply, transient=True, color=(0, 1, 0))
            bsInternal._chatMessage(reply)
            succes = False


def lolwa():
    bs.realTimer(1000, bs.Call(bsInternal._setPartyIconAlwaysVisible, True))
    bs.realTimer(1001, lolwa)


if some.os == 'nt':
    lolwa()
with bs.Context('UI'):
    bs.realTimer(5000, bs.Call(bsInternal._setPartyIconAlwaysVisible, True))


class FlyBox(bs.Actor):
    def __init__(self, position=(0, 1, 0)):
        bs.Actor.__init__(self)

        txt = bs.getTexture('rgbStripes')
        mod = bs.getModel('powerup')
        pos = (position[0], position[1] + 1.5,
               position[2])
        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={
                                   'position': pos,
                                   'colorTexture': txt,
                                   'model': mod,
                                   'body': 'box',
                                   'shadowSize': 0.5,
                                   'reflection': 'powerup',
                                   'reflectionScale': [1.0],
                                   'materials': [bs.getSharedObject('objectMaterial')]
                               })

    def handleMessage(self, msg):
        if isinstance(msg, bs.OutOfBoundsMessage):
            self.handleMessage(bs.DieMessage())
        elif isinstance(msg, bs.PickedUpMessage):
            self.node.gravityScale = -1.0
        elif isinstance(msg, bs.DroppedMessage):
            self.node.gravityScale = 1.0
        elif isinstance(msg, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        else:
            bs.Actor.handleMessage(self, msg)
