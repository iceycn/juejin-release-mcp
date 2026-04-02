"""
掘金 API 真实请求测试 - 使用完整 Cookie 和 UUID
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


def test_with_full_cookie():
    """使用完整 Cookie 测试"""
    # 从 curl 中提取的信息
    uuid = "7490587164528739867"
    cookie = '_tea_utm_cache_2608=undefined; __tea_cookie_tokens_2608=%257B%2522web_id%2522%253A%25227490587164528739867%2522%252C%2522user_unique_id%2522%253A%25227490587164528739867%2522%252C%2522timestamp%2522%253A1744038246421%257D; passport_csrf_token=cc8de54b42522649f06418716bc1a7ff; passport_csrf_token_default=cc8de54b42522649f06418716bc1a7ff; n_mh=MLV3FfM13Hf5_yPSM3_61MCJyoOsdsi1PXLocnXs_Y4; is_staff_user=false; csrf_session_id=82d93eec7892bc5a73f41cf46eeb6144; _tea_utm_cache_576092=undefined; passport_auth_status=b046cf89d796b35a85bf85c116b3cc37%2Cb465791f22516da45bfb03cadac8e172; passport_auth_status_ss=b046cf89d796b35a85bf85c116b3cc37%2Cb465791f22516da45bfb03cadac8e172; has_biz_token=false; sid_guard=dc673cde72c7c81539d2fa39e65f532e%7C1775030758%7C31536000%7CThu%2C+01-Apr-2027+08%3A05%3A58+GMT; uid_tt=1cf27f34bdcde714fd471720ab657406; uid_tt_ss=1cf27f34bdcde714fd471720ab657406; sid_tt=dc673cde72c7c81539d2fa39e65f532e; sessionid=dc673cde72c7c81539d2fa39e65f532e; sessionid_ss=dc673cde72c7c81539d2fa39e65f532e; session_tlb_tag=sttt%7C1%7C3Gc83nLHyBU50vo55l9TLv_________QBtiNXMncxmOONZYwow763xXh6wslVLlmv2NrDdqzYj4%3D; sid_ucp_v1=1.0.0-KDUxMjM3NjhkYTA2YWU0MTgzYjNlMTAyZDY0YmMyMWIxMTRkNWE5YWUKFwi6_LDnqq3OBBDmo7POBhiwFDgCQO8HGgJscSIgZGM2NzNjZGU3MmM3YzgxNTM5ZDJmYTM5ZTY1ZjUzMmU; ssid_ucp_v1=1.0.0-KDUxMjM3NjhkYTA2YWU0MTgzYjNlMTAyZDY0YmMyMWIxMTRkNWE5YWUKFwi6_LDnqq3OBBDmo7POBhiwFDgCQO8HGgJscSIgZGM2NzNjZGU3MmM3YzgxNTM5ZDJmYTM5ZTY1ZjUzMmU'

    headers = {
        "Cookie": cookie,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://juejin.cn",
        "Referer": "https://juejin.cn/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "x-secsdk-csrf-token": "000100000001aa18e22d22dcf09e3ec12f241f23ec229f4c899a60758e27a5a31135eadd8eef18a2790e04483215",
    }

    results = []

    # 1. 文章列表 (使用完整 aid/uuid)
    print("\n📄 测试: 文章列表 (完整Cookie)")
    try:
        url = f"https://api.juejin.cn/content_api/v1/article/list_by_user?aid=2608&uuid={uuid}&spider=0"
        raw = request_post(url, {"audit_status": None, "keyword": "", "page_size": 10, "page_no": 1}, headers)
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

    # 2. 草稿列表 (使用完整 aid/uuid)
    print("\n📝 测试: 草稿列表 (完整Cookie)")
    try:
        url = f"https://api.juejin.cn/content_api/v1/article_draft/list?aid=2608&uuid={uuid}"
        raw = request_post(url, {"page_no": 1, "page_size": 10}, headers)
        if raw.get("err_no") == 0:
            drafts = raw.get("data", [])
            print(f"   ✅ 成功! 共 {len(drafts)} 篇草稿")
            for draft in drafts[:2]:
                print(f"      - {draft.get('title', '(无标题)')} (ID: {draft.get('id')})")
            results.append(("草稿列表", True, f"{len(drafts)} 篇草稿"))
        else:
            print(f"   ❌ 失败: {raw.get('err_msg')}")
            results.append(("草稿列表", False, raw.get('err_msg')))
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        results.append(("草稿列表", False, str(e)))

    # 3. 创建草稿
    print("\n✏️ 测试: 创建草稿 (完整Cookie)")
    draft_id = None
    try:
        url = f"https://api.juejin.cn/content_api/v1/article_draft/create?aid=2608&uuid={uuid}"
        data = {
            "title": "测试草稿 - API测试",
            "mark_content": "这是一篇测试草稿，用于验证API功能。",
            "brief_content": "测试草稿摘要",
            "category_id": "6809637769959178254",
            "tag_ids": ["6809640408797167623"],
            "edit_type": 10,
            "html_content": "deprecated",
        }
        raw = request_post(url, data, headers)
        if raw.get("err_no") == 0:
            draft_id = raw.get("data", {}).get("id")
            print(f"   ✅ 成功! 草稿ID: {draft_id}")
            results.append(("创建草稿", True, f"草稿ID: {draft_id}"))
        else:
            print(f"   ❌ 失败: {raw.get('err_msg')}")
            results.append(("创建草稿", False, raw.get('err_msg')))
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        results.append(("创建草稿", False, str(e)))

    # 4. 发布草稿
    if draft_id:
        print("\n🚀 测试: 发布草稿")
        try:
            url = f"https://api.juejin.cn/content_api/v1/article/publish?aid=2608&uuid={uuid}"
            data = {
                "draft_id": draft_id,
                "sync_to_org": False,
                "column_ids": [],
                "theme_ids": [],
            }
            raw = request_post(url, data, headers)
            if raw.get("err_no") == 0:
                article_id = raw.get("data", {}).get("article_id")
                print(f"   ✅ 成功! 文章ID: {article_id}")
                print(f"   链接: https://juejin.cn/post/{article_id}")
                results.append(("发布文章", True, f"文章ID: {article_id}"))
            else:
                print(f"   ❌ 失败: {raw.get('err_msg')}")
                results.append(("发布文章", False, raw.get('err_msg')))
        except Exception as e:
            print(f"   ❌ 异常: {e}")
            results.append(("发布文章", False, str(e)))

    return results


def main():
    print("\n" + "=" * 60)
    print("🔥 掘金 API 真实请求测试 - 完整 Cookie")
    print("=" * 60)

    results = test_with_full_cookie()

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
