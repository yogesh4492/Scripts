from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, io, pickle
import typer
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress
import time

SCOPES = ['https://www.googleapis.com/auth/drive']
app=typer.Typer()

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def download_file(service, file_id, file_name):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        # print(f"Downloading {file_name}: {int(status.progress()*100)}%")
    typer.echo(f"Downloaded {file_name}")
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
    


def download_folder(service, folder_id, parent_path):
    # List files in folder
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id,name,mimeType)").execute()
    files = results.get('files', [])

    for f in files:
        file_path = os.path.join(parent_path, f['name'])
        if f['mimeType'] == 'application/vnd.google-apps.folder':
            download_folder(service, f['id'], file_path)  # Recursive for subfolders
        else:
            with Progress() as p:
                task=p.add_task("Downloading....",total=len(all_files))
                with ThreadPoolExecutor(max_workers=8) as ex:
                    futures=[ex.submit(download_file(service, f['id'], file_path))]
                    for i in futures:
                        p.update(task,advance=50)
                        time.sleep(1)

        


# Usage

@app.command()
def main(folder_id:str=typer.Argument(...,help="enter folder id of gdrive folder"),
         output_folder:str=typer.Argument(...,help="Insert Name of output_folder for store downloaded file")):
    service = authenticate()
    global all_files
    all_files=list_files(service, folder_id)
    download_folder(service,folder_id,output_folder)
    
if __name__=="__main__":
    app()