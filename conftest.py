# Root conftest.py — Global fixtures available to all tests
import pytest

from utils.pricing import build_order


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