import bpy
from bpy.types import PropertyGroup


class VertexColorCol(PropertyGroup):
    index: bpy.props.IntProperty()  # type: ignore
    color: bpy.props.FloatVectorProperty(
        name="VertexColor", size=3, subtype='COLOR', default=(0, 0, 0), min=0, max=1)  # type: ignore


cls = [VertexColorCol]


def register():
    try:
        for i in cls:
            bpy.utils.register_class(i)

        # 注册预设顶点色集合
        bpy.types.Scene.ho_VertexColorCol = bpy.props.CollectionProperty(
            type=VertexColorCol)
        # 注册自建缓存顶点色集合
        bpy.types.Scene.ho_TempVertexColor = bpy.props.CollectionProperty(
            type=VertexColorCol)

        # 注册顶点色预览布尔开关
        def changeViewMode(self, context):
            if context.scene.ho_VertexColorViewMode:
                bpy.ops.ho.entervertexcolorview()
            else:
                bpy.ops.ho.quitvertexcolorview()
        bpy.types.Scene.ho_VertexColorViewMode = bpy.props.BoolProperty(
            default=False, update=changeViewMode)

        # 注册吸色模式布尔开关
        def changeGetColorMode(self, context):
            if context.scene.ho_GetVertexColorViewMode:
                bpy.ops.ho.entergetvertexcolorview()
            else:
                bpy.ops.ho.quitgetvertexcolorview()
        bpy.types.Scene.ho_GetVertexColorViewMode = bpy.props.BoolProperty(
            default=False, update=changeGetColorMode)

        # 注册缓存色，前景色，背景色
        bpy.types.Scene.ho_PaintTempVertexColor = bpy.props.FloatVectorProperty(
            name="缓存颜色", size=3, subtype="COLOR", default=(1, 0, 0), min=0, max=1)
        bpy.types.Scene.ho_FrontTempVertexColor = bpy.props.FloatVectorProperty(
            name="前景颜色", size=3, subtype="COLOR", default=(1, 1, 1), min=0, max=1)
        bpy.types.Scene.ho_BackTempVertexColor = bpy.props.FloatVectorProperty(
            name="背景颜色", size=3, subtype="COLOR", default=(0, 0, 0), min=0, max=1)

        # 注册默认组赋色的布尔开关，以及组赋色的index
        bpy.types.Scene.ho_isGroupPaintMode = bpy.props.BoolProperty(
            default=True)
        bpy.types.Scene.ho_GroupPaintDefaultIndex = bpy.props.IntProperty(
            default=1)

        # 注册选择同顶点色的容差
        bpy.types.Scene.ho_chooseSameVertexColorMeshThreshold = bpy.props.FloatProperty(
            name="容差", description="选择同顶点色时的容差(通道共用容差)", default=0.01, max=1, min=0, step=0.01)

    except Exception:
        print("Props load failed!!!")


def unregister():
    bpy.utils.unregister_class(VertexColorCol)
