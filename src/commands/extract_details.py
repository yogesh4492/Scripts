import logging
import json,os
from common import job_engine
from common.aws_fs_helper import AwsS3FsHelper, S3File
from entities.cmd_entities import SwarCommandContext
from common import helper
from commands.extract_details import *
from tqdm import tqdm

class SwarJob:
    def __init__(self, file: S3File, s3_helper: AwsS3FsHelper):
        self.file = file
        self.s3_helper = s3_helper
        self.data = []

    def __call__(self):
        try:
            json_data = json.loads(self.s3_helper.get_reader(f"s3://{self.file.bucket}/{self.file.prefix}").read())
            domain = json_data.get('value',{}).get('domains',"")
            topic = json_data.get('value',{}).get('topics',"")
            speakers = json_data.get('value',{}).get('speakers',"")
            segments = json_data.get('value',{}).get('segments',"")
            if speakers:
#                 json_data["Data_Proprietor"] = "Healthly.AI data dba Shaip"
                for speaker in speakers:
                    csv_dict = {}
                    csv_dict["Filepath"] = self.file.prefix
                    csv_dict["Domain"] = domain 
                    csv_dict["Topic"] = topic 
    #                 csv_dict["Gender"] = speaker['gender'] 
    #                 csv_dict["Transcription"] = segments[0].get("transcriptionData",{}).get("content","")
                    self.data.append(csv_dict)
            else:
#                 json_data.append({"Data_Proprietor":"Healthly.AI data dba Shaip"})
                domain = json_data.get('domain',"")
                topic = json_data.get('topic',"")
                speakers = json_data.get('speakers',"")
                if speakers:
                    for speaker in speakers:
                        csv_dict = {}
                        csv_dict["Filepath"] = self.file.prefix
                        csv_dict["Domain"] = domain 
                        csv_dict["Topic"] = topic 
    #                     csv_dict["Gender"] = speaker['gender'] 
    #                     csv_dict["Transcription"] = segments[0].get("transcriptionData",{}).get("content","")
                        self.data.append(csv_dict)
#             helper.dump_json(os.path.basename(self.file.prefix),json_data,False)
#             self.s3_helper.upload_to(os.path.basename(self.file.prefix), f"s3://{self.file.bucket}/{self.file.prefix}")
#             os.remove(os.path.basename(self.file.prefix))
        except: 
            print(self.file)
class SwarCommand:
    def __init__(self, ctx: SwarCommandContext, s3_helper: AwsS3FsHelper):
        self.log = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self.ctx = ctx
        self.s3_helper = s3_helper
    
    def __call__(self):
        self.log.info('Executing Tsv Details Extract Command')
        self.log.info(self.ctx)

        tsv_files = self.s3_helper.get_files(self.ctx.s3path, '.json')
        jobs = [SwarJob(file, self.s3_helper) for file in tsv_files]
        job_engine.execute(jobs, desc='Processing')
        data = []
        for job in jobs:
            data.extend(job.data)
        helper.dump_csv(self.ctx.output_csv,data)
        
        