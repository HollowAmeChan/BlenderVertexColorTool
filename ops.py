import time
import random
import mathutils
from bpy.types import Operator
import bpy
import bmesh


DEFAULT_COLOR_GROUP1 = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1),
    (1, 0.5, 0),
    (0, 1, 0.5),
    (0.5, 0, 1),
    (0.25, 0.75, 0.5),
    (0.5, 0.25, 0.75),
    (0.75, 0.5, 0.25)]
DEFAULT_COLOR_GROUP2 = [
    (0.051269, 0.025187, 0.025187),
    (0.21586, 0.095307, 0.095307),
    (1.0, 0.417885, 0.417885),
    (1.0, 0.672443, 0.376262),
    (0.98225, 1.0, 0.467784),
    (0.590618, 1.0, 0.520996),
    (0.327777, 0.921581, 1.0),
    (0.351532, 0.552011, 1.0),
    (0.508881, 0.445201, 1.0),
    (1.0, 0.564711, 1.0),
    (1.0, 0.76815, 1.0),
    (1.0, 0.879622, 1.0)]
DEFAULT_COLOR_GROUP3 = [
    (0, 0.005182, 0.008568),
    (0.0, 0.014444, 0.027321),
    (0.0, 0.049707, 0.107023),

    (0.025187, 0.064803, 0.177888),
    (0.254152, 0.08022, 0.274677),
    (0.502886, 0.08022, 0.278894),

    (1.0, 0.124771, 0.119538),
    (1.0, 0.23455, 0.030714),
    (1.0, 0.381326, 0.0),

    (1.0, 0.651405, 0.215861),
    (1.0, 0.814846, 0.527115),
    (1.0, 0.90466, 0.745404),
]

# 自建缓存颜色相关


class addTempVertexCol(Operator):
    """
    添加缓存颜色
    """
    bl_idname = "ho.addtempvertexcol"
    bl_label = "添加缓存颜色"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        color = context.scene.ho_PaintTempVertexColor
        vtx_color = context.scene.ho_TempVertexColor.add()
        vtx_color.color = color
        return {'FINISHED'}


class removeTempVertexCol(Operator):
    """
    删除缓存颜色
    """
    bl_idname = "ho.removetempvertexcol"
    bl_label = "删除缓存颜色"

    index: bpy.props.IntProperty()  # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        col = context.scene.ho_TempVertexColor
        col.remove(self.index)
        return {'FINISHED'}


class clearTempVertexCol(Operator):
    """
    清空缓冲颜色
    """
    bl_idname = "ho.cleartempvertexcol"
    bl_label = "清除缓冲颜色"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.scene.ho_TempVertexColor.clear()
        return {'FINISHED'}


class changeTempVertexCol(Operator):
    """
    改变缓存颜色
    """
    bl_idname = "ho.changetempvertexcol"
    bl_label = "改变缓存颜色"

    index: bpy.props.IntProperty()  # type: ignore
    color: bpy.props.FloatVectorProperty(size=3)  # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.scene.ho_PaintTempVertexColor = self.color
        return {'FINISHED'}


class changeFBVertexCol(Operator):
    """
    对前背景颜色进行操作
    """
    bl_idname = "ho.changefbvertexcol"
    bl_label = "对前背景颜色进行操作"

    switch: bpy.props.BoolProperty(default=False)  # type: ignore
    refresh: bpy.props.BoolProperty(default=False)  # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        if self.switch:
            temp = context.scene.ho_FrontTempVertexColor.copy()
            context.scene.ho_FrontTempVertexColor = context.scene.ho_BackTempVertexColor.copy()
            context.scene.ho_BackTempVertexColor = temp
            return {'FINISHED'}

        if self.refresh:
            context.scene.ho_FrontTempVertexColor = (1, 1, 1)
            context.scene.ho_BackTempVertexColor = (0, 0, 0)
            return {'FINISHED'}

        return {'FINISHED'}


# 预设顶点色组相关


