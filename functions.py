import bpy
import textwrap
from datetime import datetime

import bpy

def create_postit(context, title, description, user, color, size, location, rotation=None):
    # Crea l'oggetto Post-it come un cubo sottile
    bpy.ops.mesh.primitive_cube_add(scale=(size, size, 0.01), location=location)
    postit_obj = bpy.context.object
    postit_obj.name = title

    # Aggiungi materiale per il colore
    material = bpy.data.materials.new(name="PostItMaterial")
    material.diffuse_color = (*color, 1.0)
    postit_obj.data.materials.append(material)

    # Applica la rotazione se fornita
    if rotation:
        postit_obj.rotation_euler = rotation

    # Assegna i dati come proprietà personalizzate
    postit_obj["postit_title"] = title
    postit_obj["postit_description"] = description
    postit_obj["postit_user"] = user
    postit_obj["postit_datetime"] = datetime.now().strftime("%H:%M %d/%m/%Y")

    return postit_obj

def split_description(description, segment_length=26):
    """Divide la descrizione in segmenti di `segment_length` caratteri, cercando di non troncare le parole."""
    # Usa textwrap per suddividere il testo mantenendo le parole intatte
    return textwrap.wrap(description, width=segment_length)