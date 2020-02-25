#!/bin/bash

folder=$1

if [ -z "$folder" ]; then
  echo "no folder"
  exit 1
fi

if [ ! -d "$folder" ]; then
  echo "folder $folder does not exist"
  exit 1
fi

files=$(ls $folder)

echo $files

for file in $(ls $folder)
do
  if [[ $file == tags* ]]; then
    tags=${file:5}
    tags=${tags//+/" "}
    echo "tags are: $tags"
    ./konachan.sh "$tags"
  elif [[ $file == yandere* ]]; then
    tags=${file:8}
    tags=${tags//+/" "}
    echo "tags are: $tags"
    ./yandere "$tags"
  fi
done
