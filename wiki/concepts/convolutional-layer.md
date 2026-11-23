---
title: Convolutional Layer
type: concept
first_introduced: unknown
aliases: [CONV layer, conv layer, 卷積層, convolution, filter, kernel, receptive field, parameter sharing, stride, zero-padding, 1x1 convolution, dilated convolution, im2col]
tags: [cnn, layer, foundation]
sources: [CS231n]
related:
  - concepts/convolutional-neural-network.md
  - concepts/pooling-layer.md
  - concepts/backpropagation.md
  - models/alexnet.md
  - concepts/hyperparameter-tuning.md
created: 2026-11-23
updated: 2026-11-23
---

# Convolutional Layer（卷積層）

## 一句話說明

CNN 的核心元件：用一組**小的、可學習的 filter**，在輸入上逐一滑過，每到一個位置就算一次內積，產生一張「這個 filter 在哪裡有反應」的 activation map [CS231n convolutional-networks "Convolutional Layer"]。

## 直觀理解

想像你拿著一張小小的透明片（filter），上面畫著某種圖案，例如一條斜線。你把它在照片上從左到右、從上到下慢慢移動，每到一個位置就看看「這裡和透明片上的圖案有多像」，把結果記在一張新的圖上。這張新的圖，就是 **activation map**：它告訴你照片的哪些地方有斜線。

Conv layer 就是同時拿著很多張不同的透明片（例如 12 個 filter），各自產生一張 activation map，再把它們疊起來，成為輸出的 volume [CS231n convolutional-networks "Convolutional Layer"]。

網路會自己學出這些 filter：在第一層，可能學到某個方向的邊緣、某種顏色的色塊；到了較高的層，可能學到蜂巢狀或輪子狀的圖案 [CS231n convolutional-networks "Convolutional Layer"]。

筆記展示了 AlexNet 第一層學到的 96 個 filter（每個 11 × 11 × 3）：上半部大多是各種方向的黑白條紋（邊緣偵測器），下半部則有很多彩色的色塊 [CS231n convolutional-networks "Convolutional Layer" 圖]。

Conv layer 是 CNN 中**計算量最大**的部分 [CS231n convolutional-networks "Convolutional Layer"]。

## 技術細節

### Local connectivity：只看一小塊區域

處理影像這種高維輸入時，讓每個 neuron 連到上一層的所有 neuron 並不實際。所以每個 neuron 只連到輸入 volume 的**一小塊區域**，這個區域的大小是一個 hyperparameter，叫做 **receptive field**，也就是 filter 的大小 [CS231n convolutional-networks "Convolutional Layer"]。

重要的不對稱：連接在**空間上是局部的**（width、height），但在 **depth 方向上永遠是完整的** [CS231n convolutional-networks "Convolutional Layer"]。

| 例子 | 輸入 volume | filter 大小 | 每個 neuron 的權重數 |
|---|---|---|---|
| 1 | 32 × 32 × 3 | 5 × 5 | 5 × 5 × 3 = 75（再加 1 個 bias） |
| 2 | 16 × 16 × 20 | 3 × 3 | 3 × 3 × 20 = 180 |

（依據 [CS231n convolutional-networks "Convolutional Layer"]。）

### 輸出的大小：depth、stride、zero-padding

三個 hyperparameter 控制輸出 volume 的大小 [CS231n convolutional-networks "Convolutional Layer"]：

1. **Depth**：filter 的數量。看著輸入同一個區域的一整排 neuron，叫做 **depth column**（也叫 fibre）。
2. **Stride**：filter 每次移動幾個像素。stride 1 一次移一格；stride 2 一次跳兩格（3 以上很少見），輸出會比較小。
3. **Zero-padding**：在輸入的邊緣補 0。最常見的用途是讓輸出和輸入的空間尺寸**完全相同**。

**輸出大小的公式** [CS231n convolutional-networks "Convolutional Layer"]：

$$
\text{輸出大小} = \frac{W - F + 2P}{S} + 1
$$

