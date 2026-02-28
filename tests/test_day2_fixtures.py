import pytest

from utils.pricing import calculate_discount, calculate_shipping, build_order

@pytest.mark.parametrize("price,role,expected", [(100, "vip", 80), (50, "member", 45), (10, "guest", 10)])
def test_discount_by_role(price, role, expected):
    """規格驗證：每個 role 折扣計算正確"""
    # function 單元測試 (黑箱)
    assert calculate_discount(price=price, role=role) == expected
    
def test_vip_pays_less_than_member_less_than_guest():
    """行為驗證：折購等級排序正確"""
    # function 行為測試 (白箱)
    vip_discount = calculate_discount(price=100, role="vip")
    member_discount = calculate_discount(price=100, role="member")
    guest_discount = calculate_discount(price=100, role="guest")
    assert vip_discount < member_discount < guest_discount

@pytest.mark.parametrize("weight_kg, region, expected_fee", [(2,"domestic", 60), (1, "asia", 200), (10, "international", 600), (3, "africa", 500)])
def test_shipping_by_region(weight_kg, region, expected_fee):
    """測試 shipping 計算邏輯"""
    assert calculate_shipping(weight_kg=weight_kg, region=region) == expected_fee 

@pytest.mark.parametrize("role, region, expected_total", [("vip", "asia", 720.0), ("member", "domestic", 645.0)])
def test_build_order(role, region, expected_total, sample_cart):
    """測試 build_order 計算正確"""
    assert build_order(items=sample_cart, role=role, region=region)["total"] == expected_total


def test_order_total(order):
    order_key = ["total", "discounted", "shipping", "total", "item_count"]
    for k in order_key:
        assert k in order
    assert order["total"] == round(order["discounted"] + order["shipping"], 2)