import os
import typer
import csv


app=typer.Typer()

def rename(directory,output):

    fields=['old_name','new_name']
    with open(output,'w',encoding="utf-8") as cw:
        csw=csv.DictWriter(cw,fieldnames=fields)
        csw.writeheader()
        for i in os.listdir(directory):
            if i.endswith('_left.wav'):
                new_name=i.replace("_left.wav","_in.wav")
            elif i.endswith("_right.wav"):
                new_name=i.replace("_right.wav","_out.wav")
            else:
                continue
            
            old_file=os.path.join(directory,i)
            new_file=os.path.join(directory,new_name)
            os.rename(old_file,new_file)
            row={}
            row['old_name']=old_file
            row['new_name']=new_file
            csw.writerow(row)
                
@app.command()
def main(input_dir:str=typer.Argument(...,help="Input Directory path for rename files"),
         output_csv:str=typer.Option("file_rename.csv","--output",help="Output csv File name")):
    rename(input_dir,output_csv)
if __name__=="__main__":
    app()