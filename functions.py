import bpy
import textwrap
from datetime import datetime

def create_postit(title, description, user, color, size, location=(0, 0, 0)):
    # Esci dalla modalità di modifica (Edit Mode) se necessario
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
    
    # Genera la data/ora corrente
    current_time = datetime.now().strftime("%H:%M %d/%m/%Y")

    # Suddividi la descrizione in segmenti
    description_segments = split_description(description)

    # Crea l'oggetto Post-it nella scena
    bpy.ops.mesh.primitive_cube_add(scale=(size, size, 0.01), location=location)
    postit_obj = bpy.context.object
    postit_obj.name = title

    # Aggiungi materiale per il colore
    material = bpy.data.materials.new(name="PostItMaterial")
    material.diffuse_color = (*color, 1.0)
    postit_obj.data.materials.append(material)

    # Verifica che l'oggetto creato sia il post-it e non un altro oggetto selezionato
    if postit_obj.data.materials:
        postit_obj.active_material = material

    # Assegna i dati come proprietà personalizzate
    postit_obj["postit_title"] = title
    postit_obj["postit_description"] = description_segments
    postit_obj["postit_user"] = user
    postit_obj["postit_datetime"] = current_time

    return postit_obj


def split_description(description, segment_length=26):
    """Divide la descrizione in segmenti di `segment_length` caratteri, cercando di non troncare le parole."""
    # Usa textwrap per suddividere il testo mantenendo le parole intatte
    return textwrap.wrap(description, width=segment_length)



''' Logica per calcolo postIT da implementare
import bmesh
from mathutils import Matrix

class MESH_OT_add_postit(bpy.types.Operator):
    bl_idname = "mesh.add_postit"
    bl_label = "Aggiungi Post-it"
    bl_description = "Aggiunge un post-it alla faccia selezionata"
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

        # Calcola l'area della faccia per determinare la dimensione del post-it
        area = face.calc_area()
        size = area ** 0.5  # Prendiamo la radice quadrata dell'area per ottenere la scala

        # Calcola la normale della faccia e crea una matrice di rotazione
        normal = face.normal
        up = (0, 0, 1)  # Assumiamo che la normale del post-it sia lungo l'asse Z
        rotation_matrix = normal.rotation_difference(up).to_matrix().to_4x4()

        # Esci dalla modalità Edit per creare il post-it come un nuovo oggetto
        bpy.ops.object.mode_set(mode='OBJECT')

        # Crea il post-it come un cubo con poco spessore
        bpy.ops.mesh.primitive_cube_add(scale=(size, size, 0.01), location=obj.matrix_world @ center)
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

def menu_func(self, context):
    layout = self.layout
    layout.operator("mesh.add_postit", text="Aggiungi Post-it", icon='FILE_TEXT')

def register():
    bpy.utils.register_class(MESH_OT_add_postit)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(MESH_OT_add_postit)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
'''