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
    filename = str(time.time())
    def invoke(self, context, event):
        filepath = bpy.data.filepath
        bpy.ops.wm.save_mainfile(filepath=f"/home/fred/cloudrender/scenes/{filename}.blend")
        bpy.ops.wm.save_mainfile(filepath=filepath)
        start = bpy.data.scenes["Scene"].frame_start
        end = bpy.data.scenes["Scene"].frame_end
        os.system(f"python /home/fred/cloudrender/render.py {start} {end} {filename} &")
        return {'FINISHED'}

def cloud_render(self, context):
    self.layout.operator("my.operator")

def register():
    bpy.utils.register_class(myOperator)
    bpy.types.TOPBAR_MT_render.append(cloud_render)
    print("Hello World")
def unregister():
    print("Goodbye World")
