---
title: Neural Network
type: concept
first_introduced: unknown
aliases: [神經網路, Neural Networks, ANN, Artificial Neural Networks, MLP, Multi-Layer Perceptrons, hidden layer, fully-connected layer, universal approximator]
tags: [architecture, foundation]
sources: [CS231n]
related:
  - concepts/linear-classifier.md
  - concepts/activation-function.md
  - concepts/overfitting.md
  - concepts/backpropagation.md
  - concepts/convolutional-neural-network.md
  - datasets/cifar-10.md
created: 2026-11-23
updated: 2026-11-23
---

# Neural Network（神經網路）

## 一句話說明

把多個 [linear classifier](linear-classifier.md) 疊起來，並在中間插入**非線性函數**：例如兩層的神經網路是 $s = W_2 \max(0, W_1 x)$ [CS231n neural-networks-1 "Quick intro"]。

## 直觀理解

[Linear classifier](linear-classifier.md) 的問題是「每個類別只能有一個模板」，所以朝左和朝右的馬會被混成一匹兩個頭的馬 [CS231n linear-classify "Interpreting a linear classifier"]。

神經網路的解法很直接：**先用很多個「中間的分類器」各自偵測一些東西，再用下一層把它們的結果組合起來**。linear-classify 筆記當時就預告了：中間層的 neuron 可以分別偵測特定類型的車（朝左的綠車、朝前的藍車），下一層再把它們加權組合成更準確的 car 分數 [CS231n linear-classify "Interpreting a linear classifier"]。

不需要用大腦來比喻也能理解神經網路 [CS231n neural-networks-1 "Quick intro"]：

| | 公式 | [CIFAR-10](../datasets/cifar-10.md) 的例子 |
|---|---|---|
| Linear classifier | $s = Wx$ | $W$ 是 10 × 3072 |
| 兩層神經網路 | $s = W_2 \max(0, W_1 x)$ | $W_1$ 是 100 × 3072（先轉成 100 維的中間向量），$W_2$ 是 10 × 100 |
| 三層神經網路 | $s = W_3 \max(0, W_2 \max(0, W_1 x))$ | |

（依據 [CS231n neural-networks-1 "Quick intro"]。）

**非線性是關鍵**：如果拿掉中間的 $\max(0, -)$，$W_2 W_1$ 可以直接合併成一個矩陣，整個網路又變回輸入的線性函數。非線性才是讓網路能「彎曲」的地方 [CS231n neural-networks-1 "Quick intro"]。

參數 $W_1, W_2$ 用 stochastic [gradient descent](gradient-descent.md) 學習，gradient 用 chain rule 推導、用 [backpropagation](backpropagation.md) 計算 [CS231n neural-networks-1 "Quick intro"]。中間向量的大小是 [hyperparameter](hyperparameter-tuning.md) [CS231n neural-networks-1 "Quick intro"]。

## 技術細節

### Neuron 模型與生物的靈感

神經網路最初是受到「模擬生物神經系統」的啟發，但後來已經走向工程，以在機器學習任務上取得好成績為目標 [CS231n neural-networks-1 "Modeling one neuron"]。

- 大腦的基本計算單元是 **neuron**。人類神經系統約有 860 億個 neuron，透過約 $10^{14}$～$10^{15}$ 個 **synapse** 互相連接 [CS231n neural-networks-1 "Biological motivation and connections"]。
- 在數學模型中，每個 neuron 把輸入和權重做**內積**、加上 bias，再套用一個 **[activation function](activation-function.md)**（非線性）[CS231n neural-networks-1 "Biological motivation and connections"]。權重對應 synapse 的強度：正的權重代表興奮，負的代表抑制 [CS231n neural-networks-1 "Biological motivation and connections"]。
- 筆記的示意圖左邊是生物 neuron 的卡通圖（dendrite、cell body、axon），右邊是數學模型：輸入 $x_i$ 乘上權重 $w_i$，在 cell body 加總並加上 bias，再經過 activation function 輸出 [CS231n neural-networks-1 "Biological motivation and connections" 圖]。

**這個模型非常粗糙**：生物 neuron 有很多種類；dendrite 會做複雜的非線性計算；synapse 不只是一個權重，而是一個複雜的動態系統。所以 CS231n 提醒，如果拿神經網路和真實大腦類比，有神經科學背景的人會抱怨 [CS231n neural-networks-1 "Biological motivation and connections"]。

