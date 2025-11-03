from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.auth.credentials import Credentials


import typer
import pickle
import os
import time
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress
scope=['https://www.googleapis.com/auth/drive']

app=typer.Typer()
class Main:
    def __init__(self,folder_id):
        self.folder_id=folder_id

    def Authenticate(self):
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
        self.service=build('drive','v3',credentials=creds)
    def List_main_folder(self):
        files_only=[]
        folder_only=[]
        page_token=None
        while True:
            resp=self.service.files().list(
                q=f"'{self.folder_id}' in parents and trashed=false",
                spaces='drive',
                fields='nextPageToken,files(id,name,mimeType,size)',
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                pageToken=page_token
            ).execute()
            for i in resp.get('files',[]):
                if i.get('mimeType')=='application/vnd.google-apps.folder':
                    folder_only.append(i)
                else:
                    files_only.append(i)
            page_token=resp.get('nextPageToken')
            if not page_token:
                break

        print(f"Total Files in Main Folder= {len(files_only)}")
        print(f"Total Folder in Main Folder= {len(folder_only)}")
    def list_sub_folder(self,folder_id):
        all_files=[]
        page_token=None
        while True:
            resp=self.service.files().list(
                q=f"'{folder_id}' in  parents and trashed=false",
                spaces='drive',
                fields='nextPageToken,files(id,name,mimeType,size)',
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                pageToken=page_token
            ).execute()
            for i in resp.get('files',[]):
                if i.get('mimeType')=='application/vnd.google-apps.folder':
                    all_files.extend(self.list_sub_folder(i.get('id')))
                else:
                    all_files.append(i)
            page_token=resp.get('nextPageToken')
            if not page_token:
                break
        # print(len(all_files))
        # return all_files
    
    def run(self):
        self.Authenticate()
        self.List_main_folder()

        with Progress() as p:
            tab=p.add_task("Listing Files....")
            with ThreadPoolExecutor(max_workers=8) as ex:
                future={ex.submit(self.list_sub_folder(self.folder_id))}
                for i in as_completed(future):
                    p.update(tab,advance=100)
                    time.sleep(2)
        
                
@app.command()
def main(folder_id):
    obj=Main(folder_id)
    obj.run()

if __name__=="__main__":
    app()

        
        
        

        
        
