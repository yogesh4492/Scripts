from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google.auth.credentials import Credentials


import typer
import pickle
import os
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress
app=typer.Typer()
scope=['https://www.googleapis.com/auth/drive']

def authenticate():
    creds=[]
    if os.path.exists('token.pickle'):
        with open('token.pickle','rb') as tr:
            creds=pickle.load(tr)
    if not creds or not creds.valid:
        if creds and creds.refresh_token and creds.expired:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file('credentials.json',scope)
            creds-flow.run_local_server(port=0)
            with open('token.pickle','wb') as tw:
                pickle.dump(creds,tw)
    return creds
def list_file(service,folder_id):
    file=[]
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
                file.extend(list_file(service,i['id']))
            else:
                file.append(i)
        page_token=resp.get('nextPageToken')
        if not page_token:
            break
    return file


def list_folder(service,folder_id):
    folder=[]
    page_token=None
    while True:
        resp=service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            spaces='drive',
            fields='nextPageToken,files(id,name,mimeType,size)',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            pageToken=page_token
        ).execute()
        for i in resp.get('files',[]):
            if i.get('mimeType')=='application/vnd.google-apps.folder':
                folder.append(i)
        page_token=resp.get('nextPageToken')
        if not page_token:
            break
    return folder

@app.command()
def main(folder_id):
    cred=authenticate()
    service=build('drive','v3',credentials=cred)
    files=list_file(service,folder_id)
    print(len(files))
    folders=list_folder(service,folder_id)
    print(len(folders))

if __name__=="__main__":
    app()

