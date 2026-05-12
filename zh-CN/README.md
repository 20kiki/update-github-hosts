<div align="center">
  <h1>GitHub Hosts 更新工具</h1>
  <p>一键更新系统 hosts 文件，畅快访问 GitHub — 自动拉取 GitHub520 最优 IP。</p>

  [![GitHub stars](https://img.shields.io/github/stars/20kiki/update-github-hosts?style=social)](https://github.com/20kiki/update-github-hosts/stargazers)
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
  [![Python: 3.x](https://img.shields.io/badge/Python-3.x-green)](https://python.org)
  [![Platform: Windows|macOS|Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()
</div>

**Language:** [English](../README.md) | [简体中文](README.md)

---

## 📋 目录
- [它能解决什么](#-它能解决什么)
- [快速开始](#-快速开始)
- [安装](#-安装)
- [使用方法](#-使用方法)
- [工作原理](#-工作原理)
- [常见问题](#-常见问题)
- [标签](#标签)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

---

GitHub520 项目维护着 GitHub 最优 IP 列表，但手动更新 hosts 文件很麻烦。本工具把它自动化了——拉取、写入、刷新 DNS 缓存，一条命令搞定。

## ✨ 它能解决什么

GitHub 网页加载慢、图片裂开、连接超时，在某些地区是家常便饭。根本原因是 DNS 解析走了不稳定的线路。本工具通过向系统 hosts 写入已知最快的 GitHub IP，解决**网页访问**问题。

> 如果你的问题是 `git push` 超时，hosts 只能优化 DNS 解析，传输链路需要走 SSH 443 端口，见[常见问题](#常见问题)。

## 🚀 快速开始

**Windows：** 双击 `scripts/update.bat`（自动提权）

**macOS / Linux：** 终端运行 `bash scripts/update.sh`（自动提权）

DNS 缓存自动刷新，修改立即生效。

## 📦 安装

```bash
git clone https://github.com/20kiki/update-github-hosts.git
cd update-github-hosts
```

需要 Python 3 环境（终端中能执行 `python` 或 `python3`）。

## 📖 使用方法

### 一次性更新

```bash
# Windows — 双击
scripts/update.bat

# macOS / Linux
bash scripts/update.sh
```

### 定时自动更新

- **Windows：** 在任务计划程序中创建每日任务，运行 `scripts/update.bat`
- **macOS：** 使用 `launchd` 设置定时执行
- **Linux：** 添加 `cron` 任务或 `systemd timer`

## 🔧 工作原理

1. 从 `raw.hellogithub.com` 拉取最新 hosts 列表
2. 提取 GitHub 服务相关的 IP 到域名映射
3. 写入系统 hosts 文件（通过注释标记管理）
4. 刷新系统 DNS 缓存，使修改立即生效

## 🔨 常见问题

### `git push` 超时？把流量切到 SSH 443 端口

hosts 优化解决的是 DNS 解析（网页访问）问题。`git push` 走的是独立传输链路，需要把流量切到 GitHub 的备用 SSH 443 端口来绕过干扰：

> 以下操作 Windows 用户请用 **Git Bash**（安装 Git 时自带），不要用 CMD 或 PowerShell。

**① 准备 SSH 密钥（已有可跳过）**
```bash
ls ~/.ssh/id_*
# 没有的话生成：
ssh-keygen -t ed25519 -C "your-email@example.com"
# 一路回车
```

**② 把公钥告诉 GitHub**
```bash
cat ~/.ssh/id_ed25519.pub 2>/dev/null || cat ~/.ssh/id_rsa.pub 2>/dev/null
# 复制输出 → https://github.com/settings/ssh/new → 粘贴保存
```

**③ 配置 SSH 走 443 端口**
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

**④ 改仓库远程地址为 SSH**
```bash
git remote -v
# 看到 https:// 就换成下面格式：
git remote set-url origin git@github.com:用户名/仓库名.git
```

**⑤ 测试并 push**
```bash
ssh -T git@github.com
# 看到 "Hi 用户名!" 即成功
git push
```

## 标签

[`github`](https://github.com/topics/github) [`hosts`](https://github.com/topics/hosts) [`dns`](https://github.com/topics/dns) [`python`](https://github.com/topics/python) [`windows`](https://github.com/topics/windows) [`macos`](https://github.com/topics/macos) [`linux`](https://github.com/topics/linux)

## 🤝 贡献指南

欢迎贡献。详见 [CONTRIBUTING.md](../CONTRIBUTING.md)。

## 📄 许可证

MIT
