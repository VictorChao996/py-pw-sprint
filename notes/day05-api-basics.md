# Day 5: API 測試基礎 — requests + JSON 驗證

> ⏱ 2 小時 ｜ 🎯 使用 Python 進行 RESTful API 測試與 JSON 結構驗證

## 學習目標

- [x] 使用 `requests` / `httpx` 發送 HTTP 請求
- [x] 驗證 status code、headers、response body
- [x] 使用 Pydantic 進行 JSON schema 驗證
- [x] 理解 REST API 測試的常見模式

## 核心知識點

### 5.1 使用 requests 進行 API 測試

```python
# tests/api/test_day5_api_basics.py
import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"


class TestGetRequests:
    """GET 請求測試"""

    def test_get_all_posts(self):
        response = requests.get(f"{BASE_URL}/posts")
        assert response.status_code == 200

        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) > 0

    def test_get_single_post(self):
        response = requests.get(f"{BASE_URL}/posts/1")
        assert response.status_code == 200

        post = response.json()
        assert post["id"] == 1
        assert "title" in post
        assert "body" in post
        assert "userId" in post

    def test_get_nonexistent_post(self):
        response = requests.get(f"{BASE_URL}/posts/99999")
        assert response.status_code == 404


class TestPostRequests:
    """POST 請求測試"""

    def test_create_post(self):
        payload = {
            "title": "Test Post",
            "body": "This is a test post body",
            "userId": 1
        }
        response = requests.post(f"{BASE_URL}/posts", json=payload)
        assert response.status_code == 201

        data = response.json()
        assert data["title"] == payload["title"]
        assert "id" in data  # 新建資源應回傳 id
```

### 5.2 JSON Schema 驗證 — 使用 Pydantic

```python
# utils/schemas.py
from pydantic import BaseModel, Field
from typing import Optional


class Post(BaseModel):
    """定義 Post API 的回應結構"""
    id: int
    title: str = Field(min_length=1)
    body: str
    userId: int = Field(gt=0)


class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    phone: Optional[str] = None
```

```python
# tests/api/test_day5_schema.py
import requests
from utils.schemas import Post, User

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_post_response_matches_schema():
    """用 Pydantic 驗證 API 回應符合預期結構"""
    response = requests.get(f"{BASE_URL}/posts/1")
    post = Post(**response.json())  # 若結構不符會拋出 ValidationError

    assert post.id == 1
    assert len(post.title) > 0


def test_all_users_match_schema():
    """批次驗證所有 user 都符合 schema"""
    response = requests.get(f"{BASE_URL}/users")
    users = [User(**u) for u in response.json()]

    assert len(users) == 10
    assert all(u.email for u in users)
```

### 5.3 驗證 Response Headers

```python
def test_response_headers():
    response = requests.get(f"{BASE_URL}/posts")

    assert response.headers["Content-Type"] == "application/json; charset=utf-8"
    assert "X-Powered-By" in response.headers

    # 驗證回應時間（效能基本檢查）
    assert response.elapsed.total_seconds() < 5
```

### 5.4 使用 Playwright 的 API Testing 功能（替代 requests）

1. 沒有瀏覽器的範例 （獨立 HTTP client, 沒有 cookie, 沒有 session）
```python
def test_api_with_playwright(playwright):
    """Playwright 也可以做 API 測試，不需要啟動瀏覽器"""
    api_context = playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com"
    )

    response = api_context.get("/posts/1")
    assert response.ok
    assert response.json()["id"] == 1

    api_context.dispose()
```

2. 共用 page 的瀏覽器 context (自動帶上該 page 的 cookie, session, auth token)
> **適用場景**：當 API 和 UI 測試混在一起，需要共用瀏覽器登入 session 時特別有用：

```python
def test_user_flow(page):
    # UI 登入
    page.goto("/login")
    page.fill("#email", "user@test.com")
    page.click("button[type=submit]")

    # 用同一個已登入的 context 打 API，不需要另外處理 token
    response = page.request.get("/api/profile")
    assert response.json()["email"] == "user@test.com"
```

## 實作練習

> **練習 5**：建立 `tests/api/test_day5_api_basics.py`
> - 對 `https://jsonplaceholder.typicode.com` 撰寫完整 CRUD 測試：
>   - GET（單一 / 列表 / 404）
>   - POST（建立資源）
>   - PUT（更新資源）
>   - DELETE（刪除資源）
> - 在 `utils/schemas.py` 定義至少 2 個 Pydantic Model
> - 至少 3 個測試使用 schema 驗證

## 完成標準

```bash
pytest tests/api/test_day5_api_basics.py -v  # 全部 PASSED
pytest tests/api/ -v  # 包含 schema 驗證的測試也通過
```

## 今日重點
- Python 進行 RESTful API 測試可以借助 requests/httpx 等 HTTP client package
  - RESTful 是一種 API 風格, 包含：GET, POST, PUT, DELETE 等操作動作
  - request header + body, response header + body 都可以作為驗證的重點
- Pydantic 是一個協助資料驗證的 Package
  - 能夠驗證 data type, 當不符時拋出 validateError
  - 型別定義在 API 的 request/response 皆有用處, 更進一步 fastAPI 也有內兼容 pydantic 進行驗證 & swagger API 的呈現
- API 測試、request 邏輯可以與 schema 分離, 就如 service 開發中 model & controller 分離一樣 （資料結構 & 業務邏輯分離）