import os
import boto3
import typer
from rich.progress import Progress
from concurrent.futures import ThreadPoolExecutor,as_completed
from botocore.exceptions import ClientError

app=typer.Typer()
session=boto3.Session(profile_name="Yogesh")
class Main:
    def __init__(self,s3path,output_Folder):
        self.s3path=s3path
        self.split=s3path.split("/")
        self.bucket=self.split[2]
        self.prefix="/".join(self.split[3:])
        self.output_folder = output_Folder.rstrip("/\\")
        # print(self.output_folder)
        # self.output_folder=output_Folder
        self.s3=session.client("s3")
    def list_files(self):
        
        response=self.s3.get_paginator('list_objects_v2')
        files=[]
        for i in response.paginate(Bucket=self.bucket,Prefix=self.prefix):
            for obj in i.get('Contents',[]):
                files.append(obj.get('Key'))
        print("Total Files =  ",len(files))
        return files


    def download_file(self,file):
        local=os.path.join(self.output_folder,file)
        os.makedirs(os.path.dirname(local),exist_ok=True)
           # this with original path
        if os.path.exists(local):
            return f"Skipped (exists):{file}"
        try:
                # fi=os.path.join(self.output_folder,file)
            self.s3.download_file(self.bucket,file,local)
            return f"Downloaded : {file}"
        except ClientError as e:
            return f"Failed: {file} ({e.response['Error']['Message']})"
        #    # if you want olnly file 
        #    fi=os.path.join(self.output_folder,file.rsplit("/",1)[1])
           

    def run(self):
        total_files=self.list_files()
        with Progress() as p:
            task=p.add_task("Processing....",total=len(total_files))
            with ThreadPoolExecutor(max_workers=20) as ex:
                future={ex.submit(self.download_file,f):f for f in total_files}
                for i in as_completed(future):
                    result=i.result()
                    p.update(task,advance=1)
                    print(result)

@app.command()
def main(s3path:str=typer.Argument(...,help="Input s3 path"),output_folder:str=typer.Option("output_folder/","--output","-o",help="Output folder for files")):
    obj=Main(s3path,output_folder)
    obj.run()


if __name__=="__main__":
    app()


# import os
# import boto3
# import typer
# from rich.progress import Progress
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from botocore.exceptions import ClientError

# app = typer.Typer()
# session = boto3.Session(profile_name="Yogesh")

# class Main:
#     def __init__(self, s3path, output_folder):
#         self.s3path = s3path
#         parts = s3path.replace("s3://", "").split("/", 1)
#         self.bucket = parts[0]
#         self.prefix = parts[1] if len(parts) > 1 else ""
#         self.output_folder = output_folder.rstrip("/\\")
#         self.s3 = session.client("s3")

#     def list_files(self):
#         paginator = self.s3.get_paginator("list_objects_v2")
#         files = []
#         for page in paginator.paginate(Bucket=self.bucket, Prefix=self.prefix):
#             for obj in page.get("Contents", []):
#                 files.append(obj["Key"])
#         print(f"Total Files Found: {len(files)}")
#         return files

#     def download_file(self, key):
#         # Keep full folder structure
#         local_path = os.path.join(self.output_folder, key)
#         os.makedirs(os.path.dirname(local_path), exist_ok=True)

#         # Skip if already downloaded (resume support)
#         if os.path.exists(local_path):
#             return f"Skipped (exists): {key}"

#         try:
#             self.s3.download_file(self.bucket, key, local_path)
#             return f"Downloaded: {key}"
#         except ClientError as e:
#             return f"Failed: {key} ({e.response['Error']['Message']})"

#     def run(self):
#         files = self.list_files()
#         if not files:
#             print("No files found.")
#             return

#         with Progress() as progress:
#             task = progress.add_task("Downloading...", total=len(files))
#             with ThreadPoolExecutor(max_workers=8) as executor:
#                 futures = {executor.submit(self.download_file, f): f for f in files}
#                 for future in as_completed(futures):
#                     result = future.result()
#                     progress.update(task, advance=1)
#                     typer.echo(result)


# @app.command()
# def main(
#     s3path: str = typer.Argument(..., help="Input S3 path, e.g. s3://bucket/prefix/"),
#     output_folder: str = typer.Option(
#         "output_folder/", "--output", "-o", help="Output folder for files"
#     ),
# ):
#     obj = Main(s3path, output_folder)
#     obj.run()


# if __name__ == "__main__":
#     app()
