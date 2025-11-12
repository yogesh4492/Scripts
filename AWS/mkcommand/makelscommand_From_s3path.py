import os
import typer
from itertools import accumulate
app=typer.Typer()
@app.command()
def main(input_file:str=typer.Argument(...,help="enter the name or path of txt file that contain the s3 paths"),output_file:str=typer.Option("lscommads.txt","-u",help="Output file that contain The commands")):
    with open(input_file,'r') as read:
        data=read.readlines()
        for i,j in enumerate(data,start=1):
            # print(i,j)
            # with open("2.txt",'w') as ex:
            print(f"file name = {i}.txt")
            with open(output_file,'a') as wr:
                wr.write(f'aws s3 ls "{j.strip()}" --recursive --human-readable --summarize > {i}.txt\n')

    # for i,r in read.ecumulate()
if __name__=="__main__":
    app()