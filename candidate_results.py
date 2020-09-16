import configs
from sheets import Sheet
import datetime


class CandidateResult:

    def __init__(self):
        self.sheet = Sheet()

    def add_results(self, match, results):
        if not self.sheet.if_exists(configs.CANDIDATE_RESULTS_SHEET_ID, match['no']):
            response = self.sheet.create_sheet(
                configs.CANDIDATE_RESULTS_SHEET_ID, match['no'])

        values = [["Match Number", match['no'], '','','',
                   '', '', '', '', 'Created Date Time']]
        values.append(["Teams", match["team1"] +
                       ' - vs - '+match["team2"], '', '', '', '','','', '', '', str(datetime.datetime.now())])
        values.append(["No", "Name", "Email", "Player 1", "Player 1 runs, wickets", "Player 1 Points",
                       "Player 2","Player 2 runs, wickets", "Player 2 Points", "Total Points"])

        point_results = results['results']

        for res in point_results:
            values.append([res['no'], res['email'], res['name'], res['player1']+'('+res['player1_name']+')',res['player1_run_wicket'],
                           res['player1_points'], res['player2']+'('+res['player2_name']+')',res['player2_run_wicket'], res['player2_points'], res['total']])

        values.append(["Winners", '', '', '', '', '', '', '','',''])

        winners = results['winners']
        for winner in winners:
            values.append([winner['no'], winner['email'], winner['name'], winner['player1']+'('+winner['player1_name']+')',winner['player1_run_wicket'],
                           winner['player1_points'], winner['player2']+'('+winner['player2_name']+')',winner['player2_run_wicket'], winner['player2_points'], winner['total']])
        self.sheet.update_values(
            configs.CANDIDATE_RESULTS_SHEET_ID, match['no']+"!A1", 'USER_ENTERED', values)
        return None
