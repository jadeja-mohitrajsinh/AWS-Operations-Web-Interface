Markdown
# AWS Automation with Python CGI Scripts

This project provides a set of Python CGI scripts to automate various tasks on AWS, including:

* Launching EC2 instances (standard and RHEL GUI)
* Accessing CloudWatch logs
* Transcribing audio to text (using S3 and Transcribe)
* Connecting to MongoDB databases
* Uploading files to S3
* Integrating Lambda, S3, and SES for sending emails

## Prerequisites

* **Python 3:**  Make sure you have Python 3 installed.
* **AWS Account:**  An active AWS account with the necessary permissions.
* **Boto3:**  Install the AWS SDK for Python using `pip install boto3`.
* **PyMongo:**  Install the MongoDB driver using `pip install pymongo`.
* **dotenv:**  Install for managing environment variables with `pip install python-dotenv`.
* **.env file:** Create a `.env` file in your project directory and add the following:

Use code with caution.
content_copy
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY
AWS_DEFAULT_REGION=YOUR_AWS_REGION
MONGO_DB_USERNAME=YOUR_MONGO_USERNAME
MONGO_DB_PASSWORD=YOUR_MONGO_PASSWORD


## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://your-repository-url.git
Install Dependencies:
Bash
pip install -r requirements.txt
Use code with caution.
content_copy
Running the Scripts
Make Scripts Executable:

Bash
chmod +x script_name.py
Use code with caution.
content_copy
Execute:  You can run the scripts in two ways:

From the Command Line:

Bash
./script_name.py 
Use code with caution.
content_copy
Using a Web Server:

Set up a web server (e.g., Apache) that supports CGI scripts.
Place the .py scripts in your web server's CGI directory.
Access them via URLs like http://your-server/cgi-bin/script_name.py
Sending Parameters
You can send parameters to the scripts through URL query strings or form data:

Example URL: http://your-server/cgi-bin/script_name.py?operation=launch_ec2_instance
Form Data: Use HTML forms to send data to the scripts.
Operations
The script supports the following operations:

launch_ec2_instance: Launches a basic EC2 instance.
launch_rhel_gui_instance: Launches an EC2 instance with RHEL GUI.
access_cloud_logs: Retrieves CloudWatch logs.
audio_to_text_event: Transcribes an audio file from S3 to text.
connect_python_to_mongodb: Establishes a connection to a MongoDB database.
upload_to_s3: Uploads a file to S3.
integrate_lambda_s3_ses: Downloads email IDs from an S3 file and sends test emails.
Important Considerations
Security: Store your AWS and MongoDB credentials securely (e.g., in environment variables, not directly in the code).
Resource Management: Be mindful of AWS resource limits and cost implications.
