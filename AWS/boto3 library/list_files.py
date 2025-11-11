# for normal less that 1000 file we use list_objects_v2 
import boto3
import typer
import csv

# if we use normal
"""
s3=boto3.client('s3')

"""
#if you want do using some user credentials use sesion its some time fast

session=boto3.Session(profile_name="Yogesh")

s3=session.client('s3')
#if you want to using resources

"""
s3=boto3.resource('s3')
"""
def list_files(s3path):
    split=s3path.split("/")
    bucket=split[2]
    prefix="/".join(split[3:])
    response=s3.list_objects_v2(Bucket=bucket,Prefix=prefix)
    
    for i in response.get('Contents',[]):
        print(i.get('Key'))



app=typer.Typer()

@app.command()
def main(s3path:str=typer.Argument(...,help="Input s3 path for list files")):
    list_file=list_files(s3path)

if __name__=="__main__":
    app()



