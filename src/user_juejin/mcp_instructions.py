"""
MCP 服务端 instructions（随 initialize 下发给客户端，供模型理解约束与联调结论）。
"""

# 与 README、mcps/user-juejin/MCP_PROTOCOL.md 保持一致；修改时请同步文档。
JUEJIN_MCP_INSTRUCTIONS_ZH = """
你是掘金（juejin.cn）创作者能力扩展：通过 Cookie 调用掘金非公开 HTTP API。

## 运行前必配
- 环境变量 `JUEJIN_COOKIE`：从已登录掘金的浏览器请求头复制**完整 Cookie**（推荐）。仅 `sessionid=...` 在部分接口上可能创建草稿成功但发布失败，若遇 `err_no=2 参数错误` 或鉴权失败，请补全 Cookie，并配置与网页一致的 `JUEJIN_AID`（默认 2608）、`JUEJIN_UUID`（从 `list_by_user` 等请求的 Query 复制）。
- 可选：`JUEJIN_CSRF_TOKEN`（对应请求头 `x-secsdk-csrf-token`），当接口返回校验相关错误时从同一次浏览器请求复制。

## 联调测试结论（已实现于 HTTP 客户端）
- Python `urllib` 在部分环境会出现 `SSL: CERTIFICATE_VERIFY_FAILED`：本服务依赖 **certifi** 指定 CA 路径发起 HTTPS；若仍失败，请检查系统/公司代理与证书。
- 创建草稿：`POST .../article_draft/create?aid=...`；发布：`POST .../article/publish?aid=...&uuid=...`；我的文章列表：`POST .../article/list_by_user?aid=...&uuid=...&spider=0`。与创作者中心抓包保持一致即可。
- 工具 `publish_article` 内部顺序为：创建草稿 → 发布；`update_draft` 可设 `publishAfterUpdate=true` 实现「更新并发布」。

## 安全
- 勿在对话或仓库中粘贴完整 Cookie；日志中不得打印 Cookie。
""".strip()
