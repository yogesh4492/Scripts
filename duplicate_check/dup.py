import boto3
import pandas as pd
import hashlib
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress
import csv
import tempfile
import typer
from urllib.parse import urlparse

app=typer.Typer()
def get_s3_files(bucket_name:str,prefix_name:str):
    pass

def get_hash():
    pass

def dump_csv():
    pass

if __name__=="__main__":
    app()