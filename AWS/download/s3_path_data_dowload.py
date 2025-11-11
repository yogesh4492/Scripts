import boto3
import typer
app=typer.Typer()

@app.command()
def main(input,output):
    jay=str(input)
    om=jay.split("/")
    bucket=str(om[2])
    yog=""
    yog="/".join(om[3:])
    s3=boto3.client("s3")
    s3.download_file(bucket,yog,output)
if __name__=="__main__":
    app()
