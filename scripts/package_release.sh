#!/usr/bin/env bash
set -euo pipefail

# Simple local packer to create release.zip matching CI behavior
# Usage: ./scripts/package_release.sh

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
TMP_DIR="$ROOT_DIR/tmp_release"
RELEASE_ZIP="$ROOT_DIR/release.zip"

rm -rf "$TMP_DIR" || true
mkdir -p "$TMP_DIR"

# copy top-level files
cp "$ROOT_DIR/manifest.yaml" "$TMP_DIR/" || true
for f in README.md PRIVACY.md LICENSE requirements.txt; do
  [ -f "$ROOT_DIR/$f" ] && cp "$ROOT_DIR/$f" "$TMP_DIR/" || true
done

# provider
if [ -d "$ROOT_DIR/provider" ]; then
  mkdir -p "$TMP_DIR/provider"
  cp -r "$ROOT_DIR/provider/"* "$TMP_DIR/provider/" || true
fi

# provider_files and assets
[ -d "$ROOT_DIR/provider_files" ] && cp -r "$ROOT_DIR/provider_files" "$TMP_DIR/" || true
[ -d "$ROOT_DIR/_assets" ] && cp -r "$ROOT_DIR/_assets" "$TMP_DIR/" || true
[ -d "$ROOT_DIR/assets" ] && cp -r "$ROOT_DIR/assets" "$TMP_DIR/" || true

# include difypkg if present
[ -f "$ROOT_DIR/heygen-dify-plugin.difypkg" ] && cp "$ROOT_DIR/heygen-dify-plugin.difypkg" "$TMP_DIR/" || true

# zip
rm -f "$RELEASE_ZIP" || true
(cd "$TMP_DIR" && zip -r "$RELEASE_ZIP" .) || true

echo "Created $RELEASE_ZIP"
echo "Contents:" 
unzip -l "$RELEASE_ZIP"

echo "Quick verification: looking for top-level provider/"
unzip -l "$RELEASE_ZIP" | awk '{print $4}' | grep -x 'provider/' || echo 'WARNING: provider/ missing'

exit 0
