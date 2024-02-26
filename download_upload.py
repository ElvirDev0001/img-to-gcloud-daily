import requests
import time
from datetime import datetime, timedelta
from google.cloud import storage
import schedule
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

    # Create a client instance with the specified credentials
    client = storage.Client(credentials=credentials_dict)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(data)

    print(f"File {destination_blob_name} uploaded to {bucket_name}.")

def scheduled_job():
    image_url = "http://sosrff.tsu.ru/srimage1/shm.jpg"
    bucket_name = "bucketforimages666"  # Change this to your bucket name
    file_name = datetime.now().strftime("schuman/%d%m%y.jpg")  # Prefix with 'schuman/' to save in the schuman folder

    image_data = download_image(image_url)
    upload_to_gcs(bucket_name, image_data, file_name)

def wait_until_time(target_hour=17, target_minute=0, timezone_offset=0):
    # Adjust target hour based on timezone offset
    target_hour -= timezone_offset
    # Get current time
    now = datetime.utcnow()
    # Calculate target datetime for today
    target_time = datetime(now.year, now.month, now.day, target_hour, target_minute)
    # If we're past the target time, schedule for the next day
    if now > target_time:
        target_time += timedelta(days=1)
    # Calculate how long to wait and delay execution
    wait_seconds = (target_time - now).total_seconds()
    time.sleep(wait_seconds)

def main():
    #wait_until_time()  # Wait until the target time (6 PM UTC+1)
    scheduled_job()  # Run the scheduled job

if __name__ == "__main__":
    main()
