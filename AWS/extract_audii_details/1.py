import boto3
from pydub import AudioSegment
from io import BytesIO
from urllib.parse import urlparse
import os

s3 = boto3.client("s3")

AUDIO_EXTENSIONS = (
    ".wav", ".mp3", ".flac", ".m4a", ".aac",
    ".ogg", ".opus", ".wma", ".aiff", ".alac"
)

def parse_s3_path(s3_path):
    p = urlparse(s3_path)
    return p.netloc, p.path.lstrip("/")

def extract_audio_info(bucket, key):
    # File size from S3 (no download)
    head = s3.head_object(Bucket=bucket, Key=key)
    size_bytes = head["ContentLength"]

    # Stream file into memory
    obj = s3.get_object(Bucket=bucket, Key=key)
    audio_bytes = BytesIO(obj["Body"].read())

    # Detect format from extension
    ext = os.path.splitext(key)[1].lower().replace(".", "")

    audio = AudioSegment.from_file(audio_bytes, format=ext)

    duration = len(audio) / 1000
    sample_rate = audio.frame_rate
    channels = audio.channels
    bit_depth = audio.sample_width * 8
    bitrate = sample_rate * channels * bit_depth

    return {
        "file": key,
        "format": ext,
        "duration_sec": round(duration, 2),
        "sample_rate": sample_rate,
        "true_frequency": sample_rate,
        "channels": channels,
        "bit_depth": bit_depth,
        "bitrate_bps": bitrate,
        "size_mb": round(size_bytes / (1024 * 1024), 2)
    }

def process_s3_folder(s3_folder_path):
    bucket, prefix = parse_s3_path(s3_folder_path)

    paginator = s3.get_paginator("list_objects_v2")

    results = []

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"].lower()

            if not key.endswith(AUDIO_EXTENSIONS):
                continue

            try:
                info = extract_audio_info(bucket, obj["Key"])
                results.append(info)
                print("Processed:", obj["Key"])
            except Exception as e:
                print("Failed:", obj["Key"], e)

    return results
audio_data = process_s3_folder(
    "s3://prod-shaip-bucket/bhasha/Oracle/audio/"
)

print("Total audio files:", len(audio_data))
