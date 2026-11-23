---
title: Activation Function
type: concept
first_introduced: unknown
aliases: [激活函數, 活化函數, non-linearity, 非線性, sigmoid, tanh, ReLU, Rectified Linear Unit, Leaky ReLU, PReLU, Maxout, dead ReLU]
tags: [neural-network, foundation]
sources: [CS231n]
related:
  - concepts/neural-network.md
  - concepts/backpropagation.md
  - concepts/gradient-descent.md
  - concepts/data-preprocessing.md
  - models/alexnet.md
created: 2026-11-23
updated: 2026-11-23
---

# Activation Function（激活函數）

## 一句話說明

[神經網路](neural-network.md)中，每個 neuron 在算完內積之後套用的**非線性函數**，它讓網路不只是一個線性函數 [CS231n neural-networks-1 "Quick intro"; CS231n neural-networks-1 "Commonly used activation functions"]。

## 直觀理解

如果沒有 activation function，不管疊幾層，整個網路都只是一連串矩陣乘法，可以合併成一個矩陣，又變回 [linear classifier](linear-classifier.md) [CS231n neural-networks-1 "Quick intro"]。activation function 就是讓網路能「彎曲」的地方。

每個 activation function 都是**對單一數字做一個固定的數學運算** [CS231n neural-networks-1 "Commonly used activation functions"]。

它的靈感來自生物 neuron 的 **firing rate**（放電頻率）：輸入的訊號總和越強，neuron 放電越頻繁 [CS231n neural-networks-1 "Biological motivation and connections"]。

## 技術細節

### 一覽

| 函數 | 公式 | 輸出範圍 | 優點 | 缺點 |
|---|---|---|---|---|
| **Sigmoid** | $\sigma(x) = 1/(1 + e^{-x})$ | 0～1 | 可以解讀成 neuron 的 firing rate | 會飽和、讓 gradient 消失；輸出不是 zero-centered |
| **Tanh** | $\tanh(x) = 2\sigma(2x) - 1$ | −1～1 | zero-centered | 一樣會飽和 |
| **ReLU** | $f(x) = \max(0, x)$ | 0 以上 | 收斂快、計算便宜 | neuron 可能「死掉」 |
| **Leaky ReLU** | x < 0 時是一個很小的斜率 $\alpha x$（例如 0.01） | | 嘗試修正 dying ReLU | 效果不一定穩定 |
| **Maxout** | $\max(w_1^T x + b_1, w_2^T x + b_2)$ | | 有 ReLU 的優點，沒有 dying ReLU | 每個 neuron 的參數變成兩倍 |

（表中內容依據 [CS231n neural-networks-1 "Commonly used activation functions"]。）

### Sigmoid

把實數「壓」到 0 到 1 之間：很大的負數變成 0，很大的正數變成 1。以前很常用，因為它可以漂亮地解讀成 neuron 的 firing rate：從完全不放電（0）到飽和的最大頻率（1）[CS231n neural-networks-1 "Commonly used activation functions"]。

但（截至 CS231n 筆記撰寫時）sigmoid 已經不再流行，很少被使用，因為有兩個主要缺點 [CS231n neural-networks-1 "Commonly used activation functions"]：

1. **會飽和，讓 gradient 消失**：當 neuron 的輸出接近 0 或 1 時，那裡的 gradient 幾乎是 0。在 [backpropagation](backpropagation.md) 中，這個 local gradient 會被乘到上游傳來的 gradient 上；如果它很小，就等於「殺死」了 gradient，幾乎沒有訊號能傳到權重。初始化權重時也要特別小心：權重太大的話，大部分 neuron 會飽和，網路幾乎學不動 [CS231n neural-networks-1 "Commonly used activation functions"]。
2. **輸出不是 zero-centered**：下一層的 neuron 會收到全部為正的資料。如果輸入一個 neuron 的資料都是正的，backprop 時權重的 gradient 會**全部同號**（全正或全負），造成 gradient 更新時「之字形」（zig-zag）前進 [CS231n neural-networks-1 "Commonly used activation functions"]。不過一個 batch 的 gradient 加總之後，符號可能不同，所以這個問題比飽和來得輕微 [CS231n neural-networks-1 "Commonly used activation functions"]。

> **和資料前處理的關聯**：第 2 點說的是「**輸入一個 neuron 的資料**都是正的」會造成問題。原始像素值 0～255 也全部是正數，所以這很可能就是 linear-classify 筆記預告的「zero-centering 為什麼重要」的答案（綜合推論，依據 [CS231n neural-networks-1 "Commonly used activation functions"; CS231n linear-classify "Interpreting a linear classifier"]）。詳見 [Data Preprocessing](data-preprocessing.md)。

（[Backpropagation](backpropagation.md) 頁用 sigmoid 當作計算 gradient 的範例 [CS231n optimization-2 "Modularity: Sigmoid example"]，那是教學上的例子；實務上的建議是不要用 sigmoid。）

### Tanh

