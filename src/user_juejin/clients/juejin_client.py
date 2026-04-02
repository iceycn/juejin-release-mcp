"""
掘金 API 客户端
封装所有掘金平台 API 调用
"""

import json
import logging
import ssl
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

try:
    import certifi

    _CERTIFI_CAFILE = certifi.where()
except ImportError:
    _CERTIFI_CAFILE = None  # 回退为系统默认 CA（部分环境可能仍报 SSL 错误，请安装 certifi）

from ..config import JuejinConfig
from ..models.request import (
    CreateDraftRequest,
    UpdateDraftRequest,
    PublishArticleRequest,
    ListDraftsRequest,
    ListArticlesRequest,
    ListTagsRequest,
)
from ..models.response import (
    CreateDraftResponse,
    PublishArticleResponse,
    ListDraftsResponse,
    ListArticlesResponse,
    ListCategoriesResponse,
    ListTagsResponse,
    UserInfo,
)

logger = logging.getLogger(__name__)


class JuejinClient:
    """掘金 API 客户端"""
    
    # API 端点
    CREATE_DRAFT_URL = "https://api.juejin.cn/content_api/v1/article_draft/create"
    UPDATE_DRAFT_URL = "https://api.juejin.cn/content_api/v1/article_draft/update"
    DELETE_DRAFT_URL = "https://api.juejin.cn/content_api/v1/article_draft/delete"
    LIST_DRAFTS_URL = "https://api.juejin.cn/content_api/v1/article_draft/list"
    
    PUBLISH_ARTICLE_URL = "https://api.juejin.cn/content_api/v1/article/publish"
    UPDATE_ARTICLE_URL = "https://api.juejin.cn/content_api/v1/article/update"
    DELETE_ARTICLE_URL = "https://api.juejin.cn/content_api/v1/article/delete"
    GET_ARTICLE_URL = "https://api.juejin.cn/content_api/v1/article/detail"
    LIST_ARTICLES_URL = "https://api.juejin.cn/content_api/v1/article/list_by_user"
    
    LIST_CATEGORIES_URL = "https://api.juejin.cn/tag_api/v1/query_category_list"
    LIST_TAGS_URL = "https://api.juejin.cn/tag_api/v1/query_tag_list"
    SEARCH_TAGS_URL = "https://api.juejin.cn/recommend_api/v1/tag/recommend/search"
    
    USER_INFO_URL = "https://api.juejin.cn/user_api/v1/user/info"
    
    ARTICLE_LINK_TEMPLATE = "https://juejin.cn/post/%s"
    
    def __init__(self, config: Optional[JuejinConfig] = None):
        self.config = config or JuejinConfig.from_env()
        self.config.validate()
    
    def _build_aid_uuid_url(self, base_url: str, extra_params: Optional[list[str]] = None) -> str:
        """与浏览器一致：在 create/update/publish/list 等接口上附加 aid、uuid（及可选参数）。"""
        params: list[str] = []
        if self.config.aid:
            params.append(f"aid={self.config.aid}")
        if self.config.uuid:
            params.append(f"uuid={self.config.uuid}")
        if extra_params:
            params.extend(extra_params)
        if not params:
            return base_url
        return f"{base_url}?{'&'.join(params)}"

    def _get_headers(self) -> dict:
        """获取请求头（贴近创作者中心请求，便于与 Cookie 配合通过校验）"""
        h = {
            "Cookie": self.config.cookie,
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Origin": "https://juejin.cn",
            "Referer": "https://juejin.cn/",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
        }
        if self.config.csrf_token:
            h["x-secsdk-csrf-token"] = self.config.csrf_token
        return h
    
    def _request(self, url: str, data: dict) -> dict:
        """发送 HTTP 请求"""
        headers = self._get_headers()
        body = json.dumps(data).encode("utf-8")
        
        request = Request(url, data=body, headers=headers, method="POST")
        
        try:
            if _CERTIFI_CAFILE:
                ssl_ctx = ssl.create_default_context(cafile=_CERTIFI_CAFILE)
            else:
                ssl_ctx = ssl.create_default_context()
            with urlopen(request, timeout=self.config.timeout, context=ssl_ctx) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as e:
            logger.error(f"HTTP error: {e.code} - {e.reason}")
            return {"err_no": e.code, "err_msg": f"HTTP error: {e.reason}"}
        except URLError as e:
            logger.error(f"URL error: {e.reason}")
            return {"err_no": -1, "err_msg": f"Network error: {e.reason}"}
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return {"err_no": -1, "err_msg": str(e)}
    
    # ==================== 草稿管理 ====================
    
    def create_draft(self, req: CreateDraftRequest) -> CreateDraftResponse:
        """创建草稿"""
        data = req.to_api_dict()
        # 设置默认值
        if not data.get("category_id"):
            data["category_id"] = self.config.default_category_id
        if not data.get("tag_ids"):
            data["tag_ids"] = [self.config.default_tag_id]
        
        url = self._build_aid_uuid_url(self.CREATE_DRAFT_URL)
        result = self._request(url, data)
        return CreateDraftResponse.from_dict(result)
    
    def update_draft(self, req: UpdateDraftRequest) -> CreateDraftResponse:
        """更新草稿（URL 需带 aid、uuid，与网页 article_draft/update?aid=&uuid= 一致）"""
        data = req.to_api_dict()
        url = self._build_aid_uuid_url(self.UPDATE_DRAFT_URL)
        result = self._request(url, data)
        return CreateDraftResponse.from_dict(result)
    
    def delete_draft(self, draft_id: str) -> dict:
        """删除草稿"""
        data = {"id": draft_id}
        return self._request(self.DELETE_DRAFT_URL, data)
    
    def list_drafts(self, req: Optional[ListDraftsRequest] = None) -> ListDraftsResponse:
        """获取草稿列表"""
        req = req or ListDraftsRequest()
        data = req.to_api_dict()
        result = self._request(self.LIST_DRAFTS_URL, data)
        return ListDraftsResponse.from_dict(result)
    
    # ==================== 文章管理 ====================
    
    def publish_article(self, req: PublishArticleRequest) -> PublishArticleResponse:
        """发布文章（URL 需带 aid、uuid，与网页 article/publish?aid=&uuid= 一致）"""
        url = self._build_aid_uuid_url(self.PUBLISH_ARTICLE_URL)
        data = req.to_api_dict()
        result = self._request(url, data)
        return PublishArticleResponse.from_dict(result, self.ARTICLE_LINK_TEMPLATE)
    
    def get_article(self, article_id: str) -> dict:
        """获取文章详情"""
        data = {"article_id": article_id}
        return self._request(self.GET_ARTICLE_URL, data)
    
    def list_articles(self, req: Optional[ListArticlesRequest] = None) -> ListArticlesResponse:
        """获取文章列表"""
        req = req or ListArticlesRequest()
        data = req.to_api_dict()
        
        url = self._build_aid_uuid_url(self.LIST_ARTICLES_URL, extra_params=["spider=0"])
        
        result = self._request(url, data)
        return ListArticlesResponse.from_dict(result)
    
    def update_article(self, article_id: str, **kwargs) -> dict:
        """更新文章"""
        data = {"article_id": article_id, **kwargs}
        return self._request(self.UPDATE_ARTICLE_URL, data)
    
    def delete_article(self, article_id: str) -> dict:
        """删除文章"""
        data = {"article_id": article_id}
        return self._request(self.DELETE_ARTICLE_URL, data)
    
    # ==================== 分类标签 ====================
    
    def list_categories(self) -> ListCategoriesResponse:
        """获取分类列表"""
        result = self._request(self.LIST_CATEGORIES_URL, {})
        return ListCategoriesResponse.from_dict(result)
    
    def list_tags(self, req: Optional[ListTagsRequest] = None) -> ListTagsResponse:
        """获取标签列表"""
        req = req or ListTagsRequest()
        data = req.to_api_dict()
        url = self.SEARCH_TAGS_URL if req.keyword else self.LIST_TAGS_URL
        result = self._request(url, data)
        return ListTagsResponse.from_dict(result)
    
    # ==================== 用户信息 ====================
    
    def get_user_info(self) -> UserInfo:
        """获取用户信息"""
        result = self._request(self.USER_INFO_URL, {})
        return UserInfo.from_dict(result)
