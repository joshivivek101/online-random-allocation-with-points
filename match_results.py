import configs
from sheets import Sheet


class MatchResults:

    def __init__(self):
        self.sheet = Sheet()

    def get(self, match_no):
        vals = self.sheet.get_rows(configs.MATCH_RESULTS_SHEET_ID,
                                   "'"+match_no+"'"+configs.MATCH_RESULTS_SHEET_RANGE_POSTFIX)
        results = []
        for val in vals:
            results.append(
                {
                    'player': val[0],
                    'player_name': val[1],
                    'runs': val[2],
                    'wickets': val[3]
                })
        return results


def main():
    data = MatchResults()
    data.get('1')


if __name__ == '__main__':
    exit(main())
