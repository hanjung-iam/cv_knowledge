---
title: Gradient Descent
type: concept
first_introduced: unknown
aliases: [梯度下降, gradient, 梯度, numerical gradient, analytic gradient, gradient check, learning rate, step size, 學習率, mini-batch gradient descent, Stochastic Gradient Descent, SGD]
tags: [training, optimization, foundation]
sources: [CS231n]
related:
  - concepts/optimization.md
  - concepts/loss-function.md
  - concepts/hyperparameter-tuning.md
  - datasets/ilsvrc.md
created: 2026-11-23
updated: 2026-11-23
---

# Gradient Descent（梯度下降）

## 一句話說明

反覆做兩件事：**算出 loss 對參數的 gradient，再往 gradient 的反方向走一小步** [CS231n optimization-1 "Gradient Descent"]。

## 直觀理解

延續 [Optimization](optimization.md) 頁的「蒙眼下山」：你看不到整座山，但可以**用腳感覺地面往哪邊傾斜**，然後往最陡的下坡方向走一步。重複這個動作，就能一路走到谷底 [CS231n optimization-1 "Strategy #3: Following the Gradient"]。

這個簡單的迴圈是**所有神經網路函式庫的核心** [CS231n optimization-1 "Gradient Descent"]：

```python
while True:
  weights_grad = evaluate_gradient(loss_fun, data, weights)
  weights += - step_size * weights_grad  # 往 gradient 的反方向更新
```

## 技術細節

### 什麼是 gradient

- 一維函數的**斜率**，是函數在某一點的瞬間變化率 [CS231n optimization-1 "Strategy #3: Following the Gradient"]：

$$
\frac{df(x)}{dx} = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
$$

- 輸入是一個向量時，每個維度各有一個 **partial derivative（偏導數）**，把它們排成向量就是 **gradient** [CS231n optimization-1 "Strategy #3: Following the Gradient"]。
- gradient 指向函數**上升最陡**的方向。我們要讓 loss 下降，所以往**負 gradient** 的方向更新 [CS231n optimization-1 "Computing the gradient numerically with finite differences"]。
- SVM 的 max 會造成折角，嚴格來說不可微，但 **subgradient** 仍然存在，實務上就用它。CS231n 把 subgradient 和 gradient 當成同義詞使用 [CS231n optimization-1 "Visualizing the loss function"]。

### 計算 gradient 的兩種方法

| | Numerical gradient（數值梯度） | Analytic gradient（解析梯度） |
|---|---|---|
| 做法 | 每個維度加上一個很小的 h，看 loss 變了多少 | 用微積分推導出 gradient 的公式 |
| 精確度 | 近似值，因為 h 不可能真的是 0 | 精確 |
| 速度 | 很慢 | 很快 |
| 缺點 | 計算量和參數數量成正比 | 推導和實作容易出錯 |

（依據 [CS231n optimization-1 "Computing the gradient"; CS231n optimization-1 "Computing the gradient analytically with Calculus"]。）

**Numerical gradient 的細節** [CS231n optimization-1 "Computing the gradient numerically with finite differences"]：
- 數學上 h 要趨近於 0，實務上用一個很小的值就夠了，例如範例中的 1e-5。理想上，要選「不會造成數值問題的最小值」。
- 實務上，改用 **centered difference formula** $[f(x+h) - f(x-h)] / 2h$ 通常效果更好。

**Numerical gradient 為什麼不夠用**：它的計算量和參數數量成正比。CIFAR-10 的 linear classifier 有 30,730 個參數，所以**光是為了更新一步**，就要評估 30,731 次 loss。而現代神經網路動輒有數千萬個參數，這個方法根本無法擴展 [CS231n optimization-1 "Computing the gradient numerically with finite differences"]。

**Analytic gradient 的範例**：對單一樣本的 SVM loss 求 gradient [CS231n optimization-1 "Computing the gradient analytically with Calculus"]：

$$
\nabla_{w_{y_i}} L_i = -\left(\sum_{j \neq y_i} \mathbb{1}(w_j^T x_i - w_{y_i}^T x_i + \Delta > 0)\right) x_i
$$

$$
\nabla_{w_j} L_i = \mathbb{1}(w_j^T x_i - w_{y_i}^T x_i + \Delta > 0)\, x_i \quad (j \neq y_i)
$$

其中 $\mathbb{1}$ 是 indicator function，條件成立時是 1，否則是 0。公式看起來嚇人，實作卻很簡單：對正確類別那一列，**數一數有幾個類別沒達到 margin**，再乘上 $-x_i$；對其他每一列，如果該類別沒達到 margin，gradient 就是 $x_i$，否則是 0 [CS231n optimization-1 "Computing the gradient analytically with Calculus"]。

### Gradient check

因為 analytic gradient 容易寫錯，實務上的標準做法是：**實際使用 analytic gradient，再拿 numerical gradient 和它比對**，確認實作正確。這叫做 **gradient check** [CS231n optimization-1 "Computing the gradient analytically with Calculus"; CS231n optimization-1 "Summary"]。

### Step size（learning rate）

