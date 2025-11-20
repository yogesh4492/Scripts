import typer
from dependency_injector.wiring import inject, Provide
from common.aws_fs_helper import AwsS3FsHelper
from common.fs_helper import FsHelper
from container import ApplicationContainer
from entities.cmd_entities import *
from commands.extract_details import SwarCommand


app = typer.Typer()


@inject
def read_tsv_add(s3path: str, output_csv: str, s3_helper: AwsS3FsHelper = Provide[ApplicationContainer.s3_helper]):
    ctx = SwarCommandContext(s3path=s3path, output_csv=output_csv)
    cmd = SwarCommand(ctx, s3_helper)
    cmd()


@app.command()
def read_tsv_swar(s3path: str, output_csv: str):
    read_tsv_add(s3path, output_csv)

  

if __name__ == '__main__':
    app_container = ApplicationContainer()

    app_container.init_resources()
    app_container.wire(modules=[__name__])

    app()
