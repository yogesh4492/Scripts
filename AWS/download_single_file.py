import csv
import json
import boto3
import typer
import os
app=typer.Typer()


@app.command()
def main(s3path):
    ls=s3path.split("/")
    # strin="/".join(l[2:])
    # print(strin)
    # print(ls)
    # print(l)
    bucket=ls[2]
    input="/".join(ls[3:])
    output=ls[-1]
    print(f"Bucket: {bucket},\nPrefix :{input},\noutput_File : {output}")
    s3=boto3.client("s3")
    s3.download_file(bucket,input,output)

if __name__=="__main__":
    app()
