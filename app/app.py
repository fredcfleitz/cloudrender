import json
import os
import boto3


def handler(event, context):
    print(event)
    body = json.loads(event['body'])
    frame = body["frame"]
    filename = body["filename"]

    s3 = boto3.resource("s3")
    BUCKET_NAME = "lambda-render-bucket2"

    s3.Bucket(BUCKET_NAME).download_file(f"scenes/{filename}.blend", "/tmp/scene.blend")

    os.system(f"blender -b /tmp/scene.blend -o /tmp/####.png -f {frame}")

    #os.system("sudo cp -r /tmp/* /mnt/render/renders")

    for file in os.listdir("/tmp"):
        if "png" in file:
            s3.Bucket(BUCKET_NAME).upload_file(f"/tmp/{file}", f"renders/{file}")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": 'ok'})
    }
