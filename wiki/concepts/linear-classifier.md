---
title: Linear Classifier
type: concept
first_introduced: unknown
aliases: [線性分類器, score function, 分數函數, parametric approach, template matching, bias trick]
tags: [classifier, parametric, foundation]
sources: [CS231n]
related:
  - concepts/loss-function.md
  - concepts/softmax-cross-entropy.md
  - concepts/regularization.md
  - concepts/k-nearest-neighbor.md
  - tasks/image-classification.md
  - datasets/cifar-10.md
  - concepts/optimization.md
  - concepts/gradient-descent.md
created: 2026-11-23
updated: 2026-11-23
---

# Linear Classifier（線性分類器）

## 一句話說明

把影像的所有像素乘上一組**學出來的權重**再加總，得到每個類別的分數，分數最高的類別就是答案：$f(x_i, W, b) = W x_i + b$ [CS231n linear-classify "Parameterized mapping from images to label scores"]。

## 直觀理解

[kNN](k-nearest-neighbor.md) 的做法是把所有訓練圖片都記下來，每次預測都要從頭比對一遍。Linear classifier 換了一個思路：**從訓練資料中提煉出一小組參數，之後就只靠這組參數做判斷**。

可以想成：kNN 是帶著整本圖鑑去考試；linear classifier 則是讀完圖鑑後，只帶一張「重點筆記」（權重 W）進考場。

這是整個深度學習框架的起點。CS231n 把方法拆成兩個部分 [CS231n linear-classify "Linear Classification"]：

1. **Score function（分數函數）**：把原始像素映射成每個類別的分數。
2. **Loss function（損失函數）**：衡量預測的分數和真實標籤有多吻合，詳見 [Loss Function](loss-function.md)。

接著把學習變成一個最佳化問題：**調整 score function 的參數，讓 loss 最小** [CS231n linear-classify "Linear Classification"]。

> CS231n 的伏筆：Convolutional Neural Networks 從像素映射到分數的方式，和這裡**完全一樣**，只是映射 $f$ 更複雜、參數更多 [CS231n linear-classify "Parameterized mapping from images to label scores"]。

## 技術細節

### Score function

設訓練資料為影像 $x_i \in R^D$ 和標籤 $y_i \in \{1 \dots K\}$，共 N 筆。目標是定義 $f: R^D \mapsto R^K$，把像素映射到 K 個類別的分數 [CS231n linear-classify "Parameterized mapping from images to label scores"]。

$$
f(x_i, W, b) = W x_i + b
$$

| 符號 | 形狀 | 意義 | CIFAR-10 的例子 |
|---|---|---|---|
| $x_i$ | D × 1 | 影像攤平成一行 | 3072 × 1（32 × 32 × 3）|
| $W$ | K × D | **weights（權重）** | 10 × 3072 |
| $b$ | K × 1 | **bias vector（偏差向量）**：影響輸出分數，但不和資料 $x_i$ 互動 | 10 × 1 |

（以上依據 [CS231n linear-classify "Parameterized mapping from images to label scores"]。CIFAR-10 的 N = 50,000、D = 3072、K = 10，同樣出自這一節。）

幾個重點 [CS231n linear-classify "Parameterized mapping from images to label scores"]：

- 一次矩陣乘法 $W x_i$，其實是**同時跑 10 個獨立的分類器**，每個類別一個，W 的每一列就是一個分類器。
- 資料 $(x_i, y_i)$ 是給定、不能改的；我們能調整的是參數 W 和 b。目標是讓正確類別的分數高於錯誤類別。
- 學完之後就可以**丟掉整個 training set**，只保留參數。
- 分類一張新圖只需要一次矩陣乘法加一次加法，比跟所有訓練圖片逐一比對快得多。

### 範例：一張貓的圖片怎麼變成分數

筆記用了一個簡化的例子：影像只有 4 個灰階像素，共 3 個類別（cat、dog、ship）[CS231n linear-classify "Interpreting a linear classifier" 圖]。

