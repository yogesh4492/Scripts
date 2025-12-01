import typer
from google.auth.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaIoBaseUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from concurrent.futures import ThreadPoolExecutor,as_completed
import json
import csv
import os
import time
import pickle
from rich.progress import Progress

app=typer.Typer()
scope=['https://www.googleapis.com/auth/drive']

def auth():
    creds=[]
    if os.path.exists("token.pickle"):
        with open("token.pickle","rb") as p:
            creds=pickle.load(p)
    if  not creds or not creds.valid:
        if creds and creds.refresh_token and creds.expired:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file("credentials.json",scope)
            creds=flow.run_local_server(port=0)
            with open("token.pickle","wb") as p:
                pickle.dump(creds,p)
    print(creds)
    return creds



def list_files(service,folder_id):
    files=[]
    page_token=None
    while True:
        re=service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            spaces="drive",
            fields="nextPageToken,files(id,name,mimeType,size)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            pageToken=page_token
        ).execute()
        for i in re.get("files",[]):    
            if i.get("mimeType")=="application/vnd.google-apps.folder":
                files.extend(list_files(service,i.get("id")))
            else:
                files.append(i)
        page_token=re.get("nextPageToken")
        if not page_token:
            break
    return files
        

@app.command()
def main(gdrive_id:str=typer.Argument(...,help="enter gdrive folder id ")):
    authen=auth()
    service=build("drive","v3",credentials=authen)
    print(service)
    total=list_files(service,gdrive_id)
    print(len(total))


if __name__=="__main__":
    app()