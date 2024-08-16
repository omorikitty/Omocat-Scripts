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
    votes = 0
    max_vote = 0
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
    active_players = [handle.getAccountIDFromClientID(i['clientID']) for i in bsInternal._getGameRoster() if len(i['players']) > 0]
    voters = [voter for voter in voters if voter in active_players]

    for voter in voters:
        if voter not in active_players:
            voters.remove(voter)
    if pb_id not in voters:
        voters.append(pb_id)
        bs.screenMessage("Thanks for vote\nencourage other players to type 'end' too.", color=(0.7, 0.7, 1), transient=True,
                         clients=[client_id])
        update_vote_text(len(voters), required_votes(len(active_players)))
        if len(active_players) - len(voters) == 3:
            bs.screenMessage("3 more end votes required", color=(0.7, 0.7, 1))

    if len(voters) >= required_votes(len(active_players)):
        bs.screenMessage("end vote succeed", color=(0, 2, 0))
        try:
            with bs.Context(bsInternal._getForegroundHostActivity()):
                bsInternal._getForegroundHostActivity().endGame()
        except:
            pass


def required_votes(voters_count, method="mayoria", percentage=0.75, min_votes=3):
    if method == "mayoria":
        return max(1, int(voters_count / 2) + 1)
    elif method == "forpercentage":
        return max(1, int(voters_count * percentage))
    elif method == "minvotes":
        return max(min_votes, int(voters_count / 2) + 1)
    else:
        raise ValueError("invalid method xd")


def update_vote_text(votes_needed, max_vote):
    activity = bsInternal._getForegroundHostActivity()

    try:
        activity.end_vote_text.node.text = "Skip Votes: {}/{}".format(votes_needed, max_vote)
    except:
        with bs.Context(bsInternal._getForegroundHostActivity()):
            node = bs.NodeActor(bs.newNode('text',
                                           attrs={
                                               'vAttach': 'top',
                                               'hAttach': 'center',
                                               'hAlign': 'center',
                                               'vAlign': 'center',
                                               'color': (1, 1, 1),
                                               'flatness': 0.5,
                                               'shadow': 0.5,
                                               'position': (0, -80),
                                               'scale': 0.5,
                                               'text': 'Skip Votes: {}/{}'.format(
                                                   votes_needed, max_vote)
                                           })).autoRetain()
            activity.end_vote_text = node
            bs.Timer(20, remove_vote_text)


def remove_vote_text():
    activity = bsInternal._getForegroundHostActivity()
    if hasattr(activity, "end_vote_text") and activity.end_vote_text.node.exists():
        activity.end_vote_text.node.delete()
