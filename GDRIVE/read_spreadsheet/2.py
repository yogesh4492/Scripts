import gspread
from google.oauth2.service_account import Credentials

# -----------------------------
# Google Sheet Authentication
# -----------------------------

def connect_to_sheet(sheet_name):
    # Define scope
    scope = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]

    # Load credentials
    creds = Credentials.from_service_account_file(
        "service_account.json",
        scopes=scope
    )

    # Authorize client
    client = gspread.authorize(creds)

    # Open Google Sheet
    sheet = client.open(sheet_name)
    return sheet


# -----------------------------
# Fetch Data from Sheet
# -----------------------------

def fetch_sheet_data(sheet_name, tab_name):
    sheet = connect_to_sheet(sheet_name)

    # Open specific worksheet/tab
    worksheet = sheet.worksheet(tab_name)

    # Read all rows
    data = worksheet.get_all_records()

    return data


# -----------------------------
# Main Example
# -----------------------------

if __name__ == "__main__":
    SHEET_NAME = ""
    TAB_NAME = "Sheet1"

    data = fetch_sheet_data(SHEET_NAME, TAB_NAME)

    print("Fetched Data:")
    for row in data:
        print(row)
