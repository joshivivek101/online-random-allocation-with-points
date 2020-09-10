from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import configs
from exceptions import DabboException


class Sheet:
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/spreadsheets']

    CREDS_FILE = 'credentials.json'

    def __init__(self):
        self.creds = None
        self._do_auth()
        self.sheet = self._get_service()

    def _do_auth(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDS_FILE, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    def _get_service(self):
        service = build('sheets', 'v4', credentials=self.creds)
        return service.spreadsheets()

    def get_rows(self, sheet_id: str, range: str):
        result = self.sheet.values().get(spreadsheetId=sheet_id,
                                         range=range).execute()
        values = result.get('values', [])

        if not values:
            raise DabboException('No values in sheet')
        else:
            return values

    def create_sheet(self, spreadsheet_id, name):
        body = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": name
                        }
                    }
                }
            ]
        }
        result = self.sheet.batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()

    def update_values(self, spreadsheet_id, range_name, value_input_option,
                      values):
        service = self.sheet
        body = {
            'values': values
        }
        result = service.values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))
        # [END sheets_update_values]
        return result

    def if_exists(self, spreadsheet_id, sheet_name):
        response = self.sheet.get(spreadsheetId=spreadsheet_id).execute()
        if response:
            sheets = response['sheets']
            for sheet in sheets:
                if sheet['properties']['title'] == sheet_name:
                    return True
        return False


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1XQONns4-Dq3mS3Wxb5168TIhvR2qPC-E1Wm-0eUDnqk'
SAMPLE_RANGE_NAME = 'A2:B3'
CREDS_FILE = 'credentials.json'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    st = [{'candidate': {'id': '2', 'email': 'Vishal', 'name': 'vishal@sculptsoft.com'}, 'players': ['A7', 'A6']}, {'candidate': {'id': '13', 'email': '11', 'name': 'k'}, 'players': ['A9', 'A4']}, {'candidate': {'id': '4', 'email': '2', 'name': 'b'}, 'players': ['B8', 'A2']}, {'candidate': {'id': '1', 'email': 'Vivek', 'name': 'vivek@sculptsoft.com'}, 'players': ['B5', 'B9']}, {'candidate': {'id': '11', 'email': '9', 'name': 
'i'}, 'players': ['A1', 'B1']}, {'candidate': {'id': '3', 'email': '1', 'name': 'a'}, 'players': ['B6', 'B10']}, {'candidate': {'id': '12', 
'email': '10', 'name': 'j'}, 'players': ['B7', 'B2']}, {'candidate': {'id': '10', 'email': '8', 'name': 'h'}, 'players': ['A10', 'A11']}, {'candidate': {'id': '15', 'email': '13', 'name': 'm'}, 'players': ['B3', 'B4']}, {'candidate': {'id': '6', 'email': '4', 'name': 'd'}, 'players': ['A5', 'A8']}, {'candidate': {'id': '14', 'email': '12', 'name': 'l'}, 'players': ['A3', 'B11']}, {'candidate': {'id': '8', 'email': '6', 'name': 'f'}, 'players': ['B6', 'B11']}, {'candidate': {'id': '9', 'email': '7', 'name': 'g'}, 'players': ['B5', 'A6']}, {'candidate': {'id': '5', 'email': '3', 'name': 'c'}, 'players': ['B10', 'B2']}, {'candidate': {'id': '7', 'email': '5', 'name': 'email'}, 'players': ['B3', 'B8']}]
    d = {'KEY1': {'name': 'google', 'date': 20100701, 'downloads': 50},
          'KEY2': {'name': 'chrome', 'date': 20071010, 'downloads': 0},
          'KEY3': {'name': 'python', 'date': 20100710, 'downloads': 100}}

    fdic = []
    for i in range(1, len(st)+1):
        fdic.append([data for data in st if int(data['candidate']['id']) == i][0])

    res = sorted(d.items(), key = lambda x: x[1]['downloads']) 
    print(str(res))
    # s = Sheet()
    # s.if_exists(configs.ALLOCATIONS_SHEET_ID,'1')
    # rows = s.get_rows(sheet_id=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
    # for row in rows:
    #     print(row[0], row[1])


if __name__ == '__main__':
    main()
