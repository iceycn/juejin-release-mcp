"""
配置模块测试
"""

import os
import pytest
from user_juejin.config import JuejinConfig


class TestJuejinConfig:
    """测试 JuejinConfig 配置类"""

    def test_default_values(self):
        """测试默认值"""
        config = JuejinConfig()
        assert config.cookie == ""
        assert config.aid == "2608"
        assert config.uuid == ""
        assert config.base_url == "https://api.juejin.cn"
        assert config.timeout == 30
        assert config.max_retries == 3

    def test_from_env(self, monkeypatch):
        """测试从环境变量加载配置"""
        monkeypatch.setenv("JUEJIN_COOKIE", "test_cookie")
        monkeypatch.setenv("JUEJIN_AID", "1234")
        monkeypatch.setenv("JUEJIN_UUID", "test_uuid")
        monkeypatch.setenv("JUEJIN_TIMEOUT", "60")

        config = JuejinConfig.from_env()
        assert config.cookie == "test_cookie"
        assert config.aid == "1234"
        assert config.uuid == "test_uuid"
        assert config.timeout == 60

    def test_validate_raises_without_cookie(self):
        """测试没有 cookie 时验证失败"""
        config = JuejinConfig(cookie="")
        with pytest.raises(ValueError, match="JUEJIN_COOKIE"):
            config.validate()

    def test_validate_passes_with_cookie(self):
        """测试有 cookie 时验证通过"""
        config = JuejinConfig(cookie="test_cookie")
        assert config.validate() is True