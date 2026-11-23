---
title: Pooling Layer
type: concept
first_introduced: unknown
aliases: [POOL layer, pooling, 池化層, max pooling, average pooling, downsampling]
tags: [cnn, layer]
sources: [CS231n]
related:
  - concepts/convolutional-neural-network.md
  - concepts/convolutional-layer.md
  - concepts/backpropagation.md
  - concepts/overfitting.md
created: 2026-11-23
updated: 2026-11-23
---

# Pooling Layer（池化層）

## 一句話說明

逐步縮小特徵圖的空間尺寸（width、height），以減少參數和計算量，也藉此控制 [overfitting](overfitting.md) [CS231n convolutional-networks "Pooling Layer"]。

## 直觀理解

把一張圖切成很多 2 × 2 的小方格，每格只留下最大的那個數字。圖的長和寬各縮小一半，但「這一區有沒有強烈的反應」這個資訊被保留下來了。

筆記的範例：一個 4 × 4 的 depth slice，用 2 × 2、stride 2 的 max pooling，切成 4 個方格，各取最大值，得到 2 × 2 的結果 (6, 8, 3, 4) [CS231n convolutional-networks "Pooling Layer" 圖]。

## 技術細節

### 怎麼運作

- 在 CNN 中，通常會在連續的 conv 層之間**定期插入** pooling 層 [CS231n convolutional-networks "Pooling Layer"]。
- 它**對每個 depth slice 獨立運作**，只縮小空間尺寸，**depth 不變** [CS231n convolutional-networks "Pooling Layer"]。例如 224 × 224 × 64 的輸入，經過 2 × 2、stride 2 的 pooling，變成 112 × 112 × 64 [CS231n convolutional-networks "Pooling Layer" 圖]。
- 最常見的形式是 2 × 2、stride 2：長寬各縮小一半，**丟掉 75% 的 activation**，每個 max 運算從 4 個數字中取最大值 [CS231n convolutional-networks "Pooling Layer"]。

### 規格

| 項目 | 內容 |
|---|---|
| 輸入 | $W_1 \times H_1 \times D_1$ |
| 2 個 hyperparameter | 大小 $F$、stride $S$ |
| 輸出 | $W_2 = (W_1 - F)/S + 1$，$H_2$ 同理，$D_2 = D_1$ |
| 參數 | **0 個**，因為它是輸入的固定函數 |
| Padding | pooling 層通常不做 zero-padding |

（依據 [CS231n convolutional-networks "Pooling Layer"]。）

實務上常見的只有兩種設定 [CS231n convolutional-networks "Pooling Layer"]：

- $F = 2, S = 2$：最常見。
- $F = 3, S = 2$：也叫 **overlapping pooling**。

更大的 pooling 範圍**破壞性太強**，通常會讓效能變差 [CS231n convolutional-networks "Pooling Layer"; CS231n convolutional-networks "Layer Sizing Patterns"]。

### 其他 pooling 方式

除了 max pooling，也可以用 **average pooling** 或 **L2-norm pooling**。average pooling 以前很常用，但（截至 CS231n 筆記撰寫時）已經比較少用了，因為實務上 max pooling 的效果比較好 [CS231n convolutional-networks "Pooling Layer"]。

### Backward pass

在 [backpropagation](backpropagation.md) 頁提過，$\max(x, y)$ 的 backward 只會把 [gradient](gradient-descent.md) **傳給 forward 時值最大的那個輸入**。所以 pooling 層在 forward 時，通常會記下每個最大值的位置（有時叫做 **switches**），讓 backward 時能有效率地把 gradient 傳到正確的位置 [CS231n convolutional-networks "Pooling Layer"]。

### 不用 pooling 的主張

很多人不喜歡 pooling，認為沒有它也行 [CS231n convolutional-networks "Pooling Layer"]：

- *Striving for Simplicity: The All Convolutional Net* 主張完全拿掉 pooling 層，只用重複的 conv 層，偶爾用比較大的 stride 來縮小尺寸 [CS231n convolutional-networks "Pooling Layer"]。
- 在訓練好的生成模型（例如 VAE、GAN）時，拿掉 pooling 層也被發現很重要 [CS231n convolutional-networks "Pooling Layer"]。
- （截至 CS231n 筆記撰寫時）筆記預測，未來的架構很可能只有很少，甚至沒有 pooling 層 [CS231n convolutional-networks "Pooling Layer"]。

這是筆記撰寫當時的預測，本 Wiki 目前沒有來源可以驗證後來的發展。

## 出現在哪些地方

- [Convolutional Neural Network](convolutional-neural-network.md)：在架構中負責縮小空間尺寸
- [Convolutional Layer](convolutional-layer.md)：pooling 通常接在 conv 層之後；conv 層用 stride 1 維持尺寸，縮小的工作交給 pooling
- [Backpropagation](backpropagation.md)：max pooling 的 backward 就是 max gate 的模式
