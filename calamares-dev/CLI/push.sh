#!/bin/bash
set -e

echo "📂 Cambios detectados:"
echo

files=$(git diff --name-only)

if [ -z "$files" ]; then
  echo "✔ No hay cambios"
  exit 0
fi

echo "$files" | while read -r f; do
  case "$f" in
  PKGBUILD | .SRCINFO) icon="📦" ;;
  *.rs) icon="🦀" ;;
  *.svg) icon="🎨" ;;
  *.png) icon="🖼" ;;
  *.desktop) icon="🖥" ;;
  meson.build) icon="⚙" ;;
  *.patch) icon="🔧" ;;
  *.sh) icon="🔧" ;;
  *) icon="📄" ;;
  esac

  echo "$icon $f"
done

echo
echo "✏️ Commit:"
read -r msg

git add -A
git commit -m "$msg"
git push

echo
echo "✅ Done"
