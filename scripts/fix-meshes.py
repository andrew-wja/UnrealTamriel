import os
import bpy

path = "D:\\UnrealTamriel\\Data\\meshes\\x"

for root, dirs, files in os.walk(path):
  for f in files:
    if f.endswith('hlaalu_b_17.nif'):
      mesh_file = os.path.join(root, f)
      out_file = os.path.join("D:\\UnrealTamriel\\Data\\meshes\\x\\output",f)
      if bpy.context.object:
          bpy.ops.object.mode_set(mode='OBJECT')
      bpy.ops.object.select_all(action='SELECT')
      bpy.ops.object.delete()
      for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
            
      for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

      for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

      for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)
      try:
        if True:
            print("Converting {}...".format(mesh_file))
            bpy.ops.import_scene.mw(filepath=mesh_file)
            bpy.ops.object.select_all(action='DESELECT')
            
            if True and any(obj for obj in bpy.data.objects if obj.name.startswith('Tri Tri Tri')):
                print('Mesh with invalid start node found: {}', f)
                
                rootTri = next((obj for obj in bpy.data.objects if obj.name.startswith('Tri Ex')), None)
                incorrectRootTri = next((obj for obj in bpy.data.objects if obj.name.startswith('Tri Tri Ex')), None)
                sceneRoot = next((obj for obj in bpy.data.objects if obj.name.startswith('Ex')), None)
                
                print('current rootTri: {}:', rootTri)
                print('incorrect rootTri: {}:', incorrectRootTri)
                print('sceneRoot: {}', sceneRoot)
                
                for obj in incorrectRootTri.children:
                    obj.parent = rootTri
                
                bpy.ops.object.select_all(action='DESELECT')
                incorrectRootTri.select_set(True)
                bpy.ops.object.delete()
            
            if False:
                print('Attempting to merge meshes')
                for obj in bpy.data.objects:
                    if obj.name.startswith('Tri'):
                        obj.select_set(True)
                        if obj.name.endswith('0'):
                            bpy.context.view_layer.objects.active = obj
                        
                bpy.ops.object.join()
                
                if False:
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.ops.object.bake_image()
                    for obj in bpy.data.meshes:
                        if obj.name.startswith('Tri') and obj.name.endswith('0'):
                            print("Processing mesh: {}".obj.name)
                
                bpy.ops.export_scene.mw(filepath=out_file)
      except Exception as e:
        print("Corrupted NIF file: {}".format(mesh_file))
        print(e)