| | 像素 1 | 像素 2 | 像素 3 | 像素 4 | b | 分數 |
|---|---|---|---|---|---|---|
| $x_i$（像素值） | 56 | 231 | 24 | 2 | | |
| cat 那一列 W | 0.2 | −0.5 | 0.1 | 2.0 | 1.1 | **−96.8** |
| dog 那一列 W | 1.5 | 1.3 | 2.1 | 0.0 | 3.2 | **437.9** |
| ship 那一列 W | 0 | 0.25 | 0.2 | −0.3 | −1.2 | **61.95** |

（表中數值都來自 [CS231n linear-classify "Interpreting a linear classifier" 圖]。內文也寫了 cat −96.8、dog 437.9、ship 61.95 [CS231n linear-classify "Loss function"]。）

這組 W 很差：明明是貓，cat 的分數卻最低，模型「深信」這是一隻狗 [CS231n linear-classify "Interpreting a linear classifier"]。要衡量「有多差」，就需要 [loss function](loss-function.md)。

> **圖中數字的驗算**：用圖上的 W、x、b 實際計算，cat = 0.2×56 − 0.5×231 + 0.1×24 + 2.0×2 + 1.1 = −96.8，dog = 1.5×56 + 1.3×231 + 2.1×24 + 0.0×2 + 3.2 = 437.9，兩者都和圖相符。但 ship = 0×56 + 0.25×231 + 0.2×24 − 0.3×2 − 1.2 = **60.75**，和圖上與內文的 61.95 不同。差額正好是 ship 的 bias −1.2，看起來是原圖計算 ship 分數時漏加了 bias（綜合推論，依據 [CS231n linear-classify "Interpreting a linear classifier" 圖]）。這不影響本節的重點：cat 的分數仍然最低。

### 三種理解方式

**1. 加權總和：喜歡或討厭某些位置的某些顏色**

每個類別的分數，是所有像素在 3 個顏色通道上的加權總和。依照權重的正負，分類器可以「喜歡」或「討厭」某些位置的某些顏色。例如 ship 類別可能喜歡圖片兩側有大量藍色（像是水），所以藍色通道的權重偏正，紅色和綠色通道的權重偏負 [CS231n linear-classify "Interpreting a linear classifier"]。

**2. 幾何：高維空間中的分界線**

把每張影像看成高維空間中的一個點，例如 CIFAR-10 的每張圖都是 3072 維空間中的一點 [CS231n linear-classify "Interpreting a linear classifier"]。每個類別的分數是這個空間上的線性函數：

- W 的每一列對應一條分界線（高維空間中是超平面）。線上的點，該類別的分數是 0；沿著箭頭方向，分數線性增加 [CS231n linear-classify "Interpreting a linear classifier" 圖]。
- 改變 W 的某一列，那條線會**旋轉**；bias b 則讓線**平移**。如果沒有 bias，所有線都被迫通過原點，因為 $x_i = 0$ 時分數一定是 0 [CS231n linear-classify "Interpreting a linear classifier"]。

**3. Template matching（模板比對）**

W 的每一列可以看成一個類別的 **template（模板）**，也叫 prototype。把影像和每個模板做 **inner product（內積）**，最吻合的那個就是答案。這些模板是學出來的 [CS231n linear-classify "Interpreting a linear classifier"]。

換個角度看，這其實**還是 Nearest Neighbor**，只是 [CS231n linear-classify "Interpreting a linear classifier"]：
- 每個類別只保留**一張**圖，而不是幾千張訓練圖片。這張圖是學出來的，不一定是訓練集裡的某張圖。
- 距離改用（負的）內積，而不是 L1 或 L2。

在 CIFAR-10 上學完之後，把 10 個模板畫出來，可以看到 ship 模板有大量藍色，plane 模板也偏藍，frog 模板偏黃綠色 [CS231n linear-classify "Interpreting a linear classifier" 圖]。

## 極限：一個類別只能有一個模板

模板的視覺化也暴露了 linear classifier 的根本限制 [CS231n linear-classify "Interpreting a linear classifier"]：

