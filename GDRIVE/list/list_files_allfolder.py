import os
import pickle
import typer
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress
from google.auth.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport import Request
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaIoBaseUpload
app=typer.Typer()
scope=['https://www.googleapis.com/auth/drive']
def authenticate():
    creds=[]
    if os.path.exists('token.pickle'):
        with open('token.pickle','rb') as pr:
            creds=pickle.load(pr)
    if not creds or not creds.valid:
        if creds and creds.refresh_token and creds.expired:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file('credentials.json',scope)
            creds=flow.run_local_server(port=0)
            with open('token.pickle','wb') as b:
                pickle.dump(creds,b)

    return creds
def list_all_files(service,folder_id):
    files=[]
    page_token=None
    count=0
    while True:
        resp=service.files().list(
            q=f"'{folder_id}' in parents and trashed=False",
            spaces='drive',
            fields='nextPageToken,files(id,name,mimeType,size)',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            pageToken=page_token
        ).execute()
        for i in resp.get('files',[]):
            if i.get('mimeType')=="application/vnd.google-apps.folder":
                count+=1
                sub_files,subFolder=list_all_files(service,i['id'])
                files.extend(sub_files)
                count+=subFolder
            else:
                files.append(i)
        page_token=resp.get('nextPageToken')
        if not page_token:
            break
    return files,count


@app.command()
def main(folder_id:str=typer.Argument(...,help="Gdrive Folder ID ")):
    cred=authenticate()
    service=build('drive','v3',credentials=cred)
    all_Files,count=list_all_files(service,folder_id)
    print(f"Total Files In Given Folder Id {len(all_Files)} ")
    print(f"and total directory contain is = {count}")


if __name__=="__main__":
    app()

                

