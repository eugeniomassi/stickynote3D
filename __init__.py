import bpy
from .operators import CreatePostItOperator, EditPostItOperator, SelectPostItOperator, DeletePostItOperator, CreatePostItFaceSelectedOperator, ViewPostItOperator
from .panels import PostItPanel, MESH_MT_add_postit, menu_func

bl_info = {
    "name": "StickyNotes 3D",
    "blender": (4, 0, 0),
    "category": "Object",
    "author": "Eugenio Massi",
    "version": (1, 0, 8),
    "description": "A plugin to manage 3D sticky notes in Blender",
}

def register():
    #operators
    bpy.utils.register_class(CreatePostItOperator)
    bpy.utils.register_class(CreatePostItFaceSelectedOperator)
    bpy.utils.register_class(EditPostItOperator)
    bpy.utils.register_class(SelectPostItOperator)
    bpy.utils.register_class(DeletePostItOperator)
    bpy.utils.register_class(ViewPostItOperator)
    #panels
    bpy.utils.register_class(PostItPanel)
    bpy.utils.register_class(MESH_MT_add_postit)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    #operators
    bpy.utils.unregister_class(CreatePostItOperator)
    bpy.utils.unregister_class(CreatePostItFaceSelectedOperator)
    bpy.utils.unregister_class(EditPostItOperator)
    bpy.utils.unregister_class(SelectPostItOperator)
    bpy.utils.unregister_class(DeletePostItOperator)
    bpy.utils.unregister_class(ViewPostItOperator)
    #panels
    bpy.utils.unregister_class(PostItPanel)
    bpy.utils.unregister_class(MESH_MT_add_postit)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
