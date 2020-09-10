import random
import copy

def make_chits():
     # create players array
    team_1, team_2 = 'A', 'B'
    chits = []
    for x in range(1, 12):
        chits.append(team_1+str(x))
        chits.append(team_2+str(x))
    # shuffle players
    random.shuffle(chits)
    random.shuffle(chits)
    random.shuffle(chits)
    return chits

def get_random_allocation(candidates):
    # shuffle candidates
    random.shuffle(candidates)
    random.shuffle(candidates)
    random.shuffle(candidates)
    chits = None
    local_candidates = copy.deepcopy(candidates)
    allocation = []
    next_chit_to_give = 0
    chits_track = None
    for candidate in candidates:
        if not chits_track:
            chits = make_chits()
            chits_track = copy.deepcopy(chits)
            next_chit_to_give = 0
        p1 = chits[next_chit_to_give]
        p2 = chits[next_chit_to_give + 1]
        allocation.append({
            'candidate': candidate,
            'players': [p1,p2]
        })
        chits_track.remove(p1)
        chits_track.remove(p2)
        next_chit_to_give = next_chit_to_give + 2
    return allocation

        

