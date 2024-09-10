import bpy
from bpy.app.handlers import persistent

bl_info = {
    "name": "Outliner Select ShowActive",
    "author": "sh",
    "version": (0, 1),
    "blender": (3, 6, 10),
    "location": "3D View > test addons > Outliner_ShowActive",
    "description": "select object focus outliner",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"
}

TEMP_NAME = ""

class Outliner_ShowActive(bpy.types.Panel):
    bl_label = "Outliner_ShowActive"
    bl_idname = "OBJECT_PT_outliner_showactive"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "test addons"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "osa_checkbox_bool", text="enable")
        layout.prop(context.scene, "osa_cc_checkbox_bool", text="close_collection")
            
        
@persistent
def selection_changes(scene):
    global TEMP_NAME

    if bpy.context.object.mode == 'EDIT':
        return
    
    if TEMP_NAME != bpy.context.selected_objects[0]:
        TEMP_NAME = bpy.context.selected_objects[0]
        if len(bpy.context.selected_objects) and bpy.context.scene.osa_checkbox_bool:
            override = None

            for area in bpy.context.screen.areas:
                if area.type == 'OUTLINER':
                    for region in area.regions:
                        if 'WINDOW' in region.type:
                            override = {'area': area, 'region': region}
                            break
                    break

            with bpy.context.temp_override(area = bpy.context.area):
                if bpy.context.scene.osa_cc_checkbox_bool:
                    bpy.ops.outliner.expanded_toggle(override)
                    bpy.ops.outliner.expanded_toggle(override)
                bpy.ops.outliner.show_active(override)


def register():
    bpy.types.Scene.osa_checkbox_bool = bpy.props.BoolProperty(name="OSA Checkbox Property", default=True)
    bpy.types.Scene.osa_cc_checkbox_bool = bpy.props.BoolProperty(name="OSA CC Checkbox Property", default=False)
    bpy.utils.register_class(Outliner_ShowActive)
    bpy.app.handlers.depsgraph_update_post.append(selection_changes)


def unregister():
    bpy.utils.unregister_class(Outliner_ShowActive)
    del bpy.types.Scene.osa_checkbox_bool
    del bpy.types.Scene.osa_cc_checkbox_bool
    bpy.app.handlers.depsgraph_update_post.remove(selection_changes)


if __name__ == "__main__":
    register()