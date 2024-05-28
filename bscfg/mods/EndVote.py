import bs
import time
import handle
import bsInternal

last_end_vote_start_time = 0
end_vote_duration = 50
game_started_on = 0
min_game_duration_to_start_end_vote = 30

voters = []

def vote_end(pb_id, client_id):
    global voters
    global last_end_vote_start_time
    now = time.time()
    if now > last_end_vote_start_time + end_vote_duration:
        voters = []
        last_end_vote_start_time = now
    if now < game_started_on + min_game_duration_to_start_end_vote:
        bs.screenMessage("Seems game just started\nTry again after some time", color=(0.7, 0.7, 1), transient=True,
                          clients=[client_id])
        return
    if len(voters) == 0:
        bs.screenMessage("end vote started", color=(0.7, 0.7, 1))

    # clean up voters list
    active_players = []
    #print active_players
    for i in bsInternal._getGameRoster():
        if len(i['players']) > 0:
            n = handle.getAccountIDFromClientID(i['clientID'])
            active_players.append(n)

    for voter in voters:
        if voter not in active_players:
            voters.remove(voter)
    if pb_id not in voters:
        voters.append(pb_id)
        bs.screenMessage("Thanks for vote\nencourage other players to type 'end' too.", color=(0.7, 0.7, 1), transient=True,
                          clients=[client_id])
        update_vote_text(required_votes(len(active_players)) - len(voters))
        if required_votes(len(active_players)) - len(
                voters) == 3:  # lets dont spam chat/screen message with votes required , only give message when only 3 votes left
            bs.screenMessage("3 more end votes required", color=(0.7, 0.7, 1))

    if len(voters) >= required_votes(len(active_players)):
        bs.screenMessage("end vote succeed", color=(0, 2, 0))
        try:
            with bs.Context(bsInternal._getForegroundHostActivity()):
                bsInternal._getForegroundHostActivity().endGame()
        except:
            pass


def required_votes(players):
    if players == 2:
        return 1
    elif players == 3:
        return 2
    elif players == 4:
        return 2
    elif players == 5:
        return 3
    elif players == 6:
        return 3
    elif players == 7:
        return 4
    elif players == 8:
        return 4
    elif players == 10:
        return 5
    else:
        return players - 4



def update_vote_text(votes_needed):
    activity = bsInternal._getForegroundHostActivity()
    try:
        activity.end_vote_text.node.text = "{}\nvotos".format(votes_needed)
    except:
        with bs.Context(bsInternal._getForegroundHostActivity()):
            node = bs.NodeActor(bs.newNode('text',
                                           attrs={
                                               'vAttach': 'top',
                                               'hAttach': 'center',
                                               'hAlign': 'center',
                                               'color': (0.5,0.5,0.5),
                                               'flatness': 0.5,
                                               'shadow': 0.5,
                                               'position': (-10, -50),
                                               'scale': 0.7,
                                               'text': '{}\nvotos'.format(
                                                   votes_needed)
                                           })).autoRetain()
            activity.end_vote_text = node
            bs.Timer(20, remove_vote_text)


def remove_vote_text():
    activity = bsInternal._getForegroundHostActivity()
    if hasattr(activity, "end_vote_text") and activity.end_vote_text.node.exists():
        activity.end_vote_text.node.delete()