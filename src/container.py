"""Application Container"""

import os
import logging.config
import boto3

from dependency_injector import containers, providers

from common.fs_helper import LocalFsHelper
from common.aws_fs_helper import AwsS3FsHelper


FILE_DIR = os.path.dirname(__file__)
DEFAULT_CONFIG = os.path.join(FILE_DIR, './configs/config.yml')
LOGGING_FILE = os.path.join(FILE_DIR, './configs/logging.ini')


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=[DEFAULT_CONFIG])

    logging = providers.Resource(
        logging.config.fileConfig,
        fname = LOGGING_FILE
    )

    local_fs_helper = providers.Singleton(
        LocalFsHelper
    )

    session = providers.ThreadLocalSingleton(
        boto3.session.Session
    )

    s3 = providers.ThreadLocalSingleton(
        session.provided.resource.call(),
        service_name='s3'
    )

    s3_client = providers.ThreadLocalSingleton(
        session.provided.client.call(),
        service_name="s3"
    )

    s3_helper = providers.ThreadLocalSingleton(
        AwsS3FsHelper,
        s3=s3,
        s3_client=s3_client
    )

