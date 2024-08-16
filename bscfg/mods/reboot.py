import bs
import bsInternal
import urllib2
import bsUtils
import DB_Manager
import bsUtils
import some
import ChatManager
from datetime import datetime
from datetime import timedelta

try:
    req = urllib2.Request('http://icanhazip.com', data=None)
    response = urllib2.urlopen(req, timeout=5)
    ip = str(bs.uni(response.read())).rstrip()
except:
    ip = 'Failed To Fetch IP'
port = str(bs.getConfig().get('Port', 43210))

def restart():
    bs.screenMessage(bs.Lstr(resource='internal.serverRestartingText'),transient=True)
    text = 'IP: %s  Port: %s' % (ip, port)
    bsInternal._chatMessage(text)
    ChatManager.save_cache_phrase()
    bs.realTimer(3000, bs.Call(bs.quit))



bs.realTimer(2 * 60 * 60 * 1000, restart)


def warn():
    bs.screenMessage('Server is going to reboot in 1 minute', transient=True)


bs.realTimer((2 * 60 * 60 * 1000) - 60000, warn)


# def _init_map(func):
#     def deco(*args, **kwargs):
#         func(*args, **kwargs)


#         def _restart_ticks():
#             args[0]._restart_time = -1
#             if args[0]._restart_time <= 0:
#                 args[0]._restart_timer = None
#                 #bs.Timer(1000, bs.quit)


#         def _restart_server(duration=60 * 60):
#             if duration <= 0:
#                 return
#             args[0]._restart_time = duration
#             args[0]._restart_timer = bs.Timer(
#                 1000, _restart_ticks, repeat=True)
#             args[0]._restart_server = bs.newNode('text',
#                     attrs={
#                        'vAttach': 'top',
#                        'hAttach': 'center',
#                        'hAlign': 'center',
#                        'color': (0.5,0.5,0.5),
#                        'flatness': 0.5,
#                        'shadow': 0.5,
#                        'position': (-10, -50),
#                        'scale': 0.7
#                     })
#             args[0]._restart_server_input = bs.newNode(
#                     'timeDisplay', attrs={'time2': duration*1000, 'timeMin': 0})
#             bs.getSharedObject('globals').connectAttr(
#                 'gameTime', args[0]._restart_server_input, 'time1')
#             args[0]._restart_server_input.connectAttr(
#                 'output', args[0]._restart_server, 'text')
#         _restart_server()

#     return deco

# import bsMap
# bsMap.Map.__init__ = _init_map(bsMap.Map.__init__)
