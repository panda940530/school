n8n 技術文章
============
學生：邱顯崴   指導教授：陳裕賢教授

摘要 (Abstract)
------------
本文章以 n8n 自動化流程平台（workflow automation） 為核心，建置一套「校務資料智慧查詢系統」。系統整合自然語言查詢、AI SQL 生成、PostgreSQL 校務資料庫、AI自然回應生成以及 Flask 前端介面，使本校師生無需撰寫大量程式或 SQL，即可快速查詢不同專案等校務資料。

使用者僅需在網頁端輸入自然語言問題（如「111–114 年度各學院計畫件數與總金額」），n8n 流程即會自動：

1. 接收 Webhook 請求
2. 透過 LLM 產生 PostgreSQL 查詢語句
3. 查詢校務資料庫
4. 自動生成統計圖表規格
5. LLM產生中文分析解讀
6. 回傳 JSON 給 Flask 前端顯示表格、圖表與 AI 說明 

本系統示範 n8n 在校務流程上的應用價值：

* 行政單位可快速取得統計資訊
* 教師查詢計畫資訊更便利
* 兼具低程式碼、自動化、高擴充性
* 並透過容器化部署方式（Image 打包），提升可移植性與部署效率

目錄(Catalog)
-------------
### 1. [系統簡介](#system)

* 核心概念（Core Concept）
* 使用者介面導覽（UI Walkthrough）
* 使用範例（Example Workflow）

### 2. [n8n 基礎教學與本地部署](#introduction)  

* n8n 安裝指南（Installation & Setup）  
* 核心節點深度解析（Core Nodes Deep Dive）  
* 憑證安全設置（Credential Management）  
* 工作流管理與技巧（Workflow Management）
  
### 3. [系統架構與設計概念](#system_design)  

* 系統架構圖（Architecture Diagram）  
* n8n 裡的邏輯解析：從自然語言到資料庫的 AI 旅程  
* 自然語言查詢設計（Natural Language Query Design）

### 4. [資料庫架構與 AI 自動化入庫流程](#database)

* 校務資料庫架構設計（Schema Design）
* LLM 如何自動分類（AI-Assisted Data Classification）
* 資料存取流程總結（Ingestion Summary）

### 5. [系統核心工作流拆解](#workflow)

* 第一階段：動態情境注入（Dynamic Context Injection）
* 第二階段：SQL 與圖表規格雙重生成（Dual Output: SQL \+ Chart Spec）
* 第三階段：安全查詢資料庫（Secure SQL Execution）
* 第四階段：AI 資料分析師（Semantic Interpretation）
* 第五階段：建構 API 回應（Response Construction）

### 6. [n8n 與外部系統整合方法](#integrations)

* 與 PostgreSQL 的整合
* 與 Flask、前端的資料交換
* 前端視覺化實作

### 7. [校務自動化應用案例](#result)

* 年度經費總額與計畫件數統計
* 執行中計畫查詢
* 多年期計畫分析
* 委託單位（政府 / 企業 / 其他）分布
* 教師承接計畫排行

### 8. [部署與 Image 打包](#container)

* 打包成image的好處
* Dockerfile 撰寫
* Docker Compose 部署

### 9. [結語：n8n 在校務與教學創新的價值](#conculation)

* 低程式碼與 AI 的未來趨勢
* 提升行政效率與資料可及性

### 10. [附錄](#appendix)

* GitHub 連結
* 教學:如何複製我的代碼，到自己電腦執行

<h2 id="system">系統簡介</h2>

歡迎踏入自動化的世界。在開始構建複雜的自動化流程之前，我們需要先熟悉手中的工具。本章將帶領您認識 n8n 的核心運作邏輯，並深入導覽其使用者介面（Editor UI）。一旦您熟悉了這個「數位工作檯」，您將發現自動化並不只是編寫程式碼，更像是一場充滿邏輯美感的積木遊戲。

---

### 核心概念 (Core Concept)

#### 什麼是 n8n？

n8n (Nodemation) 是一款**基於節點 (Node-based)** 的工作流自動化工具。

想像一下，傳統的自動化工具通常是線性的——「如果發生 A，就執行 B」。但現實世界的業務邏輯往往更加複雜，充滿了分支、迴圈與數據處理。

n8n 採用了「流程圖」的概念。您在一個無限延伸的畫布上，將代表不同功能的**節點 (Nodes)** 放置其中，並用**連線 (Connections)** 將它們串連起來。數據就像流水一樣，沿著這些連線從一個節點流向另一個節點，途中經過變形、篩選或增強，你可以在其中看到每個資料在不同節點是怎麼被處理的，最終完成任務。

#### n8n 與傳統工具的區別

| 特性 | 傳統工具 (如 Zapier) | n8n |
| :---- | :---- | :---- |
| **視覺呈現** | 垂直列表 (Linear List) | 網狀流程圖 (Flowchart) |
| **邏輯複雜度** | 適合簡單、單向觸發 | 擅長複雜分支、迴圈、錯誤處理 |
| **數據透明度** | 看到的是「結果」 | 可檢視每個節點輸入/輸出的 JSON 數據 |
| **部署方式** | 僅限雲端 (SaaS) | 可雲端，也可**私有化部署 (Self-hosted)** |

簡單來說，如果傳統工具是「設定清單」，那麼 n8n 就是在「繪製藍圖」。它給予了開發者與非技術人員極高的自由度，去構建真正符合需求的自動化邏輯。

---

### 使用者介面導覽 (UI Walkthrough)

當您第一次進入 n8n 的編輯器時，可能會被眼前空白的網格所困惑。別擔心，這個介面設計得非常直觀。我們可以將其劃分為四個主要區域：

<img width="1586" height="792" alt="image" src="https://github.com/user-attachments/assets/f9802591-ce96-4dcd-a298-d40b6c386d97" />

#### 圖1:n8n第一次進入畫面，畫布(藍框)、節點面板(綠框)、執行條(黃框)、側邊欄(紅框)

#### 畫布 (Canvas)

這是您的主要工作檯。這是一個無限大的二維平面，您可以按住滑鼠中鍵拖曳畫面，或使用Ctrl \+ 滾輪縮放視角。所有的自動化邏輯都在這裡發生。

* **操作技巧：** 點擊任何空白處並拖曳可框選多個節點；選中節點後按 Ctrl+C / Ctrl+V 可快速複製邏輯。

#### 節點面板 (Nodes Panel)

位於介面右側（或點擊畫布上的 \+ 號喚起），這是您的「工具箱」。

* **Trigger (觸發器)：** 點擊 \+ 號之後需要選擇一個觸發器，這是工作流的起點，透過事件來觸發工作流。例如：當收到 Email 時、每週一早上 9 點、或是 Webhook 被呼叫時。  
* **Action (動作)：** 當你選擇完觸發器之後可以選擇，這是執行具體任務的節點。例如：寫入 Google Sheets、發送 Slack 訊息、或是進行 HTTP 請求。這裡支援數百種整合服務，您只需在搜尋框輸入服務名稱即可找到對應節點。

#### 執行條 (Execution Bar)

位於畫面底部。這是控制工作流運作的駕駛艙。

* **Test workflow (測試工作流)：** 點擊此按鈕，n8n 會立即執行當前畫布上的流程，你也可以把滑鼠移到觸發器上面左邊會出現execute workflow，會執行那一個觸發器的工作流。  
* **execution logs (執行過程)：** 每個節點詳細執行了什麼，資料怎麼被處理，都會顯示在下面。(當你加入On Chat Message這個觸發器，聊天框會顯示在左下角)

#### 側邊欄 (Sidebar)

位於畫面最左側與上方，用於管理全域設定。

* **Workflows：** 回到您的工作流列表。  
* **Credentials (憑證)：** 這是存放 API Key、密碼等敏感資訊的金庫。在 n8n 中，憑證與工作流是分開管理的，這意味著同一組 Google 帳號憑證可以被多個不同的工作流重複使用。  
* **Executions (執行紀錄)：** 位於畫面上方，這裡記錄了每一次工作流運行的詳細歷史，是除錯 (Debug) 的重要區域。  
* **Active (啟用開關)：** 位於畫面右上角。當您完成測試並準備正式上線時，需將此開關打開，工作流才會在後台自動運行。  

---

### 使用範例 (Example)

為了讓您更直觀地理解 UI 的運作，我們將建立一個最基礎的 **"Hello World"** 工作流：**「每當我手動點擊測試時，系統產生一條訊息並顯示出來」**。

#### 步驟一：建立起點 (Trigger)

我們需要一個觸發點。在這個範例中，我們使用 **"Trigger manually" (手動觸發)** 。

1. 點擊畫布上的 `\+` 號。  
2. 選擇 `Trigger manually` 。  
3. 將其加入畫布。

#### 步驟二：添加動作 (Action)

接下來，我們讓系統產生一筆資料。

1. 點擊 `Manual Trigger` 節點右側的小圓點（連接點）。  
2. 這會自動打開節點面板。搜尋 `Code` 節點，選擇`Code in Javascript`。  
3. 選擇後，節點會自動連接。

#### 步驟三：設定內容與執行

1. 點擊打開 `Code` 節點。  
2. 在 JavaScript 編輯區輸入簡單的代碼：

	return [{json: {message: "Hello world"}}];		

3. 關閉節點設定視窗。  
4. 點擊底部的 **"execute workflow"** 按鈕。

此時，您會看到介面發生變化，執行條上方會展開一個結果面板，輸出會顯示Message:Hello world。

