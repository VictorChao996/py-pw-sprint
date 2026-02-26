# Day 4: Playwright 進階 + Page Object Model

> ⏱ 2 小時 ｜ 🎯 實作 POM 設計模式，建立可維護的 UI 測試架構

## 學習目標

- [ ] 理解 Page Object Model 的設計原則
- [ ] 在 Python 中實作 POM
- [ ] 處理等待策略與網路攔截
- [ ] 使用 Playwright 的 codegen 工具加速開發

## 核心知識點

### 4.1 Page Object Model 實作

```python
# pages/login_page.py
from playwright.sync_api import Page, expect


class LoginPage:
    """封裝 Login 頁面的所有操作與元素定位"""

    URL = "https://the-internet.herokuapp.com/login"

    def __init__(self, page: Page):
        self.page = page
        # 集中管理 locators
        self.username_input = page.get_by_label("Username")
        self.password_input = page.get_by_label("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.flash_message = page.locator("#flash")

    def navigate(self):
        self.page.goto(self.URL)
        return self

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return self

    def expect_success(self):
        expect(self.flash_message).to_contain_text("You logged into a secure area!")

    def expect_failure(self):
        expect(self.flash_message).to_contain_text("Your username is invalid!")
```

```python
# tests/ui/test_day4_pom.py
import pytest
from pages.login_page import LoginPage


@pytest.fixture
def login_page(page):
    """建立 LoginPage 實例的 fixture"""
    return LoginPage(page).navigate()


def test_successful_login(login_page):
    login_page.login("tomsmith", "SuperSecretPassword!")
    login_page.expect_success()


def test_failed_login(login_page):
    login_page.login("wronguser", "wrongpass")
    login_page.expect_failure()


@pytest.mark.parametrize("username, password", [
    ("", "SuperSecretPassword!"),
    ("tomsmith", ""),
    ("", ""),
])
def test_login_with_missing_fields(login_page, username, password):
    login_page.login(username, password)
    login_page.expect_failure()
```

### 4.2 等待策略

```python
def test_wait_strategies(page):
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/1")

    # Playwright 預設自帶 auto-waiting，但某些場景需要手動等待
    page.get_by_role("button", name="Start").click()

    # 等待元素出現
    page.locator("#finish").wait_for(state="visible")

    # 等待特定網路請求完成
    with page.expect_response("**/dynamic_loading/*") as response_info:
        page.get_by_role("button", name="Start").click()
    assert response_info.value.ok
```

### 4.3 網路攔截（Mock API Response）

```python
import json

def test_mock_api_response(page):
    """攔截 API 請求並回傳假資料 — UI 測試解耦後端的關鍵技巧"""
    mock_data = {"users": [{"id": 1, "name": "Mocked User"}]}

    def handle_route(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mock_data)
        )

    page.route("**/api/users", handle_route)
    page.goto("https://example.com/users")  # 假設此頁面會呼叫 /api/users
```

### 4.4 Codegen — 自動產生測試程式碼

```bash
# 開啟 codegen 工具，操作瀏覽器後自動產生 Python 程式碼
playwright codegen https://the-internet.herokuapp.com/login

# 指定語言（預設 Python）
playwright codegen --target python https://the-internet.herokuapp.com/login

# 搭配裝置模擬
playwright codegen --device "iPhone 13" https://example.com
```

## 實作練習

> **練習 4**：
> 1. 在 `pages/` 建立至少 2 個 Page Object（LoginPage 已有，再加一個）
> 2. 在 `tests/ui/test_day4_pom.py` 中用 POM 撰寫測試
> 3. 使用 `playwright codegen` 產生程式碼，再重構為 POM 模式
> 4. 嘗試 `page.route()` 攔截一個 API 請求

## 完成標準

```bash
pytest tests/ui/test_day4_pom.py -v --headed
# 測試程式碼中沒有直接出現 CSS selector，全部透過 POM 封裝
```
