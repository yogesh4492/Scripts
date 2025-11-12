import json
import os
import glob
import typer
from concurrent.futures import ThreadPoolExecutor,as_completed
from rich.progress import Progress

app=typer.Typer()

class Main:
    def __init__(self,input_dir,out_dir):
        self.out_dir=out_dir
        self.input_dir=input_dir
    def load_json(self,file):
        with open(file,'r') as jr:
            return dict(json.load(jr))
    def dump_json(self,file,data):
        with open(file,'w') as jw:
            json.dump(data,jw,indent=4)
    def processing(self,file):
        data=self.load_json(file)
        for j in data.values():
            for k in j.get('speakers'):
                if k.get('languages')==['en_US_VNM']:
                    k['languages']=['en_US']
        name=os.path.join(self.out_dir,os.path.basename(file))
        self.dump_json(name,data)
    def run(self):
        file=glob.glob(f"{self.input_dir}/**/*.json",recursive=True)
        os.makedirs(self.out_dir,exist_ok=True)
        
        with Progress() as p:
            tab=p.add_task("Processing....",total=len(file))
            with ThreadPoolExecutor(max_workers=10) as ex:
                future={ex.submit(self.processing,f)for f in file}
                for i in as_completed(future):
                    p.advance(tab)
@app.command()
def main(input_dir,out_dir):
    obj=Main(input_dir,out_dir)
    obj.run()
                
if __name__=="__main__":
    app()



