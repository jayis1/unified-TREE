#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
VERSION="0.1.1"
ARCH="all"
BUILD=$(mktemp -d /tmp/unified-tree-deb.XXXXXX)
PKG="$BUILD/unified-tree_${VERSION}_${ARCH}"
OUT="$ROOT/dist"
trap 'rm -rf "$BUILD"' EXIT HUP INT TERM

mkdir -p "$PKG/DEBIAN" "$PKG/opt/unified-tree" "$PKG/usr/bin" \
    "$PKG/usr/share/applications" "$PKG/usr/share/icons/hicolor/scalable/apps" "$OUT"

cp "$ROOT/server.py" "$ROOT/desktop.py" "$ROOT/devices.json" "$ROOT/platform.json" "$PKG/opt/unified-tree/"
cp -R "$ROOT/web" "$ROOT/protocol" "$PKG/opt/unified-tree/"
cp "$ROOT/packaging/debian/control" "$PKG/DEBIAN/control"
cp "$ROOT/packaging/debian/unified-tree.desktop" "$PKG/usr/share/applications/"
cp "$ROOT/packaging/debian/unified-tree.svg" "$PKG/usr/share/icons/hicolor/scalable/apps/"

cat > "$PKG/usr/bin/unified-tree" <<'EOF'
#!/bin/sh
exec /usr/bin/python3 /opt/unified-tree/desktop.py "$@"
EOF
chmod 0755 "$PKG/usr/bin/unified-tree"
chmod 0644 "$PKG/usr/share/applications/unified-tree.desktop" "$PKG/usr/share/icons/hicolor/scalable/apps/unified-tree.svg"
find "$PKG/opt/unified-tree" -type f -exec chmod 0644 {} \;
find "$PKG/opt/unified-tree" -type d -exec chmod 0755 {} \;

DEB="$OUT/unified-tree_all.deb"
if command -v dpkg-deb >/dev/null 2>&1; then
    dpkg-deb --root-owner-group --build "$PKG" "$DEB"
else
    # Portable fallback for building on non-Debian development machines.
    printf '2.0\n' > "$BUILD/debian-binary"
    tar --owner=0 --group=0 -C "$PKG/DEBIAN" -czf "$BUILD/control.tar.gz" .
    tar --owner=0 --group=0 -C "$PKG" --exclude='./DEBIAN' -czf "$BUILD/data.tar.gz" .
    rm -f "$DEB"
    (cd "$BUILD" && ar r "$DEB" debian-binary control.tar.gz data.tar.gz)
fi
echo "Built $DEB"
