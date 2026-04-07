# 掘金 MCP 完整 API 参考

## 工具详细说明

### publish_article

一键发布文章到掘金（自动完成创建草稿 + 发布）。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | 文章标题 |
| `content` | string | ✅ | 文章正文，Markdown 格式 |
| `description` | string | ❌ | 文章摘要，为空时自动提取 |
| `categoryId` | string | ❌ | 分类 ID |
| `tagIds` | array | ❌ | 标签 ID 列表 |

**返回值：**

```json
{
  "success": true,
  "article_id": "7382918472656487462",
  "link": "https://juejin.cn/post/7382918472656487462"
}
```

---

### create_draft

创建文章草稿，不自动发布。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | 文章标题 |
| `content` | string | ✅ | 文章正文 |
| `description` | string | ❌ | 摘要 |
| `categoryId` | string | ❌ | 分类 ID |
| `tagIds` | array | ❌ | 标签 ID 列表 |
| `coverImage` | string | ❌ | 封面图片 URL |

---

### update_draft

更新草稿内容。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `draftId` | string | ✅ | 草稿 ID |
| `title` | string | ❌ | 标题 |
| `content` | string | ❌ | 正文 |
| `description` | string | ❌ | 摘要 |
| `categoryId` | string | ❌ | 分类 ID |
| `tagIds` | array | ❌ | 标签列表 |
| `publishAfterUpdate` | boolean | ❌ | 更新后是否立即发布 |

---

### delete_draft

删除指定草稿。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `draftId` | string | ✅ | 草稿 ID |

---

### list_drafts

获取当前用户的草稿列表。

**参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `page` | integer | ❌ | 1 | 页码 |
| `pageSize` | integer | ❌ | 10 | 每页数量 |

---

### get_article

获取单篇文章详情。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `articleId` | string | ✅ | 文章 ID |

---

### list_articles

获取当前用户的文章列表。

**参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `page` | integer | ❌ | 1 | 页码 |
| `pageSize` | integer | ❌ | 10 | 每页数量 |
| `keyword` | string | ❌ | - | 搜索关键词 |
| `auditStatus` | integer | ❌ | - | 审核状态 |

---

### update_article

更新已发布的文章。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `articleId` | string | ✅ | 文章 ID |
| `title` | string | ❌ | 标题 |
| `content` | string | ❌ | 正文 |
| `description` | string | ❌ | 摘要 |
| `categoryId` | string | ❌ | 分类 ID |
| `tagIds` | array | ❌ | 标签列表 |

---

### delete_article

删除已发布的文章（不可恢复）。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `articleId` | string | ✅ | 文章 ID |

---

### list_categories

获取所有可用的文章分类。

**返回值示例：**

```json
{
  "success": true,
  "categories": [
    {"id": "6809637769959178254", "name": "后端"},
    {"id": "6809637769959178253", "name": "前端"},
    {"id": "6809637769959178255", "name": "Android"},
    {"id": "6809637769959178256", "name": "iOS"},
    {"id": "6809637769959178257", "name": "人工智能"},
    {"id": "6809637769959178258", "name": "开发工具"},
    {"id": "6809637769959178259", "name": "代码人生"},
    {"id": "6809637769959178260", "name": "阅读"}
  ]
}
```

---

### list_tags

获取标签列表，支持搜索。

**参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `keyword` | string | ❌ | - | 搜索关键词 |
| `page` | integer | ❌ | 1 | 页码 |
| `pageSize` | integer | ❌ | 20 | 每页数量 |

---

### get_user_info

获取当前登录用户信息，用于验证 Cookie 有效性。

**返回值示例：**

```json
{
  "success": true,
  "user_id": "123456789",
  "user_name": "用户名",
  "avatar_url": "https://...",
  "company": "公司名",
  "job_title": "职位",
  "level": 3,
  "article_count": 10,
  "follower_count": 100
}
```

## 掘金 API 端点

本服务对接的掘金 API（前缀 `https://api.juejin.cn`）：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/content_api/v1/article_draft/create` | POST | 创建草稿 |
| `/content_api/v1/article_draft/update` | POST | 更新草稿 |
| `/content_api/v1/article_draft/delete` | POST | 删除草稿 |
| `/content_api/v1/article_draft/list_by_user` | POST | 草稿列表 |
| `/content_api/v1/article/publish` | POST | 发布文章 |
| `/content_api/v1/article/list_by_user` | POST | 文章列表 |
| `/tag_api/v1/query_category_list` | POST | 分类列表 |
| `/tag_api/v1/query_tag_list` | POST | 标签列表 |

## 常见问题

### Q: 提示 "JUEJIN_COOKIE 环境变量未设置"

确保已正确设置环境变量，或在 MCP 配置中添加 `env` 配置。

### Q: 发布失败，提示鉴权错误

Cookie 可能已过期，请重新获取并更新。

### Q: 提示 "参数错误"

检查必填参数是否正确传递，特别是 `title` 和 `content` 字段。

## 注意事项

1. **Cookie 安全**：Cookie 包含敏感信息，请勿泄露或提交到代码仓库
2. **Cookie 有效期**：Cookie 可能会过期，如遇鉴权失败请重新获取
3. **接口限制**：掘金 API 可能有频率限制，请合理使用
