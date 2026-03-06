# Root conftest.py — Global fixtures available to all tests
import pytest

from utils.pricing import build_order
from utils.api_client import APIClient


@pytest.fixture(scope="session")
def base_url():
    """Base URL for UI tests."""
    return "https://the-internet.herokuapp.com"


@pytest.fixture(scope="session")
def api_base_url():
    """Base URL for API tests."""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="function")
def test_data():
    return {"name": "data", "id": 1}


@pytest.fixture(scope="session")
def product_catalog():
    
    print("\n[Session Setup] 載入商品目錄")
    product_list = [
        {"name": "hat", "price": 100, "qty": 2, "weight_kg": 0.3},
        {"name": "clothes", "price": 200, "qty": 1, "weight_kg": 0.5},
        {"name": "shorts", "price": 150, "qty": 3, "weight_kg": 0.4},
        {"name": "shoes", "price": 300, "qty": 1, "weight_kg": 1.0},
    ]
    yield product_list
    print("[Session Teardown] 釋放商品目錄")

@pytest.fixture(scope="module")
def sample_cart(product_catalog):
    print("[Module Setup] 載入購物車")
    cart_list = product_catalog[::2]
    yield cart_list
    print("[Module Teardown] 釋放購物車")

@pytest.fixture(scope="function")
def order(sample_cart):
    print("[Setup] 訂單建立")
    o = build_order(items=sample_cart,role="vip", region="asia")
    yield o
    print("[Teardown] 訂單銷毀")


@pytest.fixture(scope="session")
def json_place_holder_api_client():
    """Json Place Holder 網站 API Client 封裝"""
    client = APIClient(base_url="https://jsonplaceholder.typicode.com")

    # 以下模擬一個假的登入取 token & 設定流程
    # 設定完畢後此 client 的任意請求都包含 token
    # res = client.post("/auth/login", json={"username":"aaa", "password": "bbb"})
    # token = res.json()["token"]
    # client.set_auth_token(token)

    yield client
    client.close()