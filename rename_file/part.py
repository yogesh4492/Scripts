import os 
import glob
import typer
app=typer.Typer()

@app.command()
def main(input_dir):
    file=os.listdir(input_dir)
    for i in file:
        if i.endswith("_left.wav"):
            new_file=i.replace("_left.wav","_in.wav")
        elif i.endswith("_right.wav"):
            new_file=i.replace("_right.wav","_out.wav")
        old_file=os.path.join(input_dir,i)
        new_files=os.path.join(input_dir,new_file)

        os.rename(old_file,new_files)


if __name__=="__main__":
    app()