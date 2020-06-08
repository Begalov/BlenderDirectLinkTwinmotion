# todo: 
#   link operator
#   reset to factory operator
#   i18n
#   logo if needed
# author: 
# start: 200606

bl_info = {
    "name": "Twinmotion DirectLink",
    "author": "RUben Begalov@gmail.com",
    "version": (0, 1, 0),
    "blender": (2, 82, 0),
    "location": "Properties > Scene > Twinmotion DirectLink",
    "description": "Blender Direct Link to Twinmotion.",
    "warning": "UI blank for future addon.",
    "wiki_url": "https://twinmotionhelp.epicgames.com/",
    "tracker_url": "https://github.com/Begalov/BlenderDirectLinkTwinmotion/issues",
    "support": "COMMUNITY",
    "category": "Import-Export",
}

import bpy
from bpy.props import EnumProperty, BoolProperty, FloatProperty, IntProperty
from bpy.types import Panel, PropertyGroup, Operator


class TM_PG_Scene(bpy.types.PropertyGroup):
    collapse: EnumProperty(
        name = "Collapse objects",
        items = [
            ("NONE", "None", "Do not collapse"),
            ("MATE", "Meterial", "Collapse objects by material")
        ],
        description = 'Collapse scene objects.',
        default = 'NONE'
    )
    
    exclude: BoolProperty(
        name = "Exclude objects smaller than",
        default = True
    )
    
    exclude_size: FloatProperty(
        #name = "Size excluding objects",
        name = "Meter",
        default = 0.1
    )
    
    optimize: BoolProperty(name = "Optimize Model")
    
    fix: BoolProperty(name = "Fix UV/Texture")
    
    port: IntProperty(
        name = "Communication port",
        default = -1
        )


class TM_OP_DirectLink(bpy.types.Operator):
    """Twinmotion Direct Link renderable objects from curent scene.."""
    bl_idname = "scene.twinmotion_directlink"
    bl_label = "Link"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        return {'FINISHED'}


class TM_OP_ResetToFactory(bpy.types.Operator):
    """Twinmotion Direct Link settings reset to factory."""
    bl_idname = "scene.twinmotion_reset"
    bl_label = "Reset to Factory"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        return {'FINISHED'}

class TM_PT_PanelBase():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"


class TM_PT_Panel(TM_PT_PanelBase, Panel):
    """Twinmotion main panel."""
    bl_label = "Twinmotion Direct Link"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Link renderable objects from curent scene.")

        row = layout.row()
        row.operator("scene.twinmotion_directlink", icon = "HIDE_OFF")
        row.operator("wm.url_open", text="Online Help", icon='HELP').url = "https://twinmotionhelp.epicgames.com/"
        
        
class TM_PT_PanelSettings(TM_PT_PanelBase, Panel):
    bl_label = "Settings"
    bl_parent_id = "TM_PT_Panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        #layout.use_property_split = True
        #layout.alignment = 'LEFT'
        layout.use_property_decorate = False  # No animation.

        TM = context.scene.TwinmotionDirectLink
        
        col = layout.column()#align=True
        col.prop(TM, "collapse")
        
        box = layout.box()
        box.label(text="Optimization")
        box.prop(TM, "exclude", expand = False)
        box.prop(TM, "exclude_size", expand = False)
        box.prop(TM, "optimize")
        box.prop(TM, "fix")
        
        box = layout.box()
        box.label(text="Connection options")
        box.prop(TM, "port")
           
        row = layout.row()        
        row.label(text="V2020.1.1.0")
        row.operator("scene.twinmotion_reset", icon = "LOOP_BACK")
        
classes = (
    TM_PG_Scene,
    TM_OP_DirectLink,
    TM_OP_ResetToFactory,
    TM_PT_Panel,
    TM_PT_PanelSettings,
    )
    
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    bpy.types.Scene.TwinmotionDirectLink = bpy.props.PointerProperty(type = TM_PG_Scene)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
        
    del(bpy.types.Scene.TwinmotionDirectLink)

if __name__ == "__main__":
    register()