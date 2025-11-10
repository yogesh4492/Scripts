from googleapiclient.discovery import build
from google.auth.transport import Request
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.credentials import Credentials
import os
import typer
import pickle
app=typer.Typer()
scope=['https://www.googleapis.com/auth/drive']
def authenticate():
    creds=[]
    if os.path.exists("token.pickle"):
        with open('token.pickle','rb') as pr:
            creds=pickle.load(pr)
    if not creds or not creds.valid:
        if creds and creds.refresh_token and creds.expired:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file('credentials.json',scope)
            creds=flow.run_local_server(port=0)
            with open('token.pickle','wb') as pw:
                pickle.dump(creds,pw)
    return creds

def list_files(folder_id):
    file=[]
    page_token=None
    while True:
        resp=service.files().list(
            q=f"'{folder_id}' in parents and trashed =False",
            spaces='drive',
            fields='nextPageToken,files(id,name,mimeType,size)',
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
            pageToken=page_token
        ).execute()
        for i in resp.get('files',''):
            if i.get('mimeType')=='application/vnd.google-apps.folder':
                print("hello")
                file.extend(list_files(i['id']))
            else:
                file.append(i)

        page_token=resp.get('nextPageToken')
        if not page_token:
            break
    return file

@app.command()
def main(folder_id):
    cred=authenticate()
    print(cred)
    global service
    service=build('drive','v3',credentials=cred)
    print(service)
    ls=list_files(folder_id)
    print(len(ls))

if __name__=="__main__":
    app()



    


