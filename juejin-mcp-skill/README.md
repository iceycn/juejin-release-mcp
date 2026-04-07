# 掘金 MCP Skill

[![SkillHub](https://img.shields.io/badge/SkillHub-Available-green)](https://agentskillhub.dev)
[![PyPI](https://img.shields.io/badge/PyPI-juejin--release--mcp-blue)](https://pypi.org/project/juejin-release-mcp/)

用于通过 MCP 协议管理掘金（Juejin）文章的 Cursor Skill。

## 功能概述

本 Skill 让 AI 助手能够：

- **直接发布文章**到掘金平台
- **管理草稿** - 创建、更新、删除、列出
- **查询内容** - 获取文章、分类、标签
- **自动化工作流** - 简化内容发布流程

## 安装配置

### 方式一：AI 助手配置（最简单）

直接告诉你的 AI 助手（如龙虾、Cursor）：

```
请帮我配置 juejin-mcp-skills 技能，
我的掘金 Cookie 是：sessionid=dc673cde72c7c81539d2fa3xxxxxxxx
```

AI 会自动帮你完成配置。

### 方式二：手动配置

#### 1. 安装 MCP 服务器

```bash
# 使用 uvx（推荐）
uvx juejin-release-mcp

# 或使用 pip
pip install juejin-release-mcp
```

#### 2. 获取 Cookie

1. 登录[掘金](https://juejin.cn/)并进入创作者中心
2. 打开开发者工具（F12）→ Network 标签
3. 刷新页面，找到任意 API 请求
4. 从 Request Headers 中复制 `sessionid`

> ⚠️ **重要提醒**：掘金 Cookie 有效期约为 **30 天**，过期后需要重新获取并更新配置。如果遇到鉴权失败，请重新执行上述步骤获取新的 Cookie。

#### 3. 配置 Cursor

添加到你的 Cursor MCP 设置：

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

## 可用工具

| 工具 | 功能 | 必填参数 |
|------|------|----------|
| `publish_article` | 发布文章（创建草稿+发布） | `title`, `content` |
| `create_draft` | 创建草稿 | `title`, `content` |
| `update_draft` | 更新草稿 | `draftId` |
| `delete_draft` | 删除草稿 | `draftId` |
| `list_drafts` | 列出所有草稿 | - |
| `get_article` | 获取文章详情 | `articleId` |
| `list_articles` | 列出已发布文章 | - |
| `update_article` | 更新已发布文章 | `articleId` |
| `delete_article` | 删除已发布文章 | `articleId` |
| `list_categories` | 获取分类列表 | - |
| `list_tags` | 获取标签列表 | - |
| `get_user_info` | 获取当前用户信息 | - |

## 快速示例

### 发布文章

```
请帮我发布一篇掘金文章：
- 标题：我的 2024 技术总结
- 内容：# Hello World

这是我的第一篇博客...
- 分类：后端
- 标签：Python, MCP
```

### 查看草稿

```
列出我在掘金的所有草稿
```

### 更新文章

```
更新文章 7382918472656487462，在末尾添加「更新于 2024-01-01」
```

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `JUEJIN_COOKIE` | ✅ | Session cookie（格式：`sessionid=xxx`，有效期约 30 天） |
| `JUEJIN_AID` | ❌ | 应用 ID（默认：2608） |
| `JUEJIN_UUID` | ❌ | 用户 UUID |
| `JUEJIN_TIMEOUT` | ❌ | 请求超时秒数（默认：30） |
| `JUEJIN_MAX_RETRIES` | ❌ | 最大重试次数（默认：3） |

### ⚠️ Cookie 有效期提醒

掘金 Cookie 的有效期约为 **30 天**，过期后会导致发布失败。建议：
- 记录配置日期，定期更新
- 如遇「鉴权失败」错误，请重新获取 Cookie
- 可在浏览器无痕模式下登录获取长期有效的 Cookie

## 文档

- [API 参考](reference.md) - 完整工具文档
- [使用示例](examples.md) - 使用示例和工作流

## 相关项目

- [juejin-release-mcp](https://github.com/iceycn/juejin-release-mcp) - 底层 MCP 服务器

## 许可证

MIT
