#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Re-execute with sudo if not root
if [ "$(id -u)" -ne 0 ]; then
    echo "请求 root 权限..."
    exec sudo bash "$0"
fi

# Find python3
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        PYTHON="$cmd"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "[ERROR] 未找到 Python 3，请先安装。"
    exit 1
fi

"$PYTHON" "$SCRIPT_DIR/update_github_hosts.py"