<img width="2447" height="661" alt="image" src="https://github.com/user-attachments/assets/622a5184-d0c0-47f5-818b-70998b5e0139" />

<h2 id="introduction">n8n 基礎教學與本地部屬</h2>

在上一章我們了解了 n8n 的介面概觀，現在是時候捲起袖子，打造屬於你自己的自動化引擎了。

本章的目標非常明確：**將n8n在你的電腦本地部屬**，並且會講解構建查詢校務系統的幾個常用節點的功能方便後續理解。

---

### n8n 安裝指南 (Installation & Setup)

雖然 n8n 提供付費的 Cloud 版本，但作為開發者或學校單位，**部屬在本地 (Self-hosted)** 往往是更具彈性且成本效益的選擇。

#### Docker Desktop安裝

要將n8n部屬在本地，首先要先安裝**Docker**，對於正式的校務系統或長期運作的自動化任務，**Docker** 是最佳選擇。它能確保環境隔離，並且容易維護與升級。

安裝docker前，我們要先安裝WSL2，在桌面底下的搜尋欄裡，搜尋Windows PowerShell，到命令行執行指令`wsl -v`，如果顯示未安裝適用於Linux的Windows子系統(如果有顯示版本，代表你已經裝好了)，執行指令`wsl \--install`，即可安裝WSL2。

<img width="711" height="348" alt="image" src="https://github.com/user-attachments/assets/6407a08f-dcf8-4a43-b432-35e911cb017e" />

圖2:安裝好WSL2，執行`wsl \-v`的畫面，顯示這些表示成功安裝。

接下來到[Docker官網][docker_url]，選擇下載**Docker Desktop**，選**Windows \- AMD64。**

<img width="1798" height="1181" alt="image" src="https://github.com/user-attachments/assets/62921ea6-d780-4738-880b-cd51ad9825f6" />

 [docker_url]: https://www.docker.com/

打開下載好的安裝包，勾選Use WSL 2 instead of Hyper-V，安裝好之後重啟電腦。

<img width="1350" height="934" alt="image" src="https://github.com/user-attachments/assets/263ba66e-4ef9-4f36-ae38-99b80e96cde7" />

安裝好之後會看到，這時什麼東西都沒有。

![][image7]

我們在上面搜尋欄搜尋n8n，對n8nio/n8n點選Pull。

<img width="1204" height="957" alt="image" src="https://github.com/user-attachments/assets/b394609e-cd44-4d16-9f68-e7a572910936" />

下載完成之後，你會發現旁邊的最左側的images點進去之後，多了n8nio/n8n。

<img width="2080" height="120" alt="image" src="https://github.com/user-attachments/assets/23fb31f5-e048-4731-bd33-5687e387ded8" />


點選run之後，在name填入n8n，Host port裡填入5678，點擊run。

<img width="962" height="941" alt="image" src="https://github.com/user-attachments/assets/4e97bca5-4f07-4faf-ab54-090edfc934bb" />

回到containers，會發現多了一個n8n，確保左邊的燈是綠的，如果燈不是綠的點擊左側的start鍵。

<img width="2066" height="63" alt="image" src="https://github.com/user-attachments/assets/7185e42b-21e0-4309-92bd-5490095478a4" />

點擊5678:5678會到一個瀏覽器，需要設置帳號，設置完帳號按Next。

<img width="692" height="1152" alt="image" src="https://github.com/user-attachments/assets/6a009b1b-278c-4294-95e5-41d4cbe0d5cc" />

可以不用填任何東西直接點 Get started。

<img width="2559" height="1231" alt="image" src="https://github.com/user-attachments/assets/d0ded24b-790c-4b88-83a1-42753f49c09e" />

這個也可以直接點 skip。

<img width="2557" height="1233" alt="image" src="https://github.com/user-attachments/assets/afade37d-850c-41aa-a9cf-bd19f215b195" />

這樣你就會獲得一個空的本地自架的n8n，點選中間的 Start from scratch，開啟你的第一個工作流\!

<img width="2558" height="1157" alt="image" src="https://github.com/user-attachments/assets/eba5fd59-2d74-42b4-b790-bfbc8088d03c" />

---

### 核心節點深度解析 (Core Nodes Deep Dive)

安裝完成後，接下來為了方便你之後能了解，我們將介紹「校務查詢系統」會用到的節點，以及用這個來舉例。

#### Trigger \- Webhook Node (觸發器)

這是許多自動化的起點。它讓你的工作流能夠「聆聽」外部世界的呼叫。

* **概念：** 就像一個專屬的電話號碼，當有人撥打 (發送 HTTP 請求) 時，工作流就會啟動。  
* **設定重點：**  
  * **HTTP Method:** 通常設為 `POST` 以接收資料（如表單內容）。  
  * **Path:** 自定義網址路徑，例如設置 `school`，節點會變成`http://localhost:5679/webhook-test/school`。  
  * **Respond:** 什麼時候以及如何回應這個節點，例如當選擇`Using 'Respond to Webhook' Node`，當工作流執行到`Respond to Webhook`這個節點時，會將資料回傳回去。  
  * **Test vs. Production URL:**  
    * **Test URL:** 僅在編輯器打開且點擊「Listen」時有效，用於開發除錯。  
    * **Production URL:** 需點擊右上角「Activate」啟用自動工作流後才生效，用於正式上線。  
* **應用場景：** 在前端輸入問題，系統透過 Webhook 將輸入的問題傳送給 n8n。

<img width="2502" height="1189" alt="image" src="https://github.com/user-attachments/assets/b81c5839-f5ac-4191-8ced-67b6fb8e9537" />

#### Data Transformation \- Code Node (邏輯處理)

當內建節點無法滿足複雜邏輯時，程式碼就是你的救星。

* **概念：** 使用 JavaScript (或 Python) 處理進階的資料轉換。  
* **設定重點：** 選擇 `Run Once for All Items` (批次處理) 或 `Run Once for Each Item` (逐筆處理)。  
* **應用場景：** 處理AI回應或postgreSQL回應的資料格式。

<img width="2508" height="1194" alt="image" src="https://github.com/user-attachments/assets/0ae5512e-0cbf-4ff1-80d1-b1cda78c31bd" />

#### AI \- Google Gemini \- Message a model (連接外部)
如果說 Code Node 是邏輯運算核心，那麼 Google Gemini Node 就是你的「AI 秘書」。透過 **Message a model**動作，你可以將任何的資料輸入至Gemini，設定好提示詞，讓AI進行任何您想的操作(僅限文本)。

* **概念:** 這個節點允許你將前一個步驟的資料（例如：學生的問題、會議記錄、報名表內容）作為「提示詞 (Prompt)」的一部分發送給 Google 的 AI 模型。AI 處理後，會回傳一段人類可讀的文字。  
* **設定重點:**  
  * **Model (模型選擇):**  
    * **Gemini 2.5 Flash:** 速度快、成本低，適合處理大量簡單任務（如：分類、擷取關鍵字）。  
    * **Gemini 2.5 Pro:** 推理能力強，適合複雜任務（如：長文摘要、創意寫作）。  
  * **Resource(輸入格式):** 給模型的資料格式、例如文本、檔案、圖片、影片。  
  * **Messages \- Prompt (提示詞):** 這是提示詞輸入的地方，你要告訴AI你需要做什麼，AI要怎麼回答，以及一些規則。你不能只寫死文字，必須善用 Expression (表達式)。
    
    **寫法範例：** 請閱讀以下學生回饋，並用一句話總結他的主要訴求：`{{ $json.feedback\_text }}`
      
    **技巧：** 直接從左側輸入面板將變數（如 `feedback\_text`）拖曳到 Prompt 欄位中，n8n 會自動產生綠色的表達式標籤。  
* **應用場景:** 將自然問題轉換成SQL指令。

<img width="2501" height="1175" alt="image" src="https://github.com/user-attachments/assets/14fbc872-7d4f-413e-8adc-150fad5b82d2" />

#### **Action in an app \- Postgres \- Execute a SQL query (資料庫操作)**

自動化的核心往往離不開資料的讀寫，需要用到資料庫，這次的校務查詢系統就需要操作PostgresSQL這個資料庫。

* **概念：** 直接對關聯式資料庫進行增刪改查 (CRUD)。  
* **設定重點：**  
  * **Operation:** 選擇 `Execute Query` (執行 SQL)，Exete Query其實就包括了Delete、Select、Update、Insert，可以讓我們執行刪除、查詢、更新、插入等對資料庫的操作，只是要執行SQL指令。  
* **應用場景：** 將處理好的計畫資料，寫入 `Projects` 資料表。

<img width="2511" height="1203" alt="image" src="https://github.com/user-attachments/assets/777202d6-2304-4a24-a3c4-3ee845752b79" />
  
---

### 憑證安全設置 (Credential Management)

在 n8n 中，我們絕不將密碼直接寫在節點或程式碼裡。憑證 (Credentials) 是獨立管理的，這確保了安全性與重用性。

#### 為什麼要分開管理？

1. **安全性：** 憑證會被加密儲存。  
2. **便利性：** 修改一次密碼，所有使用該憑證的工作流都會自動更新。

#### **在校務查詢系統裡，需要設置的關鍵憑證**

**1. Google Gemini API (AI 整合)**

為了讓校務系統具備 AI 摘要或自動回覆功能，我們需要連接 Gemini。