### 一個 neuron 就是一個 linear classifier

一個 neuron 的 forward 計算，形式和 linear classifier 一樣。只要在它的輸出接上適當的 loss，它就是一個二元分類器 [CS231n neural-networks-1 "Single neuron as a linear classifier"]：

- **Binary Softmax classifier**：把 $\sigma(\sum_i w_i x_i + b)$ 解讀成其中一類的機率，用 [cross-entropy loss](softmax-cross-entropy.md) 訓練，就是 binary Softmax classifier，也叫 **logistic regression**。輸出大於 0.5 就判斷為那一類 [CS231n neural-networks-1 "Single neuron as a linear classifier"]。
- **Binary SVM classifier**：接上 hinge loss，就是 binary SVM [CS231n neural-networks-1 "Single neuron as a linear classifier"]。
- **Regularization 的生物詮釋**：regularization 會在每次更新後把權重往 0 拉，可以解讀成「**逐漸遺忘**」（gradual forgetting）[CS231n neural-networks-1 "Single neuron as a linear classifier"]。

### 層狀組織

- 神經網路是由 neuron 組成的**無環圖**：有些 neuron 的輸出是其他 neuron 的輸入。不允許有環，否則 forward pass 會變成無窮迴圈 [CS231n neural-networks-1 "Layer-wise organization"]。
- 一般的神經網路最常見的層是 **fully-connected layer**：相鄰兩層的 neuron 兩兩全部相連，但同一層內的 neuron 彼此不相連 [CS231n neural-networks-1 "Layer-wise organization"]。
- 筆記的示意圖：一個 2 層的網路，輸入層有 3 個輸入、hidden layer 有 4 個 neuron、output layer 有 2 個 neuron，相鄰兩層之間的箭頭全部相連 [CS231n neural-networks-1 "Layer-wise organization" 圖]。

**命名慣例** [CS231n neural-networks-1 "Layer-wise organization"]：

- 說「N 層神經網路」時，**不算輸入層**。所以「單層神經網路」就是沒有 hidden layer、輸入直接對應到輸出的網路。從這個角度，logistic regression 和 SVM 可以看成單層神經網路的特例。
- 也叫做 **Artificial Neural Networks（ANN）**或 **Multi-Layer Perceptrons（MLP）**。
- 很多人不喜歡大腦的類比，偏好把 neuron 稱為 **unit**。

**輸出層通常沒有 activation function**：因為輸出層代表類別分數（可以是任意實數），或迴歸問題的實數目標值 [CS231n neural-networks-1 "Layer-wise organization"]。

### 網路的大小

衡量網路大小的兩種常見指標是 neuron 數，以及更常用的**參數數量** [CS231n neural-networks-1 "Layer-wise organization"]：

| 網路 | neuron 數（不算輸入） | 權重 | bias | 參數總數 |
|---|---|---|---|---|
| 2 層：3 → 4 → 2 | 6 | 3 × 4 + 4 × 2 = 20 | 6 | 26 |
| 3 層：3 → 4 → 4 → 1 | 9 | 12 + 16 + 4 = 32 | 9 | 41 |

（依據 [CS231n neural-networks-1 "Layer-wise organization"]。）

作為對照，（截至 CS231n 筆記撰寫時）現代的 Convolutional Networks 約有 1 億個參數、大約 10～20 層，這也是「**deep** learning」名稱的由來 [CS231n neural-networks-1 "Layer-wise organization"]。

### Forward pass：矩陣乘法加上 activation

把網路組織成層，最主要的原因之一，是這樣就能用**矩陣運算**簡單又有效率地計算 [CS231n neural-networks-1 "Example feed-forward computation"]：

- 一層所有 neuron 的權重可以放在一個矩陣裡，每個 neuron 的權重是一列。
- 例如上面的 3 層網路，$W_1$ 是 4 × 3、$W_2$ 是 4 × 4、$W_3$ 是 1 × 4。
- 整個 forward pass 就是**三次矩陣乘法，中間穿插 activation function**。
- 輸入也可以是一整個 batch 的資料，所有樣本會被平行計算。

