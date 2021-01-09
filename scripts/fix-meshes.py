import os
import bpy

path = "D:\\UnrealTamriel\\Data\\meshes\\x"

for root, dirs, files in os.walk(path):
  for f in files:
    if f.endswith('hlaalu_b_17.nif'):
      mesh_file = os.path.join(root, f)
      out_file = os.path.join("D:\\UnrealTamriel\\Data\\meshes\\x\\output",f)
      fbx_out = out_file + '.fbx'
      
      export_fbx = True
      
      if bpy.context.object:
          bpy.ops.object.mode_set(mode='OBJECT')
      bpy.ops.object.select_all(action='SELECT')
      bpy.ops.object.delete()
      for block in bpy.data.meshes:
            bpy.data.meshes.remove(block)
            
      for block in bpy.data.materials:
            bpy.data.materials.remove(block)

      for block in bpy.data.textures:
            bpy.data.textures.remove(block)

      for block in bpy.data.images:
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
            
            if True:
                print('Attempting to merge meshes')
                for obj in bpy.data.objects:
                    if obj.name.startswith('Tri'):
                        obj.select_set(True)
                        if obj.name.endswith('0'):
                            bpy.context.view_layer.objects.active = obj
                        
                bpy.ops.object.join()
                
                
                if True:
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.scene.render.engine = 'CYCLES'
                    
                    rootTri = next((obj for obj in bpy.data.objects if obj.name.startswith('Tri Ex')), None)
                    rootTri.children[0].select_set(True)
                    
                    obj = bpy.context.active_object
                    print('Selected: {}', obj.name)
                    print('Selected Type: {}', obj.type)
                    
                    # You can choose your texture size (This will be the de bake image)
                    image_name = obj.name + '_BakedTexture'
                    img = bpy.data.images.new(image_name,1024,1024)
                    
                    #Due to the presence of any multiple materials, it seems necessary to iterate on all the materials, and assign them a node + the image to bake.
                    for mat in obj.data.materials:
                        print('adding node to material: {}', mat.name)
                        mat.use_nodes = True #Here it is assumed that the materials have been created with nodes, otherwise it would not be possible to assign a node for the Bake, so this step is a bit useless
                        nodes = mat.node_tree.nodes
                        texture_node = nodes.new('ShaderNodeTexImage')
                        texture_node.name = 'Bake_node'
                        texture_node.select = True
                        nodes.active = texture_node
                        texture_node.image = img #Assign the image to the node
                        
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.bake(type='DIFFUSE', save_mode='EXTERNAL')

                    img.save_render(filepath='C:\\TEMP\\baked.png')
                        
                    #In the last step, we are going to delete the nodes we created earlier
                    for mat in obj.data.materials:
                        for n in mat.node_tree.nodes:
                            if n.name == 'Bake_node':
                                mat.node_tree.nodes.remove(n)
                        
                
                bpy.ops.export_scene.mw(filepath=out_file)
                bpy.ops.export_scene.fbx(filepath=fbx_out)
      except Exception as e:
        print("Corrupted NIF file: {}".format(mesh_file))
        print(e)
