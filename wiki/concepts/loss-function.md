---
title: Loss Function
type: concept
first_introduced: unknown
aliases: [損失函數, cost function, objective, hinge loss, Multiclass SVM loss, max-margin loss, data loss]
tags: [training, foundation]
sources: [CS231n]
related:
  - concepts/linear-classifier.md
  - concepts/softmax-cross-entropy.md
  - concepts/regularization.md
  - concepts/hyperparameter-tuning.md
created: 2026-11-23
updated: 2026-11-23
---

# Loss Function（損失函數）

## 一句話說明

一個把「模型預測得有多差」變成**一個數字**的函數。預測越差，loss 越高；預測越好，loss 越低 [CS231n linear-classify "Loss function"]。

## 直觀理解

[Linear classifier](linear-classifier.md) 的範例裡，模型看到一張貓，卻給 cat −96.8、dog 437.9、ship 61.95 [CS231n linear-classify "Loss function"]。我們知道這很糟，但要讓電腦**自動改進**，就必須先把「很糟」量化成一個數字。Loss function 就是這把尺。

loss 也叫 **cost function** 或 **objective** [CS231n linear-classify "Loss function"]。CS231n 的說法是：**loss 量化了我們對 training set 上預測結果的不滿意程度** [CS231n linear-classify "Multiclass Support Vector Machine loss"]。

一旦有了這個數字，「學習」就變成「找讓 loss 最小的參數」，也就是最佳化問題 [CS231n linear-classify "Multiclass Support Vector Machine loss"]。

## 技術細節

### 完整 loss 的結構

$$
L = \underbrace{\frac{1}{N}\sum_i L_i}_{\text{data loss}} + \underbrace{\lambda R(W)}_{\text{regularization loss}}
$$

- **Data loss**：所有訓練樣本 loss $L_i$ 的平均，衡量預測和標籤吻不吻合 [CS231n linear-classify "Multiclass Support Vector Machine loss"]。
- **Regularization loss**：只跟權重有關，跟資料無關，用來偏好某些 W，詳見 [Regularization](regularization.md)。
- $\lambda$ 是 hyperparameter，通常用 cross-validation 決定 [CS231n linear-classify "Multiclass Support Vector Machine loss"]。

$L_i$ 怎麼定義有很多種選擇。CS231n 介紹了兩種最常見的：**Multiclass SVM loss** 和 **Softmax（cross-entropy）loss** [CS231n linear-classify "Summary"]。

### Multiclass SVM loss（hinge loss）

**想法**：SVM 希望正確類別的分數，比每一個錯誤類別的分數都**至少高出一個固定的 margin $\Delta$** [CS231n linear-classify "Multiclass Support Vector Machine loss"]。

設分數向量為 $s = f(x_i, W)$，第 j 類的分數是 $s_j$，正確類別是 $y_i$ [CS231n linear-classify "Multiclass Support Vector Machine loss"]：

$$
L_i = \sum_{j \neq y_i} \max(0,\ s_j - s_{y_i} + \Delta)
$$

白話解釋：逐一檢查每個錯誤類別 j。如果它的分數沒有比正確類別低至少 $\Delta$，就把「差了多少」加進 loss；如果已經夠低，這一項就是 0。

**範例** [CS231n linear-classify "Multiclass Support Vector Machine loss"]：分數 $s = (13, -7, 11)$，正確的是第一類，$\Delta = 10$。

| 錯誤類別 | 計算 | 結果 | 解讀 |
|---|---|---|---|
| 分數 −7 | max(0, −7 − 13 + 10) | 0 | 正確類別高出 20，已經超過 margin 10，不計 loss |
| 分數 11 | max(0, 11 − 13 + 10) | 8 | 雖然 13 > 11，但只高出 2，沒達到 margin 10，差了 8 |

所以 $L_i = 0 + 8 = 8$。注意 SVM **只在意差距是否達到 $\Delta$**，超過的部分不會帶來額外好處 [CS231n linear-classify "Multiclass Support Vector Machine loss"]。

筆記的示意圖把它畫成一條數線：正確類別的分數往左一個 delta 的範圍是紅色區域，其他類別的分數只要落在紅色區域或更右邊，就會累積 loss [CS231n linear-classify "Multiclass Support Vector Machine loss" 圖]。

**術語** [CS231n linear-classify "Multiclass Support Vector Machine loss"]：

- $\max(0, -)$ 這種在 0 截斷的函數叫做 **hinge loss**。
- **Squared hinge loss**（L2-SVM）用 $\max(0, -)^2$，對沒達到 margin 的情況懲罰更重（平方而不是線性）。不平方的版本比較標準，但在某些資料集上平方版效果更好，可以用 cross-validation 決定。

### Δ 要設多少？

答案是可以**直接設成 $\Delta = 1.0$**，不需要調 [CS231n linear-classify "Practical Considerations"]。原因是：

