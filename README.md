# Python + Playwright 自動化測試框架

> Python + pytest + Playwright 建構的多層自動化測試框架，涵蓋 UI 測試、API 測試、整合測試，支援 CI/CD 平行執行。

## 技術棧

Python 3.11+ · pytest · Playwright · requests / httpx · Pydantic · pytest-xdist · Docker · Jenkins / Bitbucket Pipelines

## Quick Start

```bash
# 建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate

# 安裝依賴
pip install -r requirements.txt
playwright install

# 執行測試
pytest tests/ -v                    # 全部測試
pytest tests/ -m smoke -v           # Smoke 測試
pytest tests/api/ -v                # API 測試
pytest tests/ui/ -v --headed        # UI 測試（有畫面）
pytest tests/ -n auto -v            # 平行執行

# 產出報告
pytest tests/ --html=reports/report.html --self-contained-html
```

## 專案結構

```
py-pw-sprint/
├── conftest.py                ← 全域 fixtures (page, api_client, settings)
├── pytest.ini                 ← pytest 設定 & markers
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
├── bitbucket-pipelines.yml
│
├── config/
│   └── settings.py            ← 多環境設定 (dev / staging / prod)
│
├── pages/                     ← Page Object Model
│   ├── base_page.py
│   └── login_page.py
│
├── utils/
│   ├── api_client.py          ← HTTP client wrapper
│   ├── db.py                  ← SQL 查詢工具
│   ├── logger.py              ← Logging
│   ├── schemas.py             ← Pydantic models (API schema)
│   └── test_data.py           ← 測試資料工廠
│
├── tests/
│   ├── api/                   ← API 測試 (requests + schema 驗證)
│   ├── ui/                    ← UI 測試 (Playwright + POM)
│   └── integration/           ← 整合測試 (API + UI + DB)
│
├── fixtures/                  ← 外部測試資料
├── notes/                     ← 學習筆記（見下方）
├── reports/                   ← HTML 報告
├── screenshots/               ← 截圖
└── logs/                      ← 日誌
```

## 學習筆記重點 & 總結

10 天衝刺學習計畫，每天 2 小時，核心學習重點 & 筆記放在 `notes/` 目錄：

| Day | 主題 | 筆記 | 狀態 |
|-----|------|------|------|
| 0 | 環境建置 + JS ↔ Python 對照 | [day00-setup](notes/day00-setup.md) | ✅ |
| 1 | pytest 入門 (discovery, assert, markers) | [day01-pytest-basics](notes/day01-pytest-basics.md) | ✅ |
| 2 | Fixtures & Parametrize | [day02-fixtures-parametrize](notes/day02-fixtures-parametrize.md) | ✅ |
| 3 | Playwright 基礎 (locator, expect, trace) | [day03-playwright-basics](notes/day03-playwright-basics.md) | ✅ |
| 4 | POM + 等待策略 + 網路攔截 | [day04-pom](notes/day04-pom.md) | ✅ |
| 5 | API 測試 (requests + Pydantic schema) | [day05-api-basics](notes/day05-api-basics.md) | ✅ |
| 6 | API 框架化 + 認證 | [day06-api-advanced](notes/day06-api-advanced.md) | ✅ |
| 7 | 框架設計 (設定管理, logging, 報告) | [day07-framework-design](notes/day07-framework-design.md) | ⬜ |
| 8 | 測試金字塔 + DB 驗證 | [day08-test-strategy-db](notes/day08-test-strategy-db.md) | ⬜ |
| 9 | CI/CD + Docker + 平行執行 | [day09-cicd](notes/day09-cicd.md) | ⬜ |
| 10 | 整合 + 面試準備 | [day10-integration-review](notes/day10-integration-review.md) | ⬜ |

其他筆記：[推薦資源](notes/resources.md) ｜ [面試 Q&A](notes/interview-qa.md)

### 學習 TOP 5 觀念

**Junior SDET — 把一個測試寫好**

| # | 觀念 | 重點 | 對應 Day |
|---|------|------|----------|
| 1 | Fixture 依賴注入 + Scope 生命週期 | 測試宣告「我需要什麼」由 pytest 注入；scope 控制資源壽命；yield 實現 setup/teardown；conftest.py 跨檔共享 | Day 2 |
| 2 | Playwright Locator 策略 + expect 自動等待 | Locator 優先順序：role > label > test-id > CSS > XPath；expect 自動重試至條件成立或 timeout，不同於 assert 的一次性判斷 | Day 3 |
| 3 | Page Object Model (POM) | locator 集中在 `__init__`、操作封裝為方法、測試中不出現任何 `page.locator()`；UI 改版只改 POM | Day 4 |
| 4 | API 測試 + Pydantic Schema 驗證 | 完整 CRUD + 正反向覆蓋；Pydantic `model_validate()` 一行完成結構驗證；schema 與測試邏輯分離 | Day 5 |
| 5 | Parametrize 資料驅動測試 | 一個 function + 多組資料 = 多個獨立測試案例；規格驗證（絕對值）vs 行為驗證（相對關係） | Day 2, 6 |

**Mid-level SDET — 能獨立建構可複用的測試元件**

| # | 觀念 | 重點 | 對應 Day |
|---|------|------|----------|
| 1 | API Client 抽象層 + 認證流程 | APIClient wrapper 統一管理 session/headers；token auth 封裝為 `set_auth_token()`；與 conftest fixture 整合，整個 session 共用已認證 client | Day 6 |
| 2 | 多環境設定管理 | dataclass 定義 Settings；環境變數 `TEST_ENV=staging` 切換；設定與程式碼分離，不寫死 URL | Day 7 |
| 3 | 測試金字塔 — 分層判斷 | Unit 驗邏輯、API 驗合約、UI 只驗關鍵流程；同一功能 API 已驗邏輯，UI 層只驗「有沒有正確顯示」 | Day 8 |
| 4 | 資料驅動測試進階 | 測試資料外部化 (JSON/CSV)；parametrize `ids` 讓報告可讀；從「手寫 test case」到「管理測試資料」 | Day 6 |
| 5 | POM 三層架構 | BasePage (通用方法) → 具體 Page (繼承 + 專屬 locator) → Test (只呼叫 Page 方法)；設計給團隊共用的頁面元件 | Day 4 |

**Senior SDET — 設計讓整個團隊高效運作的測試基礎建設**

| # | 觀念 | 重點 | 對應 Day |
|---|------|------|----------|
| 1 | 框架架構設計 | Logging 雙 handler (console INFO + file DEBUG)；pytest Hook (`pytest_runtest_makereport`) 實現失敗自動截圖；Allure history/trending 跨次執行保留 | Day 7 |
| 2 | 整合測試設計模式 | API 快速建資料 → UI 驗證顯示 → API 清除；`page.route()` mock 外部依賴解耦後端；`expect_response()` 監聽 UI 觸發的 API 請求 | Day 8 |
| 3 | CI/CD Pipeline 設計 + 平行執行 | 分層觸發 (PR: Smoke <5min / Merge: API+UI <15min / Nightly: Full <60min)；Docker 保證環境一致；xdist 每 worker 各建 session fixture 需 filelock | Day 9 |
| 4 | 測試資料管理策略 | Factory Pattern (動態產生) / Fixture Files (固定參考) / API Seeding (真實 DB 狀態) 三種策略按場景取捨 | Day 8 |
| 5 | DB 驗證 + 資源生命週期 | SQL 交叉驗證 API 回應是否真正寫入 DB；context manager 管理連線不 leak；fixture scope 控制 seed data 共用範圍與清除時機 | Day 8 |