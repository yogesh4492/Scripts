import typer
import os
import boto3
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress
from botocore.exceptions import ClientError

session=boto3.Session(profile_name="Yogesh")
app=typer.Typer()

class Main:


    def __init__(self,s3path,output_folder,max_worker):
        self.s3path=s3path
        self.output_folder=output_folder.rstrip("/\\")
        self.split=s3path.split("/")
        self.bucket=self.split[2]
        self.prefix="/".join(self.split[3:])
        self.max_worker=max_worker
        self.s3=session.client('s3')


    def list_Files(self):
        paginator=self.s3.get_paginator("list_objects_v2")
        files=[]
        for i in paginator.paginate(Bucket=self.bucket,Prefix=self.prefix):
            # print("hello")
            for obj in i.get('Contents',[]):
                files.append(obj.get('Key'))
        print("Total Files In Give S3 path is = ",len(files))
        return files
    

    def download_file(self,file):
        local=os.path.join(self.output_folder,file)
        os.makedirs(os.path.dirname(local),exist_ok=True)
        if os.path.exists(local):
            return f"Skipped (exists):{local}"
        
        try:
            self.s3.download_file(self.bucket,file,local)
            return f"Downloaded: {file}"
        except ClientError as e:
            return f"Error : {e} "
        

    def run(self):
        total_files=self.list_Files()
        with Progress() as p:
            task=p.add_task("Downloading....",total=len(total_files))
            with ThreadPoolExecutor(max_workers=self.max_worker) as ex:
                futures={ex.submit(self.download_file,f):f for f in total_files}
                for i in as_completed(futures):
                    result=i.result()
                    p.update(task,advance=1)
                    typer.echo(result)        

@app.command()
def main(s3path:str=typer.Argument(...,help="input s3path"),output_folder:str=typer.Argument(...,help="Output folder name"),max_worker:int=typer.Option(8,"--max-workers",help="Multithread Max workers")):
    obj=Main(s3path,output_folder,max_worker)
    obj.run()



if __name__=="__main__":
    app()



