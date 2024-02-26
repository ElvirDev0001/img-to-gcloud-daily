# Use an official Python runtime as a parent image
FROM python:3.12.1

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY download_upload.py /app/

# Command to run the script
CMD ["python", "download_upload.py"]