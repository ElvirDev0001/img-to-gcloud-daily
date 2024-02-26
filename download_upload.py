import requests
from datetime import datetime
from google.cloud import storage
import schedule
import time
import os

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download image from {url}")

def upload_to_gcs(bucket_name, data, destination_blob_name):
    # Construct the credentials dictionary from environment variables
    credentials_dict = {
        "type": os.getenv("type"),
        "project_id": os.getenv("project_id"),
        "private_key_id": os.getenv("private_key_id"),
        "private_key": os.getenv("private_key").replace('\\n', '\n'),
        "client_email": os.getenv("client_email"),
        "client_id": os.getenv("client_id"),
        "auth_uri": os.getenv("auth_uri"),
        "token_uri": os.getenv("token_uri"),
        "auth_provider_x509_cert_url": os.getenv("auth_provider_x509_cert_url"),
        "client_x509_cert_url": os.getenv("client_x509_cert_url")
    }

    # Convert the credentials dictionary to a credentials object
    from google.oauth2.service_account import Credentials
    credentials = Credentials.from_service_account_info(credentials_dict)

    # Create a client instance with the specified credentials and project ID
    client = storage.Client(credentials=credentials, project=credentials_dict["project_id"])
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(data)

    print(f"File {destination_blob_name} uploaded to {bucket_name}.")

def scheduled_job():
    image_url = "http://sosrff.tsu.ru/srimage1/shm.jpg"
    bucket_name = "bucketforimages666"  # Change this to your bucket name
    file_name = datetime.utcnow().strftime("schuman/%d%m%y.jpg")  # Keeping format as ddmmyy

    image_data = download_image(image_url)
    upload_to_gcs(bucket_name, image_data, file_name)

def run_scheduled_jobs():
    schedule.every().day.at("17:00").do(scheduled_job)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait for 1 minute between checks

if __name__ == "__main__":
    run_scheduled_jobs()
