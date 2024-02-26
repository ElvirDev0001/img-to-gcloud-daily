import requests
from datetime import datetime
from google.cloud import storage

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download image from {url}")

def upload_to_gcs(bucket_name, data, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(data)

    print(f"File {destination_blob_name} uploaded to {bucket_name}.")

def main():
    image_url = "http://sosrff.tsu.ru/srimage1/shm.jpg"
    bucket_name = "bucketforimages666"  # Change this to your bucket name
    file_name = datetime.now().strftime("%d%m%y.jpg")

    image_data = download_image(image_url)
    upload_to_gcs(bucket_name, image_data, file_name)

if __name__ == "__main__":
    main()