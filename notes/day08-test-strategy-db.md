# Day 8: 多層測試策略 + 資料庫驗證

> ⏱ 2 小時 ｜ 🎯 理解測試金字塔，實作 UI + API 整合測試與 SQL 驗證

## 學習目標

- [ ] 理解測試金字塔（Test Pyramid）在實務中的應用
- [ ] 實作 UI + API 的整合測試場景
- [ ] 使用 SQL 查詢驗證測試資料
- [ ] 管理測試資料的建立與清除

## 核心知識點

### 8.1 測試金字塔 — 應用於網路產品

```
                    ╱╲
                   ╱  ╲         E2E / UI Tests (最少)
                  ╱ UI ╲        → 關鍵使用者流程
                 ╱──────╲       → 每個 feature 1-2 個
                ╱        ╲
               ╱ API/整合  ╲     Integration Tests (中等)
              ╱────────────╲    → API 合約測試
             ╱              ╲   → 服務間互動測試
            ╱   Unit Tests   ╲   Unit Tests (最多)
           ╱──────────────────╲  → 純邏輯驗證
          ╱                    ╲ → 執行速度最快

在網路產品中：
├── Unit Tests: 設定解析、協定處理邏輯
├── API Tests: REST API CRUD、韌體更新 API、裝置管理 API
├── UI Tests:  管理後台的關鍵流程（設備配對、網路設定）
└── System Tests: Mesh networking 連線、無線顯示
```

### 8.2 UI + API 整合測試

```python
# tests/integration/test_day8_integration.py

def test_create_post_via_api_then_verify_ui(api_client, page):
    """
    整合測試模式：
    1. 透過 API 建立資料（快速、可靠）
    2. 透過 UI 驗證資料是否正確顯示
    """
    # Step 1: API 建立資料
    payload = {"title": "Integration Test Post", "body": "Created via API", "userId": 1}
    response = api_client.post("/posts", json=payload)
    assert response.status_code == 201
    post_id = response.json()["id"]

    # Step 2: UI 驗證（假設有對應的前端頁面）
    # page.goto(f"https://example.com/posts/{post_id}")
    # expect(page.get_by_text("Integration Test Post")).to_be_visible()

    # Step 3: API 清除資料
    # api_client.delete(f"/posts/{post_id}")
```

### 8.3 SQL 查詢驗證

```python
# utils/db.py
import sqlite3
from contextlib import contextmanager


@contextmanager
def get_db_connection(db_path: str = "test.db"):
    """Context manager 管理資料庫連線"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 讓結果可以用欄位名稱存取
    try:
        yield conn
    finally:
        conn.close()


def query(sql: str, params: tuple = (), db_path: str = "test.db"):
    """執行 SQL 查詢並回傳結果"""
    with get_db_connection(db_path) as conn:
        cursor = conn.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]
```

```python
# tests/integration/test_day8_db.py
from utils.db import query, get_db_connection
import pytest


@pytest.fixture(scope="module")
def setup_test_db():
    """建立測試用的 SQLite 資料庫"""
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT DEFAULT 'viewer'
            )
        """)
        conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'Alice', 'alice@test.com', 'admin')")
        conn.execute("INSERT OR IGNORE INTO users VALUES (2, 'Bob', 'bob@test.com', 'viewer')")
        conn.commit()
    yield
    import os
    os.remove("test.db")  # 測試結束後清除


def test_user_exists_in_db(setup_test_db):
    results = query("SELECT * FROM users WHERE name = ?", ("Alice",))
    assert len(results) == 1
    assert results[0]["role"] == "admin"


def test_user_count(setup_test_db):
    results = query("SELECT COUNT(*) as count FROM users")
    assert results[0]["count"] == 2
```

### 8.4 測試資料管理策略

```python
# utils/test_data.py
"""
測試資料管理的三種模式：

1. Factory Pattern — 動態產生測試資料
2. Fixture Files — 從 JSON/YAML 載入固定資料
3. API Seeding — 透過 API 建立/清除資料
"""
import json
from pathlib import Path


def load_test_data(filename: str) -> dict:
    """從 fixtures 目錄載入測試資料"""
    filepath = Path(__file__).parent.parent / "fixtures" / filename
    with open(filepath) as f:
        return json.load(f)


class UserFactory:
    """Factory Pattern: 動態產生測試用的 User 資料"""
    _counter = 0

    @classmethod
    def create(cls, **overrides) -> dict:
        cls._counter += 1
        defaults = {
            "name": f"Test User {cls._counter}",
            "email": f"user{cls._counter}@test.com",
            "role": "viewer",
        }
        defaults.update(overrides)
        return defaults
```

## 實作練習

> **練習 8**：
> 1. 建立 `tests/integration/test_day8_integration.py`，寫一個 API → UI 驗證流程
> 2. 建立 `utils/db.py`，實作 SQLite 查詢工具
> 3. 寫 2-3 個 SQL 驗證測試
> 4. 建立 `utils/test_data.py`，實作 Factory Pattern

## 完成標準

```bash
pytest tests/integration/ -v  # 整合測試全部通過
pytest tests/ -v --tb=short  # 全部測試依然通過
```
