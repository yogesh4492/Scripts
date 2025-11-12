import typer
import re
import json
import os
import csv
import glob
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress

app=typer.Typer()

class Main:
    def __init__(self,input,output):
        self.input=input
        self.output=output
    def load_json(self,file):
        with open(file,'r') as jr:
            return json.load(jr)
    def change_language(self,obj):
        # print(obj)
        if isinstance(obj,dict):
            return {k: self.change_language(v) for k,v in obj.items()}
        elif isinstance(obj,list):
            return [self.change_language(i) for i in obj]
        elif isinstance(obj,str):
            obj=re.sub(r'en_us_vnm',"en_US",obj,re.IGNORECASE)
            obj=re.sub(r'en_US_VNM','en_US',obj,re.IGNORECASE)
            return obj
        else:
            return obj
            

    def dump_json(self,file,data):
        with open(file,'w') as jw:
            json.dump(data,jw,indent=4)
    def processing(self,file):
            data=self.load_json(file)
            fi=os.path.join(self.output,os.path.basename(file))
            updated_data=self.change_language(data)
            self.dump_json(fi,updated_data)

            
    def run(self):
        files=glob.glob(f"{self.input}**/*.json",recursive=True)
        os.makedirs(self.output,exist_ok=True)
        with Progress() as p:
            tab=p.add_task('processing....',total=len(files))
            with ThreadPoolExecutor(max_workers=8) as ex:
                future={ex.submit(self.processing,file)for file in files}
                for i in as_completed(future):
                    p.update(tab,advance=1)
            
        
@app.command()
def main(input_dir:str =typer.Argument(...,help="input directory that contain original json files"),output_dir:str=typer.Argument(...,help="Output Directory where updated json file will store")):
    obj=Main(input_dir,output_dir)
    obj.run()


if __name__=="__main__":
    app()