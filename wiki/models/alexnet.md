---
title: AlexNet
type: model
year: 2012
family: cnn
tasks: [image-classification]
aliases: [Krizhevsky et al.]
tags: [cnn, classic, ilsvrc-winner]
sources: [CS231n]
related:
  - concepts/convolutional-neural-network.md
  - concepts/convolutional-layer.md
  - models/vggnet.md
  - datasets/ilsvrc.md
  - concepts/activation-function.md
created: 2026-11-23
updated: 2026-11-23
---

# AlexNet

> 本頁目前只依據 **CS231n convolutional-networks 筆記**。raw 中已有 AlexNet 原始論文，**ingest 之後要核對**本頁的數字，以及下方「待核對」一節的問題。

## 一句話說明

**第一個讓 CNN 在 Computer Vision 中流行起來的工作**，由 Alex Krizhevsky、Ilya Sutskever 和 Geoff Hinton 開發，在 ILSVRC 2012 以大幅領先的成績勝出 [CS231n convolutional-networks "Case studies"]。

## 直觀理解

在 AlexNet 之前，CNN 已經存在（LeNet，1990 年代），但主要用在讀郵遞區號、數字這類任務 [CS231n convolutional-networks "Case studies"]。AlexNet 把 CNN 帶到大規模的影像分類比賽 [ILSVRC](../datasets/ilsvrc.md)，而且贏得很明顯：

| | top-5 error |
|---|---|
| AlexNet（ILSVRC 2012） | 16% |
| 第二名 | 26% |

（依據 [CS231n convolutional-networks "Case studies"]。）

## 要解決的問題

目前的來源沒有詳細說明 AlexNet 的動機。CS231n 的描述是：AlexNet 的架構和 LeNet 很相似，但**更深、更大**，而且把 conv 層**一層一層疊起來**；在那之前，常見的做法是每個 conv 層後面都馬上接一個 [pool 層](../concepts/pooling-layer.md) [CS231n convolutional-networks "Case studies"]。

## 架構細節

### 第一層 conv

CS231n 用 AlexNet 的第一層，當作 [conv layer](../concepts/convolutional-layer.md) 的真實範例 [CS231n convolutional-networks "Convolutional Layer"]：

| 項目 | 數值 |
|---|---|
| 輸入影像 | 227 × 227 × 3 |
| receptive field（filter 大小）F | 11 |
| stride S | 4 |
| zero-padding P | 0 |
| filter 數 K（depth） | 96 |
| 輸出 volume | 55 × 55 × 96，因為 (227 − 11)/4 + 1 = 55 |

（依據 [CS231n convolutional-networks "Convolutional Layer"]。）

- 第一層如果不共用參數，會有 105,705,600 個參數；共用之後只剩 34,944 個 [CS231n convolutional-networks "Convolutional Layer"]。詳見 [Convolutional Layer](../concepts/convolutional-layer.md) 的 parameter sharing 一節。
- 學出來的 96 個 filter，每個都是 11 × 11 × 3，每個 filter 被一個 depth slice 中的 55 × 55 個 neuron 共用 [CS231n convolutional-networks "Convolutional Layer" 圖]。視覺化後可以看到各種方向的邊緣和色塊 [CS231n convolutional-networks "Convolutional Layer" 圖]。
- 第一層用 11 × 11 的大 filter 和 stride 4，是為了節省記憶體而做的妥協。CS231n 指出，實務上這種妥協通常只出現在網路的第一層 [CS231n convolutional-networks "Layer Sizing Patterns"]。

### 最後幾層

AlexNet 最後有兩個大小 4096 的 FC 層，接著是一個 1000 個 neuron 的 FC 層，用來計算類別分數 [CS231n convolutional-networks "Converting FC layers to CONV layers"]。

### 參數量

AlexNet 約有 60M 個參數 [CS231n convolutional-networks "Case studies"]。相比之下，GoogLeNet 只有 4M [CS231n convolutional-networks "Case studies"]。

