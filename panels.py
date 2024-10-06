import bpy
from .functions import split_description

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

        layout.separator()
        
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
                    row = box.row(align=True)
                    row.label(text=f"{obj['postit_title'].upper()} :")
                    op = row.operator("object.view_postit", text="", icon='HIDE_OFF')
                    op.postit_name = obj.name
                    
                    #logica per la descrizione
                    description_lines = []
                    description = obj.get("postit_description", "")
                    if isinstance(description, list):
                        description = " ".join(description)
                    if isinstance(description, str):
                        description_lines = split_description(description)
                    for line in description_lines:
                        box.label(text=line)

                    box.label(text=f"Autore: {obj.get('postit_user', 'Sconosciuto')}", icon='USER')
                    box.label(text=f"Data: {obj.get('postit_datetime', 'N/A')}", icon='TIME')
                    box.operator("object.edit_postit", text="Modifica", icon='GREASEPENCIL').postit_name = obj.name
                    box.operator("object.delete_postit", text="Elimina", icon='TRASH').postit_name = obj.name
                    col.separator()

class MESH_MT_add_postit(bpy.types.Menu):
    bl_idname = "MESH_MT_add_postit"
    bl_label = "Aggiungi Post-it"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.create_postit", text="Aggiungi Post-It")
        layout.operator("mesh.create_postit_face", text="Aggiungi Post-It su questa faccia")

def menu_func(self, context):
    self.layout.menu(MESH_MT_add_postit.bl_idname)