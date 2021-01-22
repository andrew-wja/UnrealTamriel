#!/usr/bin/env python3

import os
import bpy
from enum import Enum
import argparse

parser = argparse.ArgumentParser(description='Convert Morrowind asset files.')
parser.add_argument('--asset-path', type=str, required=True,
                    help='Path to your extracted game asset files')

# Awful hack for Blender python CLI argument passing
parser.add_argument('-p', '--python', type=str, required=False)
parser.add_argument('-b', '--background', action='store_true', required=False)

def main():
    args = parser.parse_args()

    processed = set()

    for root, dirs, files in os.walk(args.asset_path):
      for f in files:
        if f.endswith('.nif') and not f in processed:
          processed.add(f)

          in_file = os.path.join(root, f)
          out_file = os.path.join(root, os.path.splitext(f)[0] + '.converted.' + str(args.mesh_format))

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

          for block in bpy.data.node_groups:
                bpy.data.node_groups.remove(block)
          try:
            bpy.ops.import_scene.mw(filepath=in_file)
            bpy.ops.object.select_all(action='DESELECT')

          except Exception as e:
            print("Corrupted NIF file: {}".format(in_file))
            print(e)
            continue

          try:
            print('Attempting to merge meshes')

            for obj in bpy.data.objects:
                if obj.name.startswith('Tri'):
                    print('Adding submesh ' + obj.name + ' to selection set')
                    obj.select_set(True)
                    if obj.name.endswith('0'):
                        bpy.context.view_layer.objects.active = obj
                else:
                    print('Ignoring unknown object ' + obj.name)

            bpy.ops.object.join()

            bpy.ops.export_scene.gltf(export_format='GLTF_SEPARATE', filepath=out_file)

          except Exception as e:
            print("Blender error: {}".format(e))
            continue

if __name__ == "__main__":
    main()
