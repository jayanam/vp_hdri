import bpy
from bpy.types import Panel

class VP_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "VP HDRI"
    bl_category = "VP HDRI"
    
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('vp_hdri.vp_create_hdri', text='Create HDRI setup')

        row = layout.row()
        row.operator('vp_hdri.vp_remove_hdri', text='Remove HDRI setup')