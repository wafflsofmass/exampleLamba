import json
import tarfile
import os
import boto3
import io
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

target_bucket_name = os.environ.get('TARGET_BUCKET', '')

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')


def s3ObjectToBytes(s3_object):
    return io.BytesIO(s3_object['Body'].read())

def uploadFile(key, file):
    s3_resource.meta.client.upload_fileobj(
        file,
        Bucket=target_bucket_name,
        Key=key
    )

def delete(bucket_key, obj_key):
    LOGGER.info(f"Attempting to delete {obj_key} from {bucket_key}")
    s3_client.delete_object(Bucket=bucket_key, Key=obj_key)
    LOGGER.info("Success!")

def extract(src_bucket, obj_key):
    s3_object = s3_client.get_object(Bucket=src_bucket, Key=obj_key)

    LOGGER.info(f"Attempting to extract {obj_key} from {src_bucket}")
    # Extract files & save to unzipped-documents w/ dir name as source_file_name
    with tarfile.open(fileobj=s3ObjectToBytes(s3_object), mode='r') as z:
        for filename in z.getmembers():
            if filename.isfile():
                uploadFile(f'{obj_key}/{filename.name}', z.extractfile(filename))
    
    LOGGER.info("Success!")

    delete(src_bucket, obj_key)

    


def lambda_handler(event, context):
    for record in event["Records"]:

        source_bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        try:
            extract(source_bucket_name, object_key)
        except Exception as e:
            LOGGER.info(f"Error: {str(e)}")
            
    return {
        'statusCode': 200
    }
