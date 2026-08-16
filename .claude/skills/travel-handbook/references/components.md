# 元件 markup 契約

照著寫，不要自創 class。CSS 已經幫這些結構排好，換了標籤或層級就會壞。

## 區塊骨架

固定順序：**總覽 → 住宿 → 費用 → 行程 → 當地 → 待辦**。
底部導覽的按鈕順序**必須跟區塊順序一致**——`spy()` 靠陣列索引對應，不是靠 id 比對。

```html
<section class="wrap rv" id="stay">
  <div class="sec-head"><h2>住宿</h2><span class="rule"></span><span class="eyebrow">Bases</span></div>
  …
</section>
```

`rv` = 進場揭露。每個 section 都要有。

## meta-strip（總覽四格）

固定四格。手機會變 2×2。

```html
<div class="meta-strip">
  <div><small>Outbound</small><b class="num">8/19 13:25</b><small class="lo">VZ571 TPE → BKK</small></div>
  …
</div>
```

## 住宿卡

```html
<div class="duo">
  <article class="card">
    <span class="tag">01</span>
    <span class="eyebrow">19 → 21 Aug · 2 nights</span>
    <h3>名稱</h3>
    <dl>
      <div class="kv"><dt>房東</dt><dd>值</dd></div>
      <div class="kv"><dt>地址</dt><dd>值<a class="mapbtn" href="…" target="_blank" rel="noopener">Map</a></dd></div>
      <div class="kv"><dt>房費</dt><dd class="num">1,675 TWD（可鈞負擔）</dd></div>
    </dl>
    <div class="alert">硬底線提醒。</div>
  </article>
</div>
```

`.duo` 只吃兩個孩子（偶數項會自動垂直錯位）。三段以上住宿就用兩個 `.duo`。

## 費用：分頁 + 表格

`.tabbar` / `.tab-panel` 用 `data-tabgroup` 分組，**同一頁可以有好幾組互不干擾**。
目前用了三組：`money`、`phrase`、`todo`（`todo` 內還巢了一組 `prep`）。

```html
<div class="tabbar-wrap">
  <div class="tabbar" role="tablist" aria-label="依角色檢視費用">
    <button type="button" class="on" data-tabgroup="money" data-tab="both">兩人</button>
    <button type="button" data-tabgroup="money" data-tab="kj">可鈞</button>
  </div>
</div>
<div class="tab-panel" data-tabgroup="money" data-tab="both">…</div>
<div class="tab-panel" data-tabgroup="money" data-tab="kj" hidden>…</div>
```

**用 `[hidden]` 屬性而不是 CSS class 控制顯示**——這樣 `.tab-panel` 的
`animation:tabPanelIn` 每次從隱藏變顯示都會重播（瀏覽器對 `display:none → 顯示`
的元素會重跑 CSS animation），不用額外寫 JS toggle 動畫 class。

內容切法：**共用資訊放「兩人」分頁**（誰付、交通費、餐費——兩人數字一樣不用拆兩份），
個人分頁只放自己的固定花費表 + 合計小結，小結重述算式但**不重複列共用表格**，
只在 `.cost-note` 註明明細在哪一頁。改共用數字時，個人分頁小結裡的算式要一起改。

```html
<p class="mini-h">已知固定花費 · 可鈞</p>
<table class="cost-tbl">
  <tr><th>路段</th><th>系統</th><th class="r">單程／人</th></tr>   <!-- 有表頭才寫 -->
  <tr><td>項目<small>備註</small></td><td class="r">300</td></tr>
  <tr class="sum"><td>小計</td><td class="r">5,180 THB</td></tr>
</table>
<p class="cost-note">說明。</p>
```

`.r` = 右對齊 + tabular numerals。`.sum` = 上方粗線的合計列。

## 行程

```html
<div class="daybar-wrap">
  <div class="daybar" role="tablist" aria-label="跳到指定日期">
    <button type="button" data-day="d0819"><b>19</b><i>WED</i></button>
  </div>
</div>
<div class="legend">
  <i><span class="chip solid"></span>兩人同行</i>
  <i><span class="chip"></span>各自行動</i>
  <i><span class="chip half"></span>待定 / 待確認</i>
</div>
<div class="route">
  <article class="day rv" id="d0819">
    <div class="day-head"><span class="day-num num">8/19</span><span class="day-dow">Wed</span><span class="day-title">主題</span></div>
    <ul class="stops">
      <li class="stop together"><time class="num">07:30</time><div class="body">項目<a class="mapbtn" href="…">Map</a><span class="note">補充</span></div></li>
      <li class="stop"><time>上午</time><div class="body">項目<span class="who">可鈞</span></div></li>
      <li class="stop pending"><time class="num">20:00</time><div class="body">項目<span class="note"><b>官方 8/16 才公告</b></span></div></li>
    </ul>
    <div class="alert">當天硬底線。</div>
  </article>
</div>
```

- 每個 `.day` 都要有 `id="d<MMDD>"`，`.daybar` 的按鈕靠它跳轉。**新增／刪除日期時
  要同步加減 `.daybar` 的按鈕**。
- `.stop` 的三種圓點狀態見 design-system.md，半實心必須配文字說明。
- 分岔選項用 `.fork`：

```html
<div class="fork">
  <p>選項標題</p>
  <div><span>01</span>選項一<a class="mapbtn" href="…">Map</a></div>
</div>
```

## 地點卡

```html
<div class="places">
  <div class="place">
    <div class="zh">中文名</div><div class="en">Category</div>
    <div class="native loc">當地文字</div>
    <div class="rom">羅馬拼音</div>
    <div class="memo">備註。</div>
    <a class="map" href="…" target="_blank" rel="noopener">Google Map</a>
  </div>
</div>
```

`.places` 是共用邊框的網格，**不要對它加旋轉或位移**——那個規律本身是分類資訊。
`.native`/`.rom` 可省略（拉丁字母目的地就不用）。

## 語言短句

```html
<div class="phrase-group">
  <h3>基本禮貌 <em>Basics</em></h3>
  <div class="ph"><div class="zh">你好</div><div class="native loc">สวัสดีค่ะ</div><div class="rom">sà-wàt-dii khâ<b>沙瓦低 卡</b></div></div>
</div>
```

`.rom` 裡的 `<b>` 是中文近似音。**目的地語言跟你共通就整組拿掉，別硬湊。**

## 待辦打勾

固定九項通用清單 + 這趟專屬事項，兩組分頁，都可勾選，狀態存本機。

```html
<ul class="todo" data-owner="kejun">
  <li><label class="chk">
    <input type="checkbox" data-todo="flight"><span class="box"></span>
    <span class="txt">訂機票<small>備註</small></span>
  </label></li>
</ul>
```

- `data-owner` 區分是誰的清單（每人一個 `<ul>`）
- `data-todo` 是**固定英文 id**，儲存 key 是 `<owner>:<todo>`。
  **改中文標題不會弄丟已勾狀態，改 id 會。**
- `.txt` 這層不能省，勾選後的刪除線靠它
- 進度計數 `<p class="chk-progress">已完成 <b>0</b> / 9</p>` 要放在 `<ul>` 的
  **同一個父層**，JS 用 `ul.parentNode.querySelector` 找它

JS 那段的 `TRIP_ID` **每趟必改**，理由見 pitfalls.md 第 11 條。
