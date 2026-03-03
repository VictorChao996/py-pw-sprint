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
| 4 | POM + 等待策略 + 網路攔截 | [day04-pom](notes/day04-pom.md) | ⬜ |
| 5 | API 測試 (requests + Pydantic schema) | [day05-api-basics](notes/day05-api-basics.md) | ⬜ |
| 6 | API 框架化 + 認證 + MQTT 概念 | [day06-api-advanced](notes/day06-api-advanced.md) | ⬜ |
| 7 | 框架設計 (設定管理, logging, 報告) | [day07-framework-design](notes/day07-framework-design.md) | ⬜ |
| 8 | 測試金字塔 + DB 驗證 | [day08-test-strategy-db](notes/day08-test-strategy-db.md) | ⬜ |
| 9 | CI/CD + Docker + 平行執行 | [day09-cicd](notes/day09-cicd.md) | ⬜ |
| 10 | 整合 + 面試準備 | [day10-integration-review](notes/day10-integration-review.md) | ⬜ |

其他筆記：[推薦資源](notes/resources.md) ｜ [面試 Q&A](notes/interview-qa.md)
