#!/usr/bin/env python3

import os
import argparse
import subprocess
from wand import image

parser = argparse.ArgumentParser(description='Convert Morrowind asset files.')
parser.add_argument('--asset-path', type=str, required=True,
                    help='Path to your extracted game asset files')

def main():
    args = parser.parse_args()

    for root, dirs, files in os.walk(args.asset_path):
      for f in files:
        if f.endswith('.dds'):
          in_file = os.path.join(root, f)
          out_file = os.path.splitext(in_file)[0] + ".bmp"
          try:
            print("Converting {}...".format(in_file))
            with image.Image(filename=in_file) as img:
              img.compression = "no"
              img.save(filename=out_file)
              os.remove(in_file)
          except Exception as e:
            print("Corrupted DDS file: {}".format(in_file))

        elif f.endswith('.mp3'):
          in_file = os.path.join(root, f)
          out_file = os.path.join(root, os.path.splitext(f)[0] + ".wav")
          print("Converting {}...".format(in_file))
          subprocess.run(["ffmpeg", "-v", "quiet", "-i", in_file, out_file])
          os.remove(in_file)

        else:
          print("Not converting {}".format(os.path.join(root, f)))

if __name__ == "__main__":
    main()
