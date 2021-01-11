#!/usr/bin/env python3

import os
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Unpack Morrowind data files.')
parser.add_argument('--openmw-path', type=str, required=True,
                    help='Path to your OpenMW installation')
parser.add_argument('--data-path', type=str, required=True,
                    help='Path to your data files')
parser.add_argument('--output-path', type=str, required=True,
                    help='Path to unpack data to (created if nonexistent)')

def main():
    args = parser.parse_args()

    for root, dirs, files in os.walk(args.data_path):
      for f in files:
        if f.endswith('.bsa'):
          bsa_file = os.path.join(root, f)
          bsa_dir = os.path.join(args.output_path, f)

          print("Extracting {} to {}".format(os.path.abspath(bsa_file), os.path.abspath(bsa_dir)))

          os.makedirs(bsa_dir, exist_ok=True)
          subprocess.run([os.path.join(args.openmw_path, "bsatool"), "extractall", bsa_file, bsa_dir])

        if f.endswith('.esm'):
          esm_file = os.path.join(root, f)
          esm_dump_path = os.path.join(args.output_path, f)
          esm_dump = open(esm_dump_path, "w")

          print("Extracting {} to {}".format(os.path.abspath(esm_file), os.path.abspath(esm_dump_path)))

          subprocess.run([os.path.join(args.openmw_path, "esmtool"), "dump", "-C", "-p", esm_file], stdout=esm_dump)


    # Just copy all the loose files
    subprocess.run(["cp", "-r", os.path.join(args.data_path, "Fonts"),
                                os.path.join(args.data_path, "Music"),
                                os.path.join(args.data_path, "Sound"),
                                os.path.join(args.data_path, "Splash"),
                                os.path.join(args.data_path, "Video"), args.output_path])

if __name__ == "__main__":
    main()
