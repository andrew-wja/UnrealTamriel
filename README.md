# Unreal Tamriel

Morrowind conversion in Unreal Engine 4

For some reason, all the texture paths in assets in Morrowind point to .tga files, yet the game ships with .dds files

After unpacking the game data you'll need to `find . -iname '*.dds' -exec UnrealTamriel/scripts/convert-dds-to-tga.sh {} \;` in the game data folder
