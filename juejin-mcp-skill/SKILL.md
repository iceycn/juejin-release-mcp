---
name: juejin-mcp
description: 通过 MCP 协议管理掘金文章，支持发布文章、管理草稿、更新内容、获取分类标签等功能。适用于需要向掘金平台发布文章、管理博客草稿或自动化内容发布流程的场景。
---

# 掘金 MCP 服务器

## 概述

告别手动复制粘贴，通过自然语言让 AI 帮你发布掘金文章、管理草稿、获取内容列表，实现「动动嘴皮子就能写博客」的流畅体验。

**核心功能：**
- ✍️ **一键发布** - 自动完成创建草稿 + 发布两步操作
- 📝 **草稿管理** - 创建、更新、删除、列出草稿
- 📄 **文章管理** - 获取、更新、删除已发布文章
- 🏷️ **分类标签** - 自动获取掘金官方分类和热门标签
- 👤 **用户信息** - 获取当前登录用户信息

---

## 快速配置

### 方式一：龙虾/AI 助手配置（最简单）

直接告诉你的 AI 助手（如龙虾、Cursor）：

```
请帮我配置 juejin-mcp-skill 技能，
我的掘金 Cookie 是：sessionid=dc673cde72c7c81539d2fa3xxxxxxxx
```

AI 会自动帮你完成配置，无需手动编辑文件。

### 方式二：uvx 运行（推荐，无需安装）

```json
{
  "mcpServers": {
    "juejin": {
      "command": "uvx",
      "args": ["juejin-release-mcp"],
      "env": {
        "JUEJIN_COOKIE": "sessionid=your_sessionid"
      }
    }
  }
}
```

### 方式三：pip 安装后运行

```bash
pip install juejin-release-mcp
```

```json
{
  "mcpServers": {
    "juejin": {
      "command": "juejin-release-mcp",
      "env": {
        "JUEJIN_COOKIE": "sessionid=your_sessionid"
      }
    }
  }
}
```

---

## 🚀 使用指南

### 第一步：获取掘金 Cookie

1. 登录 [掘金](https://juejin.cn/)，进入[创作者中心](https://juejin.cn/creator)
2. 按 **F12** 打开浏览器开发者工具，切换到 **Network（网络）** 标签
3. 刷新页面，找到任意 API 请求（如 `list_by_user` 或 `query_category_list`）
4. 在 **Request Headers** 中找到并复制 `sessionid` 字段

![获取 Cookie 示意图](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/placeholder.png)

> ⚠️ **重要提醒**：掘金 Cookie 有效期约为 **30 天**，过期后会导致发布失败。如遇「鉴权失败」错误，请重新获取 Cookie。

### 第二步：配置到 Cursor

1. 打开 Cursor 设置 → MCP 页面
2. 点击「添加服务器」
3. 粘贴上面的配置 JSON
4. 将 `your_sessionid` 替换为你复制的真实 Cookie
5. 保存配置

### 第三步：开始使用

配置完成后，直接在对话中使用：

```
请帮我发布一篇掘金文章：
- 标题：我的 2024 技术总结
- 内容：# Hello World

这是我的第一篇博客文章...
- 分类：后端
- 标签：Python, MCP
```

---

## 核心工具

| 工具 | 功能 | 必填参数 |
|------|------|----------|
| `publish_article` | 发布文章（创建草稿+发布） | `title`, `content` |
| `create_draft` | 创建草稿 | `title`, `content` |
| `update_draft` | 更新草稿 | `draftId` |
| `delete_draft` | 删除草稿 | `draftId` |
| `list_drafts` | 草稿列表 | - |
| `get_article` | 获取文章详情 | `articleId` |
| `list_articles` | 文章列表 | - |
| `update_article` | 更新文章 | `articleId` |
| `delete_article` | 删除文章 | `articleId` |
| `list_categories` | 分类列表 | - |
| `list_tags` | 标签列表 | - |
| `get_user_info` | 用户信息 | - |

---

## 使用示例

### 发布文章

```
请帮我发布一篇掘金文章：
- 标题：Python 异步编程入门指南
- 内容：# Python 异步编程入门指南

异步编程是现代 Python 开发中的重要技能...
- 分类：后端
- 标签：Python, 异步编程, asyncio
```

### 查看草稿列表

```
请列出我在掘金的所有草稿
```

### 获取分类标签

```
请显示掘金的文章分类和热门标签
```

### 更新文章

```
请帮我更新文章 7382918472656487462，在末尾添加「更新于 2024-01-01」
```

---

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `JUEJIN_COOKIE` | ✅ | Cookie，格式：`sessionid=xxx`（有效期约 30 天） |
| `JUEJIN_AID` | ❌ | 应用 ID，默认 2608 |
| `JUEJIN_UUID` | ❌ | 用户 UUID |
| `JUEJIN_TIMEOUT` | ❌ | 超时秒数，默认 30 |
| `JUEJIN_MAX_RETRIES` | ❌ | 最大重试次数，默认 3 |

### ⚠️ Cookie 有效期提醒

掘金 Cookie 的有效期约为 **30 天**，过期后会导致发布失败。建议：
- 记录配置日期，定期更新
- 如遇「鉴权失败」错误，请重新获取 Cookie
- 可在浏览器无痕模式下登录获取长期有效的 Cookie

---

## 常见问题

### Q: 提示 "JUEJIN_COOKIE 环境变量未设置"

A: 请确保已正确设置环境变量，或在 MCP 配置中添加 `env` 配置。

### Q: 发布失败，提示鉴权错误

A: Cookie 可能已过期（有效期约 30 天），请重新获取并更新。

### Q: 提示 "参数错误"

A: 请检查必填参数是否正确传递，特别是 `title` 和 `content` 字段。

---

## 更多资源

- 完整 API 参考：[reference.md](reference.md)
- 使用示例：[examples.md](examples.md)
- PyPI: https://pypi.org/project/juejin-release-mcp/
- GitHub: https://github.com/iceycn/juejin-release-mcp
