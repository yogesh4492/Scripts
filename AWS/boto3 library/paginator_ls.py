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
    response=s3.get_paginator("list_objects_v2")
    field=['path']
    count=0
    with open('f.csv','w') as cw:
        csw=csv.DictWriter(cw,fieldnames=field)
        csw.writeheader()
        for i in response.paginate(Bucket=bucket,Prefix=prefix):
            for obj in i.get('Contents',[]):
                print(obj)
                count+=1
                row={}
                row['path']=obj.get('Key')
                csw.writerow(row)

    return count



app=typer.Typer()

@app.command()
def main(s3path:str=typer.Argument(...,help="Input s3 path for list files"),output_csv:str=typer.Option("f.csv",'-o',help="name of output csv")):
    list_file=list_files(s3path)
    print("Total Files in given path= ",list_file)

if __name__=="__main__":
    app()



