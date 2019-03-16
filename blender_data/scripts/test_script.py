import bpy
from mathutils import Vector

C= bpy.context
d = C.collection.objects
cube = d["Cube"]
cube.location = Vector((0.0, 0.0, 4.0))
cube.dimensions = Vector((1.0, 1.0, 3.0))
print(">>>>", cube.name)