# 掘金 MCP 项目代码实施计划

## 一、项目概述

基于本地 `apollo-mcp` 项目结构规范，参考 `mcp-server-article-main` 的掘金 API 实现细节，构建掘金 MCP 服务器，支持自动发文及其他掘金平台功能。

---

## 二、项目结构设计

### 2.1 目录结构（完全参考 apollo-mcp）

```
mcps/user-juejin/
├── SERVER_METADATA.json          # 服务器元数据（必需）
├── tools/                        # 工具定义目录（必需）
│   ├── publish_article.json      # 发布文章
│   ├── create_draft.json         # 创建草稿
│   ├── update_draft.json         # 更新草稿
│   ├── delete_draft.json         # 删除草稿
│   ├── list_drafts.json          # 获取草稿列表
│   ├── get_article.json          # 获取文章详情
│   ├── update_article.json       # 更新文章
│   ├── delete_article.json       # 删除文章
│   ├── list_articles.json        # 获取文章列表
│   ├── list_categories.json      # 获取分类列表
│   ├── list_tags.json            # 获取标签列表
│   ├── search_tags.json          # 搜索标签
│   └── get_user_info.json        # 获取用户信息
└── prompts/                      # 提示词目录（可选）
    └── article_writing_guide.json
```

### 2.2 SERVER_METADATA.json 格式

```json
{
  "serverIdentifier": "user-juejin",
  "serverName": "juejin"
}
```

---

## 三、工具定义规范

### 3.1 工具 JSON 文件格式

每个工具定义文件遵循以下结构（与 apollo-mcp 一致）：

| 字段 | 说明 |
|------|------|
| `name` | 工具名称，与文件名（不含 `.json`）一致 |
| `description` | 中文描述，说明用途与约束 |
| `arguments` | JSON Schema：`type: object`，含 `properties` 与 `required` |

示例骨架：

```json
{
  "name": "publish_article",
  "description": "发布文章到掘金：先创建草稿再发布。需配置 JUEJIN_COOKIE。",
  "arguments": {
    "type": "object",
    "properties": {
      "title": { "type": "string", "description": "文章标题" },
      "content": { "type": "string", "description": "正文，Markdown" },
      "description": { "type": "string", "description": "摘要，可选；为空则从正文截取" },
      "categoryId": { "type": "string", "description": "分类 ID，可选" },
      "tagIds": {
        "type": "array",
        "items": { "type": "string" },
        "description": "标签 ID 列表，可选"
      }
    },
    "required": ["title", "content"]
  }
}
```

### 3.2 prompts 格式（可选，参考 user-plantuml）

```json
{
  "name": "article_writing_guide",
  "description": "掘金发文时的写作与合规提示",
  "arguments": []
}
```

---

## 四、掘金 API 实现细节（参考 mcp-server-article-main）

### 4.1 自动发文主流程

1. **创建草稿** `POST https://api.juejin.cn/content_api/v1/article_draft/create`
2. **发布文章** `POST https://api.juejin.cn/content_api/v1/article/publish?aid=...&uuid=...`

### 4.2 创建草稿请求字段映射

| 业务含义 | 请求字段（蛇形） | 说明 |
|----------|------------------|------|
| 标题 | `title` | 必填 |
| 摘要 | `brief_content` | 可选；可从 Markdown 转纯文本后截断（如 100 字） |
| 正文 | `mark_content` | Markdown |
| 编辑类型 | `edit_type` | 示例：`10` |
| HTML 占位 | `html_content` | 示例：`"deprecated"` |
| 分类 | `category_id` | 可选 |
| 标签 | `tag_ids` | 字符串数组 |

### 4.3 发布请求字段映射

| 业务含义 | 请求字段 | 说明 |
|----------|----------|------|
| 草稿 ID | `draft_id` | 创建草稿返回 |
| 同步组织 | `sync_to_org` | 示例：`false` |
| 专栏 | `column_ids` | 示例：`[]` |
| 话题 | `theme_ids` | 示例：`[]` |

### 4.4 响应与错误

- 业务成功：`err_no === 0`
- 文章链接：`https://juejin.cn/post/{articleId}`
- 鉴权：请求头携带 `Cookie: <JUEJIN_COOKIE>`

### 4.5 环境变量

```bash
JUEJIN_COOKIE=        # 必填，浏览器登录后 Cookie
JUEJIN_AID=2608       # 发布 URL 查询参数，可与 Java 示例对齐
JUEJIN_UUID=          # 发布 URL 查询参数，与当前账号/端一致
```

---

## 五、Python 包与代码布局（实现层，用于 PyPI 发布）

`mcps/user-juejin/` 仅描述 MCP 工具；可执行实现建议放在仓库根或独立子包，便于 `pip install`：

```
juejin-release-mcp/
├── mcps/user-juejin/           # 与 apollo-mcp 对齐的描述符
├── pyproject.toml
├── src/
│   └── user_juejin/
│       ├── __init__.py
│       ├── server.py           # MCP stdio 入口，注册工具
│       ├── config.py
│       ├── clients/juejin_client.py
│       └── services/
│           ├── article_service.py
│           └── draft_service.py
└── README.md
```

- 包名建议：`user-juejin-mcp`（PyPI 上需查重）
- Python：`>=3.10`
- 入口脚本：`user-juejin-mcp = user_juejin.server:main`（在 `pyproject.toml` 的 `[project.scripts]` 中声明）

---

## 六、PyPI 发布流程

1. **本地构建**：`python -m build`
2. **检查**：`twine check dist/*`
3. **测试索引（可选）**：`twine upload --repository testpypi dist/*`
4. **正式上传**：`twine upload dist/*`
5. **验证**：新建 venv，`pip install user-juejin-mcp==x.y.z`，运行 CLI 与 Cursor MCP 联调

版本遵循语义化版本；每次发版更新 `CHANGELOG.md`。

---

## 七、工具优先级与里程碑

| 阶段 | 工具 | 说明 |
|------|------|------|
| P0 | `publish_article`、`create_draft`、`list_categories` | 打通自动发文 |
| P1 | `list_drafts`、`update_draft`、`delete_draft`、`list_tags`、`search_tags`、`get_user_info` | 运营与元数据 |
| P2 | `get_article`、`list_articles`、`update_article`、`delete_article` | 已发文管理（依赖具体接口选型） |

---

## 八、测试与验收

- 单元测试：参数校验、错误码解析、`err_no` 分支
- 集成测试：真实 `JUEJIN_COOKIE` 下执行 `publish_article`，断言返回链接可访问
- 验收：描述符与 apollo-mcp 风格一致；P0 工具可用；PyPI 可安装

---

## 九、风险与注意

- 掘金非公开 API 可能变更：集中封装 `juejin_client`，版本化 URL/字段
- Cookie 失效：统一错误提示，避免日志打印完整 Cookie
- 发布 URL 的 `aid`、`uuid` 需与线上一致，否则与 Java 示例行为可能不同
