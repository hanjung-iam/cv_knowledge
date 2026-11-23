# 簡報大綱：電腦怎麼學會看圖（上）— 從比對像素到自己調整參數

- 狀態：第二版（2026-11-23）。依使用者對第一版（`pixels-to-cnn`，36 張）的回饋重新製作；HTML 已生成，等待使用者確認定稿
- 依據：schema 9.5（簡報只從 `wiki/` 取材）、第 10 節（簡報規格）
- 對象：沒有背景的人；**沒有講稿**，所以投影片本身要把話說完整

## 第二版的修改（依使用者回饋）

| 回饋 | 修改 |
|---|---|
| kNN 一律寫成 KNN | 簡報與 Wiki 全部改成 KNN（引用中的 CS231n 原文小節標題除外） |
| 沒有說明 L1、L2 是什麼 | KNN 站新增 L1、L2 距離各一頁（定義、公式逐項解釋、示意計算、兩者差別）；regularization 頁說明 L2 penalty 的算法 |
| 「每類只保留一張圖的 kNN」看不懂 | 模板比對獨立一頁：先定義內積、模板，再用表格逐項對照 KNN 與 linear classifier |
| SVM 算式要解釋清楚 | 拆成「定義（公式逐項解釋）」和「逐步計算（為什麼是 0 + 8）」兩頁，另一頁說明 Δ 與 hinge loss |
| 每一站要有轉場頁說明原因 | 每一站開頭一張轉場頁：上一站留下的問題 → 這一站的想法 → 要回答的問題 → 會出現的名詞 |
| 「機率要加引號」太突然；要說明為什麼用 softmax | 新增「為什麼需要 Softmax」一頁（SVM 分數難解讀、好處）；「機率」加引號移到 regularization 之後獨立一頁，說明原因 |
| 整體太概略、越後面越抽象 | 專有名詞第一次出現都附定義框；計算全部逐步展開；每站結尾有小結；最後加回顧表與名詞索引 |
| 第 5、6 站先移除 | 神經網路、CNN、ILSVRC、VGGNet 移到下一份簡報（見文末附錄） |

## 故事線

每一站都回答前一站留下的問題：

| 站 | 要解決的問題 | 這一站的答案 | 留下的問題 |
|---|---|---|---|
| 0 影像分類 | 電腦只看到數字，規則寫不出來 | data-driven：從有標籤的例子學 | 最直接的學法是什麼？ |
| 1 KNN | 怎麼從例子分類 | 找最像的 k 張投票（L1／L2 距離） | 慢、要存全部資料、像素距離沒有語意 |
| 2 Linear classifier | 不想存全部資料、逐張比對 | 學出參數 W、b：$f = Wx + b$ | W 怎麼來？怎麼知道好不好？ |
| 3 Loss | 怎麼衡量 W 的好壞 | SVM／Softmax loss + λR(W) | 怎麼找到 loss 最小的 W？ |
| 4 Optimization | 怎麼找到好的 W | gradient descent；用 backprop 算 gradient | 一類一個模板，表達能力不足 → 下集 |

---

## 序章（1–8）

| # | 標題 | 內容重點 | 取材 |
|---|---|---|---|
| 1 | 封面 | 上集／下集範圍 | `overview.md` |
| 2 | 今天的路線圖 | 0～4 站與下集；每站一句「要回答的問題」 | `overview.md` |
| 3 | 怎麼讀這份簡報 | 轉場頁、名詞定義框、「示意」標記、頁尾的 Wiki 來源 | — |
| 4 | **轉場：起點 影像分類** | 為什麼從分類開始（核心問題、可化約） | `tasks/image-classification.md`、`overview.md` |
| 5 | 電腦看到的是一堆數字 | 定義：影像分類、像素、顏色通道；297,600；輸出機率 | `tasks/image-classification.md` |
| 6 | 為什麼很難 | 7 種難點；定義 invariant | `tasks/image-classification.md` |
| 7 | Data-driven approach | 為什麼不寫規則；三步驟；定義 training set、test set、ground truth、accuracy | `tasks/image-classification.md` |
| 8 | CIFAR-10 | 規模；攤平成 3,072 維向量；參考線 10%、約 94% | `datasets/cifar-10.md` |

## 第一站 KNN（9–18）

