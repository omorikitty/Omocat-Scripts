# -*- coding: utf-8 -*-
import bs
import bsInternal
import time
import threading
import some
import handle
banned = []
permabanned = []
old = []
maxPlayers = 15
players_num = 0
config_maxPlayers = 0

class _detect(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        try:
            global old
            global maxPlayers
            global players_num
            roster = bsInternal._getGameRoster()
            players_num = len(roster) if len(roster) != 0 else 1
            bsInternal._setPublicPartyMaxSize(
                min(max(9,
                        len(roster) + 1), maxPlayers))
            global banned
            global permabanned
            banned = set(some.banned)
            permabanned = set(some.permabanned)
            if roster != old:
                for i in roster:
                    a = bs.uni(i['displayString'])
                    name = i['players'][0]['name']
                    player = handle.getPlayerFromNick(name)
                    account_id = str(player.get_account_id())
                    # print a
                    if a in banned:
                        with bs.Context('UI'):
                            bs.screenMessage(
                                "You Have Been Banned. If The Ban Is Temporary, Try Joining After Some Time.",
                                transient=True,
                                clients=[int(i['clientID'])])
                        bsInternal._disconnectClient(int(i['clientID']))

                    if a in permabanned:
                        with bs.Context('UI'):
                            bs.screenMessage(
                                'You Have Been Permabanned.',
                                transient=True,
                                clients=[int(i['clientID'])])
                        bsInternal._disconnectClient(int(i['clientID']))

                    # if eval(i['specString'])["a"] in [
                    #         '', 'Server'
                    # ] and int(i['clientID']) != -1:
                    #     with bs.Context('UI'):
                    #         bs.screenMessage("V2 ACCOUNT DETECTED!..bee boop",
                    #                          color=(0.5, 1.0, 0.5),
                    #                          transient=True,
                    #                          clients=[int(i['clientID'])])
                    #     #bsInternal._disconnectClient(int(i['clientID']))
                old = roster
        except Exception as e:
            pass
        bs.realTimer(2000, self.run)


def setmax():
    global maxPlayers
    global config_maxPlayers
    maxPlayers = bsInternal._getPublicPartyMaxSize()
    config_maxPlayers = maxPlayers
    bs.realTimer(1500, setmax)


def reset():
    global maxPlayers
    maxPlayers = config_maxPlayers

_detect().start()