# CV Wiki Log

Append-only 操作紀錄。格式：`## [YYYY-MM-DD] <type> | <title>`，type 為 setup / ingest / lint / query / slides / schema。

## [2026-11-22] setup | 建立 Wiki 結構
- 建立 CLAUDE.md（schema）、目錄結構、index.md、log.md、report/process-journal.md
- raw/ 排除於 git 之外

## [2026-11-22] schema | 移除預設 ingest 順序與預先登記的 cite key
- 9.2 改為「每份新來源都做影響評估」
- cite key 改為 ingest 時建立於 source 頁 frontmatter

## [2026-11-22] setup | 建立 lint 與關聯圖工具
- 新增 tools/wikilib.py（共用解析）、tools/lint.py、tools/graph.py
- 以含刻意錯誤的測試 Wiki 驗證 lint：8 error / 11 warning 全數命中，無誤報
- 對目前的 Wiki 執行 lint：0 error，7 份 raw 檔待 ingest