把實數壓到 −1 到 1 之間。和 sigmoid 一樣會飽和，但**輸出是 zero-centered**，所以實務上 **tanh 一定比 sigmoid 好** [CS231n neural-networks-1 "Commonly used activation functions"]。tanh 其實就是縮放過的 sigmoid：$\tanh(x) = 2\sigma(2x) - 1$ [CS231n neural-networks-1 "Commonly used activation functions"]。

### ReLU（Rectified Linear Unit）

$f(x) = \max(0, x)$：小於 0 的值直接變成 0，大於 0 的部分是斜率 1 的直線 [CS231n neural-networks-1 "Commonly used activation functions"]。（截至 CS231n 筆記撰寫時）ReLU 在最近幾年變得非常流行 [CS231n neural-networks-1 "Commonly used activation functions"]。

**優點**：
- **大幅加速 SGD 的收斂**。筆記引用 Krizhevsky et al.（[AlexNet](../models/alexnet.md)）論文的一張圖：在相同的 training error 下，ReLU 收斂的速度約是 **tanh** 的 6 倍 [CS231n neural-networks-1 "Commonly used activation functions" 圖]。一般認為，這是因為 ReLU 是線性、不會飽和的 [CS231n neural-networks-1 "Commonly used activation functions"]。
- **計算便宜**：只要把矩陣在 0 截斷，不需要 sigmoid、tanh 那種昂貴的指數運算 [CS231n neural-networks-1 "Commonly used activation functions"]。

> **比較對象的寫法不一致**：內文說 ReLU 的收斂比「**sigmoid/tanh**」快 6 倍 [CS231n neural-networks-1 "Commonly used activation functions"]，但圖說寫的是「和 **tanh** 相比」，圖中也只有 ReLU（實線）和 tanh（虛線）兩條曲線：實線約在第 6 個 epoch 達到 0.25 的 training error，虛線約在第 36 個 epoch [CS231n neural-networks-1 "Commonly used activation functions" 圖]。本 Wiki 依圖說寫成「和 tanh 相比」。這個數字來自 AlexNet 論文，ingest 該論文時要核對。

**缺點：Dying ReLU** [CS231n neural-networks-1 "Commonly used activation functions"]：
- 一個很大的 gradient 流過 ReLU neuron，可能把權重更新到「對任何資料都不會再被激活」的狀態。從此之後，流過它的 gradient 永遠是 0，這個 neuron 就**不可逆地「死掉」了** [CS231n neural-networks-1 "Commonly used activation functions"]。
- 如果 [learning rate](gradient-descent.md) 設得太高，網路中可能有多達 40% 的 neuron 是死的 [CS231n neural-networks-1 "Commonly used activation functions"]。
- 適當地設定 learning rate，這個問題就比較少發生 [CS231n neural-networks-1 "Commonly used activation functions"]。

### Leaky ReLU 與 PReLU

- **Leaky ReLU**：x < 0 時不是 0，而是一個很小的正斜率（約 0.01），試圖修正 dying ReLU。有人回報效果不錯，但結果並不總是一致 [CS231n neural-networks-1 "Commonly used activation functions"]。
- **PReLU**：把負區間的斜率變成每個 neuron 的可學習參數，由 Kaiming He et al. 在 2015 年提出。（截至 CS231n 筆記撰寫時）它在不同任務上的效益仍然不清楚 [CS231n neural-networks-1 "Commonly used activation functions"]。

### Maxout

不是「先內積再套非線性」的形式，而是計算 $\max(w_1^T x + b_1, w_2^T x + b_2)$。ReLU 和 Leaky ReLU 都是它的特例（例如 ReLU 是 $w_1, b_1 = 0$）。所以 Maxout 有 ReLU 的所有優點，又沒有 dying ReLU 的問題；代價是每個 neuron 的參數變成兩倍 [CS231n neural-networks-1 "Commonly used activation functions"]。

### 實務建議（TLDR）

> **用 ReLU**，小心設定 learning rate，也可以監控網路中「死掉」的 unit 比例。如果擔心這個問題，試試 Leaky ReLU 或 Maxout。**永遠不要用 sigmoid**。可以試試 tanh，但預期它的效果會比 ReLU／Maxout 差 [CS231n neural-networks-1 "Commonly used activation functions"]。

在同一個網路中混用不同類型的 neuron 非常少見，雖然這麼做沒有根本上的問題 [CS231n neural-networks-1 "Commonly used activation functions"]。

### 輸出層通常不用 activation function

輸出層代表類別分數或迴歸的目標值，是任意的實數，所以通常沒有 activation function [CS231n neural-networks-1 "Layer-wise organization"]。

## 出現在哪些地方

- [Neural Network](neural-network.md)：每一層 neuron 的非線性
- [CNN](convolutional-neural-network.md)：架構中的 RELU 層
- [Backpropagation](backpropagation.md)：sigmoid 的飽和會「殺死」gradient
- [Gradient Descent](gradient-descent.md)：learning rate 太高會讓 ReLU 死掉
- [Data Preprocessing](data-preprocessing.md)：zero-centered 的輸入對 gradient 的影響
- [AlexNet](../models/alexnet.md)：ReLU 加速收斂的數據來源
