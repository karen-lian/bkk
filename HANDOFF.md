# 曼谷手冊專案 · 交接文件

> 這份文件是給 Claude Code（或任何接手的人）用的。
> 目的：不必重讀原始對話，就能理解這個網站的設計約束、內容決策與待辦事項。
> 最後更新：2026-08-10

---

## 1. 這是什麼

一組給 2026/8/19–8/24 曼谷行使用的單檔 HTML 網站，部署在 GitHub Pages（`karen-lian.github.io/bkk/`）。

| 檔案 | 用途 | 讀者 |
|---|---|---|
| `index.html` | 主手冊：行程、住宿、費用、泰語、待辦 | 鈞（Jun）與平（Ping） |
| `曼谷行程表_0819-0824.md` | 純文字版行程，內容與 index.html 同步 | 自用速查 |

**重要：`index.html` 與 markdown 兩份文件必須同步維護。** 任何行程異動兩邊都要改。

> **2026-08-16 移除**：原本還有 `saturday-with-f.html`（給 F 的 8/22 提議頁，闖關式選擇）
> 與 `en.html`（純英文六天行程表）。兩頁都不再使用，已刪除；需要時從 git 歷史取回。
> 灰銀配色、闖關流程、資訊卡等做法留在下方各節，之後要重做可以參考。

`index.html` 的 `<head>` 有 `<meta name="robots" content="noindex, nofollow">`，
**不要另外加 robots.txt Disallow**：爬蟲被擋掉就讀不到 noindex，反而可能讓網址
以無說明的形式留在搜尋結果。而且專案站的 robots.txt 必須在網域根目錄，放在這個
repo 只會是 `/bkk/robots.txt`，爬蟲不會讀。

---

## 2. 人物與關係

- **鈞**（Jun，F 認識她時用 KK）— 本人
- **平**（Ping）— 同行友人
- **F** — 男性，曼谷友人，8/21–24 的住宿就是他的 Airbnb（三人同住）
- **J朋友** — 鈞的朋友，8/20 中午一起吃飯

---

## 3. 設計系統（改動時務必遵守）

### 3.1 核心約束：單一主色 + 單一底色
整份網站只用**一個墨色 + 一個紙色**，所有層次靠線條粗細與網點密度做出來（絹印海報邏輯）。**不要引入第三個顏色。**

三組配色 × 明暗 = 6 種組合，用 `html[data-theme][data-mode]` 屬性切換：

```css
taxi  light: --ink:#B0175B  --paper:#F2ECE3   /* 計程車桃紅，預設 */
taxi  dark : --ink:#FF5C9B  --paper:#150A0F
gold  light: --ink:#8A560D  --paper:#F6F0DF   /* 廟宇金 */
gold  dark : --ink:#E9AE3E  --paper:#12100A
river light: --ink:#1C3B70  --paper:#E8EDF1   /* 湄南河靛藍 */
river dark : --ink:#7DB2EA  --paper:#070C16
```

透明度階層透過 `--ink-rgb` 產生：`--ink-85 / -60 / -38 / -18 / -08`。
**新增元素請使用這些變數，不要寫死顏色值**，否則切換主題時會脫色。

### 3.2 字體
- `Bai Jamjuree` — 拉丁字與數字（泰國 Cadson Demak 出品，呼應主題）
- `Noto Sans TC` — 中文
- `Noto Sans Thai` — 泰文（class `.th`）

只有這三種，不要再加。

### 3.3 插畫
hero 是**手寫 SVG 線稿**，非圖片：
- `index.html`：曼谷街景（頭頂電纜、鄭王廟塔、店屋、Mahanakhon 像素塔、嘟嘟車、路邊攤）

