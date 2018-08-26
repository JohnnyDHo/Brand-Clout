from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from pprint import pprint

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

spreadsheet_id = '17RNBDCwmETuDRPGxHskMzXC3tiZ-shc7xmva7QwzbB4'  # TODO: Update placeholder value.
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# The A1 notation of a range to search for a logical table of data.
# Values will be appended after the last row of the table.
range_ = 'A1:A500'  # TODO: Update placeholder value.

# How the input data should be interpreted.
value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.

# How the input data should be inserted.
insert_data_option = 'INSERT_ROWS'  # TODO: Update placeholder value.

value_range_body = {

    # TODO: Add desired entries to the request body.
}

request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
response = request.execute()

# TODO: Change code below to process the `response` dict:
pprint(response)

# # The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
# SAMPLE_RANGE_NAME = 'Class Data!A2:E'
#
# def main():
#     """Shows basic usage of the Sheets API.
#     Prints values from a sample spreadsheet.
#     """
#     store = file.Storage('token.json')
#     creds = store.get()
#     if not creds or creds.invalid:
#         flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
#         creds = tools.run_flow(flow, store)
#     service = build('sheets', 'v4', http=creds.authorize(Http()))
#
#     # Call the Sheets API
#     SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
#     RANGE_NAME = 'Class Data!A2:E'
#     result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
#                                                 range=RANGE_NAME).execute()
#     values = result.get('values', [])
#
#     if not values:
#         print('No data found.')
#     else:
#         print('Name, Major:')
#         for row in values:
#             # Print columns A and E, which correspond to indices 0 and 4.
#             print('%s, %s' % (row[0], row[4]))
#
# if __name__ == '__main__':
#     main()
# # [END sheets_quickstart]