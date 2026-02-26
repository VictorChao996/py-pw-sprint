# Day 7: 自動化框架架構設計

> ⏱ 2 小時 ｜ 🎯 建立企業級的測試框架結構，含設定管理、日誌、報告

## 學習目標

- [ ] 設計多環境設定管理（dev / staging / prod）
- [ ] 整合 logging 機制
- [ ] 產出 HTML 測試報告
- [ ] 建立自定義 pytest plugin / hook

## 核心知識點

### 7.1 多環境設定管理

```python
# config/settings.py
import os
from dataclasses import dataclass


@dataclass
class Settings:
    """集中管理所有測試設定"""
    base_url: str
    api_base_url: str
    timeout: int = 30000
    headless: bool = True
    browser: str = "chromium"


# 環境設定對照表
ENVIRONMENTS = {
    "dev": Settings(
        base_url="https://dev.example.com",
        api_base_url="https://api-dev.example.com",
    ),
    "staging": Settings(
        base_url="https://staging.example.com",
        api_base_url="https://api-staging.example.com",
    ),
    "prod": Settings(
        base_url="https://example.com",
        api_base_url="https://api.example.com",
        headless=True,  # prod 環境強制 headless
    ),
}


def get_settings() -> Settings:
    env = os.getenv("TEST_ENV", "dev")
    return ENVIRONMENTS[env]
```

```python
# conftest.py 整合設定
import pytest
from config.settings import get_settings

@pytest.fixture(scope="session")
def settings():
    return get_settings()

@pytest.fixture(scope="session")
def api_client(settings):
    from utils.api_client import APIClient
    client = APIClient(base_url=settings.api_base_url)
    yield client
    client.session.close()
```

```bash
# 切換環境執行
TEST_ENV=staging pytest tests/
TEST_ENV=prod pytest tests/ -m smoke
```

### 7.2 Logging 整合

```python
# utils/logger.py
import logging
import os

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_fmt)
        logger.addHandler(console_handler)

        # File handler
        os.makedirs("logs", exist_ok=True)
        file_handler = logging.FileHandler("logs/test.log", mode="w")
        file_handler.setLevel(logging.DEBUG)
        file_fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s"
        )
        file_handler.setFormatter(file_fmt)
        logger.addHandler(file_handler)

    return logger
```

```python
# 在測試或 Page Object 中使用
from utils.logger import get_logger

logger = get_logger(__name__)

class LoginPage:
    def login(self, username, password):
        logger.info(f"Attempting login with user: {username}")
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        logger.info("Login form submitted")
```

### 7.3 HTML 測試報告

```bash
# pytest-html 產出報告
pytest tests/ --html=reports/report.html --self-contained-html

# 也可以在 pytest.ini 設定預設值
```

```ini
# pytest.ini
[pytest]
addopts = -v --tb=short
markers =
    smoke: Smoke tests
    regression: Regression tests
    api: API tests
    ui: UI tests
testpaths = tests
```

### 7.4 自定義 Fixture — 截圖失敗時自動儲存

```python
# conftest.py
import pytest

@pytest.fixture(autouse=True)
def auto_screenshot_on_failure(request, page):
    """測試失敗時自動截圖 — autouse 表示所有 UI 測試自動啟用"""
    yield
    if request.node.rep_call and request.node.rep_call.failed:
        test_name = request.node.name
        page.screenshot(path=f"screenshots/FAIL_{test_name}.png")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """pytest hook: 把測試結果附加到 request.node 上"""
    import pytest
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
```

## 實作練習

> **練習 7**：
> 1. 建立 `config/settings.py`，支援至少 2 個環境
> 2. 建立 `utils/logger.py`，在 Page Object 和測試中使用
> 3. 設定 `pytest.ini`，包含 markers 和預設選項
> 4. 讓失敗截圖自動儲存功能生效
> 5. 產出一份 HTML 報告

## 完成標準

```bash
pytest tests/ --html=reports/report.html -v  # 產出報告
ls reports/report.html  # 確認報告存在
ls logs/test.log  # 確認日誌存在
```
