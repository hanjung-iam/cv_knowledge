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

## [2026-11-22] schema | 新增 dataset 類型、時效性規則、raw 檔讀取方式
- 新增 datasets/ 與 type: dataset；時效性主張須標（截至 …）
- 多檔來源的引用格式、圖片引用加「圖」、同一來源內部不一致的處理
- 9.0 讀取 raw 檔：md 取文字、pdf 取圖片；不把來源圖片複製進 wiki
- 工具：lint 支援 dataset、時效性檢查、教材位置格式、引用算作連入；graph 以虛線畫引用

## [2026-11-23] ingest | CS231n — classification
- 新增：sources/cs231n.md, tasks/image-classification.md, concepts/k-nearest-neighbor.md, concepts/hyperparameter-tuning.md, datasets/cifar-10.md, overview.md
- 更新：index.md
- 數字核對：26 項數字逐一對照原文；修正 1 處來源沒有的評價性推論（CIFAR-10 頁「人類 94%」）
- lint：首次 0 error / 16 warning → 修正內容 9 處、修正工具誤報 7 處 → 0 error / 0 warning
- 檢查點 A：新增 datasets/、時效性規則；使用者改為補 PDF 取得圖片
- 檢查點 B：通過

## [2026-11-23] setup | 建立 cv_wiki_env 與 pdf_tools.py
- 虛擬環境 cv_wiki_env（PyMuPDF 2.1、pypdf 7.1.1），requirements.txt
- tools/pdf_tools.py：info / text / render / images
- schema 9.0：每份 PDF 先跑 info 再決定讀法
