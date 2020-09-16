import random
import copy
import configs


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
            'players': [p1, p2]
        })
        chits_track.remove(p1)
        chits_track.remove(p2)
        next_chit_to_give = next_chit_to_give + 2
    return allocation


def generate_candidate_result(allocations, results):

    def _get_points(player):
        runs = player['runs']
        wickets = player['wickets']
        run_points = configs.RUN_POINTS
        wicket_points = configs.WICKET_POINTS
        points = (int(runs)*run_points) + (int(wickets)*wicket_points)
        return points

    candidate_results = []
    for alloc in allocations:
        player1 = alloc['player1']
        player2 = alloc['player2']

        player1_result = [
            result for result in results if result['player'] == player1][0]
        player2_result = [
            result for result in results if result['player'] == player2][0]

        player1_points = _get_points(player1_result)
        player2_points = _get_points(player2_result)

        candidate_results.append({
            'no': alloc['no'],
            'name': alloc['name'],
            'email': alloc['email'],
            'player1': alloc['player1'],
            'player1_name': player1_result['player_name'],
            'player1_points': player1_points,
            'player1_run_wicket': player1_result['runs']+' , '+player1_result['wickets'],
            'player2': alloc['player2'],
            'player2_name': player2_result['player_name'],
            'player2_run_wicket': player2_result['runs']+' , '+player2_result['wickets'],
            'player2_points': player2_points,
            'total': player1_points + player2_points
        })

    all_totals = [res['total'] for res in candidate_results]
    all_totals.sort()
    winner_points = all_totals[-1]
    winner_results = [res for res in candidate_results if res['total'] == winner_points]

    return { 'results': candidate_results, 'winners': winner_results }
