# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2025-04-02

### Added
- MCP `initialize`：**instructions**（`mcp_instructions.py`），写入联调结论与使用约束
- `mcps/user-juejin/MCP_PROTOCOL.md`：TLS、Cookie、接口形态、测试结论
- `SERVER_METADATA.json` 扩展：`version`、`description`、`runtime` 条目

### Changed
- HTTP 客户端：`certifi` 不可用时回退系统默认 SSL 上下文
- `publish_article.json` 工具描述补充协议与联调说明
- `article_draft/create`、`article_draft/update`、`article/publish`、`article/list_by_user` 请求 URL 统一附加 `aid`、`uuid`（及列表接口 `spider=0`），与创作者中心一致
- `update_draft` 支持完整草稿字段及 `publishAfterUpdate`（更新后调用 `article/publish`）
- `PublishArticleRequest` 支持可选 `encrypted_word_count`、`origin_word_count`
- 请求头增加 `Origin`/`Referer`，可选 `JUEJIN_CSRF_TOKEN`（`x-secsdk-csrf-token`）
- `list_articles` 支持 `keyword`、`auditStatus`

### Fixed
- 部分环境 `SSL: CERTIFICATE_VERIFY_FAILED`：使用 certifi CA 路径（0.1.0 已引入依赖，本版文档与 instructions 对齐）

## [0.1.0] - 2025-04-02

### Added
- 首个发布版本
- 文章发布功能 (`publish_article`)
- 草稿管理功能 (`create_draft`, `update_draft`, `delete_draft`, `list_drafts`)
- 文章管理功能 (`get_article`, `list_articles`, `update_article`, `delete_article`)
- 分类标签功能 (`list_categories`, `list_tags`)
- 用户信息查询 (`get_user_info`)
- MCP stdio 模式支持
- PyPI 发布支持

### Security
- Cookie 通过环境变量注入，不落盘存储
