---
title: Softmax and Cross-Entropy Loss
type: concept
first_introduced: unknown
aliases: [Softmax classifier, softmax function, cross-entropy loss, 交叉熵, softmax loss]
tags: [loss, probability, foundation]
sources: [CS231n]
related:
  - concepts/loss-function.md
  - concepts/linear-classifier.md
  - concepts/regularization.md
created: 2026-11-23
updated: 2026-11-23
---

# Softmax 與 Cross-Entropy Loss（交叉熵損失）

## 一句話說明

把模型輸出的分數轉換成**加總為 1 的「機率」**（softmax），再用**正確類別機率的負對數**（cross-entropy）當作 loss。

## 直觀理解

[SVM loss](loss-function.md) 只告訴你「正確類別有沒有贏過其他類別夠多」。Softmax 則把分數變成像機率的東西。例如 SVM 對 cat、dog、ship 給出的分數可能是 (12.5, 0.6, −23.0)，Softmax 則可以給出 (0.9, 0.09, 0.01) 這樣的「機率」，讓人看得出模型對每個類別有多少信心 [CS231n linear-classify "SVM vs. Softmax"]。

Cross-entropy loss 的想法很簡單：**模型給正確答案的機率越高，loss 就越低**。正確答案的機率是 1 時，loss = −log 1 = 0；機率越接近 0，loss 就越大，而且沒有上限。

Softmax classifier 是 binary **Logistic Regression** 推廣到多類別的版本 [CS231n linear-classify "Softmax classifier"]。

## 技術細節

### Softmax 函數

$$
f_j(z) = \frac{e^{z_j}}{\sum_k e^{z_k}}
$$

把任意實數組成的分數向量 $z$，「壓縮」成一個每個值都在 0 和 1 之間、而且加總為 1 的向量 [CS231n linear-classify "Softmax classifier"]。步驟就是**先取指數，再正規化** [CS231n linear-classify "SVM vs. Softmax"]。

### Cross-entropy loss

score function 和 [linear classifier](linear-classifier.md) 一樣是 $f(x_i; W) = W x_i$，但分數被解讀成**每個類別未正規化的 log 機率**，loss 改用 cross-entropy [CS231n linear-classify "Softmax classifier"]：

$$
L_i = -\log\left(\frac{e^{f_{y_i}}}{\sum_j e^{f_j}}\right) \quad\text{或等價地}\quad L_i = -f_{y_i} + \log\sum_j e^{f_j}
$$

白話解釋：先用 softmax 算出正確類別 $y_i$ 的機率，再取負對數。完整的 loss 和 SVM 一樣，是所有樣本 $L_i$ 的平均，加上 regularization 項 $R(W)$ [CS231n linear-classify "Softmax classifier"]。

**範例**：筆記的對照圖中，分數 (−2.85, 0.86, 0.28) 取指數後是 (0.058, 2.36, 1.32)，正規化後是 (0.016, 0.631, 0.353)。正確類別是第三類，所以 loss = −log(0.353) = 1.04 [CS231n linear-classify "SVM vs. Softmax" 圖]。

### 為什麼是這個形式：兩種詮釋

**1. 資訊理論的觀點** [CS231n linear-classify "Softmax classifier"]

「真實」分布 $p$ 和估計分布 $q$ 之間的 cross-entropy 定義為 $H(p, q) = -\sum_x p(x) \log q(x)$。

- 這裡的真實分布 $p$，是把所有機率都放在正確類別上的分布（one-hot）。
- 因為 $H(p, q) = H(p) + D_{KL}(p \| q)$，而 one-hot 分布的 entropy 是 0，所以最小化 cross-entropy **等於最小化兩個分布之間的 KL divergence**。
- 換句話說，cross-entropy 希望預測分布把**所有機率都集中在正確答案上**。

**2. 機率的觀點** [CS231n linear-classify "Softmax classifier"]

$$
P(y_i \mid x_i; W) = \frac{e^{f_{y_i}}}{\sum_j e^{f_j}}
$$

- 可以解讀成：給定影像 $x_i$ 和參數 $W$，模型給正確標籤 $y_i$ 的機率。
- 最小化正確類別的負 log likelihood，就是在做 **Maximum Likelihood Estimation（MLE，最大概似估計）**。
- 在這個觀點下，regularization 項 $R(W)$ 可以看成來自 W 的 **Gaussian prior**，於是整件事變成 **Maximum a posteriori（MAP）** 估計。完整推導超出這門課的範圍。

## 「機率」為什麼要加引號

Softmax 的輸出看起來像機率，但它們**有多集中或多分散，直接取決於 regularization 強度 $\lambda$** [CS231n linear-classify "SVM vs. Softmax"]。

| 分數 | 取指數 | 正規化後的「機率」 |
|---|---|---|
| (1, −2, 0) | (2.71, 0.14, 1) | (0.7, 0.04, 0.26) |
| (0.5, −1, 0)：權重減半 | (1.65, 0.37, 1) | (0.55, 0.12, 0.33)：變得更分散 |

（數值依據 [CS231n linear-classify "SVM vs. Softmax"]。）

$\lambda$ 越大，權重越小，「機率」就越平均。權重趨近於 0 時，輸出會接近均勻分布 [CS231n linear-classify "SVM vs. Softmax"]。

**結論**：最好把 softmax 的輸出看成**信心程度**。和 SVM 一樣，**分數的排序可以解讀，但絕對數值（或差值）在技術上不能直接解讀** [CS231n linear-classify "SVM vs. Softmax"]。

## 實作：數值穩定性

$e^{f_{y_i}}$ 和 $\sum_j e^{f_j}$ 可能大到溢位。解法是在分子和分母同乘一個常數 $C$，結果不變 [CS231n linear-classify "Softmax classifier"]：

$$
\frac{e^{f_{y_i}}}{\sum_j e^{f_j}} = \frac{e^{f_{y_i} + \log C}}{\sum_j e^{f_j + \log C}}
$$

常見做法是取 $\log C = -\max_j f_j$，也就是**先把分數平移，讓最大值變成 0**。例如分數 (123, 456, 789) 直接取指數會溢位；平移成 (−666, −333, 0) 之後再算，就安全了 [CS231n linear-classify "Softmax classifier"]。

## 名稱容易混淆

- **SVM classifier** 用的是 **hinge loss**，也叫 max-margin loss [CS231n linear-classify "Softmax classifier"]。
- **Softmax classifier** 用的是 **cross-entropy loss**。它的名字來自 softmax 函數，也就是把分數壓成機率的那一步 [CS231n linear-classify "Softmax classifier"]。
- 所以嚴格來說，「softmax loss」這個說法不太對，因為 softmax 只是壓縮函數，不是 loss。不過這是很常見的簡稱 [CS231n linear-classify "Softmax classifier"]。

## 出現在哪些地方

- [Loss Function](loss-function.md)：和 SVM loss 的比較
- [Linear Classifier](linear-classifier.md)：Softmax classifier = linear score function + cross-entropy loss
- [Regularization](regularization.md)：λ 會影響輸出「機率」的分散程度

## 常見誤解

- **「softmax 輸出 0.9，表示模型有 90% 的機率是對的」**：不一定。這個數值會隨著 regularization 強度改變，只能當作相對的信心程度 [CS231n linear-classify "SVM vs. Softmax"]。
