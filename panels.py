import bpy

class PostItPanel(bpy.types.Panel):
    """Pannello per gestire i Post-it nella scena"""
    bl_label = "Post-It Manager"
    bl_idname = "OBJECT_PT_postit_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Post-It"

    def draw(self, context):
        layout = self.layout

        # Pulsante per aggiungere un nuovo Post-it con un'icona
        layout.operator("object.create_postit", text="Aggiungi Post-it", icon='ADD')

        layout.separator()  # Aggiunge uno spazio di separazione
        
        # Ordina i Post-it in base alla data di modifica
        sorted_objects = sorted(bpy.data.objects, key=lambda obj: obj.get("postit_datetime", ""), reverse=True)

        # Visualizza la lista di tutti i Post-it nella scena
        col = layout.column()
        for obj in sorted_objects:
            if "postit_title" in obj.keys():
                row = col.row()
                op = row.operator("object.select_postit", text=obj["postit_title"], icon='FILE_TEXT')
                op.postit_name = obj.name
                col.separator()

                # Se l'oggetto è selezionato, mostra i dettagli
                if context.object == obj:
                    box = col.box()
                    box.label(text=f"{obj['postit_title'].upper()}")

                    # Visualizza ogni segmento di descrizione come un'etichetta separata
                    for line in obj["postit_description"]:
                        box.label(text=line)

                    box.label(text=f"{obj['postit_user']}", icon='USER')
                    box.label(text=f"{obj['postit_datetime']}", icon='TIME')
                    box.operator("object.edit_postit", text="Modifica", icon='GREASEPENCIL').postit_name = obj.name
                    box.operator("object.delete_postit", text="Elimina Post-it", icon='TRASH').postit_name = obj.name
                    col.separator()

class MESH_MT_add_postit(bpy.types.Menu):
    bl_idname = "MESH_MT_add_postit"
    bl_label = "Aggiungi Post-it"

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.create_postit_face", text="Aggiungi Post-it su Faccia Selezionata")

def menu_func(self, context):
    self.layout.menu(MESH_MT_add_postit.bl_idname)
'''
    def execute(self, context):
        # Recupera l'oggetto attivo e la BMesh
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)

        # Recupera la faccia selezionata
        selected_face = [f for f in bm.faces if f.select][0]

        # Calcola il centro della faccia e la normale PRIMA di uscire dalla modalità di modifica
        face_center = selected_face.calc_center_median()
        normal = selected_face.normal

        # Calcola l'area della faccia selezionata
        face_area = selected_face.calc_area()

        # Supponiamo che la dimensione standard di un post-it sia 0.076 metri (7,6 cm)
        # Qui lo scaleremo in base all'area della faccia.
        # Se la faccia è più grande o più piccola, il post-it si adatterà.
        base_postit_size = 0.076  # Dimensione base di un post-it
        size = (face_area ** 0.5)  # Proporzioniamo il post-it all'area della faccia

        # Evitiamo che il post-it diventi troppo grande o troppo piccolo
        size = max(base_postit_size * 0.5, min(size, base_postit_size * 2))

        # Uscire dalla modalità di modifica per evitare conflitti durante la creazione dell'oggetto
        bpy.ops.object.mode_set(mode='OBJECT')

        # Allinea il post-it con la normale della faccia
        up = bpy.context.scene.cursor.rotation_euler.to_matrix().col[2]  # Vettore "up" del piano
        axis = up.cross(normal)
        angle = up.angle(normal)
        rot_mat = Matrix.Rotation(angle, 4, axis)

        # Dettagli del post-it
        title = "Post-it"
        description = "Questa è una nota di esempio"
        user = "Utente"
        color = (1.0, 1.0, 0.0)  # Giallo tipico di un post-it

        # Crea il post-it usando la funzione già esistente
        postit_obj = create_postit(title, description, user, color, size, location=face_center)

        # Applica la rotazione per allinearlo alla faccia
        postit_obj.matrix_world = rot_mat @ postit_obj.matrix_world

        # Feedback
        self.report({'INFO'}, "Post-it aggiunto con successo")
        return {'FINISHED'}
'''