| # | 標題 | 內容重點 | 取材 |
|---|---|---|---|
| 9 | **轉場：第一站 KNN** | 最直接的做法＝比對；CS231n 用它的原因 | `concepts/k-nearest-neighbor.md` |
| 10 | Nearest Neighbor | 訓練＝存起來；預測＝和每張比距離；定義距離 | `concepts/k-nearest-neighbor.md` |
| 11 | L1 距離 | 定義、公式逐項解釋、4 像素示意計算 | `concepts/k-nearest-neighbor.md` |
| 12 | L2 距離與兩者差別 | 定義、示意計算、可省略開根號、L2 對大差異更不寬容（示意對照） | `concepts/k-nearest-neighbor.md` |
| 13 | 從 NN 到 KNN | 定義 KNN、決策邊界；k 越大越平滑 | `concepts/k-nearest-neighbor.md` |
| 14 | 結果 | 10%、35.4%、38.6%、約 94% | `concepts/k-nearest-neighbor.md`、`datasets/cifar-10.md` |
| 15 | 像素距離 ≠ 長得像 | 人臉、t-SNE、馬頭與紅車；必須超越 raw pixel | `concepts/k-nearest-neighbor.md` |
| 16 | Hyperparameter 與 test set | 定義 hyperparameter、overfitting、generalization；期末考比喻 | `concepts/hyperparameter-tuning.md`、`concepts/overfitting.md` |
| 17 | Validation set 與 cross-validation | 49,000／1,000；候選 k；5-fold 圖解；k ≈ 7 | `concepts/hyperparameter-tuning.md` |
| 18 | 第一站小結 | 優缺點；取捨方向是反的 → 下一站 | `concepts/k-nearest-neighbor.md` |

## 第二站 Linear classifier（19–24）

| # | 標題 | 內容重點 | 取材 |
|---|---|---|---|
| 19 | **轉場：第二站 Linear classifier** | KNN 的三個問題 → parametric approach | `concepts/linear-classifier.md` |
| 20 | Score function | 定義 score function、參數、W、b；形狀；丟掉訓練資料 | `concepts/linear-classifier.md` |
| 21 | 一張貓怎麼變成分數 | 每一列＝一個類別；cat 分數逐項計算；ship 驗算註記 | `concepts/linear-classifier.md` |
| 22 | 角度 ① 加權總和、② 幾何 | 權重正負＝喜歡／討厭；分界線、旋轉、平移 | `concepts/linear-classifier.md` |
| 23 | 角度 ③ 模板比對 | 定義內積、模板；KNN 與 linear classifier 逐項對照 | `concepts/linear-classifier.md`、`concepts/k-nearest-neighbor.md` |
| 24 | 極限 | 兩個頭的馬、紅色的車；定義 mode | `concepts/linear-classifier.md` |

## 第三站 Loss（25–37）

| # | 標題 | 內容重點 | 取材 |
|---|---|---|---|
| 25 | **轉場：第三站 Loss** | W 很差但電腦不知道 → 把「多糟」變成數字 | `concepts/loss-function.md` |
| 26 | Loss 的結構 | 定義 loss function；$L = \frac{1}{N}\sum L_i + \lambda R(W)$ 逐項解釋 | `concepts/loss-function.md` |
| 27 | Multiclass SVM：定義 | 想法、margin、公式逐項解釋、白話 | `concepts/loss-function.md` |
| 28 | Multiclass SVM：逐步計算 | (13, −7, 11)、Δ = 10 → 0 + 8 = 8 | `concepts/loss-function.md` |
| 29 | SVM 的兩個細節 | hinge loss、squared hinge；Δ 直接設 1.0 的原因 | `concepts/loss-function.md` |
| 30 | 為什麼需要 Softmax | SVM 分數難解讀；好處：可解讀、永遠不滿足 | `concepts/softmax-cross-entropy.md`、`concepts/loss-function.md` |
| 31 | Softmax 怎麼算 | 公式；取指數、正規化（normalize）；用語提醒 | `concepts/softmax-cross-entropy.md` |
| 32 | Cross-entropy loss | $-\log p$；曲線；1.04；名稱 | `concepts/softmax-cross-entropy.md` |
| 33 | SVM vs Softmax | 對照表；局部性例子；1.58 與 1.04 不能比 | `concepts/loss-function.md` |
| 34 | W 不只一組 | 乘以 2 仍全對（15 → 30）；定義 regularization | `concepts/regularization.md` |
| 35 | L2 regularization | 定義與算法；w₁、w₂ 逐步計算；λ；完整 loss | `concepts/regularization.md` |
| 36 | 「機率」為什麼加引號 | 權重減半的例子；λ 的影響；看成信心程度 | `concepts/softmax-cross-entropy.md` |
| 37 | 第三站小結 | 完整 loss 的計算流程圖 | `concepts/loss-function.md`、`concepts/regularization.md` |

## 第四站 Optimization（38–52）

| # | 標題 | 內容重點 | 取材 |
|---|---|---|---|
| 38 | **轉場：第四站 Optimization** | 30,730 個數字無法逐一試 → 逐步改進 | `concepts/optimization.md`、`datasets/cifar-10.md` |
| 39 | 蒙眼下山 | 比喻對照；loss 地形；convex 與 non-convex | `concepts/optimization.md` |
| 40 | 前兩種策略 | random search 約 15.5%、random local search 21.4%；iterative refinement | `concepts/optimization.md` |
| 41 | Gradient | 斜率公式逐項解釋；偏導數；最陡上升方向 | `concepts/gradient-descent.md` |
| 42 | Gradient descent | 定義；程式迴圈；訓練的資訊流 | `concepts/gradient-descent.md` |
| 43 | 怎麼算 gradient | numerical vs analytic；30,731 次；gradient check | `concepts/gradient-descent.md` |
| 44 | Learning rate | 定義；step size 實驗；太大太小 | `concepts/gradient-descent.md` |
| 45 | Mini-batch | 120 萬取 256；思想實驗；SGD；batch size | `concepts/gradient-descent.md`、`datasets/ilsvrc.md` |
| 46 | **轉場：第四站下半 Backpropagation** | numerical 太慢、analytic 易錯 → 拆成小步驟 | `concepts/backpropagation.md`、`concepts/gradient-descent.md` |
| 47 | Gradient＝敏感度 | $f = xy$ 例子；三種基本運算的 local gradient | `concepts/backpropagation.md` |
| 48 | Chain rule 逐步計算 | $(x + y)z$：forward、backward 四步 | `concepts/backpropagation.md` |
| 49 | 為什麼是「局部」的 | gate 互相傳話；實作的兩個注意事項 | `concepts/backpropagation.md` |
| 50 | 三種 gate 的模式 | add、max、mul | `concepts/backpropagation.md` |
| 51 | 資料前處理 | mul gate → 尺度影響 gradient；centering、scaling | `concepts/data-preprocessing.md`、`concepts/backpropagation.md` |
| 52 | 第四站小結：學習的迴圈 | score → loss → backprop → update | `concepts/gradient-descent.md`、`concepts/backpropagation.md` |

## 終點（53–57）

| # | 標題 | 內容重點 | 取材 |
|---|---|---|---|
| 53 | 回顧 | 故事線表格 | `overview.md` |
| 54 | 下集預告 | 一類一個模板、必須超越 raw pixel；只換 score function | `overview.md`、`concepts/optimization.md`、`concepts/backpropagation.md` |
| 55 | 名詞索引（一） | 序章、KNN、Linear classifier | 各頁 |
| 56 | 名詞索引（二） | Loss、Optimization | 各頁 |
| 57 | 參考來源 | CS231n 4 篇筆記；Wiki 頁面清單 | `sources/cs231n.md` |

---

## 附錄：移到下一份簡報（神經網路與 CNN）的內容

第一版的以下投影片不放進本份，留給下一份簡報：
- 神經網路：疊起來的 linear classifier、activation function（ReLU vs sigmoid）、網路大小與 regularization（`concepts/neural-network.md`、`concepts/activation-function.md`、`concepts/overfitting.md`）
- CNN：為什麼一般神經網路不適合影像、conv layer、parameter sharing、pooling、層的排列、CNN 學到了什麼（`concepts/convolutional-neural-network.md`、`concepts/convolutional-layer.md`、`concepts/pooling-layer.md`）
- ILSVRC 時間軸、VGGNet（`datasets/ilsvrc.md`、`models/alexnet.md`、`models/vggnet.md`）
