#!/usr/bin/env bash

base=$(dirname "$1")/$(basename "$1" .dds)
echo "Converting $base.dds"
convert "$base.dds" "${base}.tga"
ln -sf "${base}.tga" "${base^}.tga" # for NifSkope
