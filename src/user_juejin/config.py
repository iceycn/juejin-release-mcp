"""
配置管理模块
"""

import os
from dataclasses import dataclass


@dataclass
class JuejinConfig:
    """掘金 API 配置"""
    
    cookie: str = ""
    aid: str = "2608"
    uuid: str = ""
    # 与浏览器一致时部分接口需要（可选，见 README）
    csrf_token: str = ""
    
    # API 端点
    base_url: str = "https://api.juejin.cn"
    
    # 请求配置
    timeout: int = 30
    max_retries: int = 3
    
    # 默认值
    default_category_id: str = "6809637769959178254"  # 后端分类
    default_tag_id: str = "6809640408797167623"  # 后端标签
    
    @classmethod
    def from_env(cls) -> "JuejinConfig":
        """从环境变量加载配置"""
        return cls(
            cookie=os.getenv("JUEJIN_COOKIE", ""),
            aid=os.getenv("JUEJIN_AID", "2608"),
            uuid=os.getenv("JUEJIN_UUID", ""),
            csrf_token=os.getenv("JUEJIN_CSRF_TOKEN", os.getenv("JUEJIN_SECSDK_CSRF_TOKEN", "")),
            timeout=int(os.getenv("JUEJIN_TIMEOUT", "30")),
            max_retries=int(os.getenv("JUEJIN_MAX_RETRIES", "3")),
        )
    
    def validate(self) -> bool:
        """验证配置是否有效"""
        if not self.cookie:
            raise ValueError("JUEJIN_COOKIE 环境变量未设置")
        return True
