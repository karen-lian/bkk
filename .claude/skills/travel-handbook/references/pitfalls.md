# 踩過的坑

每一條都是實際繞了好幾輪才找到根因的。動 CSS/JS 前先看過，遇到版面異常也回來查。

## 1. `.wrap` 的 padding 簡寫陷阱

**症狀**：區塊大標題上方的留白整個消失。

**根因**：`padding:0 var(--gut)` 簡寫會把上下 padding 設為 `0`，而 class 選擇器
（`.wrap`）優先權高於元素選擇器（`section{padding-top}`），所以把 `section` 的
上方留白蓋掉了。

**解法**：一定寫成 `padding-left` / `padding-right` 兩行，不要用簡寫。

## 2. 自帶捲動容器（必要，勿移除）

整份內容包在 `<div class="shell" id="shell">` 裡，`height:100%; overflow-y:auto`。

**原因**：頁面可能跑在會自動撐高的 iframe 裡（artifact 預覽、嵌入式檢視），
真正捲動的是外層頁面。若依賴 document 捲動會導致：

1. 導覽跳段的 `window.scrollTo` 無效
2. IntersectionObserver 永不觸發 → 下半部內容卡在 `opacity:0` 看不見

**規則**：所有捲動邏輯（跳段、置頂列高亮、淡入偵測）都必須讀 `shell` 的位置，
不能用 `window`。IntersectionObserver 也要傳 `{root: shell}`。

## 3. 導覽用 `<button>` 不用 `<a href="#">`

錨點連結在 iframe 內會觸發「Open external link」確認視窗。改用 button + JS
`shell.scrollTo`。

## 4. 內容預設可見

`.rv` 淡入動畫**只在 `html.js` 時套用**（`<body>` 開頭有 inline script 加上 `js` class），
另有 **1.4 秒保險計時器**強制顯示全部。

**原則：寧可動畫沒播，也不能讓內容消失。** IntersectionObserver 在某些嵌入環境會靜默
失效，沒有保險的話整個下半頁就是一片空白。

## 5. 導覽列高亮判斷不要用 IntersectionObserver

多區塊同時在畫面內時，誰後回報誰贏，順序不保證，高亮會亂跳。

**改用明確規則**：以導覽列下緣 +24px 畫一條判準線，取**最後一個越過該線**的區塊；
捲到底時強制高亮最後一項。

## 6. `.day` 不可被子項 stagger 選擇器蓋到

**症狀**：六天的行程在 `#route` 一進畫面時整批顯示，逐日揭露的效果作廢。

**根因**：`.day` 自己就是 `.rv` / IntersectionObserver 的觀察目標。如果子代選擇器
寫成 `html.js .rv .day`，那麼外層 `#route`（也是 `.rv`）一進畫面時，`.day` 就會
被當成「已揭露區塊的子項」提前顯示。

**解法**：stagger 規則裡把 `.day` 排除，只寫 `html.js .day.rv .stops>li`
（限定在 `.day` 自己已經 `.in` 之後才輪到它的子項）。

## 7. `.rv` 的 transform 會影響子層 sticky 定位

`.daybar-wrap` 是 `position:sticky`，但它住在 `#route` 裡，而 `#route` 是 `.rv`
（進場時有短暫的 `transform`）。**transform 存在的當下會讓子層 sticky 的定位基準
跟著跑**。

實際影響有限：`.rv.in` 完成後 `transform:none`，問題只在最初進場那 0.8 秒短暫出現。
但如果之後又在別的 `.rv` 區塊裡放 sticky 元件，要先確認這個前提還成立。

## 8. `.switch` 靠右要用 `margin-left:auto`

**症狀**：拿掉頂部導覽的區塊按鈕後，行動版把 `.brand` 隱藏時，主題切換的色點會
跳到最左邊。

**根因**：原本靠 `justify-content:space-between` 讓品牌靠左、切換靠右。只剩兩個
flex item 時，一旦 `.brand` 被 `display:none`，`space-between` 會把唯一剩下的
項目推到起點。

**解法**：`.switch{margin-left:auto}`，不管 `.brand` 在不在都固定靠右。

## 9. 不同幣別絕對不要相加

**症狀**：產生一個看起來很精確、實際上完全錯誤的總額。

台幣支出（在出發國先刷掉的住宿、網卡、保險）與當地幣支出是不同單位，直接加會得到
沒有意義的數字。**分開列小計，並在備註寫明為什麼沒有合併。**

要提供合併總額的話，必須有實際刷卡匯率或帳單金額，用預估匯率換算會跟實際扣款對不上。

## 10. localStorage 要包 try/catch

**症狀**：整段腳本中斷，連導覽都不能用。

**根因**：在沙盒 iframe（artifact 預覽、某些嵌入情境）存取 `localStorage` 會直接
丟 `SecurityError`，不是回傳 null。無痕模式在部分瀏覽器也會在寫入時丟 `QuotaExceededError`。

**解法**：讀寫都包 try/catch，失敗就退化成「本次瀏覽有效、不持久化」，畫面照常運作。

## 11. localStorage 的 key 一定要帶行程識別

**症狀**：上一趟的打勾狀態出現在新的手冊上。

**根因**：所有 GitHub Pages 專案共用 `<帳號>.github.io` **同一個網域**。
`karen-lian.github.io/bkk/` 和 `karen-lian.github.io/tokyo/` 的 localStorage 是同一個。

**解法**：key 寫成 `handbook:<trip-id>:checks`，`TRIP_ID` 每趟必改。
另外每個項目用**固定英文 id**（`flight`、`sim`…）而不是中文標題當 key，
這樣之後改文案不會弄丟已勾狀態。

## 12. 禁用主題持久化

主題／明暗切換**不要**存進 localStorage。artifact 環境不支援，而且每次開啟回到
預設配色是刻意的——這份手冊的預設樣貌應該是穩定的。

（待辦打勾是例外：那是使用者資料，不是顯示偏好。）

## 13. `[hidden]` 會被作者端的 `display` 宣告蓋掉

**症狀**：JS 設了 `el.hidden = true`，`el.hidden` 讀回來也是 `true`，畫面上卻照樣看得到。

**根因**：`[hidden]` 只是瀏覽器預設樣式表的 `display:none`，**優先權低於任何作者寫的 `display`**。
元素只要有 `display:grid` / `flex` / `block`，`[hidden]` 就完全無效。

```css
.plan li{display:grid;}
.plan li[hidden]{display:none;}   /* 少了這行，hidden 形同虛設 */
```

`.tab-panel` 沒踩到是因為它本身沒有 `display` 宣告，純屬運氣。
**凡是用 `[hidden]` 控制顯示、又有 `display` 宣告的元素，都要自己補一條。**

**驗證時**：用 `getComputedStyle(el).display !== 'none'` 判斷，**不要**用 `el.hidden`——
讀 DOM 屬性會讓這個 bug 通過測試，最後只有截圖看得出來。
