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

### git push 仍然超时怎么办？

hosts 只解决 DNS 解析（域名 → IP），不影响 git 数据传输链路。push 超时通常是 SSH 22 端口或 HTTPS 被干扰，推荐切到 GitHub 的 SSH 443 端口：

**1. 配置 `~/.ssh/config`：**

```
Host github.com
    Hostname ssh.github.com
    Port 443
    User git
```

**2. 切换仓库远程地址为 SSH：**

```bash
git remote set-url origin git@github.com:用户名/仓库名.git
```

**3. 测试连接：**

```bash
ssh -T git@github.com
```

看到 `Hi 用户名!` 即成功。
