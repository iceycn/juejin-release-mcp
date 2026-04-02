#!/usr/bin/env python3
"""一次性：从 RootSeeker README 摘要生成测试文并调用掘金发布（需环境变量 JUEJIN_COOKIE）。"""

from __future__ import annotations

import os
import sys

# 包路径：项目根下 src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from user_juejin.services.article_service import ArticleService  # noqa: E402


def main() -> int:
    title = "【测试】RootSeeker：面向内网的 AI 驱动错误分析与根因发现"
    description = (
        "RootSeeker 将报错日志与代码检索、全链路日志、MCP 工具编排结合，"
        "用 Plan-Act / tool_use_loop 等模式缩短根因定位时间。本文为自动化连通性测试发文。"
    )
    content = """# RootSeeker 简介（测试稿）

**RootSeeker** 是一个面向公司内网的 **AI 驱动错误分析与根因发现服务**，目标是从一条报错出发，自动还原现场、定位代码并给出可落地的修复建议。

## 核心价值

- 关联 Trace，拉取链路上下文（API / SQL / RPC）
- Zoekt + Qdrant 双引擎检索，兼顾符号与语义
- MCP 网关与 Hook 体系，便于扩展工具与流程
- 支持私有化部署，日志与代码可留在内网

## 说明

本内容由 `juejin-release-mcp` 本地脚本自动生成，用于验证 **创建草稿 + 发布** 接口是否可用。若你非作者本人，请忽略或删除。

---

- 项目主页：<https://github.com/iceycn/root_seeker>
- Gitee：<https://gitee.com/icey_1/root_seeker>
"""

    if not os.getenv("JUEJIN_COOKIE"):
        print("请设置环境变量 JUEJIN_COOKIE", file=sys.stderr)
        return 2

    svc = ArticleService()
    out = svc.publish_article(
        title=title,
        content=content,
        description=description,
    )
    print(out)
    return 0 if out.get("success") else 1


if __name__ == "__main__":
    raise SystemExit(main())
