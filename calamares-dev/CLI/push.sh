#!/bin/bash
set -e

echo "📦 Añadiendo cambios..."
git add .

if [ -z "$1" ]; then
  echo "✏️  Mensaje del commit:"
  read -r msg
else
  msg="$*"
fi

echo "📝 Commit: $msg"
git commit -m "$msg"

echo "🚀 Enviando a GitHub..."
git push

echo "✅ Listo"
