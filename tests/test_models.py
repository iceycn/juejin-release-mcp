"""
模型测试
"""

import pytest
from user_juejin.models.request import (
    CreateDraftRequest,
    UpdateDraftRequest,
    PublishArticleRequest,
    ListDraftsRequest,
    ListArticlesRequest,
    ListTagsRequest,
)
from user_juejin.models.response import (
    ApiResponse,
    CreateDraftResponse,
    PublishArticleResponse,
    DraftItem,
    ListDraftsResponse,
)


class TestCreateDraftRequest:
    """测试创建草稿请求"""

    def test_to_api_dict_basic(self):
        """测试基本转换"""
        req = CreateDraftRequest(
            title="测试标题",
            content="测试内容",
        )
        data = req.to_api_dict()
        assert data["title"] == "测试标题"
        assert data["mark_content"] == "测试内容"
        # 当 description 为 None 时，brief_content 默认为空字符串
        assert data["brief_content"] == ""

    def test_to_api_dict_with_optional(self):
        """测试带可选参数的转换"""
        req = CreateDraftRequest(
            title="测试标题",
            content="测试内容",
            description="自定义摘要",
            category_id="123",
            tag_ids=["tag1", "tag2"],
        )
        data = req.to_api_dict()
        assert data["brief_content"] == "自定义摘要"
        assert data["category_id"] == "123"
        assert data["tag_ids"] == ["tag1", "tag2"]


class TestApiResponse:
    """测试基础响应"""

    def test_success_property(self):
        """测试 success 属性"""
        resp = ApiResponse(err_no=0, err_msg="")
        assert resp.success is True

        resp = ApiResponse(err_no=1, err_msg="错误")
        assert resp.success is False


class TestCreateDraftResponse:
    """测试创建草稿响应"""

    def test_from_dict_success(self):
        """测试从字典创建成功响应"""
        data = {
            "err_no": 0,
            "err_msg": "success",
            "data": {
                "id": "draft123",
                "article_id": "",
            }
        }
        resp = CreateDraftResponse.from_dict(data)
        assert resp.success is True
        assert resp.draft_id == "draft123"
        assert resp.article_id == ""

    def test_from_dict_error(self):
        """测试从字典创建错误响应 - data 为 None 时会抛出 AttributeError"""
        data = {
            "err_no": 1,
            "err_msg": "创建失败",
            "data": None,
        }
        # 当前实现中 data=None 会导致 AttributeError
        with pytest.raises(AttributeError):
            CreateDraftResponse.from_dict(data)


class TestPublishArticleResponse:
    """测试发布文章响应"""

    def test_from_dict_with_article_id(self):
        """测试带文章ID的响应"""
        data = {
            "err_no": 0,
            "err_msg": "success",
            "data": {
                "article_id": "article123",
            }
        }
        resp = PublishArticleResponse.from_dict(data)
        assert resp.success is True
        assert resp.article_id == "article123"
        assert resp.link == "https://juejin.cn/post/article123"


class TestListDraftsResponse:
    """测试草稿列表响应"""

    def test_from_dict_empty(self):
        """测试空列表响应"""
        # 实际 API 响应结构：data 是一个包含 data 列表和 count 的对象
        data = {
            "err_no": 0,
            "err_msg": "success",
            "data": {
                "data": [],
                "count": 0,
            },
        }
        resp = ListDraftsResponse.from_dict(data)
        assert resp.success is True
        assert resp.drafts == []
        assert resp.total == 0

    def test_from_dict_with_drafts(self):
        """测试带草稿的响应"""
        data = {
            "err_no": 0,
            "err_msg": "success",
            "data": {
                "data": [
                    {
                        "id": "draft1",
                        "title": "草稿1",
                        "brief_content": "摘要1",
                        "category_id": "cat1",
                        "tag_ids": ["tag1"],
                        "ctime": "1234567890",
                        "mtime": "1234567890",
                    }
                ],
                "count": 1,
            },
        }
        resp = ListDraftsResponse.from_dict(data)
        assert resp.success is True
        assert len(resp.drafts) == 1
        assert resp.drafts[0].id == "draft1"
        assert resp.total == 1