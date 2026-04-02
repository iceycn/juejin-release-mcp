"""
掘金 API 真实请求测试 - 完整测试
"""

import os
import sys
import json
import ssl
from urllib.request import Request, urlopen
from urllib.parse import urlencode

try:
    import certifi
    _CERTIFI_CAFILE = certifi.where()
except ImportError:
    _CERTIFI_CAFILE = None

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def request_get(url: str, headers: dict, timeout: int = 30) -> dict:
    """发送 GET 请求"""
    request = Request(url, headers=headers, method="GET")
    if _CERTIFI_CAFILE:
        ssl_ctx = ssl.create_default_context(cafile=_CERTIFI_CAFILE)
    else:
        ssl_ctx = ssl.create_default_context()
    with urlopen(request, timeout=timeout, context=ssl_ctx) as response:
        return json.loads(response.read().decode("utf-8"))


def request_post(url: str, data: dict, headers: dict, timeout: int = 30) -> dict:
    """发送 POST 请求"""
    body = json.dumps(data).encode("utf-8")
    request = Request(url, data=body, headers=headers, method="POST")
    if _CERTIFI_CAFILE:
        ssl_ctx = ssl.create_default_context(cafile=_CERTIFI_CAFILE)
    else:
        ssl_ctx = ssl.create_default_context()
    with urlopen(request, timeout=timeout, context=ssl_ctx) as response:
        return json.loads(response.read().decode("utf-8"))


def get_headers(cookie: str) -> dict:
    return {
        "Cookie": cookie,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://juejin.cn",
        "Referer": "https://juejin.cn/",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
    }


def test_api():
    cookie = os.getenv("JUEJIN_COOKIE", "")
    headers = get_headers(cookie)

    results = []

    # 1. 分类列表 (POST)
    print("\n📋 测试: 分类列表")
    try:
        url = "https://api.juejin.cn/tag_api/v1/query_category_list"
        raw = request_post(url, {}, headers)
        if raw.get("err_no") == 0:
            categories = raw.get("data", [])
            print(f"   ✅ 成功! 共 {len(categories)} 个分类")
            for cat in categories[:3]:
                c = cat.get("category", {})
                print(f"      - {c.get('category_name')} (ID: {c.get('category_id')})")
            results.append(("分类列表", True, f"{len(categories)} 个分类"))
        else:
            print(f"   ❌ 失败: {raw.get('err_msg')}")
            results.append(("分类列表", False, raw.get('err_msg')))
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        results.append(("分类列表", False, str(e)))

    # 2. 文章列表 (POST) - 需要 aid/uuid
    print("\n📄 测试: 文章列表")
    try:
        url = "https://api.juejin.cn/content_api/v1/article/list_by_user?aid=2608&spider=0"
        raw = request_post(url, {"page_no": 1, "page_size": 5}, headers)
        if raw.get("err_no") == 0:
            articles = raw.get("data", [])
            print(f"   ✅ 成功! 共 {len(articles)} 篇文章")
            for art in articles[:2]:
                info = art.get("article_info", {})
                print(f"      - {info.get('title', '(无标题)')}")
            results.append(("文章列表", True, f"{len(articles)} 篇文章"))
        else:
            print(f"   ❌ 失败: {raw.get('err_msg')}")
            results.append(("文章列表", False, raw.get('err_msg')))
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        results.append(("文章列表", False, str(e)))

    # 3. 草稿列表 (POST) - 需要 aid/uuid
    print("\n📝 测试: 草稿列表")
    try:
        url = "https://api.juejin.cn/content_api/v1/article_draft/list?aid=2608"
        raw = request_post(url, {"page_no": 1, "page_size": 5}, headers)
        if raw.get("err_no") == 0:
            drafts = raw.get("data", [])
            print(f"   ✅ 成功! 共 {len(drafts)} 篇草稿")
            results.append(("草稿列表", True, f"{len(drafts)} 篇草稿"))
        else:
            print(f"   ❌ 失败: {raw.get('err_msg')}")
            results.append(("草稿列表", False, raw.get('err_msg')))
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        results.append(("草稿列表", False, str(e)))

    # 4. 标签列表 (POST)
    print("\n🏷️ 测试: 标签列表")
    try:
        url = "https://api.juejin.cn/tag_api/v1/query_tag_list"
        raw = request_post(url, {"page_no": 1, "page_size": 5}, headers)
        if raw.get("err_no") == 0:
            tags = raw.get("data", [])
            print(f"   ✅ 成功! 共 {len(tags)} 个标签")
            for tag in tags[:3]:
                t = tag.get("tag", {})
                print(f"      - {t.get('tag_name')} (ID: {t.get('tag_id')})")
            results.append(("标签列表", True, f"{len(tags)} 个标签"))
        else:
            print(f"   ❌ 失败: {raw.get('err_msg')}")
            results.append(("标签列表", False, raw.get('err_msg')))
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        results.append(("标签列表", False, str(e)))

    # 5. 创建草稿测试 (POST)
    print("\n✏️ 测试: 创建草稿")
    try:
        url = "https://api.juejin.cn/content_api/v1/article_draft/create?aid=2608"
        data = {
            "title": "测试草稿 - API测试",
            "mark_content": "这是一篇测试草稿，用于验证API功能。",
            "brief_content": "测试草稿摘要",
            "category_id": "6809637769959178254",  # 后端
            "tag_ids": ["6809640408797167623"],  # 后端标签
            "edit_type": 10,
            "html_content": "deprecated",
        }
        raw = request_post(url, data, headers)
        if raw.get("err_no") == 0:
            draft_id = raw.get("data", {}).get("id")
            print(f"   ✅ 成功! 草稿ID: {draft_id}")
            results.append(("创建草稿", True, f"草稿ID: {draft_id}"))

            # 删除测试草稿
            print("\n🗑️ 测试: 删除草稿")
            del_url = "https://api.juejin.cn/content_api/v1/article_draft/delete"
            del_raw = request_post(del_url, {"id": draft_id}, headers)
            if del_raw.get("err_no") == 0:
                print(f"   ✅ 成功! 已删除草稿 {draft_id}")
                results.append(("删除草稿", True, "已删除"))
            else:
                print(f"   ❌ 失败: {del_raw.get('err_msg')}")
                results.append(("删除草稿", False, del_raw.get('err_msg')))
        else:
            print(f"   ❌ 失败: {raw.get('err_msg')}")
            results.append(("创建草稿", False, raw.get('err_msg')))
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        results.append(("创建草稿", False, str(e)))

    return results


def main():
    print("\n" + "=" * 60)
    print("🔥 掘金 API 真实请求测试")
    print("=" * 60)

    cookie = os.getenv("JUEJIN_COOKIE", "")
    if not cookie:
        print("\n❌ 错误: JUEJIN_COOKIE 环境变量未设置")
        return 1

    print(f"\n✅ JUEJIN_COOKIE 已设置 (长度: {len(cookie)})")

    results = test_api()

    # 汇总
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)

    success_count = sum(1 for _, ok, _ in results if ok)
    for name, ok, detail in results:
        status = "✅" if ok else "❌"
        print(f"{status} {name}: {detail}")

    print(f"\n总计: {success_count}/{len(results)} 项通过")

    return 0 if success_count == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
