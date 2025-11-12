import typer
import os
app=typer.Typer()
@app.command()
def main(input_file:str=typer.Argument(...,help="Input file "),output_folder:str=typer.Argument(...,help="output_folder name"),file:str=typer.Argument(...,help="file that contain commandready")):
    if os.path.exists(input_file):
        with open(input_file,'r') as re:
            data=re.readlines()
            for i in data:
                with open(file,'a') as w:
                    w.write(f'aws s3 cp "{i.strip()}" "{output_folder}"\n')

if __name__=="__main__":
    app()