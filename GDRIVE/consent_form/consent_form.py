from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaIoBaseUpload
from google.auth.credentials import Credentials
from google.auth.transport.requests import Request
import typer
import os
from pathlib import Path
from typing import List,Dict
import json
import pickle
import time
import csv
app=typer.Typer()
scope=["https://www.googleapis.com/auth/drive"]

def auth():
    cred=[]
    if os.path.exists("token.pickle"):
        with open("token.pickle","rb") as r:
            cred=pickle.load(r)
    if  not cred or not cred.valid:
        if cred and cred.refresh_token and cred.expired:
            cred.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file("credentials.json",scope)
            cred=flow.run_local_server(port=0)
            with open("token.pickle","wb") as w:
                pickle.dump(cred,w)
    return cred


def total_files(folder_id,service):
    files=[]
    page_token=None
    while True:
        resp=service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            spaces="drive",
            fields="nextPageToken,files(id,name,mimeType,size,webViewLink,webContentLink)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            pageToken=page_token
        ).execute()
        for i in resp.get('files',[]):
            if i.get("mimeType")=="application/vnd.google-apps.folder":
                files.extend(total_files(i['id'],service))
            else:
                files.append(i)
        page_token=resp.get("nextPageToken")
        if not page_token:
            break

    return files

def write_csv(file,data):
    fields=["filename",'filelink']
    with open(file,"w") as w:
        csw=csv.DictWriter(w,fieldnames=fields)
        csw.writeheader()
        csw.writerows(data)
@app.command("concent form or pdf link extract from the google drive")
def main(folder_id:str=typer.Argument(...,help="gdrive folder id")
         ,output_csv:str=typer.Option("drive_link.csv","--output","-o",help="output csv name")):
    cred=auth()
    # print(cred)
    service=build("drive","v3",credentials=cred)  
    file=total_files(folder_id,service)
    rows=[]
    for i in file:
        row={}
        row['filename']=i['name']
        row['filelink']=i['webViewLink']
        rows.append(row)
    # for i in rows:
    #     print(i)
    write_csv(output_csv,rows)

if __name__=="__main__":
    app()