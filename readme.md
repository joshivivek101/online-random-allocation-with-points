# Random Allocation With Sheets
For allocating randomely to candidates and store all in google sheets.

Enable sheets api from https://developers.google.com/sheets/api/quickstart/python and download your credentials.json. Put it in project directory.

## Allocate By Match
Allocate for a match and store to google sheets.

```
python command.py --create-allocation --match-no 1
```

## GenerateResults By Match
Generate results for a match and store to google sheets.

```
python command.py --generate-results --match-no 1
```