gradient 告訴我們**方向**，但沒有告訴我們**要走多遠**。這個步伐大小就是 **step size**，之後也叫做 **learning rate**。CS231n 說它會成為訓練神經網路時**最重要、也最令人頭痛的 hyperparameter 之一** [CS231n optimization-1 "Computing the gradient numerically with finite differences"]。

筆記在 CIFAR-10 上，從同一組隨機 W 出發，嘗試不同的 step size 各走一步。原本的 loss 是 2.200718 [CS231n optimization-1 "Computing the gradient numerically with finite differences"]：

| step size | 走一步之後的 loss |
|---|---|
| 1e-10 | 2.200652 |
| 1e-08 | 2.194116 |
| 1e-06 | **1.647802**（這組範例中最低） |
| 1e-05 | 2.844355（已經比原本還高） |
| 1e-03 | 254.086573 |
| 1e-01 | 25392.214036 |

（表中數值依據 [CS231n optimization-1 "Computing the gradient numerically with finite differences"]，這裡只列出部分 step size。）

- **太小**：進展穩定，但非常慢。
- **太大**：可能進展比較快，但風險高，會 **overstep（走過頭）**，讓 loss 反而變高 [CS231n optimization-1 "Computing the gradient numerically with finite differences"]。
- 筆記的示意圖在碗狀的 loss 地形上畫出負 gradient 的方向（白色箭頭），以及沿著這個方向延伸的虛線：小步會穩定接近谷底，大步則可能越過谷底 [CS231n optimization-1 "Computing the gradient numerically with finite differences" 圖]。

### Mini-batch gradient descent

在大規模的應用中（例如 [ILSVRC](../datasets/ilsvrc.md)），訓練資料可能有數百萬筆。只為了更新一次參數，就算完整個 training set 的 loss，很浪費。常見的做法是每次只用一小**批（batch）**資料計算 gradient [CS231n optimization-1 "Gradient Descent"]。

（截至 CS231n 筆記撰寫時）在當時 state of the art 的 ConvNets 中，一個典型的 batch 是從 120 萬張訓練影像中取出 256 張 [CS231n optimization-1 "Gradient Descent"]。

**為什麼這樣可行？** 因為訓練資料彼此相關。思想實驗：假設 ILSVRC 的 120 萬張影像，其實只是 1000 張不同影像（每類一張）的複本，每張各有 1200 份。那麼對全部 120 萬張算出來的平均 loss 和 gradient，會和只算那 1000 張完全一樣 [CS231n optimization-1 "Gradient Descent"]。真實資料當然不會有重複，但 mini-batch 的 gradient 仍然是完整 gradient 的**好近似**，用它可以更頻繁地更新參數，收斂快得多 [CS231n optimization-1 "Gradient Descent"]。

### SGD 這個名稱

- 嚴格來說，**Stochastic Gradient Descent（SGD）**，也叫 on-line gradient descent，指的是 batch 只有**一筆**資料的極端情況 [CS231n optimization-1 "Gradient Descent"]。
- 這種做法比較少見，因為向量化的程式碼一次算 100 筆的 gradient，比一筆一筆算 100 次快得多 [CS231n optimization-1 "Gradient Descent"]。
- 但實際上，大家**提到 SGD 時，通常指的是 mini-batch gradient descent**。MGD、BGD 這些縮寫很少見 [CS231n optimization-1 "Gradient Descent"]。

### Batch size 怎麼選

batch size 是 hyperparameter，但**通常不用 cross-validation 來選**，而是依記憶體限制決定，或直接設成 32、64、128 這類值。用 2 的次方，是因為很多向量化運算在輸入大小是 2 的次方時跑得比較快 [CS231n optimization-1 "Gradient Descent"]。

### 其他最佳化方法

除了 gradient descent 還有其他方法，例如 LBFGS。但（截至 CS231n 筆記撰寫時）gradient descent 是最佳化神經網路 loss 最普遍、最成熟的方法 [CS231n optimization-1 "Gradient Descent"]。之後的課程會在更新公式的細節上做各種改進，但「**沿著 gradient 走，直到結果滿意為止**」這個核心想法不會變 [CS231n optimization-1 "Gradient Descent"]。

## 整體資訊流

筆記用一張圖總結訓練時的資訊流 [CS231n optimization-1 "Summary" 圖]：

- 資料 $(x_i, y_i)$ 是固定的；權重 $W$ 從隨機值開始，會被更新。
- **Forward pass**：score function 算出分數 $f(x_i, W)$。
- **Loss**：data loss 比較分數和標籤 $y_i$；regularization loss 只看 $W$。兩者相加得到 $L$。
- **Gradient descent**：算出 $L$ 對 $W$ 的 gradient，用它來更新參數。

## 下一步：Backpropagation

CS231n 認為，**能夠計算 loss 對權重的 gradient（並且直觀地理解它），是設計、訓練和理解神經網路最重要的能力**。下一篇會用 chain rule 來計算 analytic gradient，也就是 **backpropagation** [CS231n optimization-1 "Summary"]。

## 出現在哪些地方

- [Optimization](optimization.md)：gradient descent 是策略 #3 的實作
- [Hyperparameter Tuning](hyperparameter-tuning.md)：learning rate 和 batch size
- [ILSVRC](../datasets/ilsvrc.md)：mini-batch 的動機