class clearDefaultVertexCol(Operator):
    """
    清空预设颜色
    """
    bl_idname = "ho.cleardefaultvertexcol"
    bl_label = "清除预设颜色"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.scene.ho_GroupPaintDefaultIndex = 0
        context.scene.ho_VertexColorCol.clear()
        return {'FINISHED'}


class changeDefaultVertexCol(Operator):
    """
    改变预设颜色
    """
    bl_idname = "ho.changedefaultvertexcol"
    bl_label = "改变预设颜色"

    index: bpy.props.IntProperty()  # type: ignore
    color: bpy.props.FloatVectorProperty()  # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.scene.ho_VertexColorCol[self.index].color = self.color
        return {'FINISHED'}


class set1DefaultVertexCol(Operator):
    """
    创建预设一
    """
    bl_idname = "ho.set1defaultvertexcol"
    bl_label = "清除预设颜色"

    color_list: bpy.props.FloatVectorProperty()  # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.scene.ho_GroupPaintDefaultIndex = 1
        context.scene.ho_VertexColorCol.clear()
        for i in DEFAULT_COLOR_GROUP1:
            vtx_color = context.scene.ho_VertexColorCol.add()
            vtx_color.color = i

        return {'FINISHED'}


class set2DefaultVertexCol(Operator):
    """
    创建预设二
    """
    bl_idname = "ho.set2defaultvertexcol"
    bl_label = "清除预设颜色"

    color_list: bpy.props.FloatVectorProperty()  # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.scene.ho_GroupPaintDefaultIndex = 2
        context.scene.ho_VertexColorCol.clear()
        for i in DEFAULT_COLOR_GROUP2:
            vtx_color = context.scene.ho_VertexColorCol.add()
            vtx_color.color = i

        return {'FINISHED'}


class set3DefaultVertexCol(Operator):
    """
    创建预设三
    """
    bl_idname = "ho.set3defaultvertexcol"
    bl_label = "清除预设颜色"

    color_list: bpy.props.FloatVectorProperty()  # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.scene.ho_GroupPaintDefaultIndex = 3
        context.scene.ho_VertexColorCol.clear()
        for i in DEFAULT_COLOR_GROUP3:
            vtx_color = context.scene.ho_VertexColorCol.add()
            vtx_color.color = i

        return {'FINISHED'}

# 视图模式相关


class enterVertexColorView(Operator):
    """
    进入顶点色预览模式
    """
    bl_idname = "ho.entervertexcolorview"
    bl_label = "进入预览模式"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.scene.view_settings.view_transform = 'Standard'
        context.space_data.shading.color_type = 'VERTEX'
        context.space_data.shading.background_type = 'VIEWPORT'
        context.space_data.shading.light = 'FLAT'
        return {'FINISHED'}


class quitVertexColorView(Operator):
    """
    退出顶点色预览模式
    """
    bl_idname = "ho.quitvertexcolorview"
    bl_label = "从预览模式中退出"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.scene.ho_GetVertexColorViewMode = 0
        context.scene.view_settings.view_transform = 'Standard'
        context.space_data.overlay.show_overlays = True
        context.space_data.shading.light = 'STUDIO'
        context.space_data.shading.color_type = 'MATERIAL'
        context.space_data.shading.background_type = 'THEME'
        return {'FINISHED'}

# 工具操作


