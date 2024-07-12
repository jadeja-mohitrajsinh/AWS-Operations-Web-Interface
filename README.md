# AWS Automation with Python CGI Scripts

This project provides a set of Python CGI scripts to automate various tasks on AWS, including:

- Launching EC2 instances (standard and RHEL GUI)
- Accessing CloudWatch logs
- Transcribing audio to text (using S3 and Transcribe)
- Connecting to MongoDB databases
- Uploading files to S3
- Integrating Lambda, S3, and SES for sending emails

## Prerequisites

- **Python 3:** Make sure you have Python 3 installed.
- **AWS Account:** An active AWS account with the necessary permissions.
- **Boto3:** Install the AWS SDK for Python using:

  ```bash
  pip install boto3
  ```

- **PyMongo:** Install the MongoDB driver using:

  ```bash
  pip install pymongo
  ```

- **dotenv:** Install for managing environment variables using:

  ```bash
  pip install python-dotenv
  ```

- **.env file:** Create a `.env` file in your project directory and add the following:

  ```plaintext
  AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY
  AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY
  AWS_DEFAULT_REGION=YOUR_AWS_REGION
  MONGO_DB_USERNAME=YOUR_MONGO_USERNAME
  MONGO_DB_PASSWORD=YOUR_MONGO_PASSWORD
  ```

## Supported Operations

- `launch_ec2_instance`: Launches a basic EC2 instance.
- `launch_rhel_gui_instance`: Launches an EC2 instance with RHEL GUI.
- `access_cloud_logs`: Retrieves CloudWatch logs.
- `audio_to_text_event`: Transcribes an audio file from S3 to text.
- `connect_python_to_mongodb`: Establishes a connection to a MongoDB database.
- `upload_to_s3`: Uploads a file to S3.
- `integrate_lambda_s3_ses`: Downloads email IDs from an S3 file and sends test emails.
