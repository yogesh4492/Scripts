import typer
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from rich.progress import Progress

app = typer.Typer()

def get_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()     # Opens browser for login
    return GoogleDrive(gauth)

@app.command()
def copy_folder(
    source_folder_id: str = typer.Argument(..., help="Source Google Drive Folder ID"),
    dest_folder_id: str = typer.Argument(..., help="Destination Google Drive Folder ID")
):
    """
    Copy all files from source folder to destination folder using Google Drive API.
    """
    drive = get_drive()

    # Fetch files inside source folder
    query = f"'{source_folder_id}' in parents and trashed=false"
    file_list = drive.ListFile({'q': query}).GetList()

    if not file_list:
        typer.echo("No files found in source folder.")
        raise typer.Exit()

    typer.echo(f"Found {len(file_list)} files. Copying now...")

    with Progress() as progress:
        task = progress.add_task("[cyan]Copying files...", total=len(file_list))

        for f in file_list:
            copied = drive.CreateFile({
                'title': f['title'],
                'parents': [{'id': dest_folder_id}]
            })

            # Download original content and upload into new file
            content = f.GetContentString() if f['mimeType'] == 'text/plain' else f.GetContentFile("temp.bin")
            copied.SetContentFile(f['title']) if f['mimeType'] != 'text/plain' else copied.SetContentString(content)
            copied.Upload()

            progress.update(task, advance=1)

    typer.echo("Copy Completed!")


if __name__ == "__main__":
    app()
