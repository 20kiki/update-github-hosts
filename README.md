# GitHub520 Hosts 一键更新工具

自动拉取 [GitHub520](https://github.com/521xueweihan/GitHub520) 最新 hosts 列表并写入系统 hosts 文件，解决 GitHub 网页访问慢、图片加载失败等问题。

> 如果遇到 `git push` 超时，hosts 只能优化 DNS 解析，传输链路的干扰需要走 **SSH 443 端口**，见下方[常见问题](#常见问题)。

## 使用方法

### Windows

1. 下载本项目
2. 双击 `一键更新.bat`（自动请求管理员权限）
3. 完成

### macOS / Linux

1. 下载本项目
2. 终端中运行 `./一键更新.sh`（自动请求 root 权限）
3. 完成

每次更新后会自动刷新 DNS 缓存，立即生效。

## 原理

- 从 `raw.hellogithub.com` 拉取 GitHub520 维护的最优 IP 列表
- 写入系统 hosts 文件，通过注释标记管理
- 执行对应平台的 DNS 缓存刷新命令

## 定时自动更新

- **Windows**：在任务计划程序中创建定时任务，每日运行 `一键更新.bat`
- **macOS**：使用 `launchd` 创建定时任务
- **Linux**：使用 `cron` 或 `systemd timer` 创建定时任务

## 依赖

需要 Python 3 环境（`python3` 或 `python` 命令可在终端中使用）。

## 常见问题

### git push 超时 / 推送失败怎么办？

本工具通过 hosts 优化的是 **DNS 解析**（域名 → IP），让你的浏览器能正常打开 GitHub 网页。但 `git push` 走的是独立的传输链路，即使 DNS 正常，SSH（22 端口）或 HTTPS 的流量仍可能被干扰。下面的方案把 Git 流量切到 GitHub 的 SSH 443 端口，能有效解决 push 超时。

---

#### 第一步：检查是否有 SSH 密钥

打开终端（Windows 用 Git Bash），运行：

```bash
ls ~/.ssh/id_*
```

- **有 `id_rsa` + `id_rsa.pub`**（或 `id_ed25519` + `id_ed25519.pub`）→ 跳到第二步
- **没有** → 先生成：

```bash
ssh-keygen -t rsa -b 4096 -C "你的邮箱@example.com"
```

一路回车即可（不需要设密码）。

#### 第二步：把公钥添加到 GitHub

```bash
cat ~/.ssh/id_rsa.pub
```

复制输出的全部内容 → 打开 [GitHub SSH 设置页](https://github.com/settings/ssh/new) → Title 随便填 → Key 粘贴 → 点 **Add SSH Key**。

#### 第三步：配置 SSH 走 443 端口

```bash
echo 'Host github.com
    Hostname ssh.github.com
    Port 443
    User git' >> ~/.ssh/config
```

#### 第四步：把仓库远程地址从 HTTPS 换成 SSH

先看一下当前的远程地址：

```bash
git remote -v
```

如果是 `https://github.com/...` 开头，换成 SSH：

```bash
git remote set-url origin git@github.com:用户名/仓库名.git
```

（把 `用户名/仓库名` 换成你自己的）

#### 第五步：测试连接

```bash
ssh -T git@github.com
```

显示 `Hi 你的用户名! You've successfully authenticated...` 就成功了。现在再 `git push` 试试。

---

#### 补充：让 SSH Agent 持久化（免去每次输入密钥密码）

如果没有给密钥设密码，跳过这一步。如果设了密码，避免每次 push 都输入：

```bash
# 启动 ssh-agent 并加载密钥
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

可以把这两行加到 `~/.bashrc`（Linux / Git Bash）或 `~/.zshrc`（macOS）末尾，每次打开终端自动生效。
