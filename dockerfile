FROM python:3.12.1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
CMD echo $GCS_SA_KEY | base64 -d > /app/gcs-service-account-key.json && python download_upload.py