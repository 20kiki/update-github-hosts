# GitHub520 Hosts 一键更新工具

双击 `一键更新.bat`，自动拉取 [GitHub520](https://github.com/521xueweihan/GitHub520) 最新 hosts 列表并写入系统 hosts 文件，解决 GitHub 访问慢、图片加载失败等问题。

## 使用方法

1. 下载本项目
2. 双击 `一键更新.bat`（自动请求管理员权限）
3. 完成

每次更新后会自动刷新 DNS 缓存，立即生效。

## 原理

- 从 `raw.hellogithub.com` 拉取 GitHub520 维护的最优 IP 列表
- 写入 `C:\Windows\System32\drivers\etc\hosts`，通过注释标记管理
- 执行 `ipconfig /flushdns` 刷新 DNS 缓存

## 定时自动更新

在任务计划程序中创建定时任务，每日自动运行 `一键更新.bat` 即可。

## 仅支持 Windows

需要 Python 3 环境（系统 PATH 中可用 `python` 命令）。
