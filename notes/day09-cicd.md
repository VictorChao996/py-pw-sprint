# Day 9: CI/CD 整合 + 平行執行

> ⏱ 2 小時 ｜ 🎯 將自動化測試整合至 CI/CD pipeline，並優化執行效能

## 學習目標

- [ ] 撰寫 Jenkinsfile 和 Bitbucket Pipeline 設定
- [ ] 使用 Docker 建立一致的測試環境
- [ ] 使用 `pytest-xdist` 平行執行測試
- [ ] 理解測試在 CI/CD 中的角色與觸發策略

## 核心知識點

### 9.1 Jenkinsfile

```groovy
// Jenkinsfile
pipeline {
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:v1.49.0-noble'
        }
    }

    environment {
        TEST_ENV = 'staging'
    }

    stages {
        stage('Install') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'playwright install --with-deps'
            }
        }

        stage('Smoke Tests') {
            steps {
                sh 'pytest tests/ -m smoke -v --html=reports/smoke.html --self-contained-html'
            }
        }

        stage('API Tests') {
            steps {
                sh 'pytest tests/api/ -v --html=reports/api.html --self-contained-html'
            }
        }

        stage('UI Tests') {
            steps {
                sh 'pytest tests/ui/ -v --html=reports/ui.html --self-contained-html --tracing retain-on-failure'
            }
        }

        stage('Full Regression') {
            when {
                branch 'main'
            }
            steps {
                sh 'pytest tests/ -v -n auto --html=reports/regression.html --self-contained-html'
            }
        }
    }

    post {
        always {
            publishHTML(target: [
                reportDir: 'reports',
                reportFiles: '*.html',
                reportName: 'Test Reports'
            ])
            archiveArtifacts artifacts: 'screenshots/**/*.png', allowEmptyArchive: true
        }
        failure {
            // 通知 (Slack / Email)
            echo 'Tests failed! Check the report.'
        }
    }
}
```

### 9.2 Bitbucket Pipelines

```yaml
# bitbucket-pipelines.yml
image: mcr.microsoft.com/playwright/python:v1.49.0-noble

definitions:
  steps:
    - step: &install
        name: Install Dependencies
        caches:
          - pip
        script:
          - pip install -r requirements.txt
          - playwright install --with-deps

    - step: &smoke-tests
        name: Smoke Tests
        script:
          - pytest tests/ -m smoke -v --junitxml=test-results/smoke.xml

    - step: &api-tests
        name: API Tests
        script:
          - pytest tests/api/ -v --junitxml=test-results/api.xml

    - step: &ui-tests
        name: UI Tests
        script:
          - pytest tests/ui/ -v --junitxml=test-results/ui.xml

pipelines:
  pull-requests:
    '**':
      - step: *install
      - parallel:
          - step: *smoke-tests
          - step: *api-tests

  branches:
    main:
      - step: *install
      - parallel:
          - step: *api-tests
          - step: *ui-tests
```

### 9.3 Docker 測試環境

```dockerfile
# Dockerfile
FROM mcr.microsoft.com/playwright/python:v1.49.0-noble

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 預設執行 smoke tests
CMD ["pytest", "tests/", "-m", "smoke", "-v", "--html=reports/report.html", "--self-contained-html"]
```

```bash
# 建構 & 執行
docker build -t pw-tests .
docker run --rm -v $(pwd)/reports:/app/reports pw-tests

# 執行特定測試
docker run --rm pw-tests pytest tests/api/ -v
```

### 9.4 平行執行 — pytest-xdist

```bash
# 安裝
pip install pytest-xdist

# 自動偵測 CPU 核心數
pytest tests/ -n auto

# 指定 worker 數量
pytest tests/ -n 4

# 依檔案分配（預設）
pytest tests/ -n auto --dist loadfile

# 平行 + 詳細輸出
pytest tests/ -n auto -v
```

```python
# 注意：平行執行時 fixture scope 的影響
# - session scope fixture: 每個 worker 都會各自建立一份
# - 如果測試之間有共享狀態（如 DB），需要特別處理

# 使用 file lock 保護共享資源（進階）
# pip install filelock
import pytest
from filelock import FileLock

@pytest.fixture(scope="session")
def shared_db_setup(tmp_path_factory):
    root_tmp_dir = tmp_path_factory.getbasetemp().parent
    lock = root_tmp_dir / "db.lock"

    with FileLock(str(lock)):
        # 只有第一個拿到 lock 的 worker 會執行 setup
        pass
```

### 9.5 CI/CD 觸發策略

```
推薦的測試觸發策略：

┌──────────────────┬─────────────────┬────────────────────┐
│ 觸發時機          │ 執行的測試       │ 預期時間           │
├──────────────────┼─────────────────┼────────────────────┤
│ 每次 Commit/PR   │ Smoke Tests     │ < 5 分鐘           │
│ PR Merge to main │ API + UI Tests  │ < 15 分鐘          │
│ 每日排程 (nightly)│ Full Regression │ < 60 分鐘          │
│ Release 前       │ All + 跨瀏覽器   │ < 120 分鐘         │
└──────────────────┴─────────────────┴────────────────────┘
```

## 實作練習

> **練習 9**：
> 1. 撰寫 `Jenkinsfile`（參考範例調整）
> 2. 撰寫 `bitbucket-pipelines.yml`
> 3. 撰寫 `Dockerfile`
> 4. 安裝 `pytest-xdist`，用 `-n auto` 跑全部測試，比較執行時間
> 5. 更新 `requirements.txt`

## 完成標準

```bash
pytest tests/ -n auto -v  # 平行執行全部測試
docker build -t pw-tests .  # Docker image 建構成功
cat Jenkinsfile  # 確認 pipeline 定義完整
```
