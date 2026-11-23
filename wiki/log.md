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

## [2026-11-23] ingest | CS231n — convolutional-networks
- 新增：concepts/convolutional-neural-network.md, concepts/convolutional-layer.md, concepts/pooling-layer.md, models/alexnet.md, models/vggnet.md
- 更新：datasets/ilsvrc.md（ImageNet 名稱、歷年成績）, tasks/image-classification.md（方法表加資料集與指標欄、第四步）, overview.md（第六站）, concepts/linear-classifier.md, concepts/backpropagation.md, concepts/hyperparameter-tuning.md, concepts/gradient-descent.md, concepts/regularization.md, datasets/cifar-10.md, sources/cs231n.md, index.md
- 數字核對：55 項吻合；引用的 12 個小節標題皆存在；驗算發現原文 VGG 記憶體總量（24M）與逐層加總（約 15.2M）不符、AlexNet 的一段描述與 VGGNet 吻合（皆標綜合推論）
- lint：0 / 3 → 0 / 0；review：補 8 處連結（1 處 kernel 為同形異義誤報）
- 檢查點 A：只為 AlexNet、VGGNet 建模型頁；ILSVRC 加 ImageNet aliases；使用者補下載 neural-networks-1
- 檢查點 B：通過

## [2026-11-23] schema | Ingest 步驟 ⑤ 加入 review.py
- 單次 ingest 也要跑 review.py 的「未連結的提及」，不只在全域 lint 時使用

## [2026-11-23] ingest | CS231n — neural-networks-1
- 新增：concepts/neural-network.md, concepts/activation-function.md, concepts/overfitting.md（整合 4 篇筆記）
- 更新：tasks/image-classification.md、overview.md（插入「神經網路」一步）, concepts/regularization.md（加回 weight decay）, concepts/data-preprocessing.md, concepts/backpropagation.md, concepts/linear-classifier.md, concepts/softmax-cross-entropy.md, concepts/hyperparameter-tuning.md, concepts/gradient-descent.md, models/alexnet.md, concepts/convolutional-neural-network.md, sources/cs231n.md, index.md
- 數字核對與引用標題核對：全部吻合；兩個網路的參數量驗算正確
- 修正 overview 中預測來源的句子（Vision Transformer）
- lint：0 / 1 → 0 / 0；review：補 9 處連結
- 檢查點 A：建立 overfitting 頁；ReLU 6 倍依圖說寫「和 tanh 相比」
- 檢查點 B：通過

## [2026-11-23] lint | 全域 Lint #2（6 份 ingest 之後）
- 工具：lint 新增「引用的小節標題」檢查（結果 0 個問題）與清單引用模式處理；皆以假 Wiki 測試
- schema：清單規則改為「引言行的引用涵蓋緊接的清單」（原本會產生 83 個 warning）
- 修正：overview 兩軸地圖補上神經網路；CNN 頁、data-preprocessing 頁的過時敘述；統一 neuron 用語
- 結果：lint 0 / 0；review 只剩 1 個已知誤報（kernel 同形異義）

## [2026-11-23] slides | 電腦怎麼學會看圖（上）：從比對像素到自己調整參數
- 產出：slides/2026-11-23_pixels-to-learning.html（57 張）與 .outline.md
- 第一版（從像素到 CNN，36 張）經使用者審查「太概略」，依 8 點回饋重做；神經網路與 CNN 兩站移到下一份簡報
- 用語：Wiki 中的 kNN 統一改為 KNN（11 頁）；引用的 CS231n 原文小節標題保留原樣
- 檢查：逐張截圖與版面檢查（修 7 處）、事實回溯（57 個 wiki 註解，0 個缺頁）、初學者角度重讀（補 8 個定義）
- lint：0 error, 0 warning

## [2026-11-23] schema | 簡報規格加入「沒有講稿」的寫法要求
- 第 10 節：名詞附定義、計算逐步展開、每站轉場頁、示意例子要標示
- 9.5：大綱要列出要定義的名詞與要展開的計算；④ 加入逐張截圖、版面檢查與初學者重讀
