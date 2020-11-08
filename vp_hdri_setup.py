import bpy
from bpy.types import Operator

from . vp_utils import *

class VP_OT_Create_HDRI_Operator(Operator):
    bl_idname = "vp_hdri.vp_create_hdri"
    bl_label = "Create HDRI Setup"
    bl_description = "Creates a node setup with HDRI from viewport" 
    bl_options = {'REGISTER', 'UNDO'} 

    def invoke(self, context, event):
        remove_nodes_from_world()
        add_nodes_to_world(context.space_data)
        return {'FINISHED'}

class VP_OT_Remove_HDRI_Operator(Operator):
    bl_idname = "vp_hdri.vp_remove_hdri"
    bl_label = "Remove HDRI Setup"
    bl_description = "Removes an HDRI setup if exists" 
    bl_options = {'REGISTER', 'UNDO'} 

    def invoke(self, context, event):
        remove_nodes_from_world()
        return {'FINISHED'}