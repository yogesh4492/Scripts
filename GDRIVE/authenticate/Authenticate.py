from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.http import  MediaIoBaseDownload
from google.auth.transport.requests import Request
import typer
import csv
import json
import os
import pickle
import zipfile

# import 
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress

scope=['https://www.googleapis.com/auth/drive']

def authenticate():
    creds=None
    if os.path.exists('token.pickle'):
        with open('token.pickle','rb') as p:
            creds=pickle.load(p)
    if  not creds or not creds.valid:
        if creds and creds.refresh_token and creds.expired:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file('credentials.json',scope)
            creds=flow.run_local_server(port=0)
            with open('token.pickle','wb') as toke:
                pickle.dump(creds,toke)
    print(creds)
def down():
    pass


if __name__=="__main__":
    authenticate()
  