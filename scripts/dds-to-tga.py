import os
from wand import image

path = "/home/andrew/Downloads/Morrowind-BSA"

for root, dirs, files in os.walk(path):
  for f in files:
    if f.endswith('.dds'):
      dds_file = os.path.join(root, f)
      tga_file = os.path.splitext(dds_file)[0] + ".tga"
      try:
        print("Converting {}...".format(dds_file))
        with image.Image(filename=dds_file) as img:
          img.compression = "no"
          img.save(filename=tga_file)
      except Exception as e:
        print("Corrupted DDS file: {}".format(dds_file))
