import gspread
from google.oauth2.service_account import Credentials

def connect_to_sheet_by_id(sheet_id):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]
    creds = Credentials.from_service_account_file(
        "service_account.json",
        scopes=scope
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    return sheet

def fetch_sheet_data_by_id(sheet_id, worksheet_name_or_index=0):
    """
    sheet_id  : string — the part '1WEAvtG1fXSqT_Ip6PKfcAy9Nh-3dPu7TuRLxejWzmQM' from your link.
    worksheet_name_or_index :
        - If string: use worksheet title (e.g. "Sheet1")
        - If int: use zero-based worksheet index (e.g. 0 for first sheet)
    """
    sheet = connect_to_sheet_by_id(sheet_id)
    if isinstance(worksheet_name_or_index, str):
        worksheet = sheet.worksheet(worksheet_name_or_index)
    else:
        worksheet = sheet.get_worksheet(worksheet_name_or_index)

    data = worksheet.get_all_records()
    return data

if __name__ == "__main__":
    # Extracted sheet ID from your link
    SHEET_ID = "1WEAvtG1fXSqT_Ip6PKfcAy9Nh-3dPu7TuRLxejWzmQM"

    # Option A: by worksheet name
    data = fetch_sheet_data_by_id(SHEET_ID, worksheet_name_or_index="paravision_all")
    # Option B: by worksheet index (0-based)
    # data = fetch_sheet_data_by_id(SHEET_ID, worksheet_name_or_index=0)

    print("Fetched Data:")
    row=[]
    # row///////////////////////////////////////////////s=[]
    for i in data:
        row.append(i['FileName'])
    print(len(row))
    # print(row)
        
