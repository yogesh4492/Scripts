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
    if os.path.exists(os.path.join(os.path.dirname(__file__),"..",'token.pickle')):
        with open(os.path.join(os.path.dirname(__file__),"..",'token.pickle'),'rb') as tr:
            creds=pickle.load(tr)
    if not creds or not creds.valid:
        if creds and creds.refresh_token and creds.expired:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file(os.path.join(os.path.dirname(__file__),"..","credentials.json"),scope)
            creds=flow.run_local_server(port=0)
            with open(os.path.join(os.path.dirname(__file__),"..",'token.pickle'),'wb') as tw:
                pickle.dump(creds,tw)
    return creds
def list_all_files(service,folder_id):
    page_token=None
    all_Files=[]
    while True:
        q=f"'{folder_id}' in parents and trashed=false",
        spaces='drive',
        includeItemsFromAllDrives=True,
        supportAllDrives=True,

if __name__=="__main__":
   a=Authenticate()
   print(a)
   
