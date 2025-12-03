from authenticate.Auth import *
from list.list_gdrive_files import *
import typer
from googleapiclient.discovery import build 
app=typer.Typer()

@app.command(help="program for combined all in main".upper())
def main(folder_id:str=typer.Argument(...,help="gdrive folder id".upper())):
    cred=Authenticate()
    service=build("drive","v3",credentials=cred)
    total_files=list_files(service,folder_id)
    print("total files in  given folder id = ".upper(),len(total_files))

    

if __name__=="__main__":
    app()