1. 前往 [Google AI Studio](https://aistudio.google.com/) 申請 API Key。  
2. 在 n8n 左側選單點擊 **Credentials** \-\> **Add Credential**。  
3. 搜尋 `Google Gemini(PaLM) API`。  
4. 將 API Key 貼入欄位並儲存，確保出現Connection tested successfully。

<img width="1331" height="732" alt="image" src="https://github.com/user-attachments/assets/7d04d9c3-ee6b-46b5-a5b9-8025f78cdb21" />

**2. PostgreSQL 資料庫**

連接本地部屬的資料庫：

1. 新增 Credential，搜尋 PostgreSQL。  
2. 依序填入(參考建立資料庫這個章節會告訴你這些參數怎麼設定)：  
   * **Host:** 資料庫位址 (如 `localhost` 或 IP)。  
   * **Database:** 資料庫名稱 (預設 `postgres`)。  
   * **User:** 使用者名稱。(預設 `postgres`)。  
   * **Password:** 密碼。  
   * **Port:** 預設為 `5432`。  
3. 點擊連線測試，確保出現Connection tested successfully。

<img width="1785" height="988" alt="image" src="https://github.com/user-attachments/assets/28766024-2944-4b2e-abbb-3b2d5305cf27" />

設置好憑證，就可以在剛剛的節點`Credential to connect with`選擇你設置好的節點。

<img width="875" height="814" alt="image" src="https://github.com/user-attachments/assets/9f5e9518-df56-4530-9e66-17edbcc0d7b6" />

---

### 工作流管理與技巧 (Workflow Management)

辛苦建立的工作流是重要資產，學會管理它們至關重要。

#### JSON 匯出與備份

n8n 的工作流本質上就是一串 JSON 文字。

* **匯出方法：** 在編輯器右上角的選單 (三個點圖示) 中，選擇 **"Download"**。  
* **匯入方法：** 在編輯器右上角的選單 (三個點圖示) 中，選擇 **"Import from File..."**，選擇.json即可把別人的n8n工作流匯入。  
* **備份建議：** 養成習慣將下載的`.json`檔案存入 Git 版本控制系統，或是備份到雲端硬碟。這能防止意外操作導致的邏輯遺失。

#### 操作小技巧

* **Pin Data (釘選資料)：** 在開發過程中，你可以「釘選」某個節點的輸出結果。這樣在測試後續節點時，不需要每次都重新觸發 Webhook，能大幅節省開發時間。  
* **複製貼上：** 你可以直接在畫布上選取節點，按 `Ctrl+C` / `Ctrl+V`，甚至可以跨瀏覽器分頁複製節點。

<h2 id="system_design">系統架構與設計概念</h2>

在掌握了 n8n 的基本操作與節點功能後，我們不能只滿足於簡單的自動化。在動手實作之前，必須先繪製出清晰的藍圖。

本章將帶領您設計一個「智慧校園數據查詢系統」。這不是一個簡單的聊天機器人，而是一個能夠理解自然語言、將其轉化為 SQL 指令，並從資料庫中提取精確數據的AI。

---

### 架構圖 (Architecture Diagram)

我們將採用微服務 (Microservices) 的設計思維，將系統拆解為四個核心組件。這種「各司其職」的架構能確保系統的彈性與可維護性。 

<img width="1120" height="446" alt="image" src="https://github.com/user-attachments/assets/4f0e18c5-00eb-464d-ade7-29d4e2f41612" />
  
#### 組件深度解析
* **前端呈現層：** Flask \+ Jinja2 模板（`school\_upload.html`,`school\_result.html`）負責提供查詢頁與結果頁 UI。  
* **應用邏輯層：** Flask 應用（`school.py`）接收使用者瀏覽器請求，將自然語言查詢轉送至 n8n Webhook，並把 n8n 回傳的 JSON 結果整理成表格與圖表。  
* **自動化流程/AI 層：** n8n workflow School\_SQL 負責：  
  * 接 webhook  
  * 呼叫 Gemini 產 SQL、圖表規格與中文分析  
  * 呼叫 Postgres 校務資料庫 projects 表查詢  
  * 組合 {rows, answer, chart} 回給 Flask。  
* **資料層：** PostgreSQL 校務資料庫（`projects`主表 + `college_map` 對照表等）。

---

### n8n裡的邏輯解析：從自然語言到資料庫的 AI 旅程

<img width="1369" height="781" alt="image" src="https://github.com/user-attachments/assets/0821a67d-0a20-4742-9e44-6ef6c0e5a2a7" />

在我們的架構中，最關鍵的挑戰在於：**如何讓不懂程式碼的使用者，能夠查詢複雜的資料庫？** 上圖清晰地展示了這一過程的「雙階段 AI 處理」邏輯。我們可以將其拆解為五個關鍵步驟：

#### A.意圖輸入 (User Query)

一切始於最左側的 **「使用者」**。使用者不需要學習 SQL 語法，只需使用 **「自然語言」**（如中文或英文）提出問題。

* *範例：*「請問114年承接的計畫數量？」

#### B.上下文注入與 SQL 生成 (Context Injection & SQL Generation)

這是流程圖中上方藍色箭頭與紫色 **「大語言模型 (LLM)」** 交會的地方。  
單純把問題丟給 AI 是不夠的，因為 AI 並不知道你的資料庫裡有哪些表格。因此，我們必須同時輸入三樣東西給 AI：

1. 使用者的問題。  
2. **資料庫結構 (Schema)**：即圖上方的藍色區塊。這包含了表格名稱（如 `projects`）、欄位名稱（如 `project_code`, `project_name`）以及它們的數據類型。  
3. **資料庫範例：** 能讓模型理解欄位名稱、資料類型、數值範圍與資料語意，大幅減少幻覺與欄位錯誤，提升查詢準確性。

AI 接收到這些資訊後，會進行邏輯推理，將中文問題「翻譯」成標準的 **「SQL 查詢語句」**。

* *AI 產出的 SQL：* `SELECT COUNT(\*) AS project\_count FROM projects WHERE (EXTRACT(YEAR FROM start\_date) \- 1911\) \= 114 LIMIT 100;`

#### C.資料庫執行 (Query Execution)

接著，這段生成的 SQL 語句會被傳送到 **「資料庫」**（圖中右側的青色區塊）實際執行。  
這個步驟是純粹的技術操作，不涉及 AI。資料庫會忠實地執行指令並回傳原始數據。

#### D. 數據回傳 (Raw Data Retrieval)

資料庫回傳的 **「查詢結果」** 通常是生硬的數據格式（例如 JSON 陣列或 CSV 表格）。

* *資料庫回傳：* `[{ "project\_count": 63 }]`  
  如果不做處理直接丟給使用者，體驗會非常糟糕。

#### E.結果人性化 (Result Humanization)

最後，我們再次呼叫 **「大語言模型」**（圖中下方的紫色區塊）。這次，我們將「使用者的原始問題」與「資料庫回傳的數據」一起交給 AI。  
AI 的任務不再是寫程式，而是擔任文案寫手。它會將冰冷的數字 `63` 轉化為溫暖的 **「自然語言查詢回應」**。

* *最終回應：* 「根據查詢結果，114年計畫數量總共有63件。」

---

### 自然語言查詢設計 (Natural Language Query Design)

這是本系統最具挑戰性，也最迷人的部分：**AI-to-SQL Logic**。我們要如何確保 AI 產生的 SQL 是正確且安全的？

#### A. 架構注入 (Schema Injection)

AI 不知道你的資料庫長什麼樣子。你需要透過 **System Prompt** 將資料庫結構「注入」給 AI。

**Prompt 設計範例：**

	你是一個專門為 PostgreSQL 資料庫產生查詢語句（SQL）與圖表規格（Chart Specification）的智慧分析助理。
	
	你不能編造資料，也不能修改資料，只能輸出單一條 PostgreSQL `SELECT` 或 `WITH` 查詢語句。
	
	\#\#\# 資料表結構（projects）		
	
	下方是資料表的實際結構與前幾筆資料（供你參考）：			
	
	`{{ $json.context }}`
	
#### B. 安全防護層 (Safety Layer)[

將 AI 產生的 SQL 直接丟給資料庫執行是非常高風險的（可能面臨 SQL Injection 或 AI 幻覺導致的資料刪除）。我們必須設計三道防線：

1. **Read-Only Credential:**  
   在 n8n 連接 PostgreSQL 時，**絕對不要使用 root/admin 帳號**。請在資料庫中建立一個唯讀使用者（Read-Only User），僅賦予`SELECT`權限。這是最根本的防禦。  
2. **Prompt 限制:**  
   在提示詞中明確禁止`DROP`,`DELETE`,`UPDATE`等關鍵字。  
3. **錯誤處理 (Error Handling):**  
   在 n8n 的 AI 節點後方加上檢查SQL語句的**code節點**。如果 AI 生成不允許的操作，系統應回覆「抱歉，我無法執行您的查詢」。

<h2 id="database">資料庫設計與 AI 自動化入庫 (Database Schema & AI-Enhanced Ingestion)</h2>

在打造自然語言查詢資料系統之前，我們必須先建立一個結構良好、且資料乾淨的資料庫。在工作流中，我們設計了一套自動化的 ETL (Extract, Transform, Load)流程，將原始的 Excel 報表轉化為結構化的 PostgreSQL 資料表，並利用 LLM 解決了傳統程式最頭痛的「分類問題」。

---

### 校務資料庫架構設計 (Schema Design)

我們在 PostgreSQL 中建立了一張名為 `projects` (產學計畫表) 的核心資料表。為了支援後續的金額統計與日期篩選，欄位型別的定義至關重要。

以下是資料表結構：

| 欄位名稱 (Column) | 資料型別 | 中文說明 | 備註 |
| :---- | :---- | :---- | :---- |
| **project\_code** | TEXT | **計畫代碼** | **Primary Key (主鍵)**，用於唯一識別 |
| project\_name | TEXT | 計畫名稱 |  |
| exec\_unit | TEXT | 執行單位 | 例如：資工系、商學院 |
| fund\_source | TEXT | 經費來源 | 原始資料，例如「國科會」、「某某科技公司」 |
| **unit\_category** | TEXT | **單位類別** | **由 AI 自動生成** (政府/企業/其他) |
| pi\_code | TEXT | 主持人代碼 | 用於關聯教師資料 |
| start\_date | DATE | 起始日期 | 格式轉換為 YYYY-MM-DD |
| end\_date | DATE | 應結日期 |  |
| close\_date | DATE | 實結日期 |  |
| approve\_amount | BIGINT | 核定金額 | 用於計算總經費 |
| received\_amount | BIGINT | 實收數 |  |
| spent\_amount | BIGINT | 實支數 |  |

在寫入資料庫時，我們使用了`ON CONFLICT (project\_code) DO UPDATE`語法。這意味著如果 Excel 中包含已經存在的計畫代碼，系統會自動**更新**該筆資料，而不是報錯或重複插入。這確保了資料庫永遠保持最新狀態。

---

### LLM(Large Language Model) 如何自動分類？

傳統的資料擷取最棘手的部分在於「髒資料」或「非結構化文字」。  
在原始 Excel 的「經費來源 (`fund_source`)」欄位中，可能會出現數百種不同的寫法（如：司法院、農業部、公平交易委員會、XX有限公司）。若要進行統計分析（例如：政府案 vs 企業案），傳統作法需要寫數百行的 `if-else` 或維護龐大的對照表，或者是人工一個一個填入對應的類型

在本系統中，我們利用 **Google Gemini** 進行智慧分類。以下是 n8n 工作流中的實作邏輯：

<img width="1993" height="253" alt="image" src="https://github.com/user-attachments/assets/da04289c-c3e1-41c4-896f-d09cea6c0c91" />

#### A. 資料預處理與 Prompt 組合 (Code Node)

在工作流的 `Build Funding Classification Prompt` 節點中，我們將讀取到的 Excel 資料進行批次處理，提取出所有的「經費來源」，並組裝成如下的 Prompt 發送給 AI：

```javascript
return [{
  json: {
    prompt: `以下是經費來源列表，請依照每一條的編號判斷其所屬單位：
- 若屬於政府單位輸出「政府」
- 若屬於企業部門輸出「企業」
- 若屬於其他組織輸出「其他」

政府部門-政府部門包括中央政府或地方政府，並包含由行政院國科會所訂定之中華民國科技機構名錄之總統府及行政院各部會所屬科技機構，例如：中央研究院、教育部、國科會…等。
企業部門-企業部門包括國營與民營企業
其他單位-其他大專校院及其附設醫院和育成中心、法人機構、學會、專業學術國體及其他非營利機構、國外機構等承接計畫，如：財團法人工業技術研究院、各級醫療院所、農會、漁會、信用合作社等。


請輸出 JSON 格式，例如：
[
 {"id": 1, "分類": "政府"},
 {"id": 2, "分類": "企業"},
 {"id": 3, "分類": "其他"}
]

資料如下：
${itemsList}`
  }
}];
```

讓AI回覆1、2、3代替政府、企業、其他能夠讓token降低，在處理大量資料時很有用。

#### B. AI 判讀與標籤化 (Message a Model Node)

**Gemini** 接收到指令後，會利用其廣泛的知識庫，以及我們給的提示詞來判斷。它知道「農業部」是政府機構，「XX有限公司」是企業，無需我們手動維護清單。

AI 會回傳標準的 JSON：

```json
[
	{"id": 1, "分類": "政府"},
	{"id": 2, "分類": "企業"},
	{"id": 3, "分類": "其他"}
]
```

#### C. 資料合併與清洗 (Merging Logic)

在 `Apply Funding Classification` 節點中，系統將 AI 回傳的分類結果（`unit_category`）與原始的 Excel 資料（`projects`）透過 ID 重新對接合併。

**結果：**  
每一筆寫入資料庫的計畫資料，除了原始資訊外，都多了一個乾淨的 `unit_category` 標籤。這讓後續使用者詢問「請問今年來自**企業**的產學案有多少？」時，SQL 可以直接下 `WHERE unit_category = '企業'`，大幅提升查詢精準度。

---

### 資料存取流程總結 (Ingestion Summary)

1. **Trigger:** 管理者透過`Start Import Process`這個節點上傳 Excel 檔案。  
2. **Extract:** n8n 解析 Excel，將中文欄位映射為英文變數 (`Parse Uploaded File` -> `Normalize Project Data`)。  
3. **Enrich (AI):** 將「經費來源」欄位打包送往 Gemini，獲取「單位類別」標籤 (`LLM Classify Funding Source`)。  
4. **Load:** 將處理好的完整資料（含 AI 標籤）寫入 PostgreSQL (`Upsert Project Record`)，以及根據執行單位(`exec_unit`)分類到不同學院(`college_category`)。

透過這個架構，我們不僅完成了資料的數位化，更在入庫的第一步就完成了資料的**加值**，為後續的 AI 查詢系統打下了最堅實的基礎。

<h2 id="workflow">系統核心工作流拆解 (System Core Workflow Decomposition)</h2>

在 n8n 中，我們將這個複雜的思考過程拆解為五個精密咬合的齒輪。不同於簡單的聊天機器人，雖然這個流程並非完整的 AI Agent，但它已展現 **Agentic Workflow** 的核心特徵——能夠感知環境（由 Schema 與 Sample Data 所構成的上下文）、使用工具（PostgreSQL 作為資料查詢接口）、並產生結構化輸出（SQL 查詢語句與圖表規格），以下是n8n工作流：

<img width="2053" height="246" alt="image" src="https://github.com/user-attachments/assets/01a2ddab-e4e4-4491-8371-c75315b440f4" />

### 第一階段：動態情境注入 (Dynamic Context Injection)

**節點關鍵：**

AI 無法憑空理解資料庫的結構，因此我們在此階段讓模型「看見」資料庫的真實樣貌。這不是典型 RAG（因為未使用向量檢索或文件檢索），但採用了 **Schema-Augmented Prompting** 的理念：

1. **獲取結構：** 透過PostgreSQL(`Fetch Database Schema`)這個節點，系統先查詢 PostgreSQL 的 `information_schema.columns`，取得 `projects` 表的所有欄位名稱與型別。  
2. **獲取樣本：**  透過PostgreSQL(`Fetch Sample Records`)這個節點，撈取前 5 筆真實資料作為範例 (Few-shot prompting)。  
3. **組合提示：** 在Code(`Build LLM Query Context`) 節點中，我們將「使用者問題」、「資料表欄位定義」與「樣本資料」打包成一個巨大的 Prompt 上下文 (`context`)。  
4. **學院人數：** 為了要讓AI能計算不同學院人均執行有關的問題，我們在欄位編輯(`Provide College People Mapping`)節點，提供不同學院的人數，特別寫在這裡可以方便後續調整人數。  
5. **最終組合：** 透過merge(1Merge Context and Domain Knowledge1)節點，這裡將Merge節點設成`combine`可以把`context`跟學院人數組再一起，最後一起送入AI當題示詞。

**為什麼這樣做？** 知道 `approve_amount` 是金額欄位、理解 `unit_category` 包含「政府」、「企業」等分類、正確推論 `approve_year` 是 西元年、選對欄位名稱而不是憑空猜測，最終產生的 SQL 會更接近人工手寫的版本，也能避免 LLM 常見的幻覺欄位（hallucinated fields）。

### 第二階段：雙重輸出生成 —— SQL 與圖表規格 (Dual-Output Generation)

**節點關鍵：**

這是本系統最聰明的大腦。在AI(`LLM Generate SQL & ChartSpec`)這個節點裡我們在 Prompt 中對 Gemini 下達了極為複雜的指令。我們要求 AI **同時**做兩件事，並以 JSON 格式回傳：

1. **撰寫 SQL (SQL Generation):**  
   * AI 會根據問題邏輯（如「計算成長率」），自動使用 Window Function (`LAG()`) 計算年度差異。  
   * 處理日期格式 (`TO_CHAR`)   
   * 設定欄位變數名 (例`total_approved_amount`為核定經費總額)，避免AI自己在新創一個新的變數名。  
2. **定義圖表 (Chart Specification):**  
   * AI 會判斷輸入問題需不需要產生圖表（`chart_enable`）。  
   * 它會指定 x 軸用什麼資料(`x_field`) 與 y 軸用什麼資料 (`y_field`)。  
   * 它會判定 x 軸是要用什麼單位(`x_field_unit`)、 y 軸是要用什麼單位(`y_field_unit`)以及圖表標題(`title`)

**分流處理 (Parsing):**  
由於 AI 回傳的是一包 JSON，我們使用兩個 Code Node(`Normalize ChartSpec` 和 `Validate & Extract SQL`) 進行並行拆解：

*  **(SQL Parser):** 提取 SQL 字串，並進行安全性檢查（禁止 `DELETE`/`DROP`，強制加上 LIMIT）。  
*  **(Chart Parser):** 提取 Chart 設定，並正規化陣列格式，確保前端能直接渲染。

### 第三階段：安全執行與資料獲取 (Secure Execution)

**節點關鍵：**

n8n 接收到清洗過的 SQL 後，透過 PostgreSQL(`Execute LLM SQL`) 節點執行查詢。

* **安全性機制：** 這裡使用的是我們預先設定好的 Read-Only Credential，且在前一步驟的 Code Node 中已過濾掉危險關鍵字，確保資料庫安全無虞。  
* **結果：** 資料庫回傳原始的 `Rows`（例如 20 筆 JSON 物件）。

Rows**大概長這樣：**

```json
[
	{   
		"approve_year": "111",
		"project_count": "93",
		"total_approved_amount": "83532376",
		"project_growth_rate": null,
  		"amount_growth_rate": null 
	},
	{
		"approve_year": "114",
		"project_count": "63",
		"total_approved_amount": "71681983",
		"project_growth_rate": "-0.32258064516129032258",
		"amount_growth_rate": "-0.14186586767267340749"
	}
]
```

### 第四階段：AI 資料分析師 (Semantic Interpretation)

**節點關鍵：**

拿到 Rows 後，直接丟給使用者看通常太過生硬。我們引入了**第二個 AI 模型**來扮演「分析師」。  
我們將「**使用者原始問題**」、「**執行的 SQL**」與「**查詢結果 Rows**」先用Code(`Prepare LLM Explanation Input`)這個節點整理成一起的資料，再餵給這個AI節點(`LLM Generate Explanation`)。

* **Prompt 策略：**  
  * 若無資料，回覆「查無資料，請確認條件...」。  
  * 若有資料，請 AI 用**繁體中文**摘要重點。  
  * 要求 AI 將前幾筆資料整理成 Markdown 表格。

### **第五階段：建構 API 回應 (Response Construction)**

**節點關鍵：**

最後，我們需要將散落在不同支線的資訊重新組裝。

1. **Merge 節點** (`Merge QueryResult & Explanation & ChartSpec`)：將「AI 分析文字 (`answer`)」、「圖表規格 (`chart`)」與「原始數據 (`rows`)」合併為單一物件。  
2. **標準化回應：** 透過 Code(`Send Response`) 節點，將資料格式化為前端預期的 JSON 結構：  
	
```json
[
  {
    "approve_year": "111",
    "project_count": "93",
    "total_approved_amount": "83532376",
    "project_growth_rate": null,
    "amount_growth_rate": null
  },
  {
    "approve_year": "114",
    "project_count": "63",
    "total_approved_amount": "71681983",
    "project_growth_rate": "-0.32258064516129032258",
    "amount_growth_rate": "-0.14186586767267340749"
  },
  {
    "content": {
      "parts": [
        {
          "text": "根據您的查詢，以下是 111 年度與 114 年度所核定之計畫件數及金額的比較分析。\n\n相較於 111 年度，114 年度所核定的計畫件數和總金額均呈現下降趨勢。其中計畫件數減少了 32.26%，而核定總金額也減少了 14.19%。\n\n| 年度 | 計畫件數 | 核定總金額 | 計畫件數成長率 | 金額成長率 |\n| :--- | :--- | :--- | :--- | :--- |\n| 111 | 93 件 | 83,532,376 元 | 0.00% | 0.00% |\n| 114 | 63 件 | 71,681,983 元 | -32.26% | -14.19% |"
        }
      ],
      "role": "model"
    },
    "finishReason": "STOP",
    "index": 0
  },
  {
    "charts": {
      "chart_enable": false,
      "chart_type": "bar"
    }
  }
]
```

3. **回傳：** 透過 Respond to Webhook 結束 HTTP 請求，Flask 收到後即可在網頁上同時顯示文字回答與互動式圖表。

---

#### 技術總結 (Technical Takeaway)

這個工作流展示了 LLM 在企業應用中的成熟型態：**它不只是一個對話框，而是一個「邏輯路由器」與「格式轉換器」。**  
透過 n8n 的節點拆分，我們成功讓 AI 遵守嚴格的輸出格式（JSON），並讓它具備了「看懂資料庫」與「指導前端繪圖」的能力，這正是**智慧校園查詢系統**區別於一般 GPT 的核心競爭力。

<h2 id="integrations">n8n 與外部系統的整合方法</h2>

在前幾章中，我們分別完成了 n8n 的邏輯設計與資料庫的規劃。現在，是時候將這些碎片組裝成一個完整的應用程式了。

本章將帶您透過 Flask 搭建前端介面，並實現從使用者點擊網頁到 AI 回傳圖表的完整資料迴圈。

---

### PostgreSQL 資料庫整合策略 (Database Integration Strategy)

在微服務架構中，資料庫的初始化與Schema管理至關重要。我們不希望每次部署都要手動執行 SQL 指令。

#### A. 自動化初始化

Docker 的官方 PostgreSQL 映像檔有一個強大的特性：**它會自動執行**。

我們將建立一個名為 `init.sql` 的檔案，並放入專案的 `initdb/` 資料夾中。當您執行 `docker-compose up` 時，這個腳本會自動建立資料表、索引與函數。

#### B. 關鍵 SQL 邏輯解析

我們在資料庫層解決了兩個最頭痛的問題：「民國年轉換」與「學院歸屬分類」。

#### 1. 民國日期轉換函數 (ROC Date Parser)

原始 Excel 資料常出現 `113.07.01` 這種民國格式，PostgreSQL 原生不支援。我們定義一個自訂函數來解決此問題:

```sql
--民國日期字串 → 西元 date
create or replace function parse_roc_date(p text)
returns date language sql immutable as $$
  select case
    when p ~ '^\d{2,3}[./]\d{1,2}[./]\d{1,2}$'
      then make_date(1911 + split_part(p, '[./]', 1)::int,
                     split_part(regexp_replace(p,'\.','/','g'), '/', 2)::int,
                     split_part(regexp_replace(p,'\.','/','g'), '/', 3)::int)
    else null
  end
$$;
```

透過將此邏輯下放到資料庫層 (Database Level)，n8n 的 SQL 寫入語句會變得非常簡潔，只需呼叫 `parse\_roc\_date('{{$json.date}}')` 即可。

#### 2. 主資料表設計 (Main Table Schema)

projects 表是用來儲存產學計畫的核心，並且對常常需要的資料建立索引，已增加查詢速度。

```sql
-- 主表：projects
create table if not exists projects (
  id                bigserial primary key,
  project_code      text unique,          -- 計畫代碼
  project_name      text,                 -- 計畫名稱
  exec_unit         text,                 -- 執行單位
  fund_source       text,                 -- 經費來源(原文)
  unit_category     text,                 -- 單位(政府/企業/其他) ← 由AI/觸發器產出
  pi_code           text,                 -- 計畫主持人(代號)
  start_date        date,                 -- 起始日期
  end_date          date,                 -- 應結日期
  extend_date_raw   date,                 -- 延長日期(原樣保存，因常為「…」)
  close_date        date,                 -- 簽結日期(=實結日期)
  approve_amount    numeric,              -- 計畫核定數
  received_amount   numeric,              -- 實收數
  spent_amount      numeric,              -- 實支數
  refund_amount_raw text,                 -- 餘額繳回(常見為"-"，先原樣存)
  manage_fee        numeric,              -- 管理費
  created_at        timestamptz default now()
);

create index if not exists idx_projects_code on projects(project_code);
create index if not exists idx_projects_unit_category on projects(unit_category);
create index if not exists idx_projects_year on projects(extract(year from start_date));
```

#### 3. 學院自動對照表 (College Mapping Strategy)

為了統計「各學院」的計畫數量，我們需要根據固定的關鍵字將分散的「系所」分類到「學院」。我們建立一張 `college_map` 對照表，並預先寫入關鍵字。

```sql
create table if not exists college_map (
  id            bigserial primary key,
  unit_keyword  text        not null,          -- 執行單位中會出現的關鍵字，例如「電機」「資工」
  college_name  text        not null,          -- 學院名稱，例如「電機資訊學院」
  priority      int         not null default 100, -- 關鍵字優先順序，數字越小優先度越高
  created_at    timestamptz not null default now()
);

insert into college_map (unit_keyword, college_name, priority) values
-- 法律學院
('法律學院','法律學院',1),
('法律學系','法律學院',1),
('比較法資料中心','法律學院',1),
```

**整合機制：**  
在 n8n 的工作流中（見 `Update College Mapping` 節點），我們會執行以下 SQL 來自動更新歸屬：

```sql
UPDATE projects p
SET college_category = c.college_name
FROM college_map c
WHERE p.exec_unit LIKE '%' || c.unit_keyword || '%';
```

### Flask 後端與 n8n 的資料交換 (Data Exchange)

Flask 在此架構中扮演了 **前端專用後端(Backend for Frontend)** 的角色。它負責轉發使用者的自然語言查詢，並解析 n8n 回傳的複雜 JSON。

#### A. 發送請求 (The Request)

在 school.py 中，我們定義了 `/POST` 路由。當使用者送出查詢時：

```python
payload = {"query": query_text}
r = requests.post(N8N_WEBHOOK, json=payload, timeout=90)
```

這裡 Flask 將使用者的文字包裝成 `{ "query": "..." }` 的 JSON 格式發送。

#### B. 解析回應 (The Response)

n8n 經過一連串 AI 與 SQL 處理後，會回傳一個結構化的 JSON（參見 n8n 節點 `Build response for Flask`）。Flask 接收後進行解構：

```python
raw = r.json()
print("=== n8n raw ===")
print(raw)

rows, answer, chart_spec = [], "", {}
if isinstance(raw, dict):
    rows = raw.get("rows", []) or []
    answer = raw.get("answer", "") or ""
    chart_spec = raw.get("chart", {}) or {}
else:
     rows = raw or []
     answer = ""
     chart_spec = {}
```

rows對應於n8n回傳的rows，answer對應於answer，chart\_spec對應於chart。

#### C. 伺服器端資料格式化（Server-side data formatting）

在 `school.py` 中，我們還做了一層貼心的處理：**數值格式化**。  
透過 `_fmt_money` 與 `_fmt_pct` 函式，我們確保傳給前端的金額會自動加上千分位，百分比會加上 % 符號，提升閱讀體驗。

	1234567 → 1,234,567

	0.153 → 15.3%

---

### 前端視覺化實作 (Frontend Visualization)

前端介面分為「查詢頁」與「結果頁」，採用原生 JavaScript 搭配強大的 **Chart.js** 函式庫。

#### A. 查詢頁 (`school_upload.html`)

我們整合了瀏覽器原生的 **Web Speech API**，實現「語音轉文字」功能。

**設計巧思：** 允許使用者自訂圖表顏色 (`color1` ~ `color4`)，這些色碼會隨表單傳送給後端，最終渲染在結果頁的圖表上。

<img width="1226" height="875" alt="image" src="https://github.com/user-attachments/assets/9049d471-2e72-49a3-b019-70803651c584" />

#### B. 結果頁 (`school_result.html`)

n8n 完成複雜的過程後，後端會將回傳的 JSON 數據渲染到這個結果頁面。這個頁面不只是一個靜態報表，而是一個**動態生成的數據儀表板**。

它的核心設計包含三個區塊：

**1. 動態數據表格 (Dynamic Data Table)**

由於每次查詢的 SQL 結果欄位都不同（有時查學院統計，有時查教師清單），表格採用 **Jinja2 動態迴圈**生成。

* **自適應欄位：** 無論資料庫回傳什麼欄位，網頁都能自動產生對應的表頭 (`<th>`) 與內容 (`<td>`)。  
* **CSV 匯出：** 內建一鍵下載功能，方便行政人員將查詢結果匯出至 Excel 做後續處理。

**範例:** 輸入問題為請做出本校111\~114年度不同單位類別承接計畫件數、人數、金額之統計圖

<img width="1567" height="1098" alt="image" src="https://github.com/user-attachments/assets/a5c22057-d8ce-442e-905c-7d7f7b2be4cb" />

**2. 智慧圖表區 (Smart Visualization)**

這是頁面中最吸睛的部分。我們透過內嵌的 JavaScript 與 **Chart.js** 函式庫，實現了自動化的圖表繪製邏輯：

* **自動判斷類型：** 程式會自動偵測欄位名稱。若是「金額」相關數據（如 `total_approved_amount`），會自動繪製成**黃色折線圖**並對應到右側 Y 軸；若是「件數/人數」相關，則繪製成**長條圖**並對應左側 Y 軸。  
* **雙軸呈現 (Dual Axis)：** 解決了「金額（千萬）」與「件數（個位數）」數值差距過大，無法在同一張圖表清楚顯示的問題。  
* **客製化配色：** 圖表顏色會直接讀取使用者在首頁選擇的配色方案。

<img width="1529" height="747" alt="image" src="https://github.com/user-attachments/assets/2284b463-c7bd-43c7-83cb-e289ed90377f" />

**3. AI 回應 (AI Response)**

位於頁面最下方，直接顯示由 Gemini 模型生成的自然語言分析。這讓使用者不需要自己看圖說故事，直接閱讀 AI 提供的「重點摘要」或「趨勢解讀」。

<img width="1540" height="784" alt="image" src="https://github.com/user-attachments/assets/e59fa93e-064d-40f6-94c5-673747fd0e0b" />

<h2 id="result">校務自動化應用案例</h2>

在前幾章中，我們完成了從底層資料庫到前端介面的全棧開發。現在，這套「智慧校園數據查詢系統」已經準備就緒。

本章將透過 **六個真實的校務行政場景**，展示系統如何應對複雜的查詢需求。這不僅是測試系統的極限，更是為了驗證 AI 如何透過自然語言理解業務邏輯（Business Logic），取代繁瑣的 Excel 樞紐分析操作。

---

### 多維度交叉分析

**使用者提問：**  
「本校111~114年度不同單位類別承接計畫件數、人數、金額之統計圖」

**AI運作解析：**

生成的SQL指令：

```sql
SELECT
  (EXTRACT(YEAR FROM start_date) - 1911) AS approve_year,
  unit_category,
  COUNT(*) AS project_count,
  COUNT(DISTINCT pi_code) AS pi_count,
  SUM(approve_amount) AS total_approved_amount
FROM
  projects
WHERE
  (EXTRACT(YEAR FROM start_date) - 1911) BETWEEN 111 AND 114
GROUP BY
  approve_year,
  unit_category
ORDER BY
  approve_year,
  CASE unit_category
    WHEN '政府' THEN 1
    WHEN '企業' THEN 2
    WHEN '其他' THEN 3
    ELSE 4
  END
LIMIT 100;
```

1. **生成的SQL分析：** 這段 SQL 會從 projects 資料表中擷取 111 到 114 年度（以起始日期換算民國年）的計畫資料，並依「年度 × 單位類別（政府、企業、其他）」分組，統計各組的計畫件數、不同主持人數以及核定經費總額；最後依年度排序，同年度內則按照政府、企業、其他的固定順序排列，並限制最多回傳 100 筆結果。
2. **取出的欄位：** 取出了：`approve_year` (核定年度)、`unit_category` (單位類別)、`project_count` (計畫件數)、`pi_count` (承接計畫教師人數)和'total_approved_amount' (核定經費總額)。  
3. **圖表資訊：** x軸取了`approve_year`(核定年度)、`unit_category`(單位類別)，y軸取了`project_count`(計畫件數)、`pi_count`(承接計畫教師人數)、`total_approved_amount`(核定經費總額)。

**結果：符合需求**

<img width="1018" height="1260" alt="image" src="https://github.com/user-attachments/assets/a38a124e-d899-4947-bd6a-4ee6f209e649" />

---

### 趨勢成長率計算

**使用者提問：**  
「商學院 114 年度相較於 111 年度所核定之計畫件數及金額成長率」

**系統運作解析：**

生成的SQL指令：

```sql
WITH YearlyData AS (
    SELECT
        (EXTRACT(YEAR FROM start_date) - 1911) AS approve_year,
        COUNT(*) AS project_count,
        SUM(approve_amount) AS total_approved_amount
    FROM
        projects
    WHERE
        college_category = '商學院'
        AND (EXTRACT(YEAR FROM start_date) - 1911) IN (111, 114)
    GROUP BY
        (EXTRACT(YEAR FROM start_date) - 1911)
)
SELECT
    approve_year,
    project_count,
    total_approved_amount,
    (project_count - LAG(project_count) OVER (ORDER BY approve_year))::numeric
        / NULLIF(LAG(project_count) OVER (ORDER BY approve_year), 0) AS project_growth_rate,
    (total_approved_amount - LAG(total_approved_amount) OVER (ORDER BY approve_year))::numeric
        / NULLIF(LAG(total_approved_amount) OVER (ORDER BY approve_year), 0) AS amount_growth_rate
FROM
    YearlyData
ORDER BY
    approve_year
LIMIT 100;
```

1. **生成的SQL分析：** 這段 SQL 先在 YearlyData 裡統計商學院於民國 111 與 114 年的年度計畫件數與核定經費總額，再在外層查詢中利用 LAG 視窗函數，把每一年的件數與金額拿去和前一年相比，計算出計畫件數成長率與核定金額成長率，最後依年度排序並限制最多回傳 100 筆結果。
2. **取出的欄位：** 取出了：`approve_year` (核定年度)、`project_count` (計畫件數)、`total_approved_amount` (核定經費總額)、`project_growth_rate` (件數成長率)和'amount_growth_rate' (金額成長率)。  
3. **圖表資訊：** x軸取了`approve_year`(核定年度)，y軸取了`project_count`(計畫件數)、`total_approved_amount`(核定經費總額)。

**結果：符合需求**

<img width="1009" height="861" alt="image" src="https://github.com/user-attachments/assets/cbbee840-2487-4785-a0b5-0276b63cac6b" />

---

### 關鍵字語意搜尋

**使用者提問：** 
「本校 112–113 年度計畫主題中有海洋議題（例如「永續」、「綠能」、「藍色」、「能源」等）等關鍵字之研究計畫」

生成的SQL指令：

```sql
SELECT
  project_code,
  project_name,
  exec_unit,
  fund_source,
  approve_amount,
  TO_CHAR(start_date, 'YYYY-MM-DD') AS start_date,
  TO_CHAR(end_date, 'YYYY-MM-DD') AS end_date,
  (EXTRACT(YEAR FROM start_date) - 1911) AS approve_year
FROM
  projects
WHERE
  (EXTRACT(YEAR FROM start_date) - 1911) BETWEEN 112 AND 113
  AND (
    project_name ILIKE '%海洋%' OR
    project_name ILIKE '%永續%' OR
    project_name ILIKE '%綠能%' OR
    project_name ILIKE '%藍色%' OR
    project_name ILIKE '%能源%'
  )
ORDER BY
  approve_year,
  project_code
LIMIT 100;
```

1. **生成的SQL分析：** 這段 SQL 會篩選出民國 112 至 113 年間、名稱含有「海洋、永續、綠能、藍色、能源」等關鍵字的計畫，並回傳其代碼、名稱、執行單位、經費來源、核定金額與起訖日期等資訊，最後依年度與計畫代碼排序並限制最多 100 筆。
2. **取出的欄位：** 取出了：`project_code` (計畫代碼)、`project_name` (計畫名稱)、`exec_unit` (執行單位)、`fund_source` (經費來源)、'approve_amount' (計畫核定金額)、`start_date` (起始日期)、`end_date` (應結日期)、`approve_year` (核定年度)。  
3. **圖表資訊：** `chart_enable:false`，AI判斷沒有產圖表的需求，。

**結果：符合需求**

<img width="1018" height="1126" alt="image" src="https://github.com/user-attachments/assets/d1a5d4ec-68f8-4682-b896-78a5add2619a" />

---

### 重點教師篩選 (Top PI)

**使用者提問：**  
「本校 111–114 年度核定單件計畫金額大於 200 萬元以上之教師，並列出計畫明細」

生成的SQL指令：

```sql
SELECT
    (EXTRACT(YEAR FROM start_date) - 1911) AS approve_year,
    project_code,
    project_name,
    exec_unit,
    fund_source,
    pi_code,
    TO_CHAR(start_date, 'YYYY-MM-DD') AS start_date,
    TO_CHAR(end_date, 'YYYY-MM-DD') AS end_date,
    approve_amount
FROM
    projects
WHERE
    EXTRACT(YEAR FROM start_date) BETWEEN 2022 AND 2025
    AND approve_amount > 2000000
ORDER BY
    approve_year,
    approve_amount DESC
LIMIT 100;
```

1. **生成的SQL分析：** 這段 SQL 會搜尋西元 2022～2025 年間起始、且核定金額超過 200 萬元的所有計畫，回傳其基本資訊並依民國年度排序，其中同年度的計畫再按照金額由大到小排列，最後限制最多 100 筆結果。
2. **取出的欄位：** 取出了：`approve_year` (核定年度)、`project_code` (計畫代碼)、`project_name` (計畫名稱)、`exec_unit` (執行單位)、`fund_source` (經費來源)、'pi_code' (主持人代碼)、`start_date` (起始日期)、`end_date` (應結日期)、`approve_amount` (計畫核定金額)。  
3. **圖表資訊：** `chart_enable:false`，AI判斷沒有產圖表的需求，。

**結果：符合需求**

<img width="1024" height="1437" alt="image" src="https://github.com/user-attachments/assets/d76e27b7-3d7f-402a-8364-e10b95e2c01e" />

---

### 核定與執行中計畫比較

**使用者提問：**  
「計算並比較本校 111–114 年度各年度校內經費補助之計畫件數、金額及執行中之計畫件數、金額」

生成的SQL指令：

```sql
WITH target_years AS (
    SELECT generate_series(2022, 2025) AS gregorian_year
)
SELECT
    (ty.gregorian_year - 1911) AS approve_year,
    COUNT(
        CASE WHEN EXTRACT(YEAR FROM p.start_date) = ty.gregorian_year
             THEN p.id END
    ) AS project_count,
    SUM(
        CASE WHEN EXTRACT(YEAR FROM p.start_date) = ty.gregorian_year
             THEN p.approve_amount END
    ) AS total_approved_amount,
    COUNT(
        CASE WHEN EXTRACT(YEAR FROM p.end_date) = ty.gregorian_year
             THEN p.id END
    ) AS executing_project_count,
    SUM(
        CASE WHEN EXTRACT(YEAR FROM p.end_date) = ty.gregorian_year
             THEN p.approve_amount END
    ) AS executing_total_approved_amount
FROM
    target_years ty
LEFT JOIN
    projects p
    ON EXTRACT(YEAR FROM p.start_date) = ty.gregorian_year
    OR EXTRACT(YEAR FROM p.end_date) = ty.gregorian_year
GROUP BY
    ty.gregorian_year
ORDER BY
    ty.gregorian_year
LIMIT 100;
```

1. **生成的SQL分析：** 這段 SQL 先用 generate_series 產生 2022～2025 西元年度，再透過 LEFT JOIN 把這些年度對應到 projects 表，統計每一年中「當年起始的計畫件數與核定總額」以及「當年應結束的計畫件數與核定總額」，最後換算成民國年後依年度排序並回傳最多 100 筆結果。
2. **取出的欄位：** 取出了：`approve_year` (核定年度)、`project_count` (計畫件數)、`total_approved_amount` (核定經費總額)、`executing_project_count` (執行中計畫件數)、`executing_total_approved_amount` (執行中計畫經費總額)。  
3. **圖表資訊：** x軸取了`approve_year`(核定年度)，y軸取了`project_count`(計畫件數)、`total_approved_amount` (核定經費總額)、`executing_project_count` (執行中計畫件數)、`executing_total_approved_amount` (執行中計畫經費總額)。

**結果：符合需求**

<img width="1012" height="1028" alt="image" src="https://github.com/user-attachments/assets/63f38099-6097-40e9-88e0-066a163382d0" />

---

### 績效與人均產值分析 (KPI Analysis)

生成的SQL指令：

```sql
WITH CollegeProjectSummary AS (
    SELECT
        college_category,
        COUNT(*) AS college_project_count,
        COUNT(DISTINCT pi_code) AS college_pi_count
    FROM
        projects
    WHERE
        EXTRACT(YEAR FROM start_date) = 2025  -- 民國114年度
    GROUP BY
        college_category
)
SELECT
    cps.college_category,
    CASE cps.college_category
        WHEN '法律學院' THEN (cps.college_project_count::numeric / 34)
        WHEN '商學院' THEN (cps.college_project_count::numeric / 107)
        WHEN '公共事務學院' THEN (cps.college_project_count::numeric / 69)
        WHEN '社會科學學院' THEN (cps.college_project_count::numeric / 63)
        WHEN '人文學院' THEN (cps.college_project_count::numeric / 51)
        WHEN '電機資訊學院' THEN (cps.college_project_count::numeric / 35)
        WHEN '永續創新國際學院' THEN (cps.college_project_count::numeric / 11)
        ELSE NULL
    END AS project_per_teacher,
    CASE cps.college_category
        WHEN '法律學院' THEN (cps.college_pi_count::numeric / 34)
        WHEN '商學院' THEN (cps.college_pi_count::numeric / 107)
        WHEN '公共事務學院' THEN (cps.college_pi_count::numeric / 69)
        WHEN '社會科學學院' THEN (cps.college_pi_count::numeric / 63)
        WHEN '人文學院' THEN (cps.college_pi_count::numeric / 51)
        WHEN '電機資訊學院' THEN (cps.college_pi_count::numeric / 35)
        WHEN '永續創新國際學院' THEN (cps.college_pi_count::numeric / 11)
        ELSE NULL
    END AS project_teacher_ratio
FROM
    CollegeProjectSummary cps
WHERE
    cps.college_category IS NOT NULL
ORDER BY
    cps.college_category
LIMIT 100;
```

1. **生成的SQL分析：** 這段 SQL 先計算 2025 年（民國 114 年）各學院的計畫件數與不重複主持人數，接著依照每個學院對應的教師總數，算出「每位教師平均承接計畫件數」與「主持教師占該學院教師的比率」，最後依學院名稱排序後回傳最多 100 筆。
2. **取出的欄位：** 取出了：`college_category` (學院)、`project_per_teacher` (人均計畫數)、`project_teacher_ratio` (執行計畫之教師比例)。  
3. **圖表資訊：** x軸取了`college_category` (學院)、，`project_per_teacher` (人均計畫數)、`project_teacher_ratio` (執行計畫之教師比例)。

**結果：符合需求**

<img width="1009" height="1069" alt="image" src="https://github.com/user-attachments/assets/e97b0f26-a0fb-4248-a94b-86f2418e2c03" />

---

#### 第七章總結

透過這六個案例，我們見證了系統如何將模糊的行政需求，轉化為精確的數據、圖表資訊。

* **效率提升：** 原本需要半天整理 Excel 的工作，現在縮短為 5 秒鐘的查詢。  
* **門檻降低：** 任何不懂 SQL 的行政人員，都能透過自然語言挖掘數據價值。  
* **決策品質：** 從單純的「看數字」進化到「看趨勢」。

這正是自動化技術在校園事務中的核心價值。

<h2 id="container">部署與映像檔打包(Deployment & Image Packaging)</h2>

在完成了程式碼開發與工作流設計後，我們面臨最後一個挑戰：如何讓這套系統在任何一台電腦上穩定運作？
傳統的部署方式需要手動安裝 Python、PostgreSQL、Node.js，還得處理各種版本衝突與環境變數設定。在本章中，我們將採用現代化的 Docker 容器技術，將整個校務自動化系統打包成標準化的映像檔，實現「一次構建，到處執行 」的目標。

---

### 為什麼要打包成 Image？ (Concept & Benefits)

在進入實作之前，我們需要理解 Docker 的三個核心概念，這也是為什麼我們選擇它的原因：

#### 核心概念三元素

* **Image (映像檔):** 這就像是軟體的「安裝光碟」或「食譜」。它包含了執行應用程式所需的一切（程式碼、函式庫、環境設定）。Image 是唯讀的，確保了環境的一致性。
* **Container (容器):** 這就像是透過食譜做出來的「真實料理」或「執行中的程式」。它是 Image 的實體化，是一個輕量級、隔離的執行環境。
* **Volume (資料卷):** 這就像是「外接硬碟」。容器本身是暫時的，刪除後資料會消失。為了保存 n8n 的工作流設定或 PostgreSQL 的學生資料，我們將 Volume 掛載到容器上，實現**資料持久化**。

#### 打包的好處

* **環境一致性：** 開發環境是 Python 3.11，伺服器上也保證是 3.11，不會有 "這只能在我電腦執行" 的問題。
* **快速部署：** 只要一行指令，就能同時啟動資料庫、前端與後端服務。
* **隔離性：** 資料庫服務不會干擾到伺服器上其他的應用程式。

### Dockerfile 撰寫指南 (Writing the Dockerfile)

我們的 Flask 後端 (`school-backend`) 是客製化開發的程式，因此需要編寫一份 `Dockerfile` 來告訴 Docker 如何建置它。
以下是 `Dockerfile` 的內容：

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "school.py"]
```

**1. 選擇基底映像（FROM）：** 使用 Python 官方映像即可，`slim` 版體積小、部署快。

**2. 設定環境變數（ENV）：**
* `PYTHONUNBUFFERED=1`：日誌立即輸出，方便除錯
* `LANG=C.UTF-8`：避免中文亂碼

**3. 設定工作目錄（WORKDIR)：** 把程式統一放在 /app，路徑乾淨好管理。

**4. 安裝依賴（requirements）：** 先 COPY `requirements.txt`，再 pip install→ 讓 Docker 快取發揮作用，build 速度更快。

**5. 複製程式碼（COPY . .）：** 把 Flask 程式與 HTML 模板一起放入容器。

**6. 啟動指令（CMD）：** 執行 `python school.py`，讓容器啟動 Flask 服務。

---

### 服務編排：Docker Compose 部署 (Orchestration)
有了 Dockerfile 之後，我們不只要執行 Flask，還需要同時啟動資料庫與 n8n 等多個服務。由於每個容器本身是獨立的，必須透過 `docker-compose.yml` 來把它們串接起來。Compose 能協調所有服務的啟動順序、網路連線與資料持久化，讓整套系統能像一個完整的應用程式一樣運作。

以下是本系統實際使用的 `docker-compose.yml`，包含四個服務：
PostgreSQL、Adminer、n8n、Flask 校務查詢後端。

```yaml
version: "3.8"