線條用 `.st`（1px）／`.thin`（0.6px）／`.bold`（1.6px`），窗格與招牌用 SVG `<pattern>` 產生密度。`stroke` 一律用 `var(--ink)`，`fill` 只用 `var(--paper)` 做挖空。

### 3.4 行程路線圖的圓點編碼（結構即資訊）
行程是一條連續直線，每個時間點的圓點編碼「誰參加」：

| class | 外觀 | 意義 |
|---|---|---|
| `.stop.together` | 實心 | 兩人同行 |
| `.stop`（無修飾） | 空心 | 各自行動 |
| `.stop.pending` | 半實心 | 待定／待確認 |
| `.day-head::before` | **雙層同心圓** | 日期節點（刻意與「各自行動」的單層空心圈區隔） |

### 3.5 間距系統
三層標題各自「上方留白 = 下方留白」：
```css
--gap-major: clamp(40px,6vw,64px)   /* 區塊大標題 */
--gap-mid:   clamp(28px,4vw,44px)   /* 每日日期標題 */
--gap-sub:   clamp(22px,3vw,34px)   /* 泰語分類標題 */
```

⚠️ **踩過的坑**：`.wrap` 必須用 `padding-left/right`，**不可用 `padding:0 var(--gut)` 簡寫**——簡寫會把上下 padding 設為 0，且 class 選擇器優先權高於 `section{padding-top}`，導致標題上方留白完全失效。

### 3.6 動效與版面變異（2026-08-11 起）

手冊在原本克制的單色系統上，額外疊了一層「編舞感動效」與「選擇性版面變異」，**不是取代第 3.1 節的單色/單紙約束，只是在同一套系統裡拉高表現力**：

- **進場動效**：`.rv` 區塊從單純淡入改成 `translateY + scale` 的 settle 動畫（`cubic-bezier(.16,1,.3,1)`），內部的卡片/列表項目（`.place`、`.money li`、`.ph`、`.todo li`、`.stops li`、已刪除的 F 提議頁的 `.row`）用 `nth-child` 疊加 `transition-delay` 做出逐項掉落的節奏，第 5 項起延遲封頂，長清單不會拖太久。
- **`.day`（行程日期卡）維持獨立的 `.rv` + IntersectionObserver**，不要把它併進上面的子項 stagger 規則——它本來就是自己的觀察目標，如果被 `.rv .day` 這種子代選擇器蓋到，會在外層 section 一進畫面就整批提前顯示，等於作廢了逐日揭露的效果（這裡踩過一次坑，寫下來避免重踩）。
- **導覽列**：`.links` 內加了一條 `.nav-indicator`，`spy()` 算出目前 active 按鈕的 `offsetLeft/offsetWidth` 後用 CSS transition 滑過去，取代原本純靠 `.on` 顏色切換。
- **互動微動效**：`.mapbtn`、`.place .map`、導覽按鈕、主題色點、暗底切換鈕，hover/active 都加了小幅 `transform`（不是只變顏色）。
- **版面變異只用在裝飾性、非資訊性的元素**：`.tag`／`.opt-tag` 編號徽章加了旋轉與出血（`transform:rotate()` + 負值定位），`.day-num` 奇偶交替微旋轉，`.duo`／`.opt:nth-of-type(2)` 卡片做垂直或水平位移。**行程時間軸的直線結構（3.4 節）跟 `.places` 卡片共用邊框的網格完全沒有動它**——那兩處的視覺規律本身就是資訊結構，破壞了會犧牲可讀性，不是「版面變異」該去動的地方。
- **一律遵守 `prefers-reduced-motion`**：新增的每一段動效（進場 stagger、行程直線的畫線動畫、nav-indicator 滑動、hover transform）都要在 reduced-motion 媒體查詢裡關掉或歸零，不能只關掉舊有的那幾個。
- **（已刪除的 F 提議頁）曾新增 `.rv` 揭露機制**（它原本沒有，只有 hero SVG 的進場動畫）：務必比照 4.1／4.3 節的原則，加上 `html.js` class 開關與「不論如何 1.4 秒後強制顯示」的保險 timer——這頁沒有 `.shell`，用的是預設 viewport 當 IntersectionObserver 的 root，邏輯簡單一些，但「內容不能憑空消失」這條鐵律一樣適用。

---

## 4. 技術決策與踩過的坑

### 4.1 自帶捲動容器（必要，勿移除）
整份內容包在 `<div class="shell" id="shell">` 裡，`height:100%; overflow-y:auto`。

**原因**：發布後網頁跑在會自動撐高的 iframe 裡，真正捲動的是外層頁面。若依賴 document 捲動會導致：
1. 導覽列跳段的 `window.scrollTo` 無效
2. IntersectionObserver 永不觸發 → 下半部內容卡在 `opacity:0` 看不見

所有捲動邏輯（跳段、置頂列高亮、淡入偵測）都必須讀 `shell` 的位置，不能用 `window`。

### 4.2 導覽用 `<button>` 不用 `<a href="#">`
錨點連結在 iframe 內會觸發「Open external link」確認視窗。改用 button + JS `shell.scrollTo`。

### 4.3 內容預設可見
`.rv` 淡入動畫只在 `html.js` 時套用（開頭有 inline script 加上 `js` class），另有 **1.4 秒保險計時器**強制顯示全部。原則：**寧可動畫沒播，也不能讓內容消失**。

### 4.4 導覽列高亮判斷
不用 IntersectionObserver（多區塊同時在畫面內時誰後回報誰贏，順序不保證）。改用明確規則：**以導覽列下緣 +24px 畫判準線，取最後一個越過該線的區塊**；捲到底時強制高亮最後一項。

### 4.5 localStorage：主題不存，待辦打勾要存

原本這條寫「一律禁用 localStorage」，前提是 **artifact 預覽環境**不支援。網站部署到
GitHub Pages 之後那個前提就不成立了，所以規則細分成兩半：

- **主題／明暗切換不做持久化**。每次開啟回到預設配色是刻意的，這份手冊的預設樣貌
  應該穩定。
- **待辦打勾要持久化**（2026-08-12 起）。那是使用者資料不是顯示偏好，勾完關掉再開
  必須還在。

三個實作要點，缺一個都會出事：

1. **讀寫都要包 try/catch**。沙盒 iframe 存取 `localStorage` 會丟 `SecurityError`
   （不是回傳 null），無痕模式寫入可能丟 `QuotaExceededError`。沒包的話整段 IIFE
   中斷，連導覽都會壞掉。失敗就退化成「本次瀏覽有效、不持久化」。
2. **key 一定要帶行程識別**：`handbook:<TRIP_ID>:checks`。所有 GitHub Pages 專案
   共用 `karen-lian.github.io` 同一個網域，`bkk` 跟未來的 `tokyo` 是同一個
   localStorage，key 不分行程的話上一趟的打勾會出現在下一趟的手冊上。
3. **每個項目用固定英文 id**（`data-todo="flight"`），不要拿中文標題當 key。
   這樣之後改文案不會弄丟已勾狀態；反過來說**改 id 就等於清空那一項**。

### 4.6 導覽只在底部 + 行程按日期跳轉列（僅 index.html）

`index.html` 內容長到「一路往下滑很累」，導覽拆成職責分開的兩層：

1. **頂部 `.nav`**：`position:sticky;top:0`，**只剩品牌字樣與主題切換**（三個配色圓點＋暗底切換），不放區塊按鈕。2026-08-11 一開始做過雙導覽列（頂部+底部各一份區塊清單），後來使用者反映頂部那排字在窄螢幕會被裁掉、兩層導覽也是視覺負擔，改成**區塊導覽只留底部這一份**，頂部純粹是工具列。
2. **底部 `.navbottom`**：`position:fixed;bottom:0`，7 個區塊按鈕（總覽/住宿/費用/行程/換匯/泰語/待辦），均分寬度（`flex:1`），是**唯一的區塊導覽**。純文字、無圖示，維持整站「只用字重與線條分層」的語彙，不要為了像原生 App 而加圖示集。
3. **行程區內的 `.daybar`**：只存在於 `#route` section 裡，`position:sticky;top:var(--navh)`，疊在頂部工具列正下方，讓使用者不用滑過六天份內容就能直接跳到指定日期。

