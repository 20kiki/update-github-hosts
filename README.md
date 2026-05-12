<div align="center">
  <h1>GitHub Hosts Updater</h1>
  <p>One-click update system hosts file for smooth GitHub access — fetches optimal IPs from GitHub520.</p>

  [![GitHub stars](https://img.shields.io/github/stars/20kiki/update-github-hosts?style=social)](https://github.com/20kiki/update-github-hosts/stargazers)
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
  [![Python: 3.x](https://img.shields.io/badge/Python-3.x-green)](https://python.org)
  [![Platform: Windows|macOS|Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()
</div>

**Language:** [English](README.md) | [简体中文](zh-CN/README.md)

---

## 📋 Table of Contents
- [The Problem](#-the-problem)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

The GitHub520 project maintains a list of optimal GitHub IPs, but manually updating your hosts file is tedious. This tool automates it — fetch, write, flush DNS — in one command.

## ✨ The Problem

Slow GitHub page loads, broken image rendering, and connection timeouts are common in some regions due to DNS resolution issues. This tool solves the **web access** problem by updating your local hosts file with the fastest known GitHub IPs.

> If your issue is `git push` timing out, see [Troubleshooting](#troubleshooting) — hosts alone won't fix the transfer layer.

## 🚀 Quick Start

**Windows:** Double-click `scripts/update.bat` (auto-requests admin)

**macOS / Linux:** Run `bash scripts/update.sh` (auto-requests root)

That's it. DNS cache flushes automatically, changes take effect immediately.

## 📦 Installation

```bash
git clone https://github.com/20kiki/update-github-hosts.git
cd update-github-hosts
```

Requires Python 3 (`python` or `python3` available in terminal).

## 📖 Usage

### One-Time Update

```bash
# Windows — double-click
scripts/update.bat

# macOS / Linux
bash scripts/update.sh
```

### Scheduled Auto-Update

- **Windows:** Create a daily task in Task Scheduler running `scripts/update.bat`
- **macOS:** Use `launchd` for periodic execution
- **Linux:** Add a `cron` job or `systemd timer`

## 🔧 How It Works

1. Fetches the latest hosts list from `raw.hellogithub.com`
2. Extracts IP-to-domain mappings for GitHub services
3. Writes them into your system hosts file (marked with comment tags)
4. Flushes the system DNS cache so changes take effect immediately

## 🔨 Troubleshooting

### `git push` times out? Route traffic through SSH port 443

Hosts optimization fixes DNS resolution (web browsing). `git push` uses a separate transfer layer — you need SSH over port 443 to bypass interference:

**① Prepare SSH key (skip if you have one)**
```bash
ls ~/.ssh/id_*
# If none found:
ssh-keygen -t ed25519 -C "your-email@example.com"
```

**② Add public key to GitHub**
```bash
cat ~/.ssh/id_ed25519.pub 2>/dev/null || cat ~/.ssh/id_rsa.pub 2>/dev/null
# Copy output → https://github.com/settings/ssh/new → Save
```

**③ Configure SSH to use port 443**
```bash
mkdir -p ~/.ssh
grep -q "Host github.com" ~/.ssh/config 2>/dev/null || cat >> ~/.ssh/config << 'EOF'
Host github.com
    Hostname ssh.github.com
    Port 443
    User git
EOF
chmod 600 ~/.ssh/config
chmod 700 ~/.ssh
```

**④ Switch remote to SSH**
```bash
git remote -v
git remote set-url origin git@github.com:username/repo.git
```

**⑤ Test and push**
```bash
ssh -T git@github.com
# Should see: "Hi username!"
git push
```

## 🤝 Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT
