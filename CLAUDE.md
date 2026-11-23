# CV Wiki — Schema 與工作規範

本檔是這個 LLM Wiki 的 **schema**。每次在這個專案工作前，LLM 都必須遵守本檔的規則。
規則需要調整時，由使用者與 LLM 討論後修改本檔，並在 `report/process-journal.md` 記錄修改原因。

---

## 1. 專案目的

- 建立一個以 **Computer Vision** 為核心、可長期累積與擴充的個人知識庫，服務使用者未來的研究所 CV 研究。
- Wiki 不是論文摘要的集合，而是**彼此連結的知識體系**：要說清楚技術的原理、動機、差異與演進關係。
- 以 Wiki 作為唯一知識來源，產出教學型 HTML 簡報。
- 工作原則：**先討論、後生成**。重要決定先與使用者確認，再動手寫入。

### 組織主軸：兩軸並行

- **縱軸：Backbone／模型演進**，例如 AlexNet → VGG → ResNet → ViT → ConvNeXt。
- **橫軸：任務**，包含 Image Classification、Object Detection、Image Segmentation。
- **概念層**：放跨模型共用的概念，例如 convolution、residual connection、self-attention。
- 三者之間用交叉連結串起來，例如「ResNet 是 Faster R-CNN 的 backbone」要能從兩邊互相找到。

---

## 2. 目錄結構

```
cv_wiki_project/
├── CLAUDE.md              ← 本檔（schema）
├── raw/                   ← 原始資料，唯讀，由使用者放入
│   ├── papers/            ← 論文 PDF，命名：年份_簡稱.pdf
│   └── tutorials/         ← 教學資料（CS231n、D2L）
├── wiki/
│   ├── index.md           ← 總目錄（內容導向）
│   ├── log.md             ← 操作紀錄（時間導向，append-only）
│   ├── overview.md        ← 全局綜述：CV 的演進主線
│   ├── sources/           ← 每份來源一頁摘要
│   ├── models/            ← 縱軸：模型頁
│   ├── tasks/             ← 橫軸：任務頁
│   ├── concepts/          ← 概念頁
│   ├── datasets/          ← 資料集頁（CIFAR-10、ImageNet、COCO…）
│   └── comparisons/       ← 比較與綜合分析（包含 query 產出的好答案）
├── tools/                 ← lint 與關聯圖腳本（Python，只用標準函式庫）
│   └── out/               ← 腳本產出（graph.html、lint 報告）
├── slides/                ← 產出的 HTML 簡報
└── report/
    └── process-journal.md ← 作業過程紀錄：問題、錯誤、修正、反思
```

---

## 3. 角色分工與硬性規則

| 角色 | 負責 |
|---|---|
| 使用者 | 挑選與下載來源、在檢查點確認方向、閱讀與抽查、決定故事線 |
| LLM | 讀來源、撰寫與維護所有 Wiki 頁面、交叉連結、index/log、lint、簡報 |

**硬性規則：**

1. **`raw/` 唯讀。** LLM 不得修改、移動、刪除或新增 `raw/` 底下的任何檔案。
2. **LLM 不得自行下載來源。** 所有原始資料都由使用者下載後放入 `raw/`。需要新來源時，LLM 只能「建議」，不能自己去抓。
3. **簡報只從 `wiki/` 取材**，不直接讀 `raw/`。簡報發現錯誤時，要先回頭修正 Wiki，再重新生成簡報。
4. **不得編造。** 來源沒有寫的數字、實驗結果、作者觀點都不能寫。LLM 自己的綜合推論必須標成 `（綜合推論）`。
5. **未經使用者要求，不 push 到遠端。** 本地 commit 依第 10 節的規則進行。

---

## 4. 寫作規範

### 語言

- **中文說明，術語保留英文。**
- 術語第一次出現時寫成 `中文（English）`，例如「殘差連接（residual connection）」。之後可以只寫英文或只寫中文，但同一頁裡要一致。
- 模型名稱、資料集名稱、指標名稱一律保留原文：ResNet、ImageNet、mAP、IoU。
- 沒有通用中文譯名的術語，直接用英文，例如 backbone、patch embedding、anchor box。
- **有歧義的中文術語，每次出現都要附上英文**。目前的清單（lint 會檢查，清單在 `tools/lint.py` 的 `AMBIGUOUS_TERMS`）：
  - 「正規化」：可能指 regularization 或 normalization，要寫成 `正規化（normalization）` 或 `Regularization（正規化）`。
  - 全域 lint 發現新的歧義術語時，加進這份清單。

### 寫法

- 每頁都採用**「先直觀、後技術」**：先用一段沒有背景也看得懂的說明（可以用比喻），再寫技術細節。
- 重點在 **為什麼**：動機、要解決的問題、與前一代比較改進了什麼。
- 避免逐段翻譯論文；要整理、重組、建立關聯。
- 數學式用 `$…$`（行內）和 `$$…$$`（獨立區塊），GitHub 和 VS Code 預覽都能渲染。不要用 `\( \)`。
- 數學式或內文中，避免用方括號括住以英文字母開頭的內容（例如寫成 `D × 1`，不要寫成 `[D x 1]`），以免被 lint 誤認為引用。

### 檔名與連結

- 檔名一律用英文小寫 kebab-case：`models/resnet.md`、`concepts/residual-connection.md`。
- source 頁檔名與 raw 對應：`sources/2015_resnet.md`。
- 連結一律用**標準 Markdown 相對連結**：`[ResNet](../models/resnet.md)`。不使用 `[[wikilink]]`。
- 提到 Wiki 中已存在頁面的概念或模型時，**該頁第一次提到就要加連結**。

---

## 5. YAML Frontmatter

每個 Wiki 頁面（`index.md`、`log.md` 除外）頂端都必須有 frontmatter。

### 共用欄位（必填）

```yaml
---
title: ResNet
type: model            # model | task | concept | dataset | source | comparison | overview
aliases: [Residual Network, 殘差網路]
tags: [cnn, backbone]
sources: [ResNet, CS231n]      # 本頁引用到的 cite key
related:                       # 本頁連到的主要相關頁（路徑相對於 wiki/）
  - concepts/residual-connection.md
  - models/vgg.md
created: 2026-11-22
updated: 2026-11-22
---
```

**frontmatter 也受「不得編造」約束**：`aliases` 只能放來源中出現過的名稱，或是術語的中文譯名；不能放 LLM 憑背景知識認為「也叫這個名字」的別名（例如來源沒有提到 weight decay，就不能把它列為 L2 regularization 的別名）。`first_introduced`、`year` 等欄位也一樣，來源沒寫就填 `unknown`。

### 依類型額外的欄位

| type | 額外欄位 |
|---|---|
| `source` | `cite_key`、`authors`、`year`、`venue`、`raw_path`（字串或清單：一個來源可以對應多個 raw 檔，例如同一門課的多篇筆記）、`url` |
| `model` | `year`、`family`（`cnn` / `transformer` / `hybrid`）、`tasks`（適用任務的清單） |
| `task` | `metrics`（評估指標的清單） |
| `concept` | `first_introduced`（首次提出的 cite key，若可確定） |
| `dataset` | `year`、`size`（例如 `60,000 images`）、`num_classes`、`tasks`。來源沒有提供的值寫 `unknown`，不得憑記憶補上 |

---

## 6. 引用規範（主張層級）

### Cite key

- cite key **不預先登記**，在 ingest 某份來源時才建立，寫在該 source 頁 frontmatter 的 `cite_key` 欄位。
- **唯一的權威清單**是所有 `sources/*.md` 的 `cite_key`；`index.md` 的 Sources 區會列出目前所有 key。lint 依此檢查引用。
- 命名規則：
  - 論文：常用的模型或方法名稱，去掉空白與連字號，例如 `ResNet`、`ViT`、`FasterRCNN`、`YOLOv1`。
  - 沒有明確模型名的論文：`第一作者姓氏+年份`，例如 `Lin2017`。
  - 教材或課程：簡稱，例如 `CS231n`、`D2L`。
  - 與現有 key 撞名時，加上年份或版本區分，例如 `YOLOv3`、`DETR2020`。
- source 頁檔名：`sources/<年份>_<slug>.md`；教材沒有單一年份時，用 `sources/<slug>.md`。

### 引用格式

在句子或段落後面加上：`[KEY 位置]`

- 章節：`[ResNet §3.1]`
- 頁碼：`[ViT p.5]`
- 表格／圖：`[ResNet Table 4]`、`[ViT Fig. 1]`
- 多個來源：`[ResNet §4.1; CS231n]`
- 教學網頁沒有章節編號時，寫小節標題：`[CS231n "Pooling Layer"]`
- 一個 cite key 對應多個 raw 檔時（例如同一門課的多篇筆記），位置前面要加上檔名（不含副檔名）：`[CS231n classification "Nearest Neighbor Classifier"]`
- 資訊來自圖片而不是文字時，在位置後面加「圖」：`[CS231n classification "Validation sets for Hyperparameter tuning" 圖]`

### 同一來源內部不一致

同一份來源前後說法不同（例如兩段給了不同的數字範圍）時，不使用第 7 節的來源差異標記，而是兩個說法都保留，並各自標出位置。

### 必須引用的主張

1. **所有數字**：準確率、error rate、參數量、層數、FLOPs、資料集大小。
2. **設計理由**：「作者這樣設計是因為…」。
3. **比較結論**：「A 比 B 好／快／省」。
4. **歷史主張**：「首次提出」「第一個做到」。

一般的解釋性、直觀性文字不必逐句引用。

### 引用的涵蓋範圍

- **段落**：引用涵蓋它所在的整個段落。
- **清單**：每個清單項目各自引用，不能只在引言那一行引用。
- **表格**：可以用**緊接在表格前一段或後一段**（中間最多一個空行、不隔標題）的一個引用涵蓋整張表，例如在表格下方寫「（表中數值依據 [KEY 位置]。）」。表格中各列數字的出處不同時，要逐列標出。

### 數字核對規則

- 數字要**照原文抄寫**，不得四捨五入或換算。如果需要換算（例如 error ↔ accuracy），要同時保留原始數字，並註明是換算的。
- 一定要寫清楚數字的條件：資料集、split、single-model 或 ensemble、哪一個模型變體。
  例如：「ResNet-152 single-model 在 ImageNet validation 上的 top-5 error 為 X% [ResNet Table 4]」。

### 時效性主張

「目前最好」「state-of-the-art」「最新」「最近的比賽」這類說法，只在來源撰寫的當時成立。寫入 Wiki 時必須加上時間背景，格式為 `（截至 <時間背景>）`：

```markdown
（截至 CS231n 筆記撰寫時）CIFAR-10 上 state-of-the-art 的 CNN 約達 95% [CS231n classification "Nearest Neighbor Classifier"]。
```

時間背景盡量具體（論文寫年份，例如 `截至 2015 年`）。來源沒有寫明日期時，就寫來源名稱，不要自己推測年份。lint 會檢查含 SOTA、最新等字眼的段落是否標了 `截至`。

### 綜合推論

LLM 跨來源整理出來的判斷，但沒有任何來源直接講過的，要標 `（綜合推論）`，並列出依據的來源：

```markdown
ViT 需要大量資料才能勝過 CNN，可以理解為它缺少 CNN 內建的 locality 假設（綜合推論，依據 [ViT §4.2; CS231n]）。
```

---

## 7. 來源差異（矛盾）標記

來源之間說法衝突時，**直接寫在相關頁面裡**，不另開頁面。固定格式：

```markdown
> ⚠️ **來源差異**：[ResNet §4.1] 指出…；[ViT §1] 則認為…
```

已經釐清的（例如確認只是實驗條件不同）改成：

```markdown
> ✅ **來源差異（已釐清）**：[A] 與 [B] 的數字不同，是因為…
```

lint 會統計還有幾個 `⚠️ **來源差異**` 沒有釐清。

---

## 8. 頁面模板

### 8.1 source 頁（`sources/`）

```markdown
# <論文或教材標題>

## 基本資訊
作者、年份、發表處、raw 路徑、原始連結

## 一段話摘要
用三到五句話說明：解決什麼問題、怎麼解、效果如何。

## 主要貢獻
- 條列，每點附上位置

## 關鍵結果
| 設定 | 指標 | 數值 | 位置 |

## 本來源影響的 Wiki 頁面
- [ResNet](../models/resnet.md)：新增…
- [Residual Connection](../concepts/residual-connection.md)：建立

## 討論紀錄
檢查點 A 時與使用者討論的重點、使用者特別想強調的部分
```

**多檔案來源的變體**（一個 cite key 對應多個 raw 檔，例如同一門課的多篇筆記）：頁首放共用的「基本資訊」和「各檔案 ingest 進度表」，之後**每個檔案一個大節**（`## <檔名>`），大節裡面依序放：一段話摘要、主要貢獻、關鍵結果、本檔影響的 Wiki 頁面、討論紀錄。這樣同一個檔案的資訊集中在一處，新增檔案時只要加一個大節。

### 8.2 model 頁（`models/`）

```markdown
# <模型名稱>

## 一句話說明
## 直觀理解           ← 沒有背景的人也看得懂
## 要解決的問題       ← 前一代的限制是什麼
## 核心方法
## 架構細節
## 實驗結果           ← 數字全部要引用
## 在演進中的位置
- 前身：…
- 後繼／受它影響的模型：…
- 被當作 backbone 用在：…（連到 tasks/ 與其他 models/）
## 限制與後續批評
## 相關概念
```

### 8.3 task 頁（`tasks/`）

```markdown
# <任務名稱>

## 一句話說明
## 直觀理解
## 輸入與輸出
## 評估指標           ← 連到 concepts/（例如 IoU、mAP）
## 方法演進           ← 依時間排列，連到 models/
## 方法比較           ← 表格
## 相關概念
```

### 8.4 concept 頁（`concepts/`）

```markdown
# <概念名稱>

## 一句話說明
## 直觀理解
## 技術細節           ← 可以有公式，但公式後面要用白話解釋
## 出現在哪些模型     ← 連到 models/，並說明各自怎麼用
## 常見誤解           ← 選填
```

### 8.5 comparison 頁（`comparisons/`）

```markdown
# <A vs B> 或 <主題分析>

## 要回答的問題
## 比較表
## 分析               ← 每個結論都要引用，或標（綜合推論）
## 結論
## 由哪次 query 產生  ← 日期與原始問題
```

### 8.6 dataset 頁（`datasets/`）

```markdown
# <資料集名稱>

## 一句話說明
## 規模與組成       ← 影像數、解析度、類別數、train/val/test 切分（數字要引用）
## 用途             ← 適用任務，連到 tasks/
## 在 Wiki 中的使用 ← 哪些模型或方法用它做實驗、得到什麼結果（連到 models/、concepts/）
## 限制與注意事項
```

### 8.7 overview（`overview.md`）

整個 CV 演進主線的綜述，作為 Wiki 的入口。每次 ingest 之後檢查是否需要更新。

---

## 9. Workflow

### 9.0 讀取 raw 檔的方式

- 讀 PDF 一律用 `tools/pdf_tools.py`（在 `cv_wiki_env` 中執行，見第 11 節）。**每份 PDF 先跑 `info`**，確認文字能不能抽取、圖是點陣圖還是向量圖，再決定讀法。
- **文字**：能抽取就用 `text`；抽不出來（例如「Microsoft: Print To PDF」會把文字轉成向量外框）時，改用同內容的 `.md`，或用 `render` 把頁面畫成圖片來讀。
- **圖片**：點陣圖用 `images` 抽出；**向量圖**（論文的架構圖、訓練曲線常是向量圖）用 `render` 把整頁畫成圖片來看。論文的關鍵圖都要實際看過。
- 同一份內容同時有 `.md` 和 `.pdf` 時：文字以 `.md` 為準，圖片從 `.pdf` 取得。兩個檔案都列進 `raw_path`。
- **網頁筆記的數學公式**：網頁用 MathJax 顯示公式，存成 PDF 後公式會變成圖形，抽出的文字裡**公式會整段消失**（看不出有缺漏）。因此有公式的網頁筆記，公式一律以 `.md` 的 LaTeX 原始碼為準；只有 PDF 時，要用 `render` 看頁面來讀公式。
- 網頁存成 PDF 的建議方式：瀏覽器列印時，目的地選「另存為 PDF」（文字可抽取），不要選「Microsoft Print to PDF」（文字會被轉成向量外框）。
- PDF 的文字抽不出來時，要在 source 頁的基本資訊註明。
- 圖片要實際看過才能引用；圖片裡的數字（例如曲線的數值範圍）只寫圖上直接看得到的，不推測實驗設定。
- `pdf_tools.py` 的輸出放在專案外的暫存目錄，不放進 `wiki/` 或 `raw/`。
- **不把來源的圖片複製到 `wiki/`**（版權考量）。需要時用文字描述圖片的內容；簡報需要示意圖時，用 SVG 自己重新繪製。

### 9.1 Ingest Loop（每份來源一次，逐篇進行）

```
① 讀取來源，並讀 index.md 與相關的既有頁面
② 影響評估，並向使用者報告：
   - 重點摘要、建議的 cite key
   - 這份來源與既有 Wiki 的關係（見 9.2）
   - 預計新增的頁面、預計修改的頁面（以及要改什麼）
◆ 檢查點 A：使用者確認或調整重點 → 不同意就回到 ②
③ 寫入／更新頁面（source 頁、models/tasks/concepts 頁、交叉連結、overview）
④ 數字與主張核對：每個有引用的數字，回到原文逐一比對
⑤ 執行 python tools/lint.py → 有錯誤就回到 ③
◆ 檢查點 B：使用者瀏覽更新的頁面 → 有問題就回到 ③
⑥ 更新 index.md、log.md → git commit
```

規則：
- **一次只 ingest 一份來源**，前一份完成 ⑥ 之後才開始下一份。
- 步驟 ② 必須列出「預計修改的頁面清單」，讓使用者在寫入前就看到影響範圍。
- 步驟 ④ 不能省略。數字核對要在寫入當下完成，不能等到做簡報時才檢查。
- 每次 ingest 過程中遇到的錯誤或流程問題，都要記到 `report/process-journal.md`。

### 9.2 影響評估（每份新來源都要做）

**不預設 ingest 順序，也不預測使用者之後會加入哪些來源。** Wiki 的結構隨著實際加入的來源演化。
每加入一份新來源，都要以「目前的 Wiki」為基準重新判斷，步驟 ② 至少要回答：

1. **新增**：這份來源帶來哪些 Wiki 還沒有的模型、任務、概念？要開新頁，還是併入既有頁？
2. **補充**：哪些既有頁面可以因此加深（例如新的實驗數據、新的解釋角度、新的演進關係）？
3. **修正與矛盾**：是否有既有說法被這份來源推翻、修正或質疑？如果有，依第 7 節標記來源差異，並列出要改的頁面。
4. **關聯**：要在哪些既有頁面加上指向新內容的連結（特別是「前身／後繼」「被當作 backbone」這類跨軸關係）？
5. **結構**：這份來源是否超出目前的分類（例如 3D vision、video、generative model）？
   - 能放進現有的 `models/`、`tasks/`、`concepts/` 就沿用。
   - 放不進去時，提出新增目錄或頁面類型的建議，**經使用者同意後**修改本 schema，並在 `process-journal.md` 記錄。
6. **overview**：演進主線是否需要改寫。

其他原則：
- 新來源提到某個 Wiki 還沒有頁面的基礎概念時，可以依這份來源的內容先建立該頁，但只寫來源有支持的部分；之後的來源再補充。
- 新來源的內容與既有頁面重複時，優先**整合進既有頁面**，而不是另開一頁。
- 來源加入的順序不影響最終結果：後加入的較早期論文，同樣要回頭補上它與後繼模型的關聯。

### 9.3 全域 Lint（每完成 3 份 ingest 一次，全部完成後再一次）

先執行 `python tools/lint.py` 和 `python tools/review.py`。review.py 不判斷對錯，而是整理出需要人工判斷的線索（跨頁數字、未連結的提及、候選新頁面、數學符號、待重新檢視的推論與前瞻性用語），輸出到 `tools/out/review-report.md`。

接著 LLM 依照報告和以下項目人工審查：
- 跨頁面的矛盾或說法不一致
- 重複的內容（應該合併，或改成連結）
- 被新來源推翻或修正的舊說法
- 已經被提到很多次、卻還沒有獨立頁面的概念
- overview 是否反映目前所有內容
- **用語衝突**：同一個中文詞被用來指不同的概念（例如「正規化」）。發現時加進 lint 的 `AMBIGUOUS_TERMS`
- **過度概括**：Wiki 的說法是否比來源講的範圍更廣（例如來源說「神經網路和 CNN」，Wiki 寫成「所有模型」）
- **逐次累加造成的結構問題**：例如小節標題的順序、早期寫的「下一步」已經不是下一步

審查結果**先向使用者報告，確認後才修改**。結果記入 `log.md`；發現的流程問題記入 `process-journal.md`。

### 9.4 Query

1. 先讀 `index.md` 找到相關頁面，再深入閱讀。
2. 回答時附上引用（Wiki 頁面連結 + 原始 cite key）。
3. 有價值的答案（比較、分析、新發現的關聯），經使用者同意後存成 `comparisons/` 頁，並更新 index 與 log。

### 9.5 簡報生成

```
① 選故事：等 Wiki 建完，比較各條主線的內容厚度，和使用者討論決定
② 從 Wiki 擷取大綱：每張投影片標明取材自哪幾頁
◆ 檢查點 C：使用者審查大綱 → 不 OK 就回到 ②
③ 生成 HTML
④ 事實回溯檢查 + 在瀏覽器實際開啟檢查
   → 簡報本身的問題：回到 ③
   → Wiki 本身的錯誤：先修 Wiki（走 Ingest 的 ③～⑥），再回到 ②
⑤ 定稿 → git commit
```

---

## 10. 簡報規格

- **單一、自足的 HTML 檔**：CSS、JS、SVG 全部內嵌，不載入任何外部資源（CDN、字型、圖片連結），可以完全離線開啟。
- 檔名：`slides/<YYYY-MM-DD>_<story-slug>.html`。
- 一份簡報只講**一個故事**；不限頁數，以完整表達重點為準。
- 寫法：**初學者看得懂，但不刪減技術重點**。每個概念先給直觀說明或比喻，再給技術細節。
- 功能：鍵盤左右鍵翻頁、頁碼、進度條；示意圖用內嵌 SVG（例如 residual block、patch embedding）。
- **可追溯**：每張投影片的 HTML 裡要加註解，標明取材自哪些頁面：
  `<!-- wiki: models/resnet.md, concepts/residual-connection.md -->`
- 簡報中的數字必須與 Wiki 一致；最後一頁列出參考來源。

---

## 11. 工具規格

`lint.py`、`graph.py` 只用 Python 標準函式庫，共用的解析邏輯（frontmatter、連結、引用）放在 `tools/wikilib.py`。
`pdf_tools.py`（ingest 時讀 PDF 用）需要 PyMuPDF，在專案根目錄的虛擬環境 `cv_wiki_env` 中執行：`cv_wiki_env/Scripts/python tools/pdf_tools.py <info|text|render|images> …`。環境依 `requirements.txt` 建立，`cv_wiki_env/` 不納入 git。
兩支都支援 `--root <dir>`，可以對測試用的假 Wiki 執行。**修改 lint 規則後，要先用一組故意放了錯誤的假 Wiki 測試，確認錯誤都抓得到、沒有誤報，才能用在真正的 Wiki 上。**

### `tools/lint.py`

執行：`python tools/lint.py`。輸出到終端機，並寫入 `tools/out/lint-report.md`。有 error 時 exit code 不為 0。

| 檢查項目 | 等級 |
|---|---|
| 斷掉的相對連結 | error |
| frontmatter 缺少必填欄位或格式錯誤 | error |
| 引用了不存在的 cite key（不在任何 source 頁的 `cite_key` 中） | error |
| 兩個 source 頁使用相同的 cite key | error |
| `sources` 欄位與內文實際引用的 key 不一致 | warning |
| 孤兒頁（沒有任何頁面連到它） | warning |
| 頁面沒有列在 `index.md` | warning |
| 包含數字（%、小數、M／B 參數量等）但同一段沒有引用 | warning |
| 含時效性字眼（SOTA、state-of-the-art、最新、recent…）但同一段沒有 `截至` | warning |
| `raw/` 中有檔案但沒有對應的 source 頁 | info |
| 有歧義的中文術語（`AMBIGUOUS_TERMS`，例如「正規化」）沒有附上英文 | warning |
| 未釐清的 `⚠️ **來源差異**` 數量 | info |

### `tools/review.py`

執行：`python tools/review.py`。全域 lint 時使用，輸出到終端機和 `tools/out/review-report.md`。不判斷對錯，只整理線索：

1. 跨頁數字：同一個數字出現在哪些非 source 頁面
2. 未連結的提及：A 頁提到 B 頁的標題或英文別名，卻沒有連到 B 頁（會先移除引用標記，避免把引用中的檔名當成提及）
3. 候選新頁面：在 ≥3 頁被粗體強調、卻不是任何頁面標題或別名的英文術語
4. 數學符號：各頁使用的希臘字母
5. 待重新檢視：所有（綜合推論）和前瞻性用語（待補、下一步…）

### `tools/graph.py`

執行：`python tools/graph.py`。產出 `tools/out/graph.html`。
- 自足的單一 HTML 檔，不使用外部函式庫，可以離線開啟。
- 節點：每個 Wiki 頁面，依 `type` 上色；邊：頁面之間的連結。
- 互動：可以拖曳和縮放；點節點會顯示標題、類型、連入與連出的頁面，並高亮相鄰節點；可以依類型篩選。

---

## 12. index.md 與 log.md

### index.md

依類型分區（Overview / Models / Tasks / Concepts / Comparisons / Sources），每頁一行：

```markdown
- [ResNet](models/resnet.md) — 用 residual connection 解決深層網路退化問題（sources: 2）
```

每次 ingest 或新增頁面時都要更新。

### log.md（append-only）

每筆用固定的前綴，方便 grep：

```markdown
## [2026-11-22] ingest | ResNet
- 新增：models/resnet.md, concepts/residual-connection.md
- 更新：models/vgg.md, overview.md
- lint：0 error, 2 warning（已處理）
```

類型：`setup` / `ingest` / `lint` / `query` / `slides` / `schema`。

---

## 13. 作業過程紀錄（`report/process-journal.md`）

用來回答作業的第 6、7 點：實際流程中遇到的問題、錯誤、修改方式，以及對 workflow 的反思。

每筆格式：

```markdown
## [2026-11-22] <節點，例如 Ingest-③ 寫入> | <一句話描述問題>
- 現象：發生了什麼
- 原因：為什麼發生
- 修正：怎麼修
- 是否修改 workflow／schema：是或否；是的話改了什麼
```

遇到以下情況時**必須**記錄：lint 抓到的錯誤、檢查點 A／B／C 使用者提出的修正、數字核對發現的錯誤、修改 schema 或 workflow。

最終反思要統計：哪個節點最常出錯、哪些檢查可以提前、workflow 因此做了哪些修改。

---

## 14. Git 規範

- 每次 ingest 完成（步驟 ⑥）commit 一次；schema 修改、工具修改、簡報定稿也各自 commit。
- commit message 格式：`<type>: <描述>`，例如 `ingest: ResNet`、`schema: 調整引用格式`、`tools: lint 新增數字檢查`、`slides: CNN 到 ViT 初版`。
- 只有使用者要求時才 push。
- **`raw/` 不納入版本控制**（已加入 `.gitignore`，原因是版權與檔案大小）。來源的出處（標題、作者、連結）記在 source 頁，讓別人能自行取得原檔。
