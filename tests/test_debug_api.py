"""
掘金 API 真实请求测试 - 调试版本
"""

import os
import sys
import json
import ssl
from urllib.request import Request, urlopen

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
    """获取请求头"""
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


def debug_api_response():
    """调试 API 响应"""
    cookie = os.getenv("JUEJIN_COOKIE", "")
    headers = get_headers(cookie)

    print("=" * 50)
    print("调试: 查看 API 原始响应")
    print("=" * 50)

    # 1. 测试用户信息 (GET)
    print("\n1. 用户信息接口 (GET):")
    url = "https://api.juejin.cn/user_api/v1/user/info?aid=2608"
    print(f"   URL: {url}")
    try:
        raw = request_get(url, headers)
        print(f"   返回: {json.dumps(raw, indent=4, ensure_ascii=False)[:800]}")
    except Exception as e:
        print(f"   错误: {e}")

    # 2. 测试分类列表 (POST)
    print("\n2. 分类列表接口 (POST):")
    url = "https://api.juejin.cn/tag_api/v1/query_category_list"
    print(f"   URL: {url}")
    try:
        raw = request_post(url, {}, headers)
        print(f"   返回: {json.dumps(raw, indent=4, ensure_ascii=False)[:800]}")
    except Exception as e:
        print(f"   错误: {e}")

    # 3. 测试草稿列表 (POST)
    print("\n3. 草稿列表接口 (POST):")
    url = "https://api.juejin.cn/content_api/v1/article_draft/list"
    print(f"   URL: {url}")
    try:
        raw = request_post(url, {"page_no": 1, "page_size": 5}, headers)
        print(f"   返回: {json.dumps(raw, indent=4, ensure_ascii=False)[:800]}")
    except Exception as e:
        print(f"   错误: {e}")

    # 4. 测试文章列表 (POST)
    print("\n4. 文章列表接口 (POST):")
    url = "https://api.juejin.cn/content_api/v1/article/list_by_user?aid=2608&spider=0"
    print(f"   URL: {url}")
    try:
        raw = request_post(url, {"page_no": 1, "page_size": 5}, headers)
        print(f"   返回: {json.dumps(raw, indent=4, ensure_ascii=False)[:800]}")
    except Exception as e:
        print(f"   错误: {e}")


def main():
    print("\n" + "🔍" * 25)
    print("掘金 API 调试测试")
    print("🔍" * 25 + "\n")

    cookie = os.getenv("JUEJIN_COOKIE", "")
    if not cookie:
        print("❌ 错误: JUEJIN_COOKIE 环境变量未设置")
        return 1

    print(f"✅ JUEJIN_COOKIE 已设置 (长度: {len(cookie)})\n")

    debug_api_response()
    return 0


if __name__ == "__main__":
    sys.exit(main())
