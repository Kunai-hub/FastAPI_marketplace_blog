from src.fastapi_marketplace_blog.core.config import config
import boto3
from botocore.client import Config

S3_ENDPOINT = config.S3_ENDPOINT
S3_REGION = config.S3_REGION
S3_ACCESS = config.S3_ACCESS
S3_SECRET = config.S3_SECRET
S3_BUCKET = config.S3_BUCKET

s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS,
    aws_secret_access_key=S3_SECRET,
    config=Config(signature_version="s3v4"),
    region_name=S3_REGION,
)


def generate_presigned_url(key: str, expires_in: int = 3600):
    return s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": S3_BUCKET, "Key": key, "ACL": "public-read"},
        ExpiresIn=expires_in,
    )
