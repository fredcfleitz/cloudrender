import os
import subprocess
import time

files = subprocess.check_output("aws s3 ls s3://lambda-render-bucket2/render --recursive", shell=True)

files = str(files)[2:-2]

files = files.split("\\n")

d = {}

for index, file in enumerate(files):
    new = file.split()
    new[-1] = new[-1].split("/")[1].strip("0").split(".")[0]
    new[0] = time.mktime(time.strptime(new[0] + " " + new[1], "%Y-%m-%d %H:%M:%S"))
    d[new[-1]] = new[0]

print(d)


