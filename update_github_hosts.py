#!/usr/bin/env python3
"""Fetch GitHub520 hosts and update the system hosts file."""

import os
import sys
import tempfile
import urllib.request

# GitHub520 hosts source
HOSTS_URL = "https://raw.hellogithub.com/hosts"
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"

START_MARKER = "# GitHub520 Host Start"
END_MARKER = "# GitHub520 Host End"


def fetch_hosts_content() -> str:
    """Fetch the latest GitHub520 hosts entries."""
    req = urllib.request.Request(HOSTS_URL, headers={"User-Agent": "curl/8.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read().decode("utf-8")

    # Extract only lines starting with an IP (the actual hosts mappings)
    lines = data.strip().splitlines()
    host_lines = [line for line in lines if not line.startswith("#") and line.strip()]
    return "\n".join(host_lines)


def update_hosts_file(hosts_content: str):
    """Insert or replace the GitHub520 block in the hosts file."""
    with open(HOSTS_PATH, "r", encoding="utf-8") as f:
        original = f.read()

    block = f"{START_MARKER}\n{hosts_content}\n{END_MARKER}"

    if START_MARKER in original and END_MARKER in original:
        # Replace existing block
        start = original.index(START_MARKER)
        end = original.index(END_MARKER) + len(END_MARKER)
        new_content = original[:start] + block + original[end:]
    else:
        # Append new block
        if not original.endswith("\n"):
            original += "\n"
        new_content = original + "\n" + block + "\n"

    # Write to temp file then move (avoids permission issues with direct write)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".tmp") as tmp:
        tmp.write(new_content)
        tmp_path = tmp.name

    try:
        os.replace(tmp_path, HOSTS_PATH)
        print(f"[OK] 已写入 {hosts_content.count(chr(10)) + 1} 条映射到 {HOSTS_PATH}")
    except PermissionError:
        print("[ERROR] 权限不足，请右键以管理员身份运行。")
        sys.exit(1)


def main():
    print("正在获取 GitHub520 hosts 列表...")
    try:
        hosts_content = fetch_hosts_content()
    except Exception as e:
        print(f"[ERROR] 获取失败: {e}")
        sys.exit(1)

    update_hosts_file(hosts_content)
    print("[OK] 更新完成！")


def flush_dns():
    """Flush system DNS cache so new hosts entries take effect immediately."""
    import subprocess
    try:
        subprocess.run(["ipconfig", "/flushdns"], capture_output=True, check=True)
        print("[OK] DNS 缓存已刷新")
    except Exception:
        print("[WARN] 无法刷新 DNS 缓存，重启浏览器后生效")


if __name__ == "__main__":
    main()
    flush_dns()
