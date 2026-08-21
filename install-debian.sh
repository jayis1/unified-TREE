#!/bin/sh
set -eu

PACKAGE_URL="https://github.com/jayis1/unified-TREE/releases/latest/download/unified-tree_all.deb"
PACKAGE_FILE=$(mktemp /tmp/unified-tree.XXXXXX.deb)
trap 'rm -f "$PACKAGE_FILE"' EXIT HUP INT TERM

if [ "$(id -u)" -ne 0 ]; then
    echo "Run this installer as root (for example: curl ... | sudo sh)." >&2
    exit 1
fi

if ! command -v apt-get >/dev/null 2>&1; then
    echo "This installer requires Debian or a Debian-based system with apt." >&2
    exit 1
fi

echo "Downloading unified TREE for Debian 13..."
curl -fL "$PACKAGE_URL" -o "$PACKAGE_FILE"
dpkg-deb --info "$PACKAGE_FILE" >/dev/null

echo "Installing unified TREE..."
apt-get install -y "$PACKAGE_FILE"
echo "Installed. Open unified TREE from the application menu or run: unified-tree"
