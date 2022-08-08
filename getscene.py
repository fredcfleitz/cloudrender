import boto3

s3 = boto3.resource("s3")
BUCKET_NAME = "lambda-render-bucket2"


for o in s3.Bucket(BUCKET_NAME).objects.filter(Prefix="scene"):
    print(o.last_modified)

