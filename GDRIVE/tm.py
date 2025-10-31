from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from google.auth.credentials import Credentials

import os
import typer
import pickle

app=typer.Typer()
scope=['https://www.googleapis.com/auth/drive']
def authentiction():
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

def list_files(service,folder_id):
    files=[]
    page_token=None
    while True:
        resp=service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            spaces='drive',
            fields='nextPageToken,files(id,name,mimeType,size)',
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
            pageToken=page_token
        ).execute()
        for i in resp.get('files',[]):
            if i.get('mimeType')=='application/vnd.google-apps.folder':
                files.extend(list_files(service,i['id']))
            else:
                files.append(i)
        page_token=resp.get('nextPageToken')
        if not page_token:
            break
    return files

@app.command()
def main(folder_id):
    cred=authentiction()
    service=build('drive','v3',credentials=cred)
    al=list_files(service,folder_id)
    print(len(al))

if __name__=="__main__":
    app()           