services:
  # 1) PostgreSQL 資料庫
  db:
    image: postgres
    container_name: postgres-db
    restart: always
    shm_size: 128mb
    environment:
      # 預設 user=postgres, 預設 DB=postgres
      - POSTGRES_PASSWORD=school
    volumes:
      - db_data:/var/lib/postgresql
      - ./initdb:/docker-entrypoint-initdb.d   # ★ 這裡放 schema.sql
    ports:
      - "5432:5432"
    networks:
      - school-net

  # 2) Adminer：用來操作 Postgres 的 GUI
  adminer:
    image: adminer
    container_name: adminer
    restart: always
    ports:
      - "8080:8080"
    depends_on:
      - db
    networks:
      - school-net

  # 3) n8n 自動化服務
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    restart: always
    ports:
      - "5679:5679"                 # http://127.0.0.1:5679
    environment:
      - N8N_BASIC_AUTH_ACTIVE=false
      - N8N_HOST=localhost
      - N8N_PORT=5679
      - N8N_PROTOCOL=http
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - db
    networks:
      - school-net

  # 4) Flask 校務查詢後端
  school-backend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: school-backend
    restart: always
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production

      # Flask → n8n：容器間用 service name
      - N8N_BASE=http://n8n:5679

      # Flask → PostgreSQL：使用 service name db
      - DB_HOST=db
      - DB_PORT=5432
      - DB_NAME=postgres
      - DB_USER=postgres
      - DB_PASSWORD=school
    depends_on:
      - db
    networks:
      - school-net