**實作重點／踩過的坑**：
- JS 裡只有一份 `bottomLinks`／`targets`，`spy()` 只需要同步這一組 `.on` 狀態——**不要因為想加回頂部導覽就重新引入 `topLinks` 那套雙軌邏輯**，先確認使用者是不是真的要兩層都放。
- `.nav-in` 原本用 `justify-content:space-between` 讓品牌靠左、主題切換靠右；拿掉區塊按鈕後只剩兩個 flex item，行動版 `.brand{display:none}` 一觸發，`.switch` 會被 `space-between`誤判成唯一項目而跳到最左邊。**改用 `.switch{margin-left:auto}`**，不管 `.brand` 在不在都固定靠右，這是拿掉頂部連結列時順手踩到、又順手修掉的坑。
- 每個 `.day` article 都要有 `id="d08XX"`（例如 `id="d0819"`）給 `.daybar` 的按鈕當跳轉目標；新增/刪除行程日時記得同步加減 `.daybar` 裡的按鈕與對應 id。
- `.daybar` 疊在 `#route` section 裡面，而 `#route` 本身是 `.rv`（進場時會有短暫的 `transform`）。**`transform` 存在的當下會讓子層 `position:sticky` 的定位基準跟著跑**，但 `.rv.in` 完成後 `transform:none`，問題只會在最初進場那 0.8 秒短暫出現，之後恢復正常——如果之後又在別的 `.rv` 區塊裡放 sticky 元件，先確認這個前提還成立。
- `goTo()` 統一負責「捲到某個區塊」，額外接一個 `extraOffset` 參數：一般導覽用 0，`.daybar` 跳轉要多扣一個 `.daybar-wrap` 自己的高度，不然目標日期的標題會被兩層 sticky 列蓋住。
- `.shell` 加了 `padding-bottom:calc(var(--navh) + env(safe-area-inset-bottom,0px))`，讓底部導覽列不會蓋住頁尾內容。
- （已刪除的 F 提議頁）內容短、沒有多日行程可跳，**沒有加這幾層導覽**——只有一個主題切換列，這是刻意的，不是漏改。

