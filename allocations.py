from sheets import Sheet
import configs
import logics
import datetime


class Allocation:

    def __init__(self):
        self.sheet = Sheet()

    def generate_allocation(self, candidates):
        allocation = logics.get_random_allocation(candidates)
        return allocation

    def create_allocation(self, match, allocations):
        if not self.sheet.if_exists(configs.ALLOCATIONS_SHEET_ID, match['no']):
            response = self.sheet.create_sheet(
                configs.ALLOCATIONS_SHEET_ID, match['no'])

        values = [["Match Number", match['no'], '', '', 'Created Date Time']]
        values.append(["Teams", match["team1"] +
                       ' - vs - '+match["team2"], '', '', str(datetime.datetime.now())])
        values.append(["No", "Email", "Name", "Player 1", "Player 2"])

        fdic = []
        for i in range(1, len(allocations)+1):
            fdic.append([data for data in allocations if int(
                data['candidate']['id']) == i][0])
        allocations = fdic

        for alloc in allocations:
            values.append([alloc['candidate']['id'], alloc['candidate']['email'], alloc['candidate']
                           ['name'], alloc['players'][0], alloc['players'][1]])

        self.sheet.update_values(
            configs.ALLOCATIONS_SHEET_ID, match['no']+"!A1", 'USER_ENTERED', values)
        return None

    def get_allocation(self, match):
        rows = self.sheet.get_rows(configs.ALLOCATIONS_SHEET_ID,
                            "'"+match+"'!"+configs.ALLOCATIONS_GET_SHEET_RANGE_POSTFIX)
        allocations = []
        for row in rows:
            allocations.append({
                'no':row[0],
                'name':row[1],
                'email':row[2],
                'player1':row[3],
                'player2':row[4]
            })
        return allocations

def main():
    data = Allocation()
    data.get_allocation('1')


if __name__ == '__main__':
    exit(main())