networks:
  school-net:
    driver: bridge

volumes:
  n8n_data:
  db_data:
```

#### 1. db（PostgreSQL）

* **映像(image):** 使用官方 postgres image。
* **容器名(container_name):** postgres-db
* **環境(environment):**
  * host=db
  * port=5432
  * name=postgres(預設)
  * user=postgres(預設)
  * password=school(自己設的)
* **資料卷(volumes):**./initdb 內放 schema.sql，容器啟動時會自動資料庫初始化。
* **網路(networks):** 用school-net連接
  
#### 2. adminer（PostgreSQL GUI 管理介面）

* **映像(image):** 使用官方 adminer image。
* **容器名(container_name):** adminer
* **連接埠（ports）：** 8080:8080（瀏覽器開啟 http://localhost:8080）
* **啟動順序（depends_on）：** db（確保資料庫先啟動）
* **網路（networks）：** 使用 school-net 連接至資料庫

#### 3. n8n（自動化流程引擎）

* **映像(image):** n8nio/n8n:latest
* **容器名(container_name):** n8n
* **環境(environment):**
	* N8N_BASIC_AUTH_ACTIVE=false
	* N8N_HOST=localhost
	* N8N_PORT=5679
	* N8N_PROTOCOL=http
* **連接埠（ports）：** 5679:5679（n8n Web UI 與 Webhook 使用）
* **資料卷(volumes):** n8n_data:/home/node/.n8n（儲存 workflow 與設定）
* **啟動順序（depends_on）：** db（因為 n8n 的 Credentials 通常需要資料庫）
* **網路（networks）：** 使用 school-net 讓 Flask 以 http://n8n:5679 方式訪問 n8n

#### 4. school-backend（Flask 校務查詢後端）

* **映像(image):** 透過 Dockerfile build（context = 專案根目錄）
* **容器名(container_name):** school-backend
* **環境(environment):**
	* FLASK_ENV=production
	* **給 Flask 呼叫 n8n：** N8N_BASE=http://n8n:5679
* **連接埠（ports）：** 5000:5000（Flask Web 前端）
* **資料卷(volumes):** n8n_data:/home/node/.n8n（儲存 workflow 與設定）
* **啟動順序（depends_on）：** db和n8n要先啟動
* **網路（networks）：** 使用 school-net

---

### 啟動與驗證 (Startup & Verification)

一切準備就緒，現在讓我們啟動系統。

#### 1. 啟動指令

在包含 `docker-compose.yml` 的目錄下開啟終端機，執行：

	docker-compose up -d --build

-d: 背景執行 (Detached mode)
--build: 強制重新構建 Flask 的映像檔 (確保程式碼是最新的)

#### 2. 檢查狀態

到docker看容器狀態
你應該可以看到四個服務 (postgres-db, adminer, n8n, school-backend) 的狀態皆為綠燈。

<img width="2058" height="308" alt="image" src="https://github.com/user-attachments/assets/bb7a16fc-6c34-4ce0-a817-d0dd9b7802e9" />

#### 3. 訪問系統

* **前端入口：** 打開瀏覽器訪問 `http://localhost:5000`，你應該能看到「計畫查詢入口」頁面。
* **n8n 後台：** 訪問 `http://localhost:5679`，進行工作流的匯入與設定。
* **資料庫管理：** 訪問 `http://localhost:8080` (System 選 PostgreSQL, Server 填 db, User 填 postgres, Password 填 school)，檢查資料表是否已自動建立。
  
