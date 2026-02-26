# Day 10: 整合專案 + 面試準備

> ⏱ 2 小時 ｜ 🎯 整合所有學習成果，準備技術面試話題

## 學習目標

- [ ] 確保所有測試都能成功執行
- [ ] 完善專案文件與程式碼品質
- [ ] 準備面試中的技術問答
- [ ] 回顧並補強薄弱環節

## 最終檢查清單

```bash
# 1. 全部測試通過
pytest tests/ -v --tb=short

# 2. Smoke 測試通過
pytest tests/ -m smoke -v

# 3. 平行執行通過
pytest tests/ -n auto -v

# 4. 產出報告
pytest tests/ --html=reports/final_report.html --self-contained-html

# 5. 程式碼品質
flake8 tests/ pages/ utils/ config/ --max-line-length=120 --ignore=E501
```

## 專案 Demo 腳本

準備一個 5-10 分鐘的 Demo，展示：

```
1. 框架架構總覽 (1 min)
   → 專案結構、設定管理、POM 模式

2. API 測試 Demo (2 min)
   → 執行 API 測試 + Schema 驗證
   → 展示資料驅動測試

3. UI 測試 Demo (2 min)
   → --headed 模式展示 Playwright 操作
   → 展示失敗截圖功能

4. CI/CD 設定說明 (2 min)
   → 解釋 Jenkinsfile / Bitbucket Pipeline
   → 說明測試策略與觸發時機

5. 報告展示 (1 min)
   → 開啟 HTML 報告
   → 展示 Trace Viewer
```

## 程式碼重構檢查

```python
# 確認這些好的實踐都有做到：

# ✅ 所有 Page Object 都有 type hints
class LoginPage:
    def __init__(self, page: Page): ...
    def login(self, username: str, password: str) -> None: ...

# ✅ 使用 dataclass 或 Pydantic 管理設定和資料
@dataclass
class Settings:
    base_url: str
    timeout: int = 30000

# ✅ Fixture 有適當的 scope 和 teardown
@pytest.fixture(scope="session")
def api_client():
    client = APIClient(...)
    yield client
    client.session.close()

# ✅ 測試有清楚的命名和組織
# tests/api/test_posts.py     → API 測試
# tests/ui/test_login.py      → UI 測試
# tests/integration/test_*.py → 整合測試
```
