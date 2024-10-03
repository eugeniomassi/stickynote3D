import bpy
import bmesh
from mathutils import Matrix, Vector
from datetime import datetime
from .functions import create_postit

class CreatePostItOperator(bpy.types.Operator):
    bl_idname = "object.create_postit"
    bl_label = "Crea e Modifica Post-it"

    title: bpy.props.StringProperty(name="Titolo", default="Nuovo Titolo")
    description: bpy.props.StringProperty(name="Descrizione", default="Nuova Descrizione")
    user: bpy.props.StringProperty(name="Autore", default="Utente")
    color: bpy.props.FloatVectorProperty(name="Colore", subtype='COLOR', default=(1.0, 1.0, 0.0), min=0.0, max=1.0)
    size: bpy.props.FloatProperty(name="Dimensione", default=1.0, min=0.1, max=10.0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def execute(self, context):
        location = (0, 0, 0)
        create_postit(context, self.title, self.description, self.user, self.color, self.size, location)
        return {'FINISHED'}

class CreatePostItFaceSelectedOperator(bpy.types.Operator):
    bl_idname = "mesh.create_postit_face"
    bl_label = "Crea Post-it su Faccia Selezionata"
    bl_description = "Aggiunge un Post-it sulla faccia selezionata"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if obj and obj.type == 'MESH' and context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(obj.data)
            selected_faces = [f for f in bm.faces if f.select]
            return len(selected_faces) == 1
        return False

    def execute(self, context):
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        selected_faces = [f for f in bm.faces if f.select]
        face = selected_faces[0]

        center = face.calc_center_median()
        normal = face.normal
        size = face.calc_area() ** 0.5

        rotation_matrix = normal.to_track_quat('Z', 'Y').to_euler()

        bpy.ops.object.mode_set(mode='OBJECT')

        title = "Titolo"
        description = "Descrizione del Post-it"
        user = "Utente"
        color = (1.0, 1.0, 0.0)

        # Crea il Post-it
        create_postit(context, title, description, user, color, size, obj.matrix_world @ center, rotation_matrix)
        return {'FINISHED'}
    
class EditPostItOperator(bpy.types.Operator):
    """Modifica i dati di un Post-it"""
    bl_idname = "object.edit_postit"
    bl_label = "Modifica Post-it"

    postit_name: bpy.props.StringProperty()

    new_title: bpy.props.StringProperty(name="Titolo")
    new_description: bpy.props.StringProperty(name="Descrizione")
    new_user: bpy.props.StringProperty(name="Utente")
    new_color: bpy.props.FloatVectorProperty(name="Colore", subtype='COLOR', default=(1.0, 1.0, 0.0), min=0.0, max=1.0)

    def invoke(self, context, event):
        obj = bpy.data.objects.get(self.postit_name)
        if obj:
            self.new_title = obj["postit_title"]

            description = obj["postit_description"]
            if isinstance(description, list):
                description = " ".join(description)
            self.new_description = description
            
            self.new_user = obj["postit_user"]
            if obj.active_material and obj.active_material.diffuse_color:
                self.new_color = obj.active_material.diffuse_color[:3]
            return context.window_manager.invoke_props_dialog(self)
        return {'CANCELLED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "new_title", text="Titolo")
        layout.prop(self, "new_description", text="Descrizione")
        layout.prop(self, "new_user", text="Utente")
        layout.prop(self, "new_color", text="Colore")

    def execute(self, context):
        obj = bpy.data.objects.get(self.postit_name)
        if obj:
            # Aggiorna i dati del Post-it
            obj["postit_title"] = self.new_title
            obj["postit_description"] = self.new_description
            obj["postit_user"] = self.new_user
            obj["postit_datetime"] = datetime.now().strftime("%H:%M %d/%m/%Y")
            
            if obj.active_material:
                obj.active_material.diffuse_color = (*self.new_color, 1.0)
            else:
                material = bpy.data.materials.new(name="PostItMaterial")
                material.diffuse_color = (*self.new_color, 1.0)
                obj.data.materials.append(material)
            
            return {'FINISHED'}
        return {'CANCELLED'}

class SelectPostItOperator(bpy.types.Operator):
    """Seleziona un Post-it"""
    bl_idname = "object.select_postit"
    bl_label = "Seleziona Post-it"

    postit_name: bpy.props.StringProperty()

    def execute(self, context):
        obj = bpy.data.objects.get(self.postit_name)
        if obj:
            context.view_layer.objects.active = obj
            return {'FINISHED'}
        return {'CANCELLED'}

class DeletePostItOperator(bpy.types.Operator):
    """Elimina il Post-it selezionato"""
    bl_idname = "object.delete_postit"
    bl_label = "Elimina Post-it"
    
    postit_name: bpy.props.StringProperty()
    
    def execute(self, context):
        obj = bpy.data.objects.get(self.postit_name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)
            return {'FINISHED'}
        return {'CANCELLED'}
    
class ViewPostItOperator(bpy.types.Operator):
    """Seleziona un Post-it e centra la vista su di esso"""
    bl_idname = "object.view_postit"
    bl_label = "Seleziona Post-it e centra la vista"

    postit_name: bpy.props.StringProperty()

    def execute(self, context):
        obj = bpy.data.objects.get(self.postit_name)
        if obj:
            # Seleziona l'oggetto Post-it
            context.view_layer.objects.active = obj
            obj.select_set(True)

            # Centra la vista su di esso
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    space = area.spaces.active
                    region_3d = space.region_3d

                    # Posiziona la visuale sul Post-it
                    region_3d.view_location = obj.location
                    region_3d.view_rotation = obj.rotation_euler.to_quaternion()

            return {'FINISHED'}
        return {'CANCELLED'}