import os

path = "/home/andrew/Downloads/Morrowind-BSA"

for root, dirs, files in os.walk(path):
  for f in files:
    if f.endswith('.nif'):
      mesh_file = os.path.join(root, f)
      obj_file = os.path.splitext(mesh_file)[0] + ".obj"
      bpy.ops.object.select_all(action='SELECT')
      bpy.ops.object.delete()
      try:
        print("Converting {}...".format(mesh_file))
        bpy.ops.import_scene.nif(filepath=mesh_file)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.export_scene.obj(filepath=obj_file)
      except Exception as e:
        print("Corrupted NIF file: {}".format(mesh_file))
