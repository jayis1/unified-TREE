#!/bin/sh
set -eu

SOURCE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
INSTALL_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/unified-tree"
BIN_DIR="$HOME/.local/bin"
APP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"

mkdir -p "$INSTALL_DIR" "$BIN_DIR" "$APP_DIR"
cp "$SOURCE_DIR/server.py" "$SOURCE_DIR/desktop.py" "$SOURCE_DIR/devices.json" "$SOURCE_DIR/platform.json" "$INSTALL_DIR/"
rm -rf "$INSTALL_DIR/web" "$INSTALL_DIR/protocol"
cp -R "$SOURCE_DIR/web" "$SOURCE_DIR/protocol" "$INSTALL_DIR/"

cat > "$BIN_DIR/unified-tree" <<EOF
#!/bin/sh
exec python3 "$INSTALL_DIR/desktop.py" "\$@"
EOF
chmod +x "$BIN_DIR/unified-tree"

cat > "$APP_DIR/unified-tree.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=unified TREE
Comment=Control plane for 57 interconnected SoC device nodes
Exec=$BIN_DIR/unified-tree
Icon=network-wired
Terminal=false
Categories=Development;Science;Network;
Keywords=SoC;IoT;nodes;dashboard;
EOF
chmod +x "$APP_DIR/unified-tree.desktop"

echo "unified TREE is installed."
echo "Open it from the application menu or run: $BIN_DIR/unified-tree"