### 4.7 通用分頁元件：`.tabbar` / `.tab-panel`（僅 index.html）

費用分擔（`#money`）跟泰語隨身頁（`#thai`）都改成**分頁式**，共用同一組元件，不是各寫一份：

```html
<div class="tabbar-wrap">
  <div class="tabbar" role="tablist" aria-label="...">
    <button type="button" class="on" data-tabgroup="money" data-tab="both">兩人</button>
    <button type="button" data-tabgroup="money" data-tab="kj">鈞</button>
    ...
  </div>
</div>
<div class="tab-panel" data-tabgroup="money" data-tab="both">...</div>
<div class="tab-panel" data-tabgroup="money" data-tab="kj" hidden>...</div>
```

`data-tabgroup` 是分組鍵，同一頁可以有好幾組互不干擾的分頁（目前是 `money` 與 `thai` 兩組）。JS 用同一段邏輯處理所有分頁：點按鈕時，只切換**同一個 `data-tabgroup`** 底下的按鈕 `.on` 狀態與面板 `[hidden]`，不會互相干擾。**新增第三組分頁時直接沿用這個模式，不要另外寫一套。**

**兩組分頁各自的內容切法**：
- **費用分擔**：「兩人」放雙方都要看的共用資訊（費用分擔清單、捷運車資、餐費預算，數字兩人一樣不用拆兩份）；「鈞」「平」各自只放個人固定花費表 + 合計小結，小結會重述算式但**不重複列出餐費/捷運車資的完整表格**（那些在「兩人」分頁），只在 `cost-note` 註明明細去哪裡看。改任何一邊的餐費或捷運估算金額，兩人分頁的表格與鈞/平分頁小結裡的算式**要一起改**，不然數字會對不上。
- **泰語隨身頁**：按原本的 `.phrase-group` 主題分（基本禮貌／搭車／點餐／市集殺價／按摩／其他常用），一個主題一個 `.tab-panel`，`.phrase-group` 本身結構不變，只是外面多包一層。`.hint` 開場說明（「講不通的時候…」）留在 tabbar 上方，因為對六個分頁都適用，不要塞進某一個分頁裡。

