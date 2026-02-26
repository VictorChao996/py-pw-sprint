# 面試話術重點

## Q: 描述你設計自動化框架的經驗

> 我使用 **Python + pytest + Playwright** 設計了一個多層自動化測試框架。架構上採用 **Page Object Model** 分離 UI 元素定位與測試邏輯，使用 **pytest fixtures** 進行依賴注入和資源管理。API 測試使用封裝過的 **APIClient** 搭配 **Pydantic** 做 schema 驗證。設定管理支援多環境切換，並整合 **logging** 與 **HTML 報告**。整個框架可以透過 **Jenkins/Bitbucket Pipeline** 自動觸發，支援 **pytest-xdist 平行執行**。

## Q: 如何決定測試策略？

> 我遵循 **測試金字塔** 原則：大量的 unit/API 測試確保邏輯正確，少量的 UI 測試驗證關鍵使用者流程。CI/CD 中，每次 commit 跑 **smoke tests**，merge 到 main 跑 **regression tests**，release 前跑**跨瀏覽器完整測試**。API 測試我會驗證 status code、response schema、以及 edge cases。

## Q: 如何處理不穩定的測試 (Flaky Tests)？

> 首先確認是否是 **等待策略** 問題——Playwright 有 auto-waiting 機制，但某些動態內容可能需要顯式等待。其次檢查 **測試隔離性**——每個測試是否有獨立的資料和狀態。第三是 **環境因素**——網路延遲、第三方服務不穩定等。我會用 `page.route()` **mock 外部 API** 來隔離依賴，並在 CI 中使用 **retry 機制** 作為最後手段。

## Q: Playwright vs Selenium，為什麼選 Playwright？

> Playwright 有幾個顯著優勢：**Auto-waiting** 大幅減少 flaky tests；原生支援**多瀏覽器**（Chromium, Firefox, WebKit）；**Trace Viewer** 讓 debug 更直覺；內建 **API testing** 能力不需額外工具；**codegen** 工具加速測試開發。而且 Playwright 是 Microsoft 主導開發，社群活躍、更新迅速。

## Q: 你對 MQTT 和網路產品測試的了解？

> MQTT 是 **publish/subscribe** 模式的輕量級協定，廣泛用於 IoT 和網路設備。在 mesh networking 產品中，設備間的狀態同步和指令下發常透過 MQTT 實現。Python 有 `paho-mqtt` 套件可以用來撰寫 MQTT 的自動化測試。我也了解 RESTful API 和 RPC 模式的差異，可以根據產品的通訊架構設計對應的測試策略。
