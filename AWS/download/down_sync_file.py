import typer
import os
import boto3
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress
from botocore.exceptions import ClientError

session=boto3.Session(profile_name="Yogesh")
app=typer.Typer()

class Main:
    def __init__(self):
        pass


@app.command()
def main():
    pass





if __name__=="__main":
    app()



