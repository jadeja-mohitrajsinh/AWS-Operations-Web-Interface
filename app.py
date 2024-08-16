from flask import Flask, request, jsonify, send_from_directory
import boto3
import pymongo
import os
from dotenv import load_dotenv
import time

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# AWS credentials
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')

# MongoDB credentials
MONGO_ATLAS_CONNECTION_STRING = os.getenv('MONGO_ATLAS_CONNECTION_STRING')

# SES sender email
SENDER_EMAIL = os.getenv('SENDER_EMAIL')

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
    logs = cloudwatch.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        limit=10
    )
    return logs

def audio_to_text(bucket_name, audio_file_path):
    transcribe = boto3.client('transcribe', region_name=AWS_DEFAULT_REGION,
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    job_name = 'audio-transcription-job-' + str(int(time.time()))
    job_uri = f's3://{bucket_name}/{os.path.basename(audio_file_path)}'
    
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    
    # Wait for the transcription job to complete
    while True:
        result = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        status = result['TranscriptionJob']['TranscriptionJobStatus']
        if status in ['COMPLETED', 'FAILED']:
            break
        time.sleep(15)  # Wait for 15 seconds before checking again
    
    if status == 'COMPLETED':
        transcription_url = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
        return {'message': f'Transcription completed. You can download the transcript from {transcription_url}'}
    else:
        return {'error': 'Transcription failed'}

def connect_python_to_mongodb():
    try:
        client = pymongo.MongoClient(MONGO_ATLAS_CONNECTION_STRING)
        db = client.test_database
        db_list = client.list_database_names()
        return {'message': f'Connected to MongoDB Atlas. Databases: {db_list}'}
    except pymongo.errors.ConnectionError as ce:
        return {'error': f'Connection Error: {ce}'}
    except Exception as e:
        return {'error': f'An error occurred: {e}'}

def upload_to_s3(bucket_name, file_path):
    s3 = boto3.client('s3', region_name=AWS_DEFAULT_REGION,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    file_name = os.path.basename(file_path)
    s3.upload_file(file_path, bucket_name, file_name)
    return {'message': f'File uploaded to S3 bucket {bucket_name}'}

def integrate_lambda_s3_ses():
    s3 = boto3.client('s3', region_name=AWS_DEFAULT_REGION,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    ses = boto3.client('ses', region_name=AWS_DEFAULT_REGION,
                       aws_access_key_id=AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    bucket_name = os.getenv('S3_BUCKET_NAME')
    object_key = os.getenv('S3_OBJECT_KEY')
    
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    email_addresses = response['Body'].read().decode('utf-8').splitlines()
    
    email_subject = 'Test Email from AWS Lambda'
    email_body = 'This is a test email sent from AWS Lambda using SES.'

    for email in email_addresses:
        if email:
            try:
                ses.send_email(
                    Source=SENDER_EMAIL,
                    Destination={'ToAddresses': [email]},
                    Message={
                        'Subject': {'Data': email_subject},
                        'Body': {'Text': {'Data': email_body}}
                    }
                )
            except Exception as e:
                print(f'Error sending email to {email}: {e}')
    
    return {'message': 'Emails sent successfully'}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/aws_operations', methods=['POST'])
def aws_operations():
    operation = request.form.get('operation')
    
    if operation == 'launch_ec2_instance':
        result = launch_ec2_instance()
    elif operation == 'launch_rhel_gui_instance':
        result = launch_rhel_gui_instance()
    elif operation == 'access_cloud_logs':
        log_group_name = request.form.get('log_group_name')
        log_stream_name = request.form.get('log_stream_name')
        result = access_cloud_logs(log_group_name, log_stream_name)
    elif operation == 'audio_to_text_event':
        bucket_name = request.form.get('bucket_name')
        audio_file = request.files['audio_file']
        audio_file_path = f'/tmp/{audio_file.filename}'
        audio_file.save(audio_file_path)
        result = audio_to_text(bucket_name, audio_file_path)
    elif operation == 'connect_python_to_mongodb':
        result = connect_python_to_mongodb()
    elif operation == 'upload_to_s3':
        bucket_name = request.form.get('bucket_name')
        file = request.files['file']
        file_path = f'/tmp/{file.filename}'
        file.save(file_path)
        result = upload_to_s3(bucket_name, file_path)
    elif operation == 'integrate_lambda_s3_ses':
        result = integrate_lambda_s3_ses()
    else:
        result = {'error': 'Invalid operation'}

    return jsonify(result)

if __name__ == '__main__':
    app.run(port=8000)
