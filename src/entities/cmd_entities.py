from pydantic import BaseModel


class SwarCommandContext(BaseModel):
    s3path: str
    output_csv: str


