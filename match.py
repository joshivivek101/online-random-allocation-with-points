from sheets import Sheet
import configs

class Match:

    def __init__(self):
        self.sheet = Sheet()

    def get_all(self):
        vals = self.sheet.get_rows(configs.MATCHES_SHEET_ID, configs.MATCHES_SHEET_RANGE)
        matches = []
        for val in vals:
            matches.append({
                'no': val[0],
                'team1': val[1],
                'team2': val[2]
            })
        return matches
    
    def get(self, match_no):
        matches = self.get_all()
        return [match for match in matches if match['no'] == match_no][0]

    