## 實驗結果

- ILSVRC 2012：top-5 error 16%，第二名 26% [CS231n convolutional-networks "Case studies"]。
- 更詳細的實驗結果，目前的來源沒有提供。

## 在演進中的位置

- **前身**：LeNet（1990 年代，Yann LeCun）[CS231n convolutional-networks "Case studies"]。
- **後繼**：
  - ZFNet（ILSVRC 2013 冠軍）：調整 AlexNet 的架構 hyperparameter，把中間的 conv 層變大，第一層的 stride 和 filter 變小 [CS231n convolutional-networks "Case studies"]。
  - [VGGNet](vggnet.md)、GoogLeNet（ILSVRC 2014）。
- 詳見 [CNN](../concepts/convolutional-neural-network.md) 頁的「經典架構的演進」表。

## 待核對：來源中與 AlexNet 有關的不一致

### 1. 輸入影像是 224 還是 227？

CS231n 指出，AlexNet 論文寫的輸入影像大小是 224 × 224，但這「一定是錯的」，因為 (224 − 11)/4 + 1 不是整數。筆記作者自己的猜測是，Alex 用了論文中沒有提到的 3 個像素的 zero-padding [CS231n convolutional-networks "Convolutional Layer"]。

這是筆記作者的推測。raw 中有 AlexNet 原始論文，ingest 時要確認論文實際的寫法。

### 2. 「5 個 pooling 層、7 × 7 × 512」的描述

在「FC 層轉成 Conv 層」一節，筆記說 AlexNet 是用 5 個 pooling 層、每次縮小一半，把 224 × 224 的影像縮成 7 × 7 × 512（224/2/2/2/2/2 = 7）[CS231n convolutional-networks "Converting FC layers to CONV layers"]。

> 這段描述和同一篇筆記的其他內容對不上：
> - 同一篇筆記說 AlexNet 的**第一層 conv 就用了 stride 4**，把 227 × 227 縮成 55 × 55 [CS231n convolutional-networks "Convolutional Layer"]。第一層已經縮小約 4 倍，和「全部靠 5 個 pooling 各縮小一半」互相矛盾。
> - 「5 個 2 × 2 pooling、最後是 7 × 7 × 512」和同一篇筆記的 **VGGNet 逐層表格**完全吻合（VGGNet 有 5 個 POOL2，最後一個 POOL2 的輸出是 7 × 7 × 512）[CS231n convolutional-networks "Case studies"]。
>
> 所以這一段描述的看起來比較像 VGGNet 的架構，而不是 AlexNet（綜合推論，依據 [CS231n convolutional-networks "Convolutional Layer"; CS231n convolutional-networks "Converting FC layers to CONV layers"; CS231n convolutional-networks "Case studies"]）。這一點同樣要在 ingest AlexNet 論文時核對。

### Activation function：ReLU

neural-networks-1 引用 Krizhevsky et al.（AlexNet）論文的一張圖：在相同的 training error 下，ReLU 的收斂速度約是 tanh 的 6 倍 [CS231n neural-networks-1 "Commonly used activation functions" 圖]。內文則寫成「和 sigmoid/tanh 相比」[CS231n neural-networks-1 "Commonly used activation functions"]，但圖中只有 ReLU 和 tanh 兩條曲線。這一點也要在 ingest AlexNet 論文時核對。詳見 [Activation Function](../concepts/activation-function.md)。

## 限制與後續批評

- 參數量大（約 60M），GoogLeNet 用 4M 參數就贏了 ILSVRC 2014 [CS231n convolutional-networks "Case studies"]。

## 相關概念

- [Convolutional Neural Network](../concepts/convolutional-neural-network.md)
- [Convolutional Layer](../concepts/convolutional-layer.md)
- [ILSVRC](../datasets/ilsvrc.md)