class setMeshVertexColor(Operator):
    """
    给选中网格指定顶点色
    """
    bl_idname = "ho.setmeshvertexcolor"
    bl_label = "给选中网格指定顶点色"

    color: bpy.props.FloatVectorProperty()  # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.paint.vertex_paint_toggle()
        context.object.data.use_paint_mask = True
        context.tool_settings.vertex_paint.brush = bpy.data.brushes['Draw']
        bpy.data.brushes["Draw"].color = self.color
        bpy.ops.paint.vertex_color_set()
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class chooseSameVertexColorMesh(Operator):
    """
    选择同种顶点色的网格
    """
    bl_idname = "ho.choosesamevertexcolormesh"
    bl_label = "选择同种顶点色的网格"

    threshold: bpy.props.FloatProperty(
        name="容差", description="选择同顶点色时的容差(通道共用容差)", default=0.01, max=1, min=0, step=0.01)  # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        threshold = self.threshold
        obj = bpy.context.object

        bpy.ops.object.mode_set(mode="OBJECT")

        colors = obj.data.vertex_colors.active.data
        selected_polygons = list(filter(lambda p: p.select, obj.data.polygons))

        if len(selected_polygons):
            p = selected_polygons[0]
            r = g = b = 0
            for i in p.loop_indices:
                c = colors[i].color
                r += c[0]
                g += c[1]
                b += c[2]
            r /= p.loop_total
            g /= p.loop_total
            b /= p.loop_total
            target = mathutils.Color((r, g, b))

            for p in obj.data.polygons:
                r = g = b = 0
                for i in p.loop_indices:
                    c = colors[i].color
                    r += c[0]
                    g += c[1]
                    b += c[2]
                r /= p.loop_total
                g /= p.loop_total
                b /= p.loop_total
                source = mathutils.Color((r, g, b))

                print(target, source)

                if (abs(source.r - target.r) < threshold and
                    abs(source.g - target.g) < threshold and
                        abs(source.b - target.b) < threshold):

                    p.select = True

        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class vertexGroup2RandomVertexColor(Operator):
    """
    给顶点组赋随机的顶点色
    """
    bl_idname = "ho.vertexgroup2randomvertexcolor"
    bl_label = "给顶点组赋随机的顶点色，只能为面组"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        obj = bpy.context.active_object
        # 获取所有顶点组
        vgroups = obj.vertex_groups
        bpy.ops.object.editmode_toggle()
        for i in range(len(vgroups)):
            selected_vgroup = vgroups[i]

            # 检查顶点组是否存在
            if selected_vgroup is not None:
                # 获取网格数据
                mesh = obj.data

                # 选择指定名称的顶点组所属的网格
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.vertex_group_set_active(
                    group=selected_vgroup.name)
                bpy.ops.object.vertex_group_select()
                bpy.ops.object.mode_set(mode='OBJECT')
                # 赋予颜色
                bpy.ops.paint.vertex_paint_toggle()
                bpy.context.object.data.use_paint_mask = True
                context.tool_settings.vertex_paint.brush = bpy.data.brushes['Draw']
                bpy.data.brushes["Draw"].color = (
                    random.random(), random.random(), random.random())
                bpy.ops.paint.vertex_color_set()
                bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class vertexGroup2DefaultVertexColor(Operator):
    """
    给顶点组赋指定组内的的颜色
    """
    bl_idname = "ho.vertexgroup2defaultvertexcolor"
    bl_label = "给顶点组赋指定组内的的颜色，只能为面组"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # 获取活动对象
        obj = bpy.context.active_object
        # 获取所有顶点组
        vgroups = obj.vertex_groups

        index = context.scene.ho_GroupPaintDefaultIndex
        mode = context.scene.ho_isGroupPaintMode

        if obj == None:
            return
        if mode == False:
            default_color = [
                i.color for i in context.scene.ho_TempVertexColor[:]]
        elif mode != False and index == 1:
            default_color = DEFAULT_COLOR_GROUP1
        elif mode != False and index == 2:
            default_color = DEFAULT_COLOR_GROUP2
        elif mode != False and index == 3:
            default_color = DEFAULT_COLOR_GROUP3
        else:
            default_color = DEFAULT_COLOR_GROUP1

        # 首先刷白此物体全部顶点色
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.paint.vertex_paint_toggle()
        bpy.context.object.data.use_paint_mask = True
        context.tool_settings.vertex_paint.brush = bpy.data.brushes['Draw']
        bpy.data.brushes["Draw"].color = (1, 1, 1)
        bpy.ops.paint.vertex_color_set()
        bpy.ops.object.editmode_toggle()
        # 逐顶点组操作
        bpy.ops.object.editmode_toggle()
        for i in range(len(vgroups)):
            selected_vgroup = vgroups[i]

            # 检查顶点组是否存在,颜色组是否存在
            if selected_vgroup is None:
                return {'FINISHED'}
            if len(default_color) == 0:
                return {'FINISHED'}
            # 选择指定名称的顶点组所属的网格
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.vertex_group_set_active(
                group=selected_vgroup.name)
            bpy.ops.object.vertex_group_select()
            bpy.ops.object.mode_set(mode='OBJECT')

            bpy.ops.paint.vertex_paint_toggle()
            bpy.context.object.data.use_paint_mask = True
            context.tool_settings.vertex_paint.brush = bpy.data.brushes['Draw']
            bpy.data.brushes["Draw"].color = default_color[i %
                                                           len(default_color)]
            bpy.ops.paint.vertex_color_set()
            bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class vertexWeight2vertexColor(Operator):
    """
    使用顶点权重绘制到顶点色
    """
    bl_idname = "ho.vertexweight2vertexcolor"
    bl_label = "使用选中的顶点组的权重，绘制到顶点色"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.paint.vertex_paint_toggle()
        bpy.ops.paint.vertex_color_from_weight()
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}


