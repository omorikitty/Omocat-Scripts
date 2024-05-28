# -*- coding: utf-8 -*-
import bsGame
import bsUtils
import bsInternal
import random
import bs
import some
from thread import start_new_thread
import bsScoreBoard
import weakref
import bsTeamGame
from bsTeamGame import *


def setup():
    bsTeamGame.gDefaultTeamColors = ((0.5, 1.0, 1.0), (1.0, 1.0, 0.5))
    bsTeamGame.gDefaultTeamNames = ("α Alpha Team α", "β Beta Team β")
    #if getattr(some,'four_teams',False):
    #   bsTeamGame.gDefaultTeamColors += ((1,0,0), (0, 1, 0))
    #  bsTeamGame.gDefaultTeamNames += ("y Gamma Team y", "ẟ Delta Team ẟ")


if some.logic_team_settings: setup()

def _Modify_getMaxPlayers(self):
    """
    Return the max number of bs.Players allowed to join the game at once.
    """
    if self._useTeams:
        try:
            return bs.getConfig()['Team Game Max Players']
        except Exception:
            return 8
    else:
        try:
            return bs.getConfig()['Free-for-All Max Players']
        except Exception:
            return 14

bsTeamGame.TeamBaseSession.getMaxPlayers =  _Modify_getMaxPlayers
