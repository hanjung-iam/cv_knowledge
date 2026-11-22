# CV Wiki Log

Append-only 操作紀錄。格式：`## [YYYY-MM-DD] <type> | <title>`，type 為 setup / ingest / lint / query / slides / schema。

## [2026-11-22] setup | 建立 Wiki 結構
- 建立 CLAUDE.md（schema）、目錄結構、index.md、log.md、report/process-journal.md
- raw/ 排除於 git 之外

## [2026-11-22] schema | 移除預設 ingest 順序與預先登記的 cite key
- 9.2 改為「每份新來源都做影響評估」
- cite key 改為 ingest 時建立於 source 頁 frontmatter