其中 W 是輸入大小、F 是 filter 大小、S 是 stride、P 是 padding。

| 輸入 W | filter F | padding P | stride S | 輸出 |
|---|---|---|---|---|
| 7 | 3 | 0 | 1 | 5 |
| 7 | 3 | 0 | 2 | 3 |
| 5 | 3 | 1 | 1 | 5（和輸入一樣大） |
| 5 | 3 | 1 | 2 | 3 |
| 10 | 3 | 0 | 2 | **4.5：不是整數，這組設定無效** |

（依據 [CS231n convolutional-networks "Convolutional Layer"]。）

- **讓輸出和輸入一樣大**：stride 1 時，設 $P = (F - 1)/2$ [CS231n convolutional-networks "Convolutional Layer"]。
- **算出來不是整數**：代表 neuron 沒辦法整齊、對稱地「排進」輸入，這組 hyperparameter 是無效的。函式庫可能會報錯，或自動補 0、裁切輸入 [CS231n convolutional-networks "Convolutional Layer"]。

筆記用一維的例子示意：輸入 5 個數字、兩側各補一個 0，filter 權重是 (1, 0, −1)、bias 是 0。stride 1 時輸出 5 個數字，stride 2 時輸出 3 個數字；stride 3 則不行，因為 (5 − 3 + 2) = 4 不能被 3 整除 [CS231n convolutional-networks "Convolutional Layer" 圖]。

### Parameter sharing：同一個 filter 到處用

以 AlexNet 的第一層為例，輸出是 55 × 55 × 96 的 volume [CS231n convolutional-networks "Convolutional Layer"]：

| | neuron 數 | 每個 neuron 的參數 | 第一層的參數總數 |
|---|---|---|---|
| **不共用參數** | 55 × 55 × 96 = 290,400 | 11 × 11 × 3 = 363 個權重 + 1 個 bias | 105,705,600 |
| **共用參數** | （同上） | 每個 depth slice 共用一組 | 96 × 11 × 11 × 3 = 34,848 個權重，加上 96 個 bias，共 34,944 |

（依據 [CS231n convolutional-networks "Convolutional Layer"]。）

**為什麼可以共用？** 一個合理的假設：如果某個特徵在位置 (x, y) 有用，在其他位置 (x2, y2) 也應該有用 [CS231n convolutional-networks "Convolutional Layer"]。例如偵測水平邊緣在影像某處很重要，在其他地方應該也一樣，因為影像具有平移不變（translationally-invariant）的結構。所以沒有必要在 55 × 55 個位置分別學一次「怎麼偵測水平邊緣」[CS231n convolutional-networks "Convolutional Layer" 圖]。

具體做法：同一個 **depth slice**（例如 55 × 55 × 96 的 volume 有 96 個 depth slice，每個是 55 × 55）中的所有 neuron 都用同一組權重和 bias [CS231n convolutional-networks "Convolutional Layer"]。backprop 時，每個 neuron 各自算出自己權重的 [gradient](gradient-descent.md)，再把同一個 depth slice 的 gradient **加總**，只更新一組權重 [CS231n convolutional-networks "Convolutional Layer"]。

**名稱的由來**：同一個 depth slice 共用一組權重，所以 forward 的計算就等於把這組權重和輸入做**卷積（convolution）**，這就是 Convolutional Layer 這個名稱的由來。這組權重也因此被稱為 **filter** 或 **kernel** [CS231n convolutional-networks "Convolutional Layer"]。

**什麼時候不適合共用？** 當輸入影像有特定的置中結構時，例如**已經置中的人臉**，不同位置應該學到完全不同的特徵（眼睛、頭髮）。這時通常會放寬參數共用，這種層叫做 **Locally-Connected Layer** [CS231n convolutional-networks "Convolutional Layer"]。

### 總結：Conv layer 的規格

