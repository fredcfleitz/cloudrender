import requests
import json
import threading
import time
import os
import sys
import subprocess

url = 'https://djp1kdedjl.execute-api.us-east-1.amazonaws.com/prod/render'

start = int(sys.argv[1])
end = int(sys.argv[2]) + 1
filename = sys.argv[3]

now = time.time()

def poller():
    files = subprocess.check_output("aws s3 ls s3://lambda-render-bucket2/render --recursive", shell=True)

    files = str(files)[2:-2]

    files = files.split("\\n")

    d = {}

    for index, file in enumerate(files):
        new = file.split()
        new[-1] = new[-1].split("/")[1].strip("0").split(".")[0]
        new[0] = time.mktime(time.strptime(new[0] + " " + new[1], "%Y-%m-%d %H:%M:%S"))
        d[new[-1]] = new[0]

    return d

def render(frame):
    r = requests.post(url, data=json.dumps({"frame":frame, "filename":filename}))
    print(r)

print("Uploading blend")
os.system("aws s3 rm s3://lambda-render-bucket2/scenes/ --recursive")

os.system("aws s3 cp /home/fred/cloudrender/scenes/scene.blend s3://lambda-render-bucket2/scenes/{filename}.blend")


#os.system("aws s3 rm s3://lambda-render-bucket2/renders/ --recursive")

print("Begin rendering")

threads = []
for frame in range(start, end):
    t = threading.Thread(target=render, args=(frame,))
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()

print("done rendering")

poll = True
while poll:
    print("polling...")
    time.sleep(1)
    frames = poller()
    poll = False
    for frame in range(start, end):
        if str(frame) in frames:
            if frames[str(frame)] < now:
                poll = True
        else:
            poll = True

os.system("rm -rf /home/fred/cloudrender/renders/*")

os.system("aws s3 cp --recursive s3://lambda-render-bucket2/renders/ /home/fred/cloudrender/renders")
