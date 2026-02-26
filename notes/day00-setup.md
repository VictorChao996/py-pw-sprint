# Day 0: 環境建置與專案結構

> ⏱ 預計 30 分鐘（開始前一天完成）

## 安裝清單

```bash
# 1. 確認 Python 版本 (建議 3.11+)
python3 --version

# 2. 建立專案資料夾 & 虛擬環境
cd py-pw-sprint
python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux

# 3. 安裝核心套件
pip install pytest playwright requests pytest-playwright pytest-html httpx pydantic
playwright install  # 下載瀏覽器引擎 (Chromium, Firefox, WebKit)

# 4. 驗證安裝
pytest --version
python -c "from playwright.sync_api import sync_playwright; print('Playwright OK')"
```

## 初始專案結構

```
py-pw-sprint/
├── README.md
├── requirements.txt          ← 套件依賴
├── pytest.ini                ← pytest 設定
├── conftest.py               ← 全域 fixtures
├── tests/
│   ├── ui/                   ← UI 自動化測試
│   ├── api/                  ← API 自動化測試
│   └── integration/          ← 整合測試
├── pages/                    ← Page Object Model
├── utils/                    ← 工具函式
└── config/                   ← 設定管理
```

## Node.js ↔ Python 快速對照（給有 JS 背景的你）

| 概念 | Node.js / Playwright Test | Python / pytest + Playwright |
|------|--------------------------|------------------------------|
| 測試框架 | `@playwright/test` | `pytest` + `pytest-playwright` |
| 測試檔案 | `*.spec.ts` | `test_*.py` 或 `*_test.py` |
| 斷言 | `expect(locator).toBeVisible()` | `expect(locator).to_be_visible()` |
| 非同步 | `async/await` (預設) | **同步 API 為主** (`sync_api`) |
| Hook | `beforeEach / afterEach` | `@pytest.fixture` |
| 設定檔 | `playwright.config.ts` | `pytest.ini` + `conftest.py` |
| 參數化 | `test.describe` + loop | `@pytest.mark.parametrize` |
| 套件管理 | `npm` / `pnpm` | `pip` / `poetry` |
