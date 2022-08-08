bl_info = {
    "name": "My Test Add-on",
    "blender": (2, 80, 0),
    "category": "Object",
}
import bpy
import json
import threading
import requests
import os
import time

class myOperator(bpy.types.Operator):
    bl_idname = "my.operator"
    bl_label = "Cloud Render"
    def invoke(self, context, event):
        print("operator")
        url = 'https://djp1kdedjl.execute-api.us-east-1.amazonaws.com/prod/render'

        start = 1
        end = 20

        def render(frame):
            r = requests.post(url, data=json.dumps({"frame":frame}))
            print(r)

        threads = []
        for frame in range(start, end):
            t = threading.Thread(target=render, args=(frame,))
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()

        print("done rendering")
        time.sleep(10)

        os.system("aws s3 sync s3://lambda-render-bucket2 /home/fred/cloudrender/")
        return {'FINISHED'}

def cloud_render(self, context):
    self.layout.operator("my.operator")

def register():
    bpy.utils.register_class(myOperator)
    bpy.types.TOPBAR_MT_render.append(cloud_render)
    print("Hello World")
def unregister():
    print("Goodbye World")
