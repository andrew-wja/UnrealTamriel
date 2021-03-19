#!/usr/bin/env bash

base=$(dirname "$1")/$(basename "$1" .dds)

if [[ ! -f $base.tga ]]
then
  echo "Converting $base.dds"
  convert "$base.dds" "$base.tga"
fi
