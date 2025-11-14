import os
import typer
app=typer.Typer()

@app.command()
def mkcpcommad(file):
    with open(file,'r') as re:
        data=re.readlines()
        for i in data:
            j=i.strip().replace("/","\\")
            print(f"aws s3 cp s3://prod-shaip-bucket/bhasha/Drone2-SSD/{i.strip()} \Drone2\{j}")

if __name__=="__main__":
    app()
