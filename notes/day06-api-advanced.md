# Day 6: API 測試進階 — 框架化 + 認證流程

> ⏱ 2 小時 ｜ 🎯 建立可複用的 API 測試框架，處理認證與資料驅動

## 學習目標

- [ ] 建立 API client wrapper，統一管理請求
- [ ] 處理 Token-based 認證流程
- [ ] 實作資料驅動的 API 測試
- [ ] 了解 MQTT 基本概念（加分項）

## 核心知識點

### 6.1 API Client Wrapper

```python
# utils/api_client.py
import requests
from typing import Optional


class APIClient:
    """封裝 HTTP 請求的 client，統一管理 base_url、headers、logging"""

    def __init__(self, base_url: str, headers: Optional[dict] = None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def get(self, endpoint: str, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self.session.post(f"{self.base_url}{endpoint}", **kwargs)

    def put(self, endpoint: str, **kwargs):
        return self.session.put(f"{self.base_url}{endpoint}", **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self.session.delete(f"{self.base_url}{endpoint}", **kwargs)

    def set_auth_token(self, token: str):
        self.session.headers["Authorization"] = f"Bearer {token}"
```

```python
# conftest.py 加入 API client fixture
import pytest
from utils.api_client import APIClient

@pytest.fixture(scope="session")
def api_client():
    client = APIClient(base_url="https://jsonplaceholder.typicode.com")
    yield client
    client.session.close()
```

### 6.2 認證流程測試

```python
# tests/api/test_day6_auth.py
import pytest


class TestAuthFlow:
    """模擬 Token-based 認證流程"""

    def test_login_and_access_protected_resource(self, api_client):
        # Step 1: 登入取得 token（這裡用假的 endpoint 示意）
        login_payload = {"username": "admin", "password": "admin123"}

        # 實際專案中：
        # response = api_client.post("/auth/login", json=login_payload)
        # token = response.json()["token"]
        # api_client.set_auth_token(token)

        # Step 2: 使用 token 存取受保護的資源
        # response = api_client.get("/protected/data")
        # assert response.status_code == 200

    def test_access_without_token_returns_401(self, api_client):
        """未帶 token 應回傳 401"""
        # response = api_client.get("/protected/data")
        # assert response.status_code == 401
        pass  # 替換為實際 API 時移除 pass
```

### 6.3 資料驅動 API 測試

```python
# tests/api/test_day6_data_driven.py
import pytest

# 測試資料可以從外部 JSON/CSV 載入
CREATE_POST_TEST_DATA = [
    {"title": "Post A", "body": "Body A", "userId": 1, "expected_status": 201},
    {"title": "Post B", "body": "Body B", "userId": 2, "expected_status": 201},
    {"title": "",        "body": "Body C", "userId": 1, "expected_status": 201},  # 邊界測試
]


@pytest.mark.parametrize("test_data", CREATE_POST_TEST_DATA,
                         ids=["valid_post_A", "valid_post_B", "empty_title"])
def test_create_post_data_driven(api_client, test_data):
    payload = {
        "title": test_data["title"],
        "body": test_data["body"],
        "userId": test_data["userId"],
    }
    response = api_client.post("/posts", json=payload)
    assert response.status_code == test_data["expected_status"]
```

### 6.4 MQTT 概念簡介（IoT / 網路產品常見）

```
MQTT 是物聯網（IoT）常用的輕量級訊息協定：
- Publish/Subscribe 模式（非 Request/Response）
- 常用於網路設備（router, mesh networking）的狀態回報
- Python 套件：paho-mqtt
- 在 mesh networking 產品中很可能會用到

# 基本概念：
# Publisher → Broker (e.g., Mosquitto) → Subscriber
# Topic 格式: "devices/router-01/status"
```

```python
# 了解即可，面試時能提到加分
# pip install paho-mqtt

# import paho.mqtt.client as mqtt
#
# client = mqtt.Client()
# client.connect("test.mosquitto.org", 1883, 60)
# client.subscribe("test/topic")
# client.publish("test/topic", "Hello MQTT!")
```

## 實作練習

> **練習 6**：
> 1. 實作 `utils/api_client.py` 的 APIClient 類別
> 2. 在 `conftest.py` 中加入 `api_client` fixture
> 3. 用 APIClient 重寫 Day 5 的測試
> 4. 加入至少一組資料驅動測試

## 完成標準

```bash
pytest tests/api/ -v  # 所有 API 測試通過，且使用 APIClient fixture
```
