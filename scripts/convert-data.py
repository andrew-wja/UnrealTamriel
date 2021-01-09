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
          dds_file = os.path.join(root, f)
          bmp_file = os.path.splitext(dds_file)[0] + ".bmp"
          try:
            print("Converting {}...".format(dds_file))
            with image.Image(filename=dds_file) as img:
              img.compression = "no"
              img.save(filename=bmp_file)
              os.remove(dds_file)
          except Exception as e:
            print("Corrupted DDS file: {}".format(dds_file))

        elif f.endswith('.mp3'):
          mp3_file = os.path.join(root, f)
          wav_file = os.path.join(root, os.path.splitext(f)[0] + ".wav")
          print("Converting {}...".format(mp3_file))
          subprocess.run(["ffmpeg", "-v", "quiet", "-i", mp3_file, wav_file])
          os.remove(mp3_file)

        else:
          print("Not converting {}".format(os.path.join(root, f)))

if __name__ == "__main__":
    main()