- **兩個頭的馬**：資料中有朝左和朝右的馬，linear classifier 只能把兩種**模式（mode）**混成一個模板，所以 horse 模板看起來像有兩個頭。
- **紅色的車**：car 模板要辨認各種角度、各種顏色的車，最後變成紅色。這暗示 CIFAR-10 裡紅色的車比其他顏色多。
- 筆記的結論：linear classifier **太弱**，沒辦法好好處理不同顏色的車。

CS231n 預告的解法是神經網路：hidden layer 的中間神經元可以分別偵測特定類型的車，例如朝左的綠車、朝前的藍車，下一層再把這些偵測器的結果加權組合，得到更準的 car 分數 [CS231n linear-classify "Interpreting a linear classifier"]。

## 實作技巧

### Bias trick

同時追蹤 W 和 b 兩組參數很麻煩。常見的技巧是在 $x_i$ 後面**多加一個永遠等於 1 的維度**，把 b 併進 W 成為最後一行，score function 就簡化成 $f(x_i, W) = W x_i$ [CS231n linear-classify "Interpreting a linear classifier"]。

以 CIFAR-10 為例，$x_i$ 從 3072 × 1 變成 3073 × 1，W 從 10 × 3072 變成 10 × 3073 [CS231n linear-classify "Interpreting a linear classifier"]。

### 影像前處理：Mean subtraction（減去平均）

前面的例子用的是原始像素值，範圍是 0～255。但在機器學習中，通常都會先對輸入特徵做正規化（normalization）；對影像來說，每個像素就是一個特徵 [CS231n linear-classify "Interpreting a linear classifier"]：

- **Centering（中心化）**：計算所有訓練影像的 **mean image（平均影像）**，再從每張影像減掉它，像素範圍大約變成 −127～127 [CS231n linear-classify "Interpreting a linear classifier"]。
- **Scaling（縮放）**：再把每個特徵縮放到 −1～1 [CS231n linear-classify "Interpreting a linear classifier"]。
- 其中 zero mean centering 可以說比較重要，但原因要等學到 gradient descent 的動態之後才能解釋 [CS231n linear-classify "Interpreting a linear classifier"]。

## 怎麼找到好的 W

定義好 score function 和 loss 之後，還需要**最佳化**，也就是找出讓 loss 最小的 W。詳見 [Optimization](optimization.md) 和 [Gradient Descent](gradient-descent.md)。

最佳化方法的好壞影響很大。在 CIFAR-10 上，用 SVM loss 訓練 linear classifier（筆記的範例中，W 是 10 × 3073）：

| 最佳化方法 | loss 評估次數 | test accuracy |
|---|---|---|
| Random search | 1000 | 約 15.5% |
| Random local search | 1000 | 21.4% |

（表中數值依據 [CS231n optimization-1 "Strategy #1: A first very bad idea solution: Random search"; CS231n optimization-1 "Strategy #2: Random Local Search"]。）

這兩個數字只反映**很差的最佳化方法**，不是 linear classifier 的能力上限。用 gradient descent 訓練的結果，目前收錄的來源沒有提供。

## Parametric 與 Non-parametric

| | kNN（non-parametric） | Linear classifier（parametric） |
|---|---|---|
| 訓練 | 只把資料存起來 | 學出 W、b |
| 預測時需要什麼 | 整個 training set | 只要參數 |
| 預測成本 | 跟所有訓練圖片比對 | 一次矩陣乘法 |
| 「模板」數量 | 每張訓練圖片都是一個模板 | 每個類別一個學出來的模板 |

（依據 [CS231n linear-classify "Summary"; CS231n linear-classify "Linear Classification"]。「parametric approach」是原文用語；「non-parametric」是相對的稱呼，原文沒有用這個詞。）

## 出現在哪些地方

- [Image Classification](../tasks/image-classification.md)：kNN 之後的第二個方法
- [Loss Function](loss-function.md)、[Softmax／Cross-Entropy](softmax-cross-entropy.md)：用來評估和訓練 linear classifier
- [Regularization](regularization.md)：限制 W 的大小
- [CIFAR-10](../datasets/cifar-10.md)：筆記中的例子
- 之後的神經網路和 CNN：沿用同樣的「score function + loss function」框架 [CS231n linear-classify "Parameterized mapping from images to label scores"]
