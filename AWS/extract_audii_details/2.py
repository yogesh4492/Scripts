import os
import typer
from pydub import AudioSegment
import json
import csv
import boto3

app=typer.Typer()

class Main:
    def __init__(self,s3path):
        self.parts=s3path
        self.bucket=s3path[2]
        self.prefix="/".join(s3path[3:])
        self.s3=boto3.client("s3")
        self.audio_extension=(".wav",".flac",".mp3",".m4a",".aac",".ogg",".opus",
                              ".wma",".aiff",".alac")
        
    def process_folder(self):
        pass

    def 
        

def dump_csv():
    pass
def dump_json():
    pass


if __name__=="__main__":
    app()