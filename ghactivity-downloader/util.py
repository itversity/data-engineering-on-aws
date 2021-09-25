from datetime import datetime as dt
from datetime import timedelta as td
import requests, boto3, os
from botocore.errorfactory import ClientError


def get_client():
    return boto3.client('s3')


def get_prev_file_name(bucket, file_prefix, bookmark_file, baseline_file):
    s3_client = get_client()
    try:
        bookmark_file = s3_client.get_object(
            Bucket=bucket,
            Key=f'{file_prefix}/{bookmark_file}'
        )
        prev_file = bookmark_file['Body'].read().decode('utf-8')
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            prev_file = baseline_file
        else:
            raise
    return prev_file


def upload_bookmark(bucket, file_prefix, bookmark_file, bookmark_contents):
    s3_client = get_client()
    s3_client.put_object(
        Bucket=bucket,
        Key=f'{file_prefix}/{bookmark_file}',
        Body=bookmark_contents.encode('utf-8')
    )


def get_next_file_name(prev_file):
    dt_part = prev_file.split('.')[0]
    next_file = f"{dt.strftime(dt.strptime(dt_part, '%Y-%M-%d-%H') + td(hours=1), '%Y-%M-%d-%-H')}.json.gz"
    return next_file
