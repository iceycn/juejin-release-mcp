"""
响应数据模型
"""

from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class ApiResponse:
    """API 响应基类"""
    err_no: int = 0
    err_msg: str = ""
    
    @property
    def success(self) -> bool:
        return self.err_no == 0


@dataclass
class CreateDraftResponse(ApiResponse):
    """创建草稿响应"""
    draft_id: str = ""
    article_id: str = ""
    
    @classmethod
    def from_dict(cls, data: dict) -> "CreateDraftResponse":
        return cls(
            err_no=data.get("err_no", 0),
            err_msg=data.get("err_msg", ""),
            draft_id=data.get("data", {}).get("id", ""),
            article_id=data.get("data", {}).get("article_id", ""),
        )


@dataclass
class PublishArticleResponse(ApiResponse):
    """发布文章响应"""
    article_id: str = ""
    link: str = ""
    
    @classmethod
    def from_dict(cls, data: dict, article_link_template: str = "https://juejin.cn/post/%s") -> "PublishArticleResponse":
        article_id = data.get("data", {}).get("article_id", "")
        return cls(
            err_no=data.get("err_no", 0),
            err_msg=data.get("err_msg", ""),
            article_id=article_id,
            link=article_link_template % article_id if article_id else "",
        )


@dataclass
class DraftItem:
    """草稿项"""
    id: str
    title: str
    content: str = ""
    brief_content: str = ""
    category_id: str = ""
    tag_ids: list[str] = field(default_factory=list)
    ctime: str = ""
    mtime: str = ""
    status: int = 0


@dataclass
class ListDraftsResponse(ApiResponse):
    """草稿列表响应"""
    drafts: list[DraftItem] = field(default_factory=list)
    total: int = 0
    
    @classmethod
    def from_dict(cls, data: dict) -> "ListDraftsResponse":
        drafts = []
        for item in data.get("data", {}).get("data", []):
            drafts.append(DraftItem(
                id=item.get("id", ""),
                title=item.get("title", ""),
                content=item.get("mark_content", ""),
                brief_content=item.get("brief_content", ""),
                category_id=item.get("category_id", ""),
                tag_ids=item.get("tag_ids", []),
                ctime=item.get("ctime", ""),
                mtime=item.get("mtime", ""),
                status=item.get("status", 0),
            ))
        return cls(
            err_no=data.get("err_no", 0),
            err_msg=data.get("err_msg", ""),
            drafts=drafts,
            total=data.get("data", {}).get("count", 0),
        )


@dataclass
class ArticleItem:
    """文章项"""
    article_id: str
    title: str
    content: str = ""
    brief_content: str = ""
    category_id: str = ""
    tag_ids: list[str] = field(default_factory=list)
    view_count: int = 0
    digg_count: int = 0
    comment_count: int = 0
    collect_count: int = 0
    ctime: str = ""
    rtime: str = ""
    status: int = 0
    audit_status: int = 0
    cover_image: str = ""


@dataclass
class ListArticlesResponse(ApiResponse):
    """文章列表响应"""
    articles: list[ArticleItem] = field(default_factory=list)
    total: int = 0
    has_more: bool = False
    
    @classmethod
    def from_dict(cls, data: dict) -> "ListArticlesResponse":
        articles = []
        article_data = data.get("data", {})
        for item in article_data.get("data", []):
            articles.append(ArticleItem(
                article_id=str(item.get("article_id", "")),
                title=item.get("title", ""),
                content=item.get("mark_content", ""),
                brief_content=item.get("brief_content", ""),
                category_id=item.get("category_id", ""),
                tag_ids=item.get("tag_ids", []),
                view_count=item.get("view_count", 0),
                digg_count=item.get("digg_count", 0),
                comment_count=item.get("comment_count", 0),
                collect_count=item.get("collect_count", 0),
                ctime=item.get("ctime", ""),
                rtime=item.get("rtime", ""),
                status=item.get("status", 0),
                audit_status=item.get("audit_status", 0),
                cover_image=item.get("cover_image", ""),
            ))
        return cls(
            err_no=data.get("err_no", 0),
            err_msg=data.get("err_msg", ""),
            articles=articles,
            total=article_data.get("count", 0),
            has_more=article_data.get("has_more", False),
        )


@dataclass
class CategoryItem:
    """分类项"""
    category_id: str
    category_name: str
    category_url: str = ""


@dataclass
class ListCategoriesResponse(ApiResponse):
    """分类列表响应"""
    categories: list[CategoryItem] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: dict) -> "ListCategoriesResponse":
        categories = []
        for item in data.get("data", {}).get("categories", []):
            categories.append(CategoryItem(
                category_id=item.get("category_id", ""),
                category_name=item.get("category_name", ""),
                category_url=item.get("category_url", ""),
            ))
        return cls(
            err_no=data.get("err_no", 0),
            err_msg=data.get("err_msg", ""),
            categories=categories,
        )


@dataclass
class TagItem:
    """标签项"""
    tag_id: str
    tag_name: str
    tag_url: str = ""
    article_count: int = 0


@dataclass
class ListTagsResponse(ApiResponse):
    """标签列表响应"""
    tags: list[TagItem] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: dict) -> "ListTagsResponse":
        tags = []
        for item in data.get("data", {}).get("tags", []):
            tags.append(TagItem(
                tag_id=item.get("tag_id", ""),
                tag_name=item.get("tag_name", ""),
                tag_url=item.get("tag_url", ""),
                article_count=item.get("article_count", 0),
            ))
        return cls(
            err_no=data.get("err_no", 0),
            err_msg=data.get("err_msg", ""),
            tags=tags,
        )


@dataclass
class UserInfo(ApiResponse):
    """用户信息"""
    user_id: str = ""
    user_name: str = ""
    avatar_url: str = ""
    company: str = ""
    job_title: str = ""
    level: int = 0
    article_count: int = 0
    digg_count: int = 0
    follower_count: int = 0
    
    @classmethod
    def from_dict(cls, data: dict) -> "UserInfo":
        user_data = data.get("data", {})
        return cls(
            err_no=data.get("err_no", 0),
            err_msg=data.get("err_msg", ""),
            user_id=str(user_data.get("user_id", "")),
            user_name=user_data.get("user_name", ""),
            avatar_url=user_data.get("avatar_url", ""),
            company=user_data.get("company", ""),
            job_title=user_data.get("job_title", ""),
            level=user_data.get("level", 0),
            article_count=user_data.get("article_count", 0),
            digg_count=user_data.get("digg_count", 0),
            follower_count=user_data.get("follower_count", 0),
        )