**實作細節**：
- 切換分頁用 `[hidden]` 屬性而不是 CSS class 控制 `display`，這樣 `.tab-panel{animation:tabPanelIn ...}` 每次從隱藏變顯示都會重新播放（瀏覽器對 `display:none → 顯示` 的元素會重跑 CSS animation），不用額外寫 JS 去 toggle 動畫 class。
- `.tabbar` 用 `flex-wrap:wrap` + 個別按鈕各自完整邊框（不是共用邊框的 segmented control），這樣 3 顆（費用）跟 6 顆（泰語，手機上會換行成兩排）都適用，不會有換行後邊框對不齊的問題。
- 列印（`@media print`）要強制把所有分頁都印出來（`.tab-panel{display:block!important}`），不能讓紙本只印到當下選到的那一頁。

### 4.9 `.fork` 的選項裡不能塞任何行內元素

`.fork div` 是 `display:flex`。flex 容器會把**每一段連續文字各自變成一個匿名 flex 項目**，
所以選項文字裡只要夾一個 `<b>`、`<em>`、`<span class="note">`，那個標籤就會變成**獨立的
flex 項目**，跟前後文字斷開、各自換行。加上 `.fork div span{flex:none}` 會選到裡面所有的
span，`.note` 還會變成不能收縮的項目，把本文擠成一行一個字。

```html
<!-- 壞掉 -->
<div><span>01</span>選項文字<span class="note">補充</span></div>

<!-- 正確：補充說明放在 .fork 外面 -->
<div><span>01</span>選項文字</div>
</div><!-- /.fork -->
<span class="note">補充說明</span>
```

這個坑只有截圖看得出來——DOM 結構合法、JS 沒錯、innerText 讀起來也正常。

### 4.8 `[hidden]` 會被作者端的 `display` 宣告蓋掉

`[hidden]` 的效果只是瀏覽器預設樣式表裡的 `display:none`，**優先權低於任何作者寫的 `display`**。
所以只要元素本身有 `display:grid` / `flex` / `block` 之類的宣告，設 `el.hidden = true` 後
DOM 屬性是 `true`、JS 讀 `el.hidden` 也回 `true`，但畫面上**照樣看得到**。

```css
.plan li{display:grid;}      /* 這行會蓋掉 [hidden] */
.plan li[hidden]{display:none;}  /* 一定要自己補這條 */
```

`.tab-panel` 沒踩到這個坑是因為它沒有自己的 `display` 宣告，純屬運氣。
**任何用 `[hidden]` 控制顯示、同時又有 `display` 宣告的元素，都要補一條 `[hidden]{display:none}`。**

驗證時也要注意：**用 `getComputedStyle(el).display !== 'none'` 判斷，不要用 `el.hidden`**。
這個 bug 就是因為測試腳本讀了 DOM 屬性而通過，最後是靠截圖才看出來八列全部都在。

---

## 5. 內容決策（不要「順手優化」掉）

- **費用清單一律「項目在前、負擔者在後」**，右側對齊付款標籤。
- **地圖連結**：所有地點都有 Map 按鈕，包含分岔卡裡的每個選項。已驗證的短連結（`maps.app.goo.gl/...`）優先於搜尋連結。
- **不確定的資訊要標明**：泰文店名查不到就寫「用英文名／地圖圖釘給司機看」，不憑空拼一個可能錯的泰文。
- **待確認事項用半實心點 + 文字雙重標示**，例如三場舞會都標「官方 8/16 才公告」。
- **費用估算只列有明確定價的項目**，不硬編猜測的總額。

