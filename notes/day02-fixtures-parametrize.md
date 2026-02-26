# Day 2: pytest 進階 — Fixtures & Parametrize

> ⏱ 2 小時 ｜ 🎯 掌握 fixture 依賴注入與資料驅動測試

## 學習目標

- [ ] 理解 fixture 作為「依賴注入」的核心概念
- [ ] 使用不同 scope 的 fixture（function / class / module / session）
- [ ] 使用 `@pytest.mark.parametrize` 實現資料驅動測試
- [ ] 建立 `conftest.py` 共享 fixture

## 核心知識點

### 2.1 Fixture 基礎 — 取代 setup/teardown

```python
import pytest

@pytest.fixture
def sample_user():
    """每個測試函式執行前都會建立一個新的 user dict"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "role": "admin"
    }

def test_user_has_email(sample_user):
    # sample_user 會自動被注入
    assert "@" in sample_user["email"]

def test_user_role(sample_user):
    assert sample_user["role"] in ["admin", "user", "viewer"]
```

### 2.2 Fixture Scope — 控制生命週期

```python
import pytest

@pytest.fixture(scope="session")
def db_connection():
    """整個測試 session 只建立一次 — 適合昂貴的資源"""
    print("\n[Setup] 建立資料庫連線")
    conn = {"host": "localhost", "port": 5432, "connected": True}
    yield conn  # yield 之後的程式碼是 teardown
    print("\n[Teardown] 關閉資料庫連線")
    conn["connected"] = False

@pytest.fixture(scope="function")  # 預設值，每個 test 都會重新執行
def temp_data(db_connection):
    """fixture 可以依賴其他 fixture"""
    print("  [Setup] 準備測試資料")
    data = {"id": 1, "value": "test"}
    yield data
    print("  [Teardown] 清除測試資料")
```

### 2.3 conftest.py — 共享 Fixture 的正確方式

```python
# conftest.py (放在 tests/ 目錄或專案根目錄)
# 不需要 import，pytest 會自動發現並載入

import pytest

@pytest.fixture
def base_url():
    return "https://jsonplaceholder.typicode.com"

@pytest.fixture
def auth_headers():
    return {
        "Authorization": "Bearer test-token",
        "Content-Type": "application/json"
    }
```

### 2.4 Parametrize — 資料驅動測試

```python
import pytest

# 基本用法：一個參數
@pytest.mark.parametrize("input_val, expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input_val, expected):
    assert input_val ** 2 == expected

# 實際場景：驗證多種使用者角色的權限
@pytest.mark.parametrize("role, can_delete", [
    ("admin", True),
    ("editor", False),
    ("viewer", False),
])
def test_delete_permission(role, can_delete):
    permissions = {
        "admin": ["read", "write", "delete"],
        "editor": ["read", "write"],
        "viewer": ["read"],
    }
    has_delete = "delete" in permissions.get(role, [])
    assert has_delete == can_delete
```

### 2.5 Fixture + Parametrize 組合技

```python
import pytest

@pytest.fixture(params=["chromium", "firefox", "webkit"])
def browser_name(request):
    """對每個瀏覽器都執行一次測試"""
    return request.param

def test_browser_is_supported(browser_name):
    supported = ["chromium", "firefox", "webkit"]
    assert browser_name in supported
```

## 實作練習

> **練習 2**：建立 `tests/test_day2_fixtures.py` 與根目錄的 `conftest.py`
> - 在 `conftest.py` 中建立 3 個 fixture（不同 scope）
> - 使用 `yield` 實現 setup / teardown 模式
> - 寫至少 3 個 parametrize 測試（涵蓋單參數、多參數）
> - 使用 `pytest --fixtures` 查看所有可用 fixture

## 完成標準

```bash
pytest tests/test_day2_fixtures.py -v -s  # 觀察 fixture setup/teardown 順序
pytest tests/test_day2_fixtures.py -v -k "square"  # 用 -k 過濾測試名稱
```
