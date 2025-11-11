import boto3
import typer
import os
session=boto3.Session(profile_name="Yogesh")

s3=session.client('s3')
response=s3.list_buckets()
s2=boto3.resource('s3')
# for i in response['Buckets']:
#     print(i['Name'])
# print("*"*60)
# for i in s2.buckets.all():
#     print(i.name)
app=typer.Typer()   
def upload_file(file,s3path):
    bucket=os.path.split(s3path)
    print(bucket)
    # s3.upload_file()
@app.command()
def main(file,s3path):
    upload_file(file,s3path)


if __name__=="__main__":
    app()