- W 的大小會直接影響分數之間的差距。把 W 整體縮小，差距就縮小；放大，差距就放大。
- 所以 margin 設 1 還是 100，在某種意義上沒有差別，因為 W 可以任意縮放。
- $\Delta$ 和 $\lambda$ 看起來是兩個 hyperparameter，其實控制的是**同一個取捨**：data loss 和 regularization loss 之間的平衡。真正要調的只有 $\lambda$，也就是允許 W 長到多大。

### 與 Binary SVM、其他多類別 SVM 的關係

- 只有兩個類別時，這裡的 Multiclass SVM 會退化成常見的 binary SVM $L_i = C \max(0, 1 - y_i w^T x_i) + R(W)$，其中 $C \propto 1/\lambda$ [CS231n linear-classify "Practical Considerations"]。
- 這裡的寫法依循 Weston and Watkins 1999 的版本。其他常見做法還有 **One-Vs-All（OVA）**、All-vs-All（AVA）和 Structured SVM [CS231n linear-classify "Practical Considerations"]。
- CS231n 認為這裡的版本是安全的選擇，但最簡單的 OVA 很可能效果差不多。這個看法引用自 Rifkin et al. 2004 [CS231n linear-classify "Practical Considerations"]。

### 不可微的問題

$\max(x, y)$ 在 $x = y$ 的地方有一個「折角」（kink），嚴格來說不可微。但實務上這不是問題，通常用 **subgradient** 處理 [CS231n linear-classify "Practical Considerations"]。CS231n（以及一般的神經網路）都直接最佳化沒有約束的 primal 形式，不使用 kernel、dual、SMO 等傳統 SVM 技巧 [CS231n linear-classify "Practical Considerations"]。

## SVM vs. Softmax

另一種常見的 loss 是 [Softmax 的 cross-entropy loss](softmax-cross-entropy.md)。兩者使用**同一個分數向量**，差別在於**怎麼解讀這些分數** [CS231n linear-classify "SVM vs. Softmax" 圖]：

| | SVM | Softmax |
|---|---|---|
| 怎麼看分數 | 類別分數，沒有校準過 | 未正規化的 log 機率 |
| Loss | hinge loss（max-margin loss） | cross-entropy loss |
| 什麼時候滿意 | margin 達標就滿意，不再管細節 | **永遠不滿足**：正確類別的機率永遠可以再高一點 |
| 輸出能否解讀 | 分數本身不容易解讀 | 可以得到「機率」，但有引號，詳見 Softmax 頁 |

（依據 [CS231n linear-classify "SVM vs. Softmax"]。）

**同一個例子，兩種 loss**：筆記的對照圖對同一筆資料算出分數 (−2.85, 0.86, 0.28)，正確類別是第三類。SVM 的 loss 是 1.58，Softmax 的 loss 是 1.04（自然對數）[CS231n linear-classify "SVM vs. Softmax" 圖]。但**這兩個數字不能互相比較**，只有在同一種分類器、同一份資料內比較才有意義 [CS231n linear-classify "SVM vs. Softmax" 圖]。

**「局部性」的差別** [CS231n linear-classify "SVM vs. Softmax"]：假設分數是 (10, −2, 3)，第一類正確，$\Delta = 1$。
- SVM：margin 已經滿足，loss 是 0。就算分數改成 (10, −100, −100) 或 (10, 9, 9)，SVM 也一樣不在乎，因為 margin 1 都滿足了。
- Softmax：(10, 9, 9) 的 loss 會比 (10, −100, −100) 高很多。
- 這可以看成優點：例如一個 car 分類器應該把力氣花在區分汽車和卡車這種難題上，而不是被那些早就給了很低分數的青蛙影響。

**實務上兩者表現通常差不多**，差異很小，至於哪個比較好，不同人有不同看法 [CS231n linear-classify "SVM vs. Softmax"]。延伸閱讀中提到，Tang 2013 的論文宣稱 L2-SVM 表現勝過 Softmax [CS231n linear-classify "Further Reading"]。這是該論文的主張，本 Wiki 目前沒有收錄這篇論文。

## 出現在哪些地方

- [Linear Classifier](linear-classifier.md)：用 loss 來評估和訓練 W
- [Softmax／Cross-Entropy](softmax-cross-entropy.md)：另一種 loss
- [Regularization](regularization.md)：完整 loss 的第二部分
- [Hyperparameter Tuning](hyperparameter-tuning.md)：$\lambda$ 用 cross-validation 決定

## 常見誤解

- **「loss 越低，模型越好」**：只有在 training set 上是如此。訓練的目標是讓 loss 變小，但真正要在乎的是在沒看過的資料上的表現，詳見 [Hyperparameter Tuning](hyperparameter-tuning.md)。
- **「SVM loss 1.58 比 Softmax loss 1.04 差」**：不同種類的 loss 數值不能互相比較 [CS231n linear-classify "SVM vs. Softmax" 圖]。
