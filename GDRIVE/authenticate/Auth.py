from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import pickle
import os
scope=['https://www.googleapis.com/auth/drive']
def Authenticate():
    creds=[]
    if os.path.exists('token.pickle'):
        with open('token.pickle','rb') as tr:
            creds=pickle.load(tr)
    if not creds or not creds.valid:
        if creds and creds.refresh_token and creds.expired:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file('credentials.json',scope)
            creds=flow.run_local_server(port=0)
            with open('token.pickle','wb') as tw:
                pickle.dump(creds,tw)
    return creds

if __name__=="__main__":
   a=Authenticate()
   print(a)


# from googleapiclient.discovery import build
# from google.auth.transport.requests import Request
# from google_auth_oauthlib.flow import InstalledAppFlow
# import pickle
# import os

# # Both Drive + Sheets access
# SCOPES = [
#     "https://www.googleapis.com/auth/drive",
#     "https://www.googleapis.com/auth/spreadsheets"
# ]

# def authenticate():
#     creds = None

#     # Load saved credentials
#     if os.path.exists("token.pickle"):
#         with open("token.pickle", "rb") as token:
#             creds = pickle.load(token)

#     # Check validity or refresh
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "credentials.json", SCOPES
#             )
#             creds = flow.run_local_server(port=0)  # browser login

#         # Save credentials for next use
#         with open("token.pickle", "wb") as token:
#             pickle.dump(creds, token)

#     return creds

# if __name__ == "__main__":
#     creds = authenticate()
#     print("Authentication successful!")
