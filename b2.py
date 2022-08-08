from datetime import datetime
import os
import sys

import boto3



s3 = boto3.resource("s3")
BUCKET_NAME = "lambda-render-bucket2"

print("TEST1")
s3.Bucket(BUCKET_NAME).download_file("scenes/scene.blend", "/tmp/scene2.blend")
print("TEST2")

#os.system("sudo cp -r /tmp/* /mnt/render/renders")

#s3.Bucket(BUCKET_NAME).upload_file(f"/tmp/{filename}", f"renders/{filename}")
