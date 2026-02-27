# Day 1: Python 測試基礎 + pytest 入門

> ⏱ 2 小時 ｜ 🎯 能用 pytest 撰寫、執行、組織基礎測試

## 學習目標

- [x] 理解 pytest 的自動發現機制（test discovery）
- [x] 撰寫基礎 test function 與使用 `assert`
- [x] 使用 `pytest.mark` 進行測試分類
- [x] 理解測試執行指令與常用 flags

## 核心知識點

### 1.1 pytest 測試發現規則

```python
# 檔名必須是 test_*.py 或 *_test.py
# 函式名稱必須以 test_ 開頭
# 類別名稱必須以 Test 開頭（若使用 class 組織）

# tests/test_basic.py
def test_addition():
    assert 1 + 1 == 2

def test_string_contains():
    greeting = "Hello, World!"
    assert "World" in greeting
```

### 1.2 豐富的 assert 內建支援

```python
# pytest 的 assert rewriting 會自動顯示詳細的失敗訊息
def test_list_operations():
    items = [1, 2, 3]
    assert len(items) == 3
    assert 2 in items
    assert items[0] == 1

def test_dict_validation():
    user = {"name": "Alice", "role": "SDET"}
    assert user["role"] == "SDET"
    assert "email" not in user
```

### 1.3 使用 Markers 分類測試

```python
import pytest

@pytest.mark.smoke
def test_homepage_loads():
    """冒煙測試 - 最基本的功能驗證"""
    assert True

@pytest.mark.regression
def test_login_with_valid_credentials():
    """回歸測試"""
    assert True

@pytest.mark.skip(reason="Feature not implemented yet")
def test_upcoming_feature():
    pass

@pytest.mark.xfail(reason="Known bug #123")
def test_known_broken_feature():
    assert False  # 預期會失敗，不會標記為 FAIL
```

### 1.4 常用執行指令

```bash
# 執行所有測試
pytest

# 顯示詳細輸出
pytest -v

# 只跑特定檔案
pytest tests/test_basic.py

# 只跑特定測試函式
pytest tests/test_basic.py::test_addition

# 只跑標記為 smoke 的測試
pytest -m smoke

# 第一個失敗就停止
pytest -x

# 顯示 print 輸出
pytest -s

# 組合使用
pytest -v -s -m smoke --tb=short
```

## 實作練習

> **練習 1**：建立 `tests/test_day1_basics.py`，撰寫至少 5 個測試函式，涵蓋：
> - 數值運算斷言
> - 字串操作斷言
> - List / Dict 資料結構斷言
> - 使用 `@pytest.mark.smoke` 標記其中 2 個
> - 使用 `pytest.raises` 驗證 exception

```python
# 提示: exception 測試
import pytest

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_key_error():
    data = {"a": 1}
    with pytest.raises(KeyError):
        _ = data["nonexistent"]
```

## 完成標準

```bash
pytest tests/test_day1_basics.py -v  # 全部 PASSED
pytest tests/test_day1_basics.py -m smoke -v  # 只跑 smoke 標記的測試
```

## 今日總結
- 自動化測試都有相似的設計邏輯, 包含：
  - 設定指定檔案路徑存放測試
  - 需符合特定的檔案名稱 & function 名稱規範
  - 測試標記 (tag) & 參數化執行 (限縮範圍)