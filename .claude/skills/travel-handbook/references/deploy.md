# 部署

一趟行程 = 一個新 repo。這樣每份手冊各自獨立，改壞了不會波及其他行程，
也能各自保留 commit 歷史。

## Repo 命名

`<城市>-<年月>`，全小寫：`bkk-2026-08`、`tokyo-2027-03`。
網址會是 `https://<帳號>.github.io/<repo>/`。

**這個 repo 名稱要跟 `index.html` 裡的 `TRIP_ID` 一致**，避免兩趟行程的打勾狀態
互相污染（見 pitfalls.md 第 11 條）。

## 檔案

repo 根目錄放：

```
index.html      ← 手冊本體，單一檔案
README.md       ← 一段話說明這是什麼、線上網址
```

不需要 build、不需要 package.json、不需要 CI。單檔 HTML 就是全部。

## 建立與推送

用 GitHub MCP 工具（需要時用 ToolSearch 載入）：

1. `mcp__github__create_repository` — 建立 repo。**設為 public**，GitHub Pages
   的免費方案只支援公開 repo。行程資料裡不要放護照號碼、訂位代號、信用卡末四碼
   這類東西；住宿地址與航班編號是可以的，但要意識到那是公開的。
2. `mcp__bf7c680d…__add_repo` — 把新 repo 加進這個 session 的存取範圍
3. `mcp__github__push_files` — 推 `index.html` 與 `README.md` 到 `main`

## 開啟 GitHub Pages（這步要使用者自己做）

**沒有對應的 API 工具可以代勞**，要請使用者手動點：

> Settings → Pages → Source 選 **Deploy from a branch** → Branch 選 `main` / `/ (root)` → Save

存檔後約 1–2 分鐘會生效，網址是 `https://<帳號>.github.io/<repo>/`。

告知使用者時要把這串路徑寫清楚，不要只說「去開一下 Pages」。

## 後續更新

改完 `index.html` 直接 push 到 `main`，Pages 會自動重新部署，通常一兩分鐘內生效。

**推新版不會影響已經勾好的待辦**——localStorage 存的是「網域 + key」，跟 HTML 檔案
無關。唯一會弄丟的情況是改掉 `data-todo` 的 id 或 `TRIP_ID`。

## 分支慣例

使用者若已有偏好的分支流程就照他的。預設：直接在 `main` 上改並 push（單人維護的
個人專案，開 PR 沒有實益）。
