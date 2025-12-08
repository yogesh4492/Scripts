import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os
from google.auth.transport.requests import Request
# Scopes required
SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]

def connect_with_oauth():
    # Create OAuth flow'
    creds=[]
    if os.path.exists("token.pickle"):
        with open("token.pickle","rb") as r:
            creds=pickle.load(r)
    if not creds or not creds.valid:
        if creds and creds.refresh_token and creds.expired:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                scopes=SCOPES
            )

            creds = flow.run_local_server(port=0)
            with open("token.pickle","wb") as w:
                pickle.dump(creds,w)


    client = gspread.authorize(creds)
    return client

def read_sheet(sheet_id, tab_name):
    client = connect_with_oauth()
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.get_worksheet(1)
    return worksheet.get_all_records()

if __name__ == "__main__":
    SHEET_ID = "1WEAvtG1fXSqT_Ip6PKfcAy9Nh-3dPu7TuRLxejWzmQM"
    TAB = "YOUR_TAB_NAME"  # put correct sheet name

    data = read_sheet(SHEET_ID, TAB)
    row=[]
    for i in data:
        row.append(i)
    print(len(row))



# import gspread
# from google.oauth2.service_account import Credentials

# def connect_to_sheet_by_id(sheet_id):
#     scope = [
#         "https://www.googleapis.com/auth/spreadsheets.readonly",
#         "https://www.googleapis.com/auth/drive.readonly"
#     ]
#     creds = Credentials.from_service_account_file(
#         "service_account.json",
#         scopes=scope
#     )
#     client = gspread.authorize(creds)
#     sheet = client.open_by_key(sheet_id)
#     return sheet

# def fetch_sheet_data_by_id(sheet_id, worksheet_name_or_index=0):
#     """
#     sheet_id  : string — the part '1WEAvtG1fXSqT_Ip6PKfcAy9Nh-3dPu7TuRLxejWzmQM' from your link.
#     worksheet_name_or_index :
#         - If string: use worksheet title (e.g. "Sheet1")
#         - If int: use zero-based worksheet index (e.g. 0 for first sheet)
#     """
#     sheet = connect_to_sheet_by_id(sheet_id)
#     if isinstance(worksheet_name_or_index, str):
#         worksheet = sheet.worksheet(worksheet_name_or_index)
#     else:
#         worksheet = sheet.get_worksheet(worksheet_name_or_index)

#     data = worksheet.get_all_records()
#     return data

# if __name__ == "__main__":
#     # Extracted sheet ID from your link
#     SHEET_ID = "1WEAvtG1fXSqT_Ip6PKfcAy9Nh-3dPu7TuRLxejWzmQM"

#     # Option A: by worksheet name
#     data = fetch_sheet_data_by_id(SHEET_ID, worksheet_name_or_index="paravision_all")
#     # Option B: by worksheet index (0-based)
#     # data = fetch_sheet_data_by_id(SHEET_ID, worksheet_name_or_index=0)

#     print("Fetched Data:")
#     row=[]
#     # row///////////////////////////////////////////////s=[]
#     for i in data:
#         row.append(i['FileName'])
#     print(len(row))
#     # print(row)
        
