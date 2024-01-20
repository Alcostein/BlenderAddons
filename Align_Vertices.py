bl_info = {
    "name": "Align Vertices",
    "blender": (4, 0, 0),
    "category": "Object",
}

import bpy
import bmesh

class SetVertexPosition(bpy.types.Operator):
    """Align Vertices to Reference"""
    bl_idname = "object.align_vertices"
    bl_label = "Align Vertices"
    bl_options = {'UNDO'}

    align_x: bpy.props.BoolProperty(name="X", default=True)
    align_y: bpy.props.BoolProperty(name="Y", default=False)
    align_z: bpy.props.BoolProperty(name="Z", default=False)
    
    def execute(self, context):
        # Access properties from the scene
        align_x = context.scene.align_vertices_x
        align_y = context.scene.align_vertices_y
        align_z = context.scene.align_vertices_z
        
        self.set_vertex_to_reference(context, align_x, align_y, align_z)
        return {'FINISHED'}

    def set_vertex_to_reference(self, context, align_x, align_y, align_z):
        obj = context.edit_object
        bm = bmesh.from_edit_mesh(obj.data)
        selected_verts = [v for v in bm.verts if v.select]

        if not selected_verts:
            self.report({'WARNING'}, "No vertices selected.")
            return

        reference_vertex = bm.select_history.active
        if not isinstance(reference_vertex, bmesh.types.BMVert):
            self.report({'WARNING'}, "No reference vertex selected.")
            return

        ref_vertex = reference_vertex.co.copy()

        for vert in selected_verts:
            if vert != reference_vertex:
                if align_x:
                    vert.co.x = ref_vertex.x
                if align_y:
                    vert.co.y = ref_vertex.y
                if align_z:
                    vert.co.z = ref_vertex.z

        bmesh.update_edit_mesh(obj.data)

class VIEW3D_PT_AlignVertices(bpy.types.Panel):
    bl_label = "Align Vertices"
    bl_idname = "VIEW3D_PT_align_vertices"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Edit'

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        layout.prop(scn, 'align_vertices_x')
        layout.prop(scn, 'align_vertices_y')
        layout.prop(scn, 'align_vertices_z')

        layout.operator(SetVertexPosition.bl_idname)

def register():
    bpy.utils.register_class(SetVertexPosition)
    bpy.utils.register_class(VIEW3D_PT_AlignVertices)
    
    bpy.types.Scene.align_vertices_x = bpy.props.BoolProperty(name="Align X Axis")
    bpy.types.Scene.align_vertices_y = bpy.props.BoolProperty(name="Align Y Axis")
    bpy.types.Scene.align_vertices_z = bpy.props.BoolProperty(name="Align Z Axis")

def unregister():
    bpy.utils.unregister_class(SetVertexPosition)
    bpy.utils.unregister_class(VIEW3D_PT_AlignVertices)
    
    del bpy.types.Scene.align_vertices_x
    del bpy.types.Scene.align_vertices_y
    del bpy.types.Scene.align_vertices_z


if __name__ == "__main__":
    register()