| 項目 | 內容 |
|---|---|
| 輸入 | $W_1 \times H_1 \times D_1$ |
| 4 個 hyperparameter | filter 數 $K$、filter 大小 $F$、stride $S$、padding $P$ |
| 輸出 | $W_2 = (W_1 - F + 2P)/S + 1$，$H_2$ 同理，$D_2 = K$ |
| 參數量（共用參數） | 每個 filter 有 $F \cdot F \cdot D_1$ 個權重；總共 $(F \cdot F \cdot D_1) \cdot K$ 個權重和 $K$ 個 bias |

（依據 [CS231n convolutional-networks "Convolutional Layer"]。）

常見的設定是 $F = 3$、$S = 1$、$P = 1$ [CS231n convolutional-networks "Convolutional Layer"]。這些 conv hyperparameter 的選法，詳見 [CNN](convolutional-neural-network.md) 頁的「尺寸規則」。

### 實作：用矩陣乘法計算（im2col）

卷積本質上就是 filter 和輸入局部區域的內積，所以常見的實作方式是把它轉成**一次大的矩陣乘法** [CS231n convolutional-networks "Convolutional Layer"]：

1. **im2col**：把輸入中每個局部區域拉成一行。以 AlexNet 第一層為例，每個 11 × 11 × 3 的區域拉成長度 363 的向量，共有 55 × 55 = 3025 個位置，得到 363 × 3025 的矩陣。
2. 把 96 個 filter 也各拉成一列，得到 96 × 363 的矩陣。
3. 兩者相乘，得到 96 × 3025 的結果。
4. 再 reshape 回 55 × 55 × 96。

缺點是很耗記憶體，因為區域互相重疊，同一個輸入數值會被複製很多次；優點是可以利用高度最佳化的矩陣乘法函式庫（例如 BLAS）[CS231n convolutional-networks "Convolutional Layer"]。

### Backward pass

卷積的 backward（不論是對資料還是對權重）**也是一個卷積**，只是 filter 要在空間上翻轉 [CS231n convolutional-networks "Convolutional Layer"]。這延續了 [backpropagation](backpropagation.md) 頁「每個 gate 只需要知道自己的 local gradient」的觀點。

### 1×1 convolution

1×1 conv 最早由 Network in Network 研究 [CS231n convolutional-networks "Convolutional Layer"]。從訊號處理的角度看會覺得奇怪，因為在 2D 訊號上，1×1 卷積只是逐點縮放。但在 CNN 中，filter 永遠貫穿完整的 depth，所以對 32 × 32 × 3 的輸入做 1×1 conv，實際上是在做 **3 維的內積** [CS231n convolutional-networks "Convolutional Layer"]。

### Dilated convolution

（截至 CS231n 筆記撰寫時）較新的發展之一，是在 conv 層多加一個 hyperparameter：**dilation**，讓 filter 的每一格之間有間隔 [CS231n convolutional-networks "Convolutional Layer"]。

- 疊兩層 3×3 conv，第二層 neuron 的 **effective receptive field** 是 5×5。
- 用 dilated convolution 的話，effective receptive field 會成長得快很多，可以用比較少的層，更積極地整合空間資訊 [CS231n convolutional-networks "Convolutional Layer"]。

## 出現在哪些地方

- [Convolutional Neural Network](convolutional-neural-network.md)：conv layer 是 CNN 的核心
- [AlexNet](../models/alexnet.md)：本頁大部分數字範例都來自 AlexNet 的第一層
- [Pooling Layer](pooling-layer.md)：通常接在 conv 層之後
- [Hyperparameter Tuning](hyperparameter-tuning.md)：K、F、S、P 都是 hyperparameter

## 常見誤解

- **「depth 是指網路有幾層」**：在 CNN 的 volume 中，depth 指的是第三個維度（例如 RGB 的 3、filter 的數量），不是網路的層數 [CS231n convolutional-networks "Architecture Overview"]。
- **「filter 只在 2D 上滑動，所以只處理一個顏色通道」**：filter 在空間上滑動，但永遠貫穿**完整的 depth** [CS231n convolutional-networks "Convolutional Layer"]。
