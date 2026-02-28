"""
pricing.py 模擬帶測試電商模組
"""

def calculate_discount(price: float, role: str) -> float:
    """根據會員等級計算折扣後價格"""
    rates = {"vip": 0.8, "member": 0.9, "guest": 1.0}
    return round(price * rates.get(role, 1.0), 2)


def calculate_shipping(weight_kg: float, region: str) -> float:
    """根據重量與地區計算運費"""
    base = {"domestic": 60, "asia": 200, "international": 500}
    fee = base.get(region, 500)
    if weight_kg > 5:
        fee += (weight_kg - 5) * 20  # 超過 5kg 每公斤加 20
    return fee

def build_order(items: list[dict], role: str, region: str) -> dict:
    """組合一張完整訂單"""
    subtotal = sum(item["price"] * item["qty"] for item in items)
    discounted = calculate_discount(subtotal, role)
    total_weight = sum(item.get("weight_kg", 0.5) * item["qty"] for item in items)
    shipping = calculate_shipping(total_weight, region)
    return {
        "subtotal": subtotal,
        "discounted": discounted,
        "shipping": shipping,
        "total": round(discounted + shipping, 2),
        "item_count": sum(item["qty"] for item in items),
    }
