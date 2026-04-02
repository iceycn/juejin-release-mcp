# user-juejin MCP 协议与联调说明

与仓库根目录 `README.md`、`src/user_juejin/mcp_instructions.py`（随 MCP `initialize` 下发的 **instructions**）保持一致。

## 服务元数据

| 项 | 值 |
|----|-----|
| 标识 | `user-juejin`（见 `SERVER_METADATA.json`） |
| Python 包 | `user-juejin-mcp`，入口 `user_juejin.server:main` |
| 传输 | stdio（`user-juejin-mcp` 进程由客户端拉起） |

## 联调测试结论（2025-04）

1. **TLS / 证书**  
   - 使用 Python `urllib` 直连 `https://api.juejin.cn` 时，部分环境出现 `SSL: CERTIFICATE_VERIFY_FAILED`。  
   - **实现**：HTTP 客户端使用 **certifi** 的 CA 包路径创建 SSL 上下文（`pyproject.toml` 已声明依赖 `certifi`）。  
   - 若仍失败：检查公司代理、系统根证书，或在本机配置 `SSL_CERT_FILE`。

2. **Cookie 与 Query**  
   - **仅 `sessionid=...`**：实测可完成「创建草稿 + 发布」链路（在修复 TLS 后的 Python 客户端中）。  
   - **curl 仅 sessionid 时发布曾返回 `err_no=2 参数错误`**：可能与缺少 `uuid`、字段或与浏览器不完全一致有关。  
   - **推荐**：复制浏览器 **完整 Cookie**；从 `list_by_user?aid=...&uuid=...` 同步配置 `JUEJIN_AID`、`JUEJIN_UUID`；需要时在环境变量中配置 `JUEJIN_CSRF_TOKEN`（`x-secsdk-csrf-token`）。

3. **接口形态（与创作者中心一致）**  
   - 创建草稿：`POST /content_api/v1/article_draft/create?aid=...`  
   - 发布：`POST /content_api/v1/article/publish?aid=...&uuid=...`  
   - 我的文章：`POST /content_api/v1/article/list_by_user?aid=...&uuid=...&spider=0`  
   - 更新草稿：`POST /content_api/v1/article_draft/update?aid=...&uuid=...`  

4. **工具与流程**  
   - `publish_article`：内部顺序为 **创建草稿 → 发布**。  
   - `update_draft` + `publishAfterUpdate=true`：**先更新草稿再发布**。  

5. **本地一次性脚本**  
   - `scripts/publish_rootseeker_once.py`：用于连通性验证（需 `JUEJIN_COOKIE`），非 MCP 协议的一部分。

## 安全

- Cookie 等同登录态，勿写入仓库或粘贴到公开渠道。
