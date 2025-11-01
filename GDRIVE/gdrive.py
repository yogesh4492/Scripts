from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.credentials import Credentials
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import typer
import pickle
import io
import os
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress
import time
scope=['https://www.googleapis.com/auth/drive']
app=typer.Typer()
class Main:
    def __init__(self,folder_id):
        self.folder_id=folder_id
    def authenticate(self):
        creds=[]
        if os.path.exists('token.pickle'):
            with open('token.pickle','rb') as tr:
                creds=pickle.load(tr)
        if not creds or not creds.valid:
            if creds and creds.refresh_token and creds.expired:
                creds.refresh(Request())
            else:
                flow=InstalledAppFlow.from_client_secrets_file('credentials.josn',scope)
                creds=flow.run_local_server(port=0)
                with open('token.pickle','wb') as tw:
                    pickle.dump(creds,tw)
        self.service=build('drive','v3',credentials=creds)
    def list_files_folder(self):
        self.files_only=[]
        self.folder_only=[]
        page_token=None
        while True:
            resp=self.service.files().list(
                q=f"'{self.folder_id}' in parents and trashed=false",
                spaces='drive',
                fields='nextPageToken,files(id,name,mimeType,size)',
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                pageToken=page_token

            ).execute()
            
            for i in resp.get('files',[]):
                if i.get('mimeType')=='application/vnd.google-apps.folder':
                    self.folder_only.append(i)
                    # all_files.extend()
                else:
                    self.files_only.append(i)
            page_token=resp.get('nextPageToken')
            if not page_token:
                break
        print(f"total Files In Given Folder Id Main Folder= {len(self.files_only)}")
        print(f"total Folder In Given Folder Id Main Folder= {len(self.folder_only)}")
    def run(self):
        self.authenticate()
        with Progress() as p:
            tab=p.add_task("processing....")
            with ThreadPoolExecutor(max_workers=8) as ex:
                future={ex.submit(self.list_files_folder)}
                # print(future)
                for i in as_completed(future):
                    # res=i.result()
                    # print(i)
                
                    p.update(tab,advance=100)
                    time.sleep(0.10)
        
            


@app.command()
def main(folder_id):
    obj=Main(folder_id)
    obj.run()


if __name__=="__main__":
    app()

    