### 已驗證的短連結（勿改成搜尋連結）
```
8/19 住宿              https://maps.app.goo.gl/FpSfetp1MZ25TQ4JA
8/20 中餐              https://maps.app.goo.gl/Zv3BqV2qxtLhWRxf9
Auntie Joom's          https://maps.app.goo.gl/BADAfR63XKMjJRtw6
8/20 辦公              https://maps.app.goo.gl/DiuWURFPghWnGC8T6
8/21 辦公              https://maps.app.goo.gl/4xwjukbxJhmLcPWa7
橘色 SuperRich（Asok） https://maps.app.goo.gl/xANA8z7HQ1tiZi247
橘色 SuperRich（素坤逸）https://maps.app.goo.gl/oZWnQsRxqvKCn3So9
Max Exchange（Asok）   https://maps.app.goo.gl/4KPmWt4X9ufu9Lro8
```

---

## 6. 行程摘要（截至最後更新）

| 日期 | 重點 | 晚上 |
|---|---|---|
| 8/19 三 | 07:30 朝馬統聯→機場・13:25 起飛・入住克隆托伊 | SW1 夜市＋THONGSUK 按摩 |
| 8/20 四 | 鈞辦公・12:30 與 J朋友 午餐・嵩越路＋咖啡廳 | ⏳Hot Latin Thursday @ RED DOOR |
| 8/21 五 | 鈞辦公・10:45 退房→F 房源・鄭王廟泰服 | Swing Era @ Thammasat（鈞單獨，2500）／平：Terminal 21 或 SWU |
| 8/22 六 | **分岔：問 F 要不要一起去綠肺**・16:40 離島 | ⏳Sensual Saturday @ HEAVEN 17 |
| 8/23 日 | 09:00–12:00 水門市場＋TOFU・Platinum Pop・洽圖洽・17:00 離開 | ⏳Bachata Fever @ The Mesh |
| 8/24 一 | 05:40 Uber→機場・09:10 起飛・13:55 抵台 | 客運回台中（豐原 vs 朝馬判斷） |

**8/22 的分岔邏輯**（整個早上取決於 F 的答覆）：
- 方案 A（F 一起去）：飯店運動 → 買早餐 → 10:30–11:00 出發 → **中餐在島上吃**
- 方案 B（F 不去）：買早餐 → 09:00 瑜伽 → 梳洗 → 與 F 午餐 → 島上**只喝咖啡**

---

## 7. 未解決事項

1. **8/16 官方公告後**，重新確認 8/20、8/22、8/23 三晚的舞會時間與地點（目前全是暫定）
2. **問 F**：8/22 要不要一起去綠肺（決定整個早上）、房源健身房開放時間、要 F 房源的完整泰文地址
3. **The Mesh 地址存疑**：BBG 班表寫 Sukhumvit soi 22，但 Four Points by Sheraton 實際在 soi 15，目前連結是我推測的，**需要向主辦確認**
4. 8/20 的 MRT／8/23 的 BTS 系統歸屬是推測，非鈞指定
5. 捷運站數是用「每站約 2 分鐘」從搭乘時間反推，非官方對照表
6. 平要辦 Rabbit Card（只能搭 BTS；MRT 直接刷感應信用卡）

---

## 8. 部署

```bash
# 在 bkk repo 根目錄
git add -A
git commit -m "update handbook"
git push
```

`index.html` 為 GitHub Pages 首頁，網址 `karen-lian.github.io/bkk/`。

建議放一支 `deploy.sh`：
```bash
#!/bin/bash
git add -A && git commit -m "update $(date +%F\ %H:%M)" && git push
```

---

## 9. 給接手的 Claude Code 的提醒

- 改任何行程，**`index.html` 與 markdown 兩份都要動**。
- 動 CSS 前先看第 3 節的約束，特別是**單色系統**與 **`.wrap` 的 padding 陷阱**。
- 動 JS 前先看第 4 節，**捲動一律走 `shell`，不要用 `window`**。
- 使用者的工作風格：直接、迭代快、會給結構化的修正。她會截圖圈出問題點，回應時**先講清楚問題的成因**再給修法，不要只丟結果。
- 她偏好繁體中文回覆；發想類型的請求要說明「為什麼這樣選」以及「怎麼做」。