<h2 id="conculation">結語：n8n 在校務與教學創新的價值</h2>
     
綜合本文的系統設計與實作成果，可以看出 n8n 不僅是一套流程自動化工具，更是一個能夠串接 AI、資料庫與應用系統的關鍵中樞。透過 Webhook、資料庫節點與 LLM 節點的協同運作，本文章成功將原本高度仰賴人工撰寫 SQL、整理報表的校務資料查詢流程，轉化為「以自然語言驅動」的智慧查詢體驗。使用者只需提出問題，系統即可自動完成查詢、分析、視覺化與文字解讀，展現 n8n 在校務與教學創新場域中的高度實用性與擴充潛力 

### 低程式碼與 AI 的未來趨勢

隨著低程式碼（Low-code）與 AI 技術的成熟，資訊系統的開發門檻正快速降低。n8n 提供的視覺化流程設計，讓非資工背景的行政人員或教師，也能理解並參與系統邏輯的建構；而 AI(LLM) 的導入，則進一步消弭了「資料庫語言」與「使用者語言」之間的鴻溝。這種 低**程式碼 × AI** 的結合模式，預示未來校園資訊系統將不再只是工程人員的專利，而是能由跨角色共同維護、持續演進的智慧平台。

### 提升行政效率與資料可及性

從實務角度來看，本系統有效提升了行政效率與資料可及性。行政單位能即時取得跨年度、跨學院的統計資訊，減少重複整理報表的時間成本；教師與研究人員則可快速掌握自身或所屬單位的計畫概況，作為研究規劃與決策的依據。再加上 Docker 容器化部署所帶來的可移植性與一致性，系統不僅易於展示與推廣，也具備在不同校務場景中複製應用的可能。

總結而言，n8n 在本研究中的角色，已從單純的自動化工具，升級為 校務資料智慧化的重要基石。透過低程式碼、AI 與標準化部署的結合，本系統為校務與教學創新提供了一個具體且可行的實踐範例，也為未來更廣泛的智慧校園應用奠定了良好基礎。
  
<h2 id="appendix">附錄</h2>

* **Github連結：** https://github.com/panda940530/school
* **如何在自己電腦，執行我的代碼：** youtube影片(還沒錄)


