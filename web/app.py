import configparser
import datetime
import os

import boto3
from flask import Flask, render_template
from google.cloud import storage

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

cloud_storage = config['Cloud']['storage']
bucket_name = config['Cloud']['bucket']
if cloud_storage == 'gcp':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config['Google']['credentials']
    print(config['Google']['credentials'])

stream_url = config['Stream']['url']


@app.route('/hello')
def hello_world():
    return 'Hello, World!'


@app.route("/")
def index():
    contents = []
    print(cloud_storage)
    if cloud_storage == 'aws':
        contents = show_images_aws(bucket_name)
    elif cloud_storage == 'gcp':
        contents = generate_download_signed_url_v4(bucket_name)
    return render_template('index.html', contents=contents, stream_url=stream_url)

# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('static', path)


def show_images_aws(bucket):
    s3_client = boto3.client('s3')
    public_urls = []
    try:
        for item in s3_client.list_objects(Bucket=bucket, Prefix='alarm/')['Contents']:
            presigned_url = s3_client.generate_presigned_url(
                'get_object', Params={'Bucket': bucket, 'Key': item['Key']}, ExpiresIn=900)
            public_urls.append({'name': item['Key'], 'url': presigned_url})
    except Exception as e:
        print(e)
        pass
    print("[INFO] : The contents inside show_image = ", public_urls)
    return public_urls


def generate_download_signed_url_v4(bucket_name):
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    # bucket_name = 'your-bucket-name'

    storage_client = storage.Client()

    public_urls = []
    try:
        blobs = storage_client.list_blobs(bucket_name, prefix='alarm/')
        for blob in blobs:
            url = blob.generate_signed_url(
                version="v4",
                # This URL is valid for 15 minutes
                expiration=datetime.timedelta(minutes=15),
                # Allow GET requests using this URL.
                method="GET",
            )
            public_urls.append({'name': blob.name, 'url': url})
    except Exception as e:
        print(e)
        pass
    print("[INFO] : The contents inside show_image = ", public_urls)
    return public_urls


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
