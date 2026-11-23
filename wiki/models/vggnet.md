---
title: VGGNet
type: model
year: 2014
family: cnn
tasks: [image-classification]
aliases: [VGG, VGG Net]
tags: [cnn, classic, depth]
sources: [CS231n]
related:
  - concepts/convolutional-neural-network.md
  - concepts/convolutional-layer.md
  - concepts/pooling-layer.md
  - models/alexnet.md
  - datasets/ilsvrc.md
created: 2026-11-23
updated: 2026-11-23
---

# VGGNet

> 本頁目前只依據 **CS231n convolutional-networks 筆記**。

## 一句話說明

ILSVRC 2014 的亞軍，由 Karen Simonyan 和 Andrew Zisserman 提出。它最主要的貢獻，是證明了**網路的深度是好效能的關鍵** [CS231n convolutional-networks "Case studies"]。

## 直觀理解

VGGNet 的架構非常「規律」：從頭到尾**只用 3 × 3 的 conv 和 2 × 2 的 pooling** [CS231n convolutional-networks "Case studies"]。它把 [CNN](../concepts/convolutional-neural-network.md) 頁介紹的設計原則（小 filter、stride 1、用 padding 維持尺寸、只靠 pooling 縮小）幾乎完全照做。

為什麼只用 3 × 3？CNN 頁的「用多個小 filter 取代一個大 filter」一節說明了：三層 3 × 3 的感受野和一層 7 × 7 一樣，但非線性更多、參數更少 [CS231n convolutional-networks "Layer Patterns"]。

## 架構細節

所有 conv 層都是 3 × 3、stride 1、pad 1；所有 pool 層都是 2 × 2 的 max pooling、stride 2、不 padding [CS231n convolutional-networks "Case studies"]。最好的網路共有 16 個 CONV／FC 層 [CS231n convolutional-networks "Case studies"]。

CS231n 逐層列出了每一層的輸出大小、記憶體（activation 的數量）和權重數：

| 層 | 輸出 | memory | weights |
|---|---|---|---|
| INPUT | 224 × 224 × 3 | 150K | 0 |
| CONV3-64 ×2 | 224 × 224 × 64 | 3.2M（每層） | 1,728／36,864 |
| POOL2 | 112 × 112 × 64 | 800K | 0 |
| CONV3-128 ×2 | 112 × 112 × 128 | 1.6M（每層） | 73,728／147,456 |
| POOL2 | 56 × 56 × 128 | 400K | 0 |
| CONV3-256 ×3 | 56 × 56 × 256 | 800K（每層） | 294,912／589,824／589,824 |
| POOL2 | 28 × 28 × 256 | 200K | 0 |
| CONV3-512 ×3 | 28 × 28 × 512 | 400K（每層） | 1,179,648／2,359,296／2,359,296 |
| POOL2 | 14 × 14 × 512 | 100K | 0 |
| CONV3-512 ×3 | 14 × 14 × 512 | 100K（每層） | 2,359,296（每層） |
| POOL2 | 7 × 7 × 512 | 25K | 0 |
| FC | 1 × 1 × 4096 | 4096 | 102,760,448 |
| FC | 1 × 1 × 4096 | 4096 | 16,777,216 |
| FC | 1 × 1 × 1000 | 1000 | 4,096,000 |
| **總計** | | **24M × 4 bytes ≈ 93MB／張影像（只算 forward，backward 約 ×2）** | **138M** |

（表中數值依據 [CS231n convolutional-networks "Case studies"]。原文是逐層列出，這裡把相同的連續層合併成一列。）

> **記憶體總量的驗算**：把表中每一層的 memory 逐一相加（150K + 2 × 3.2M + 800K + 2 × 1.6M + 400K + 3 × 800K + 200K + 3 × 400K + 100K + 3 × 100K + 25K + 4096 + 4096 + 1000），總和約為 **15.2M**，不是表格最後寫的 24M；以每個值 4 bytes 計算約 58MB，而不是 93MB。權重總數則驗算正確（138,344,128，約 138M）。原文沒有說明 24M 是怎麼算的，可能包含了表格沒有列出的部分，本 Wiki 不推測原因（綜合推論，依據 [CS231n convolutional-networks "Case studies"]）。

### 記憶體和參數分布在哪裡

這是 CNN 的典型特徵 [CS231n convolutional-networks "Case studies"]：

- **大部分的記憶體**（以及計算時間）用在**前面的 conv 層**。
- **大部分的參數**在**最後的 FC 層**。以 VGGNet 來說，第一個 FC 層就有約 100M 個權重，全部約 140M [CS231n convolutional-networks "Case studies"]。

> **參數總數的兩種寫法**：表格最後寫 138M，內文則寫「全部約 140M」，介紹段落也寫 140M [CS231n convolutional-networks "Case studies"]。兩者是同一個數字的精確值和概略值。

## 實驗結果

- ILSVRC 2014 亞軍 [CS231n convolutional-networks "Case studies"]。目前的來源沒有提供具體的 error 數字。

## 在演進中的位置

- **同期**：GoogLeNet 是 ILSVRC 2014 冠軍，參數只有 4M [CS231n convolutional-networks "Case studies"]。
- **前身**：[AlexNet](alexnet.md)（ILSVRC 2012）、ZFNet（ILSVRC 2013）。
- **後繼**：ResNet（ILSVRC 2015 冠軍）[CS231n convolutional-networks "Case studies"]。
- 筆記中示範 CNN 運作的示意圖，用的就是一個小型的 VGG Net [CS231n convolutional-networks "Layers used to build ConvNets" 圖]。

## 限制與後續批評

- 評估成本比較高，記憶體和參數用量也大很多 [CS231n convolutional-networks "Case studies"]。
- 大部分參數集中在第一個 FC 層；後來發現**拿掉這些 FC 層並不會降低效能**，可以大幅減少需要的參數 [CS231n convolutional-networks "Case studies"]。
- 預訓練好的模型可以在 Caffe 中直接使用 [CS231n convolutional-networks "Case studies"]。

## 相關概念

- [Convolutional Neural Network](../concepts/convolutional-neural-network.md)：設計原則
- [Convolutional Layer](../concepts/convolutional-layer.md)、[Pooling Layer](../concepts/pooling-layer.md)
- [ILSVRC](../datasets/ilsvrc.md)
