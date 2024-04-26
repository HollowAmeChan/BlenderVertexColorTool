import bpy
from bpy.types import Panel
import random
import time

from . import ops


class VertexColorTool(Panel):
    bl_idname = "VIEW_PT_Hollow_VertexColorTool"
    bl_label = "顶点色工具"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "顶点色"

    def draw(self, context):
        if context.active_object.type != "MESH":
            return

        # 手动模式
        layout = self.layout.column(align=True)
        layout.label(text="手动模式")
        # 颜色模式切换
        single = layout.row(align=True)
        single.prop(context.scene, "ho_VertexColorViewMode",
                    text="预览", toggle=True)
        single.prop(context.scene, "ho_GetVertexColorViewMode",
                    text="吸色模式", toggle=True)

        # 缓冲颜色绘制
        single = layout.row(align=True)

        change = single.operator(
            ops.setMeshVertexColor.bl_idname, text="", icon="GREASEPENCIL")
        change.color = context.scene.ho_PaintTempVertexColor  # 绘制缓冲色到面

        single.prop(context.scene, "ho_PaintTempVertexColor",
                    icon_only=True)  # 缓冲色

        single = layout.row(align=True)
        single.alignment = ("CENTER")
        change = single.operator(
            ops.changeTempVertexCol.bl_idname, text="", icon="EVENT_F")
        change.color = context.scene.ho_FrontTempVertexColor  # 切换为前景颜色

        change = single.operator(
            ops.changeTempVertexCol.bl_idname, text="", icon="EVENT_B")
        change.color = context.scene.ho_BackTempVertexColor  # 切换为背景颜色

        change = single.operator(
            ops.changeTempVertexCol.bl_idname, text="", icon="EVENT_R")
        seed = int(time.time()*10)
        random.seed(seed)  # 切换为随机颜色
        change.color = (random.random(), random.random(), random.random())

        single.operator(ops.addTempVertexCol.bl_idname,
                        text="", icon="ADD")  # 添加到缓存

        # 前后景色设置
        single = layout.row(align=True)

        single.prop(context.scene, "ho_FrontTempVertexColor", icon_only=True)
        single.prop(context.scene, "ho_BackTempVertexColor", icon_only=True)

        single = layout.row(align=True)
        single.alignment = ("CENTER")

        change = single.operator(
            ops.setMeshVertexColor.bl_idname, text="", icon="GREASEPENCIL")
        change.color = context.scene.ho_FrontTempVertexColor
        change = single.operator(
            ops.setMeshVertexColor.bl_idname, text="", icon="OUTLINER_DATA_GP_LAYER")
        change.color = context.scene.ho_BackTempVertexColor

        change = single.operator(
            ops.changeFBVertexCol.bl_idname, text="", icon="ARROW_LEFTRIGHT")
        change.switch = True
        change.refresh = False  # 交换前背景

        change = single.operator(
            ops.changeFBVertexCol.bl_idname, text="", icon="FILE_REFRESH")
        change.switch = False
        change.refresh = True  # 刷新前背景

        layout.separator()

        # 缓冲自设颜色
        vc = context.scene.ho_TempVertexColor
        if vc:
            layout.label(text="颜色组")
            col = layout.column(align=True)
            col.operator(ops.clearTempVertexCol.bl_idname,
                         text="", icon="TRASH")
            for i in range(len(vc[:])):
                # 每一行
                if not vc[i]:
                    break
                single = col.row(align=True)
                # 应用颜色到顶点色的按钮
                change = single.operator(
                    ops.setMeshVertexColor.bl_idname, text="", icon="GREASEPENCIL")
                change.color = vc[i].color

                # 颜色属性的按钮
                single.prop(data=vc[i], property="color", icon_only=True)

                # 删除颜色的按钮
                change = single.operator(
                    ops.removeTempVertexCol.bl_idname, text="", icon="TRASH")
                change.index = i

        # 预设模式
        layout = self.layout.column(align=True)
        layout.label(text="预设模式")
        single = layout.row(align=True)
        single.operator(ops.clearDefaultVertexCol.bl_idname,
                        text="", icon="TRASH")
        single.operator(ops.set1DefaultVertexCol.bl_idname,
                        text="", icon="EVENT_A")
        single.operator(ops.set2DefaultVertexCol.bl_idname,
                        text="", icon="EVENT_B")
        single.operator(ops.set3DefaultVertexCol.bl_idname,
                        text="", icon="EVENT_C")

        # 预设顶点颜色
        vc = context.scene.ho_VertexColorCol
        if vc:
            layout.label(text="预设组")
            layout = self.layout.column(align=True)
            col = layout.column(align=True)
            for i in range(len(vc[:])):
                # 每一行
                if not vc[i]:
                    break
                single = col.row(align=True)
                # 应用颜色到顶点色的按钮
                change = single.operator(
                    ops.setMeshVertexColor.bl_idname, text="", icon="GREASEPENCIL")
                change.color = vc[i].color

                # 颜色属性的按钮
                single.prop(data=vc[i], property="color", icon_only=True)

                # 刷新颜色的按钮
                change = single.operator(
                    ops.changeDefaultVertexCol.bl_idname, text="", icon="FILE_REFRESH")
                change.index = i
                change.color = ops.DEFAULT_COLOR_GROUP1[
                    i % len(ops.DEFAULT_COLOR_GROUP1)]
        # 工具类
        layout = self.layout.column(align=True)
        layout.label(text="工具")

        row = layout.row(align=True)
        row.prop(context.scene, "ho_isGroupPaintMode",
                 text="使用预设组", toggle=True)
        row.operator(
            ops.vertexGroup2DefaultVertexColor.bl_idname, text="顶点组赋颜色组", icon="FUND")
        row = layout.row(align=True)

        row.prop(context.scene, "ho_chooseSameVertexColorMeshThreshold", text="容差")
        o = row.operator(
            ops.chooseSameVertexColorMesh.bl_idname, text="选择同顶点色面", icon="SEQUENCE_COLOR_01")
        o.threshold = context.scene.ho_chooseSameVertexColorMeshThreshold

        layout.operator(
            ops.vertexGroup2RandomVertexColor.bl_idname, text="顶点组赋随机色")
        layout.operator(ops.vertexWeight2vertexColor.bl_idname,
                        text="权重到顶点色")

        # 顶点色层
        # ----绘制顶点色层面板----
        mesh = context.active_object.data
        layout = self.layout
        layout.label(text="顶点色列表")
        row = layout.row()

        col = row.column()
        col.template_list(
            "MESH_UL_color_attributes",
            "color_attributes",
            mesh,
            "color_attributes",
            mesh.color_attributes,
            "active_color_index",
            rows=3,
        )

        col = row.column(align=True)
        col.operator("geometry.color_attribute_add", icon='ADD', text="")
        col.operator("geometry.color_attribute_remove", icon='REMOVE', text="")

        col.separator()

        col.menu("MESH_MT_color_attribute_context_menu",
                 icon='DOWNARROW_HLT', text="")
        # ----层工具----
        mesh = context.object.data
        self.layout.label(text='合并通道')

        def draw_color_override(key):
            value = getattr(mesh, key)
            layout = self.layout
            if value in mesh.color_attributes and mesh.color_attributes[value].domain != 'CORNER':
                layout = self.layout.box()
                layout.label(
                    text='Only Face Corner attributes are supported', icon='ERROR')
            layout.prop_search(mesh, key, mesh, 'color_attributes')

        draw_color_override('ho_vertex_color_combine_0')
        draw_color_override('ho_vertex_color_combine_1')
        draw_color_override('ho_vertex_color_combine_2')
        draw_color_override('ho_vertex_color_combine_3')
        draw_color_override('ho_vertex_color_combine_tgt')

        layout = self.layout
        layout.operator(ops.vertexColorChannelCombine.bl_idname, text="合并到目标层")


cls = [VertexColorTool]


def register():
    bpy.types.Mesh.ho_vertex_color_combine_0 = bpy.props.StringProperty(
        name='R')
    bpy.types.Mesh.ho_vertex_color_combine_1 = bpy.props.StringProperty(
        name='G')
    bpy.types.Mesh.ho_vertex_color_combine_2 = bpy.props.StringProperty(
        name='B')
    bpy.types.Mesh.ho_vertex_color_combine_3 = bpy.props.StringProperty(
        name='A')
    bpy.types.Mesh.ho_vertex_color_combine_tgt = bpy.props.StringProperty(
        name='Target')

    try:
        for i in cls:
            bpy.utils.register_class(i)
    except Exception:
        print("Panel load failed!!!")


def unregister():
    for i in cls:
        bpy.utils.unregister_class(i)
