import logging
import boto3
from botocore.exceptions import ClientError
import os


class AwsS3:

    def __init__(self):
        self.s3_client = boto3.client('s3')

    def list_buckets(self):
        """Lists all buckets."""

        # Retrieve the list of existing buckets
        response = self.s3_client.list_buckets()

        # Output the bucket names
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(bucket['Name'])

    def get_buckets(self):
        """Get all buckets."""
        return self.s3_client.list_buckets()['Buckets']

    def list_files(self, bucket):
        """Lists all the files in the bucket."""

        response = self.s3_client.list_objects(Bucket=bucket)

        # Output the files name
        print('Existing files:')
        for file in response['Contents']:
            print(file['Key'])

    def get_files(self, bucket):
        """Get all files in the bucket."""
        return self.s3_client.list_objects(Bucket=bucket)['Contents']

    def upload_file(self, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        self.s3_client = boto3.client('s3')
        try:
            response = self.s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True


if __name__ == "__main__":
    s3 = AwsS3()
    s3.list_buckets()
    buckets = s3.get_buckets()
    s3.list_files(buckets[0]['Name'])

    # if s3.upload_file('test.txt', 'my-bucket', 'test.txt'):
    #     print("upload success")
    # else:
    #     print("upload failed")