class vertexColorChannelCombine(Operator):
    """
    合并四个顶点色层到另一个顶点色层
    """
    bl_idname = "ho.vertexcolorchannelcombine"
    bl_label = "合并四个顶点色层到另一个顶点色层"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        mesh = bpy.context.active_object.data
        self.combine_vertexcolor_channel(
            mesh.ho_vertex_color_combine_0,
            mesh.ho_vertex_color_combine_1,
            mesh.ho_vertex_color_combine_2,
            mesh.ho_vertex_color_combine_3,
            mesh.ho_vertex_color_combine_tgt,
        )
        return {'FINISHED'}

    def combine_vertexcolor_channel(self, layerR, layerG, layerB, layerA, target):
        r = 0.0
        g = 0.0
        b = 0.0
        a = 1.0
        if layerR:
            atrR = bpy.context.active_object.data.color_attributes[layerR]
            itemsR = atrR.data.items()[:]
        if layerG:
            atrG = bpy.context.active_object.data.color_attributes[layerG]
            itemsG = atrG.data.items()[:]
        if layerB:
            atrB = bpy.context.active_object.data.color_attributes[layerB]
            itemsB = atrB.data.items()[:]
        if layerA:
            atrA = bpy.context.active_object.data.color_attributes[layerA]
            itemsA = atrA.data.items()[:]
        if target:
            atrTgt = bpy.context.active_object.data.color_attributes[target]
            itemsTgt = atrTgt.data.items()[:]
        if not target:
            return

        mesh = bpy.context.active_object.data
        for poly in mesh.polygons:
            for loop_index in poly.loop_indices:
                if layerR:
                    r = itemsR[loop_index][1].color_srgb[0]
                if layerG:
                    g = itemsG[loop_index][1].color_srgb[0]
                if layerB:
                    b = itemsB[loop_index][1].color_srgb[0]
                if layerA:
                    a = itemsA[loop_index][1].color_srgb[0]
                combined_color = (r, g, b, a)
                itemsTgt[loop_index][1].color_srgb = combined_color


cls = [addTempVertexCol, removeTempVertexCol,
       changeTempVertexCol, changeFBVertexCol,
       clearDefaultVertexCol, changeDefaultVertexCol,
       clearTempVertexCol,
       set1DefaultVertexCol,
       set2DefaultVertexCol,
       set3DefaultVertexCol,
       enterVertexColorView, quitVertexColorView,
       setMeshVertexColor, chooseSameVertexColorMesh,
       vertexGroup2RandomVertexColor, vertexGroup2DefaultVertexColor, vertexWeight2vertexColor,
       vertexColorChannelCombine]


def register():
    try:
        for i in cls:
            bpy.utils.register_class(i)
    except Exception:
        print("Ops load failed!!!")


def unregister():
    for i in cls:
        bpy.utils.unregister_class(i)
