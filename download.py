import boto3

s3 = boto3.resource("s3")
BUCKET_NAME = "lambda-render-bucket2"
s3.Bucket(BUCKET_NAME).download_folder("renders", "/tmp/renders")


