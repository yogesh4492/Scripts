import os
import typer
app=typer.Typer()
import glob


def rename(directory):
    count_left=0
    count_right=0
    allfiles=glob.glob()
    for i in os.listdir(directory):
        if i.endswith("_left.wav"):
            new_file=i.replace("_left.wav","_in.wav")
            print("Renamed",i,"-->",new_file)
            count_left+=1
        elif i.endswith("_right.wav"):
            new_file=i.replace("_right.wav","_out.wav")
            print("Renamed",i,"-->",new_file)
            count_right+=1
        old_file=os.path.join(directory,i)
        new_files=os.path.join(directory,new_file)
        os.rename(old_file,new_files)
    print("left file= ",count_left)
    print("right count= ",count_right)
@app.command()
def main(input_dir:str=typer.Argument(...,help="Enter Directory Name That contain old file name")):
    rename(input_dir)



if __name__=="__main__":
    app()
    
    
    
    

