import typer
import os
import boto3
app=typer.Typer()
session=boto3.Session(profile_name="Yogesh")

s3=session.client('s3')

def download(s3path):
    split=s3path.split("/")
    bucket=split[2]
    prefix="/".join(split[3:])
    file=split[-1]
    s3.download_file(bucket,prefix,file)

@app.command()
def main(s3path:str=typer.Argument(...,help="Input path for download file")):
    download(s3path)

if __name__=="__main__":
    app()