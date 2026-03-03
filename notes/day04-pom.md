# Day 4: Playwright 進階 + Page Object Model

> ⏱ 2 小時 ｜ 🎯 實作 POM 設計模式，建立可維護的 UI 測試架構

## 學習目標

- [x] 理解 Page Object Model 的設計原則
- [x] 在 Python 中實作 POM
- [x] 處理等待策略與~~網路攔截~~
- [x] 使用 Playwright 的 codegen 工具加速開發

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

### 情境練習

以下情境皆使用 `https://the-internet.herokuapp.com`，對應今日四個知識點：

#### 情境 A：POM 封裝（對應 4.1）
> 建立 `pages/login_page.py`，將 Day 3 的 login 測試重構為 POM 模式：
> - LoginPage class 包含：`navigate()`、`login(username, password)`、`expect_success()`、`expect_error(text)`
> - 所有 locator 集中在 `__init__` 中管理
> - 測試檔中不應出現任何 `page.locator()` 或 `page.get_by_*()` 呼叫

#### 情境 B：DynamicLoadingPage + 等待元素顯示（對應 4.1 + 4.2）
> 建立 `pages/dynamic_loading_page.py`，封裝 `/dynamic_loading/1` 頁面：
> - `start()` — 點擊 Start 按鈕
> - `wait_for_result()` — 使用 `.wait_for(state="visible")` 等待結果出現
> - `expect_result_text(text)` — 使用 `expect().to_have_text()` 驗證結果
> - 測試：點擊 Start → 等待載入 → 斷言文字為 `"Hello World!"`
> - 重點：這個頁面是純前端 JS 動畫，沒有 AJAX 請求，只需等元素狀態變化

### 備註
1. 網路攔截將在未來的天數 (day 8)中練習, 會比較自然的符合情境練習

## 完成標準

```bash
pytest tests/ui/test_day4_pom.py -v --headed
# 測試程式碼中沒有直接出現 CSS selector，全部透過 POM 封裝
```


## 今日總結
1. Page Object Model (POM) 是一種設計模式, 能讓**網頁元素 & 操作**從**測試邏輯**中抽離
  - POM 封裝網頁元素, 讓測試可以專注元素運作邏輯 （而非選取元素）
    - 當相同測試使用到的網頁元素改變時, 只需要更改 POM 內即可, 避免 copy-paste 的大量後續修正
  - POM 封裝網頁相關操作, 也進一步讓測試看起來比較簡潔
    - 需注意不要過度封裝或過於細節的封裝, 不然會遇到難以擴充的問題
2. 實務上 POM 可能會發展成: BasePage, LoginPage, Test Case 的三層架構
   1. BasePage：放置頁面通用方法
   2. LoginPage; 具體頁面, 繼承 BasePage, 再加入專屬 property
   3. Test Case: 呼叫上述具體頁面進行測試