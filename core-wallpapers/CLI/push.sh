#!/bin/bash

echo "Escribe el mensaje del commit:"
read -r msg

git add .
git commit -m "$msg"
git push
