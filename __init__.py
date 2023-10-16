import bpy

from . import panels, props, ops


bl_info = {
    "name": "顶点色工具",
    "author": "Hollow_ame",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "Hollow",
    "description": "https://space.bilibili.com/60340452",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh",
}


def register():
    panels.register()
    props.register()
    ops.register()


def unregister():
    panels.unregister()
    props.register()
    ops.unregister()