> CS231n 的總結：fully-connected layer 的 forward pass，就是一次矩陣乘法，加上 bias，再套用 activation function [CS231n neural-networks-1 "Example feed-forward computation"]。

### 表達能力：universal approximator

只要有**至少一層 hidden layer**，神經網路就是 **universal approximator**：對任何連續函數 $f(x)$ 和任意 $\epsilon > 0$，都存在一個只有一層 hidden layer 的網路 $g(x)$，使得對所有 $x$，$|f(x) - g(x)| < \epsilon$ [CS231n neural-networks-1 "Representational power"]。

**但這個性質在實務上「沒什麼用」** [CS231n neural-networks-1 "Representational power"]：

- 一維的「指示函數加總」也是 universal approximator，但沒有人會用它來做機器學習。
- 神經網路在實務上有效，是因為它能簡潔地表達平滑的函數，而這些函數剛好符合實際資料的統計性質，而且容易用 gradient descent 等最佳化方法學習。
- 更深的網路常常比只有一層 hidden layer 的網路好，但這是**經驗上的觀察**；兩者的表達能力其實相同。

### 深度：FC 網路和 CNN 不一樣

| 網路類型 | 深度的效果 |
|---|---|
| Fully-connected 網路 | 3 層通常比 2 層好，但再更深（4、5、6 層）就很少有更多幫助 |
| Convolutional Networks | 深度被發現是好的辨識系統**極為重要**的因素，例如約 10 個可學習的層 |

（依據 [CS231n neural-networks-1 "Representational power"]。）

一種解釋是：**影像有階層結構**，例如臉由眼睛組成，眼睛由邊緣組成，所以對影像來說，多層處理在直覺上很合理 [CS231n neural-networks-1 "Representational power"]。這也和 [VGGNet](../models/vggnet.md)「證明深度是效能關鍵」的結論一致 [CS231n convolutional-networks "Case studies"]。

### 要用多大的網路

網路越大、層數越多，**capacity**（能表達的函數空間）就越大 [CS231n neural-networks-1 "Setting number of layers and their sizes"]。這既是好處（能學更複雜的資料），也是壞處（更容易 [overfitting](overfitting.md)）。

CS231n 的結論是：**不要因為怕 overfitting 就用比較小的網路**；應該在計算資源允許的範圍內用越大的網路越好，再用 [regularization](regularization.md) 等方法控制 overfitting [CS231n neural-networks-1 "Setting number of layers and their sizes"]。詳細的理由見 [Overfitting](overfitting.md)。

## 在學習框架中的位置

神經網路換掉的只是 **score function**：從 $Wx$ 變成多層的 $W_2 \max(0, W_1 x)$。[Loss function](loss-function.md)、[gradient descent](gradient-descent.md)、[backpropagation](backpropagation.md) 都沿用前面的內容 [CS231n neural-networks-1 "Quick intro"]。

[CNN](convolutional-neural-network.md) 則是再往前一步：CS231n 說 CNN 和這裡的一般神經網路「非常相似」，差別在於利用「輸入是影像」的前提，限制連接方式並共用參數 [CS231n convolutional-networks "Convolutional Neural Networks (CNNs / ConvNets)"]。一般神經網路的 fully-connected layer，也是 CNN 最後算出類別分數的那幾層 [CS231n convolutional-networks "Layers used to build ConvNets"]。

## 出現在哪些地方

- [Linear Classifier](linear-classifier.md)：神經網路的一層，就是 linear classifier 加上非線性
- [Activation Function](activation-function.md)：神經網路中的非線性
- [Overfitting](overfitting.md)：網路大小和 overfitting 的關係
- [CNN](convolutional-neural-network.md)：為影像特化的神經網路
- [Backpropagation](backpropagation.md)：計算神經網路的 gradient

## 常見誤解

- **「神經網路就是在模擬大腦」**：只在最初的靈感上是如此。CS231n 強調，這個 neuron 模型非常粗糙，神經網路後來已經走向工程 [CS231n neural-networks-1 "Modeling one neuron"; CS231n neural-networks-1 "Biological motivation and connections"]。
- **「既然一層 hidden layer 就是 universal approximator，就不需要更深的網路」**：universal approximator 是數學上的性質，實務上更深的網路常常比較好，而且對 CNN 來說深度非常重要 [CS231n neural-networks-1 "Representational power"]。
