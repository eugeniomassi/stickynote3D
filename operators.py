import bpy
import bmesh
from mathutils import Matrix, Vector
from datetime import datetime
from .functions import split_description, create_postit

class CreatePostItOperator(bpy.types.Operator):
    """Crea un nuovo Post-it"""
    bl_idname = "object.create_postit"
    bl_label = "Crea e Modifica Post-it"

    title: bpy.props.StringProperty(name="Titolo", default="Nuovo Titolo")
    description: bpy.props.StringProperty(name="Descrizione", default="Nuova Descrizione", options={'TEXTEDIT_UPDATE'}, maxlen=512)
    user: bpy.props.StringProperty(name="Autore", default="Utente")
    color: bpy.props.FloatVectorProperty(name="Colore", subtype='COLOR', default=(1.0, 1.0, 0.0), min=0.0, max=1.0)
    size: bpy.props.FloatProperty(name="Dimensione", default=1.0, min=0.1, max=10.0)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def execute(self, context):
        # Chiamata alla funzione per creare il Post-it
        create_postit(
            title=self.title,
            description=self.description,
            user=self.user,
            color=self.color,
            size=self.size,
            location=(0, 0, 0)
        )
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
        # Ottieni l'oggetto attivo e la faccia selezionata
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        selected_faces = [f for f in bm.faces if f.select]
        face = selected_faces[0]  # Assumendo che ci sia solo una faccia selezionata

        # Calcola il centro della faccia
        center = face.calc_center_median()

        # Calcola la normale della faccia
        normal = face.normal

        # Ottieni tre vertici della faccia selezionata per il calcolo della rotazione
        verts = [v.co for v in face.verts]
        if len(verts) >= 3:
            edge1 = (verts[1] - verts[0]).normalized()
            edge2 = (verts[2] - verts[0]).normalized()
            tangent = edge1.cross(normal).normalized()

            # Crea una matrice di rotazione basata sulla normale della faccia
            rotation_matrix = Matrix((tangent, edge1, normal)).transposed().to_4x4()
        else:
            rotation_matrix = Matrix.Identity(4)

        # Esci dalla modalità Edit per creare il post-it come un nuovo oggetto
        bpy.ops.object.mode_set(mode='OBJECT')

        # Crea il post-it come un cubo sottile
        bpy.ops.mesh.primitive_cube_add(scale=(0.5, 0.5, 0.01), location=obj.matrix_world @ center)
        postit_obj = bpy.context.object
        postit_obj.name = "Post-it"

        # Allinea il post-it alla faccia selezionata
        postit_obj.matrix_world = obj.matrix_world @ rotation_matrix
        postit_obj.location = obj.matrix_world @ center

        # Aggiungi materiale per il colore
        material = bpy.data.materials.new(name="PostItMaterial")
        material.diffuse_color = (1.0, 1.0, 0.0, 1.0)  # Colore giallo
        postit_obj.data.materials.append(material)

        # Ritorna alla modalità Edit
        bpy.ops.object.mode_set(mode='EDIT')

        self.report({'INFO'}, "Post-it 3D aggiunto al centro della faccia e allineato")
        return {'FINISHED'}
    
class EditPostItOperator(bpy.types.Operator):
    """Modifica i dati di un Post-it"""
    bl_idname = "object.edit_postit"
    bl_label = "Modifica Post-it"

    postit_name: bpy.props.StringProperty()

    new_title: bpy.props.StringProperty(name="Titolo")
    new_description: bpy.props.StringProperty(name="Descrizione")
    new_user: bpy.props.StringProperty(name="Utente")

    def invoke(self, context, event):
        obj = bpy.data.objects.get(self.postit_name)
        if obj:
            self.new_title = obj["postit_title"]
            self.new_description = ''.join(obj["postit_description"])  # Riunisce i segmenti per la modifica
            self.new_user = obj["postit_user"]
            return context.window_manager.invoke_props_dialog(self)
        return {'CANCELLED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "new_title", text="Titolo")
        layout.prop(self, "new_description", text="Descrizione")
        layout.prop(self, "new_user", text="Utente")

    def execute(self, context):
        obj = bpy.data.objects.get(self.postit_name)
        if obj:
            # Divide la descrizione in segmenti
            description_segments = split_description(self.new_description)

            # Aggiorna i dati del Post-it
            obj["postit_title"] = self.new_title
            obj["postit_description"] = description_segments
            obj["postit_user"] = self.new_user
            current_time = datetime.now().strftime("%H:%M %d/%m/%Y")
            obj["postit_datetime"] = current_time
            
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