---
name: travel-handbook
description: Build a personal travel handbook website — a single-file HTML trip site with a silkscreen-print design system (one ink colour + one paper colour, hand-drawn city line art, day-by-day route timeline with who's-coming dot encoding, cost-splitting tabs, local-language phrasebook), then deploy it to its own GitHub repo with Pages. Use this whenever the user is planning a trip and wants a handbook, itinerary page, or trip site — including when they say 旅遊手冊, 行程表, 行程網站, travel handbook, "make me a page for my trip", or name a city plus dates. Also use it when editing an existing handbook built from this template, so the design constraints and the hard-won layout fixes are respected instead of rediscovered.
---

# 旅遊手冊網站

一份行程 = 一個單檔 HTML 網站 = 一個 GitHub repo。這個 skill 帶著已經驗證過的設計系統、
元件與踩坑修正，換城市時只要換四個地方。

## 換城市要動的四個地方

模板 `assets/template.html` 裡標了 `SWAP 1/4` ～ `SWAP 4/4`，只有這四處是城市專屬：

| # | 位置 | 換什麼 |
|---|---|---|
| 1 | CSS 最上方六行 | 三組配色 × 明暗的 `--ink` / `--paper` |
| 2 | `.switch` 三顆色點 | `background` 要對上配色的 light `--ink` |
| 3 | `.art` 裡的 SVG | 該城市的天際線／街景線稿 |
| 4 | Google Fonts 網址 | 只換「當地文字」那支（拉丁字母目的地就整支拿掉） |

加上一個**每趟必改**的常數：JS 裡的 `TRIP_ID`。所有 GitHub Pages 專案共用同一個
網域，這個 id 沒換的話，上一趟的待辦打勾會出現在新手冊上。

**其他一律不要改。** CSS 與 JS 是踩過坑換來的，字型組合（Bai Jamjuree + Noto Sans TC）
是這套手冊的識別，不要因為換了國家就換字型。

## 流程

### 1. 收資料

使用者可能丟一份行程草稿，也可能什麼都沒有。**有草稿就直接解析，不要再問一遍已經寫在裡面的東西。**
缺的才問，而且一次問完：

- 城市（英文大寫 + 中文）、日期區間
- 同行者姓名與稱呼
- 幣別，以及有沒有「在台灣先刷掉」的支出
- 住宿幾段、各段誰負擔
- 目的地語言（決定要不要留語言短句區）

### 2. 挑配色與畫線稿

這兩件是唯一需要創作的部分，讀 `references/design-system.md`（配色公式與檢查標準）
與 `references/city-art.md`（線稿母題與畫法）。

配色三組的邏輯是「這座城市的三種面貌」，不是隨機三個顏色。曼谷是計程車桃紅／廟宇金／
湄南河靛藍——都能講出出處。新城市也要能講得出來。

挑完一定要跑檢查，不要用目測判斷對比夠不夠：

```bash
python3 scripts/check_palette.py --file index.html
```

### 3. 組頁面

複製 `assets/template.html` 成 `index.html`，換掉四個 SWAP 點，然後填內容。
每個區塊的 markup 契約見 `references/components.md`——照著寫，不要自創 class。

區塊順序固定：總覽 → 住宿 → 費用 → 行程 → 當地 → 待辦。
底部導覽的按鈕順序必須跟區塊順序一致（`spy()` 靠索引對應，不是靠 id 比對）。

**待辦區的九項通用清單是跨行程固定的**（訂機票／訂住宿／網卡／簽證／保健食品＋藥品／
充電器＋行動電源＋轉接頭／保險／盥洗衣物＋保養品＋化妝品／隱形眼鏡＋墨鏡＋噴香香），
每個同行者一份，只勾選、不新增不刪除。同行者人數變了就增減 `<ul data-owner>` 與對應
的人名分頁。打勾狀態存在使用者自己的瀏覽器，兩人不同步——這是刻意的，因為這九項
大多是各自打包各自的東西，而且出國時斷網也要能用。

### 4. 驗證（不要跳過）

改完一定要真的打開來看。這一步在開發過程中抓到過好幾個只有渲染才看得出來的問題：

```bash
cd <repo> && python3 -m http.server 8931 &
```

```js
// /tmp/verify.mjs — node /tmp/verify.mjs
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: 390, height: 844 } });
const errs = [];
p.on('pageerror', e => errs.push(String(e)));
await p.goto('http://localhost:8931/index.html', { waitUntil: 'networkidle' });
await p.waitForTimeout(700);
await p.screenshot({ path: '/tmp/v_top.png' });
// 每個區塊、每組分頁、每個日期鈕都點過一次
for (const s of ['stay','money','route','local','todo']) {
  await p.$eval(`.navbottom button[data-go="${s}"]`, e => e.click());
  await p.waitForTimeout(900);
  await p.screenshot({ path: `/tmp/v_${s}.png` });
}
await p.$eval('#modeBtn', e => e.click());
await p.waitForTimeout(400);
await p.screenshot({ path: '/tmp/v_dark.png' });
// .rv 的轉場是 0.8s，要等它跑完再量，否則會把轉場中間值誤判成「卡住」
await p.waitForTimeout(1200);
const stuck = await p.evaluate(() =>
  [...document.querySelectorAll('.rv')]
    .filter(e => !e.classList.contains('in') || getComputedStyle(e).opacity !== '1')
    .map(e => e.id || e.className));
console.log('JS ERRORS:', errs, '\nSTILL INVISIBLE:', stuck);
await b.close();
```

必須全部通過才算完成：JS 錯誤為空、沒有卡在隱形的 `.rv`、手機寬度不橫向捲動、
暗底可讀、每組分頁都能切、待辦勾選後重新整理狀態還在。
字型 CDN 連不到的 `ERR_CONNECTION_RESET` 與 favicon 404 可以忽略（沙盒沒外網）。

### 5. 部署

讀 `references/deploy.md`。一趟一個新 repo，開 repo 與推檔案可以代勞，
**GitHub Pages 的開關要使用者自己去點**（API 沒有對應工具）。

## 內容原則

這些是這套手冊「讀起來像人寫的」而不是「像 AI 生的」的原因，比任何視覺細節都重要。

**誠實標示不確定**。查不到當地文字的店名就寫「用英文名／地圖圖釘給司機看」，不要憑空
拼一個可能是錯的。推測值要說明推測方法（「站數是用搭乘時間換算，每站約 2 分鐘，不是
官方對照表」）。待確認的事情用半實心圓點 **加上** 文字雙重標示，不要只靠顏色。

**寫後果，不寫形容詞**。不是「記得早點到」，是「17:00 最晚離開，回住所要 30 分鐘，
17:30 才到得了」。每一條時間提醒都要讓人知道晚了會失去什麼。

**不同幣別絕對不要相加**。台幣支出與當地幣支出分開列小計，並在備註寫明為什麼沒有合併。
這是實際踩過的坑——混加會產生一個看起來很精確但完全錯誤的數字。

**費用一律「項目在前、負擔者在後」**，右側對齊付款標籤。估算只列有明確定價的項目，
不硬編一個猜測的總額。

**地圖連結**：使用者給的已驗證短連結（`maps.app.goo.gl/...`）優先於搜尋連結，不要
「順手」改成搜尋連結。每個地點都要有 Map 按鈕，包含分岔卡裡的每個選項。

**待辦清單放的是「會卡住別的事」的項目**，不是所有雜事。每條都要寫出為什麼重要、
什麼時候要做完。已經完成的項目要改寫成下一個動作（「登記」完成後改成「問同行者要不要一起，
要的話提醒她也要登記」），不是直接刪掉。

## 絕對不要做的事

每一條都是實際踩過的坑，理由見 `references/pitfalls.md`：

1. **不要引入第三個顏色。** 所有層次靠線條粗細與網點密度。加了第三色，整個資訊結構會散掉。
2. **不要用 `padding:0 var(--gut)` 簡寫在 `.wrap` 上。** 會把上下 padding 歸零，
   且 class 優先權高過 `section{padding-top}`，標題上方留白會整個消失。
3. **捲動一律讀 `shell`，不要用 `window`。** 頁面可能跑在會自動撐高的 iframe 裡。
4. **導覽用 `<button>`，不要用 `<a href="#">`。** 錨點在 iframe 內會跳「Open external link」確認視窗。
5. **不要讓內容有機會消失。** `.rv` 動畫只在 `html.js` 時套用，且一定要留 1.4 秒保險計時器。
   寧可動畫沒播，也不能讓人看到空白。
6. **不要把 `.day` 併進子項 stagger 選擇器。** 它自己就是觀察目標，被子代選擇器蓋到
   會讓六天內容在外層一進畫面時整批提前顯示。
7. **不要對承載資訊的結構加裝飾性變異。** 行程時間軸的直線、地點卡的共用邊框網格，
   那些規律本身就是資訊（誰同行、分類），歪掉是犧牲可讀性換好看。
8. **不要用 localStorage。** artifact 環境不支援，主題切換不做持久化。

## 參考文件

| 檔案 | 什麼時候讀 |
|---|---|
| `references/design-system.md` | 挑配色、確認字級與間距、圓點編碼語意 |
| `references/city-art.md` | 畫城市線稿（換城市時必讀） |
| `references/components.md` | 寫任何一個區塊的 markup 之前 |
| `references/pitfalls.md` | 動 CSS/JS 之前，或遇到版面異常時 |
| `references/deploy.md` | 開 repo 與部署 |
| `scripts/check_palette.py` | 挑完配色後跑，確認對比夠 |
