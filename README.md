# 掘金 MCP 服务器

[![PyPI version](https://badge.fury.io/py/user-juejin-mcp.svg)](https://pypi.org/project/user-juejin-mcp/)

掘金平台的 MCP (Model Context Protocol) 服务器，使大语言模型能够通过 MCP 协议管理掘金文章。支持 **Cursor**、**Trae**、**Claude Desktop** 等 MCP 客户端。

## 功能特性

基于掘金创作者中心 API 实现以下能力：

- **文章发布**: `publish_article` - 自动完成创建草稿和发布两步操作
- **草稿管理**: `create_draft`、`update_draft`、`delete_draft`、`list_drafts`
- **文章管理**: `list_articles`、`get_article`、`update_article`、`delete_article`
- **分类标签**: `list_categories`、`list_tags` - 获取分类和标签列表
- **用户信息**: `get_user_info` - 获取当前登录用户信息

## 前提条件

1. 拥有掘金账号并已登录
2. 获取掘金 Cookie（只需 `sessionid`）

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install user-juejin-mcp
```

或使用 uvx 无需安装即可运行：

```bash
uvx user-juejin-mcp
```

### 开发模式（从源码安装）

```bash
git clone https://github.com/yourname/user-juejin-mcp.git
cd user-juejin-mcp
pip install -e .
```

## 配置

### 获取 Cookie

1. 登录 [掘金](https://juejin.cn/)，进入创作者中心
2. 打开浏览器开发者工具 (F12)，切换到 **Network（网络）** 标签
3. 刷新页面，找到 `list_by_user` 请求
4. 在 **Request Headers** 中复制 `sessionid` 字段

![在 Network 中查看 Cookie](docs/assets/network-cookie-guide.png)

### 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `JUEJIN_COOKIE` | 是 | 掘金 Cookie，格式：`sessionid=xxx` |
| `JUEJIN_AID` | 否 | 默认 `2608` |
| `JUEJIN_UUID` | 否 | 用户唯一标识 |
| `JUEJIN_CSRF_TOKEN` | 否 | 防爬校验令牌 |
| `JUEJIN_TIMEOUT` | 否 | 请求超时（秒），默认 30 |
| `JUEJIN_MAX_RETRIES` | 否 | 最大重试次数，默认 3 |

### Cursor / Trae / Claude Desktop 配置

在 MCP 配置文件中添加：

```json
{
  "mcpServers": {
    "juejin": {
      "command": "uvx",
      "args": ["user-juejin-mcp"],
      "env": {
        "JUEJIN_COOKIE": "sessionid=your_sessionid"
      }
    }
  }
}
```

或使用 pip 安装后：

```json
{
  "mcpServers": {
    "juejin": {
      "command": "user-juejin-mcp",
      "env": {
        "JUEJIN_COOKIE": "sessionid=your_sessionid"
      }
    }
  }
}
```

### 命令行运行

```bash
# 设置环境变量并运行
export JUEJIN_COOKIE="sessionid=your_sessionid"
user-juejin-mcp
```

## 工具列表

| 工具名 | 描述 | 必填参数 |
|--------|------|----------|
| `publish_article` | 发布文章（创建草稿+发布） | title, content |
| `create_draft` | 创建草稿 | title, content |
| `update_draft` | 更新草稿 | draftId |
| `delete_draft` | 删除草稿 | draftId |
| `list_drafts` | 获取草稿列表 | - |
| `get_article` | 获取文章详情 | articleId |
| `list_articles` | 获取文章列表 | - |
| `update_article` | 更新文章 | articleId |
| `delete_article` | 删除文章 | articleId |
| `list_categories` | 获取分类列表 | - |
| `list_tags` | 获取标签列表 | - |
| `get_user_info` | 获取用户信息 | - |

## 使用示例

### 发布文章

```
请帮我发布一篇掘金文章：
- 标题：我的第一篇技术博客
- 内容：# Hello World

这是我的第一篇博客文章，介绍一下我的开源项目...
```

### 查看草稿列表

```
请列出我在掘金的所有草稿
```

### 获取分类标签

```
请显示掘金的文章分类和热门标签
```

## API 接口说明

本 MCP 服务对接的掘金 API（前缀 `https://api.juejin.cn`）：

| 接口 | 方法 | 说明 |
|------|------|------|
| `/content_api/v1/article_draft/create` | POST | 创建草稿 |
| `/content_api/v1/article_draft/update` | POST | 更新草稿 |
| `/content_api/v1/article_draft/delete` | POST | 删除草稿 |
| `/content_api/v1/article_draft/list_by_user` | POST | 草稿列表 |
| `/content_api/v1/article/publish` | POST | 发布文章 |
| `/content_api/v1/article/list_by_user` | POST | 文章列表 |
| `/tag_api/v1/query_category_list` | POST | 分类列表 |
| `/tag_api/v1/query_tag_list` | POST | 标签列表 |

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码检查
ruff check src/
mypy src/

# 本地运行
export JUEJIN_COOKIE="sessionid=xxx"
python -m user_juejin.server
```

## 发布到 PyPI

```bash
# 构建
python -m build

# 检查
twine check dist/*

# 发布到 TestPyPI（可选）
twine upload --repository testpypi dist/*

# 发布到 PyPI
twine upload dist/*
```

## 注意事项

1. **Cookie 安全**: Cookie 包含敏感信息，请勿泄露或提交到代码仓库
2. **Cookie 有效期**: Cookie 可能会过期，如遇鉴权失败请重新获取
3. **接口限制**: 掘金 API 可能有频率限制，请合理使用
4. **发布参数**: 发布文章时需要 `encrypted_word_count` 和 `origin_word_count` 参数，可从浏览器抓包获取

## 常见问题

### Q: 提示 "JUEJIN_COOKIE 环境变量未设置"

A: 请确保已正确设置环境变量，或在 MCP 配置中添加 env 配置。

### Q: 发布失败，提示鉴权错误

A: Cookie 可能已过期，请重新获取并更新。

### Q: 提示 "参数错误"

A: 发布文章时需要提供 `encrypted_word_count` 和 `origin_word_count`，请从浏览器开发者工具复制。

## 相关项目

- [apollo-mcp](https://github.com/iceycn/mcp-server-apollo) - Apollo 配置中心 MCP 服务器
- [root_seeker](https://gitee.com/icey_1/root_seeker) - AI 驱动的错误根因分析工具

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
