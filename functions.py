import bpy
import textwrap
from datetime import datetime

import bpy

def create_postit(context, title, description, user, color, size, location, rotation=None):
    
    bpy.ops.mesh.primitive_cube_add(scale=(size, size, 0.05), location=location)
    postit_obj = bpy.context.object
    postit_obj.name = title

    material = bpy.data.materials.new(name="PostItMaterial")
    material.diffuse_color = (*color, 1.0)
    postit_obj.data.materials.append(material)
    if rotation:
        postit_obj.rotation_euler = rotation

    postit_obj["postit_title"] = title
    postit_obj["postit_description"] = description
    postit_obj["postit_user"] = user
    postit_obj["postit_datetime"] = datetime.now().strftime("%H:%M %d/%m/%Y")

    postit_obj.hide_render = True

    return postit_obj

def split_description(description, segment_length=26):
    """Divide la descrizione in segmenti di `segment_length` caratteri, cercando di non troncare le parole."""
    # Usa textwrap per suddividere il testo mantenendo le parole intatte
    return textwrap.wrap(description, width=segment_length)