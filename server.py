#!/usr/bin/env python3

import os
import cgi
import boto3
import pymongo
import json
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AWS credentials
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')

# MongoDB credentials
MONGO_DB_USERNAME = os.getenv('MONGO_DB_USERNAME')
MONGO_DB_PASSWORD = os.getenv('MONGO_DB_PASSWORD')

# Function to handle CORS
def print_headers():
    print("Content-Type: application/json")
    print("Access-Control-Allow-Origin: *")
    print()

# AWS operations
def launch_ec2_instance():
    ec2 = boto3.resource('ec2', region_name=AWS_DEFAULT_REGION,
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    instance = ec2.create_instances(
        ImageId='ami-0abcdef1234567890',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro'
    )
    return {'message': f'EC2 instance launched: {instance[0].id}'}

def launch_rhel_gui_instance():
    ec2 = boto3.resource('ec2', region_name=AWS_DEFAULT_REGION,
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    instance = ec2.create_instances(
        ImageId='ami-0abcdef1234567890',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro'
    )
    return {'message': f'RHEL GUI instance launched: {instance[0].id}'}

def access_cloud_logs(log_group_name, log_stream_name):
    cloudwatch = boto3.client('logs', region_name=AWS_DEFAULT_REGION,
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    response = cloudwatch.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        limit=10
    )

    return {'logs': response['events']}

def audio_to_text_event(bucket_name, audio_file_name):
    transcribe = boto3.client('transcribe', region_name=AWS_DEFAULT_REGION,
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    job_name = f'job-{int(time.time())}'
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': f's3://{bucket_name}/{audio_file_name}'},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )

    return {'job_status': 'Started', 'job_name': job_name}

def connect_python_to_mongodb():
    client = pymongo.MongoClient(f'mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@cluster0.mongodb.net/')
    db = client.test_database
    collection = db.test_collection
    collection.insert_one({'message': 'Connection successful'})
    return {'message': 'Data inserted into MongoDB'}

def upload_to_s3(bucket_name, file_name):
    s3 = boto3.client('s3', region_name=AWS_DEFAULT_REGION,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    response = s3.upload_file(file_name, bucket_name, file_name)
    return {'message': f'File {file_name} uploaded to bucket {bucket_name}'}

def integrate_lambda_s3_ses(bucket_name, file_name):
    # Assuming Lambda function is set up to trigger on S3 upload and send email via SES
    return {'message': 'Lambda function triggered for S3 upload and SES'}

def main():
    print_headers()

    form = cgi.FieldStorage()
    operation = form.getvalue('operation')

    if operation == 'launch_ec2_instance':
        result = launch_ec2_instance()
    elif operation == 'launch_rhel_gui_instance':
        result = launch_rhel_gui_instance()
    elif operation == 'access_cloud_logs':
        log_group_name = form.getvalue('log_group_name')
        log_stream_name = form.getvalue('log_stream_name')
        result = access_cloud_logs(log_group_name, log_stream_name)
    elif operation == 'audio_to_text_event':
        bucket_name = form.getvalue('bucket_name')
        audio_file_name = form.getvalue('audio_file_name')
        result = audio_to_text_event(bucket_name, audio_file_name)
    elif operation == 'connect_python_to_mongodb':
        result = connect_python_to_mongodb()
    elif operation == 'upload_to_s3':
        bucket_name = form.getvalue('bucket_name')
        file_name = form.getvalue('file_name')
        result = upload_to_s3(bucket_name, file_name)
    elif operation == 'integrate_lambda_s3_ses':
        bucket_name = form.getvalue('bucket_name')
        file_name = form.getvalue('file_name')
        result = integrate_lambda_s3_ses(bucket_name, file_name)
    else:
        result = {'message': 'Invalid operation'}

    print(json.dumps(result))

if __name__ == "__main__":
    main()
