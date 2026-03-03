# Day 3: Playwright for Python — 基礎操作

> ⏱ 2 小時 ｜ 🎯 用 Python Playwright 完成基礎 UI 操作與斷言

## 學習目標

- [x] 使用 `pytest-playwright` 的內建 fixture（`page`, `browser`, `context`）
- [x] 掌握 Locator 策略（role, text, CSS, test-id）
- [x] 使用 Playwright 的 `expect` 斷言 API
- [x] 截圖與追蹤（trace）功能

## 核心知識點

### 3.1 pytest-playwright 內建 Fixture

```python
# pytest-playwright 自動提供這些 fixture，不需要自己管理瀏覽器生命週期：
#   - browser: 瀏覽器實例 (session scope)
#   - context: 瀏覽器 context (function scope)
#   - page:    頁面實例 (function scope) ← 最常用

def test_homepage_title(page):
    """page fixture 自動注入，每個測試都是乾淨的頁面"""
    page.goto("https://playwright.dev/python/")
    assert "Playwright" in page.title()
```

### 3.2 Locator 策略（依推薦優先順序）

```python
from playwright.sync_api import expect

def test_locator_strategies(page):
    page.goto("https://the-internet.herokuapp.com/login")

    # 1. 最推薦：Role-based（語意化，最接近使用者行為）
    page.get_by_role("heading", name="Login Page")

    # 2. 推薦：text / label / placeholder
    page.get_by_label("Username")
    page.get_by_placeholder("Enter username")
    page.get_by_text("Login Page")

    # 3. 推薦：test id（需要開發配合加上 data-testid）
    # page.get_by_test_id("login-button")

    # 4. 備用：CSS selector
    page.locator("#username")
    page.locator("button.radius")

    # 5. 最後手段：XPath
    page.locator("xpath=//button[@type='submit']")
```

### 3.3 常用操作

```python
def test_login_flow(page):
    page.goto("https://the-internet.herokuapp.com/login")

    # 填寫表單
    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")

    # 點擊按鈕
    page.get_by_role("button", name="Login").click()

    # 斷言 — 使用 Playwright 的 Web-First Assertions（自動重試直到條件成立或 timeout）
    expect(page).to_have_url("https://the-internet.herokuapp.com/secure")
    expect(page.get_by_text("You logged into a secure area!")).to_be_visible()
```

### 3.4 截圖與追蹤

```python
def test_with_screenshot(page):
    page.goto("https://playwright.dev/python/")

    # 單一截圖
    page.screenshot(path="screenshots/homepage.png")

    # 整頁截圖
    page.screenshot(path="screenshots/full_page.png", full_page=True)

    # 元素截圖
    page.get_by_role("heading").first.screenshot(path="screenshots/heading.png")
```

```bash
# 使用 trace 功能（命令列啟用）
pytest tests/ui/ --tracing on

# 查看 trace（會開啟互動式 viewer）
playwright show-trace test-results/trace.zip
```

### 3.5 pytest-playwright 命令列選項

```bash
# 指定瀏覽器
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit

# Headed 模式（看到瀏覽器操作）
pytest --headed

# 慢動作模式（除錯用）
pytest --slowmo 500

# 多瀏覽器測試
pytest --browser chromium --browser firefox
```

## 實作練習

> **練習 3**：建立 `tests/ui/test_day3_playwright_basics.py`
> - 對 `https://the-internet.herokuapp.com` 撰寫至少 3 個 UI 測試：
>   1. Login 頁面的成功登入流程
>   2. Login 頁面的失敗登入流程（驗證錯誤訊息）
>   3. 其他任一頁面的互動測試（如 Dropdown, Checkboxes 等）
> - 每個測試都包含 `expect` 斷言
> - 至少一個測試要截圖

## 完成標準

```bash
pytest tests/ui/test_day3_playwright_basics.py -v --headed  # headed 模式觀察執行
pytest tests/ui/test_day3_playwright_basics.py -v --tracing on  # 產出 trace
```

## 今日總結
- pytest-playwright 是 pytest 的一個插件, 支援 playwright 物件以 fixture 的方式在 test 中使用
  - 本質上還是 pytest, 過去的測試編寫以及執行邏輯不變 (ex. 檔案命名、function 命名、pytest decorator)
  - 多了瀏覽器控制 & 操作相關 API
- 使用 playwright expect 的好處為自動等待機制, pytest-playwright 提供的 fixture (page, browser, context) 以及獲取的網頁 element 都能應用自動等待機制。
  - 自動重試直到條件成立 or timeout
- playwright 提供幾種常見獲取元素的方法, 從上到下推薦優先使用：
  - .get_by_role() - 依 ARIA role 定位
  - .get_by_label() - 依 label 文字定位表單欄位
  - .locator()
    - `#` — id
    - `.` — class
    - `[]` — attribute（例如 `[data-testid="login"]`）
    - `xpath=` — XPath（最後手段）