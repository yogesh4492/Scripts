# import os
# import urllib.parse
# import logging
# import boto3
# import time
# from pydantic import BaseModel

# # from common.fs_helper import FsHelper
# # from common import helper
# # from common.readers import Reader
# # from common.writers import Writer


# class S3File(BaseModel):
#     """Holds s3 bucket and prefix"""
#     bucket: str
#     prefix: str


# def from_browser_url_to_bucket_prefix(url):
#     pi = urllib.parse.urlparse(url)
#     bucket = os.path.basename(pi.path)
#     query = urllib.parse.parse_qs(pi.query)
#     prefix = query['prefix'][0]
#     return bucket, prefix


# def from_s3_url_to_bucket_prefix(url):
#     pi = urllib.parse.urlparse(url)
#     bucket = pi.hostname
#     prefix = pi.path[1:]
#     return bucket, prefix


# def get_bucket_prefix(url):
#     if url.startswith('s3'):
#         return from_s3_url_to_bucket_prefix(url)
#     else:
#         return from_browser_url_to_bucket_prefix(url)


# def get_s3file(url):
#     bucket, prefix = get_bucket_prefix(url)
#     return S3File(bucket=bucket, prefix=prefix)


# class AwsS3Reader(Reader):
#     def __init__(self, s3file: S3File, s3, encoding='utf8'):
#         self.s3file = s3file
#         self.s3 = s3
#         self.encoding = encoding

#     def read(self) -> str:
#         obj = self.s3.ObjectSummary(self.s3file.bucket, self.s3file.prefix)
#         result = obj.get()
#         return result['Body'].read().decode(self.encoding)


# class AwsS3Writer(Writer):
#     def __init__(self, s3file: S3File, s3, encoding='utf8'):
#         self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
#         self.s3file = s3file
#         self.s3 = s3
#         self.encoding = encoding

#     def write(self, text: str):
#         obj = self.s3.ObjectSummary(self.s3file.bucket, self.s3file.prefix)
#         obj.put(Body=text.encode(self.encoding))


# class AwsS3FsHelper(FsHelper):
#     def __init__(self, s3, s3_client):
#         self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
#         self.s3 = s3
#         self.s3_client = s3_client

#     def get_files(self, path_fragment: str, ext: str):
#         self.log.debug('Getting files from path_fragment=%s', path_fragment)
#         bucket, prefix = get_bucket_prefix(path_fragment)
#         bucket_obj = self.s3.Bucket(bucket)
#         return [
#             S3File(bucket=s.bucket_name, prefix=s.key)
#             for s in bucket_obj.objects.filter(Prefix=prefix.rstrip('/') + '/')
#             if s.key.endswith(ext)
#         ]

#     def get_s3file(self, path_fragment):
#         """Get S3File Object from the path_fragment"""

#         if isinstance(path_fragment, str):
#             bucket, prefix = get_bucket_prefix(path_fragment)
#             s3file = S3File(bucket=bucket, prefix=prefix)
#         elif isinstance(path_fragment, S3File):
#             s3file = path_fragment
#         else:
#             raise ValueError("path_fragment should be str or S3File")
#         return s3file

#     def get_reader(self, path_fragment, encoding=None) -> Reader:
#         s3file = self.get_s3file(path_fragment)
#         return AwsS3Reader(s3file, self.s3)

#     def get_writer(self, path_fragment, encoding=None) -> Writer:
#         s3file = self.get_s3file(path_fragment)
#         return AwsS3Writer(s3file, self.s3)
    
#     def copy(self, from_path, to_path):
#         self.log.debug('Copying files from from_path=%s to_path=%s', from_path, to_path)
#         from_bucket, from_prefix = helper.get_bucket_prefix(from_path)
#         to_bucket, to_prefix = helper.get_bucket_prefix(to_path)
        
#         bucketObj = self.s3.Bucket(to_bucket)
#         prefixObj = bucketObj.Object(to_prefix)
#         prefixObj.copy({'Bucket': from_bucket, 'Key': from_prefix})

#     def move(self, from_path, to_path):
#         pass

#     def download_to(self, from_path, to_local_path, chunk_size=8092):
#         self.log.debug('Downloading file %s => %s', from_path, to_local_path)
#         bucket, prefix = helper.get_bucket_prefix(from_path)
#         obj = self.s3.ObjectSummary(bucket, prefix)
#         result = obj.get()
#         with open(to_local_path, 'wb') as fp:
#             data = result['Body'].read(chunk_size)
#             while data is not None and len(data) > 0:
#                 fp.write(data)
#                 data = result['Body'].read(chunk_size)
#         return obj.size

#     def upload_to(self, local_path, to_path):
#         self.log.debug('Upload from {local_path} to {to_path}')
#         bucket, prefix = helper.get_bucket_prefix(to_path)
#         with open(local_path, 'rb') as fp:
#             obj = self.s3.ObjectSummary(bucket, prefix)
#             obj.put(Body=fp.read())
    
#     def upload_bytes(self, to_path, data_bytes):
#         self.log.debug('Uploading bytes to {to_path}')
#         bucket, prefix = helper.get_bucket_prefix(to_path)
#         obj = self.s3.ObjectSummary(bucket, prefix)
#         obj.put(Body=data_bytes)

#     def get_reader_s3(self, s3file, encoding='utf8') -> Reader:
#         obj= AwsS3Reader(s3file, self.s3)
#         return obj.read()
