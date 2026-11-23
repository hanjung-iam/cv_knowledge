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

## [2026-11-23] schema | 網頁筆記的公式以 md 為準
- linear-classify.pdf 測試：Chrome「另存為 PDF」文字可抽取，但 MathJax 公式在抽出的文字中消失
- 9.0 補充公式處理方式與建議的存檔方式

## [2026-11-23] ingest | CS231n — linear-classify
- 新增：concepts/linear-classifier.md, concepts/loss-function.md, concepts/softmax-cross-entropy.md, concepts/regularization.md
- 更新：tasks/image-classification.md, concepts/k-nearest-neighbor.md, concepts/hyperparameter-tuning.md, datasets/cifar-10.md, overview.md, sources/cs231n.md, index.md
- 數字核對：33 項對照原文全部吻合；驗算圖中數字，發現原文 ship score 61.95 應為 60.75（標綜合推論）
- 自查：移除 2 個來源沒有的 aliases
- lint：0 error / 9 warning → 補引用 1、改寫 1、新增表格引用規則並修改 lint（7）→ 0 / 0
- 檢查點 A：4 個概念頁；驗算結果標綜合推論；前處理放 linear-classifier
- 檢查點 B：通過

## [2026-11-23] schema | 公式標記、frontmatter 不得編造、引用涵蓋範圍
- 第 4 節：公式用 $…$；避免方括號括住英文開頭內容
- 第 5 節：aliases 等 frontmatter 欄位也須有來源支持
- 第 6 節：段落／清單／表格的引用涵蓋規則；lint 相應修改並以假 Wiki 測試

## [2026-11-23] ingest | CS231n — optimization-1
- 新增：concepts/optimization.md, concepts/gradient-descent.md, datasets/ilsvrc.md
- 更新：concepts/loss-function.md, concepts/regularization.md, concepts/hyperparameter-tuning.md, concepts/linear-classifier.md, tasks/image-classification.md, datasets/cifar-10.md, overview.md, sources/cs231n.md, index.md
- 數字核對：28 項對照原文全部吻合
- 自查：補 1 處評價性判斷的引用
- lint：第一輪即 0 error / 0 warning
- 檢查點 A：拆兩頁；Wiki 統一用 λ（註明 α）；ILSVRC 先建頁
- 檢查點 B：通過

## [2026-11-23] lint | 全域 Lint #1（3 份 ingest 之後）
- lint.py：0 / 0；新工具 review.py 列出跨頁數字、未連結的提及等線索
- 修正：「正規化」一律附英文（9 處）；過度概括 3 處；過時推論 1 處；表格條件 1 處；小節標題與連結；漏掉的連結 8 處
- 結構：sources/cs231n.md 改為依筆記分區
- 工具：lint 新增歧義術語檢查；新增 tools/review.py
- schema：第 4、8.1、9.3、11 節
- 暫不新增頁面：neural network／CNN（來源尚未介紹）、overfitting、資料前處理

## [2026-11-23] ingest | CS231n — optimization-2
- 新增：concepts/backpropagation.md, concepts/data-preprocessing.md（整合 3 篇筆記的前處理內容）
- 更新：concepts/gradient-descent.md, concepts/linear-classifier.md, concepts/k-nearest-neighbor.md, overview.md, sources/cs231n.md, index.md
- 數字核對：19 項吻合；引用的 9 個小節標題皆存在於原文；3 個電路圖驗算正確
- 自查：移除不當的 alias（sigmoid）
- lint：0 / 3（2 處「正規化」未附英文、1 處清單未引用）→ 0 / 0
- 檢查點 A：sigmoid 不獨立成頁；建立 data-preprocessing
- 檢查點 B：通過
