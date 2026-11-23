---
title: ILSVRC
type: dataset
year: unknown
size: 1.2 million training images
num_classes: "1000"
tasks: [image-classification]
aliases: [ILSVRC challenge, ImageNet ILSVRC challenge, ImageNet challenge]
tags: [dataset, benchmark, large-scale, classification]
sources: [CS231n]
related:
  - concepts/gradient-descent.md
  - tasks/image-classification.md
  - concepts/convolutional-neural-network.md
  - models/alexnet.md
  - models/vggnet.md
created: 2026-11-23
updated: 2026-11-23
---

# ILSVRC

> 這一頁的內容來自 CS231n 筆記中順帶提到的資訊，**還沒有來源完整介紹這個資料集或比賽**。
> CS231n convolutional-networks 筆記把它稱為「**ImageNet** ILSVRC challenge」、「the ImageNet challenge」[CS231n convolutional-networks "Case studies"; CS231n convolutional-networks "Convolutional Layer"]，所以 ILSVRC 是和 ImageNet 有關的挑戰賽。但 **ImageNet 資料集本身**（規模、建立方式）目前的來源沒有介紹，所以本頁還不寫 ImageNet 的細節。

## 一句話說明

大規模的影像分類挑戰賽。歷年的冠軍架構（AlexNet、ZFNet、GoogLeNet、ResNet）構成了 CNN 發展的主線 [CS231n convolutional-networks "Case studies"]。

## 規模與組成

| 項目 | 數值 |
|---|---|
| 訓練影像數 | 1.2 million [CS231n optimization-1 "Gradient Descent"] |
| 類別數 | 1000（見下方說明） |
| 常見的輸入影像大小 | 224 × 224（常見的 ImageNet ConvNets）[CS231n convolutional-networks "Layer Sizing Patterns"] |
| 解析度、val／test 切分、年份 | unknown（目前的來源沒有提供） |

**類別數的依據**：目前的來源沒有直接寫「ILSVRC 有 1000 個類別」，但有兩個線索：
- optimization-1 的思想實驗說，假設 120 萬張影像其實是「1000 張不同影像，**每類一張**」的複本 [CS231n optimization-1 "Gradient Descent"]。
- AlexNet 最後的 FC 層有 **1000 個 neuron，用來計算類別分數** [CS231n convolutional-networks "Converting FC layers to CONV layers"]。

兩者都指向 1000 個類別（綜合推論，依據 [CS231n optimization-1 "Gradient Descent"; CS231n convolutional-networks "Converting FC layers to CONV layers"]）。

## 用途

- [Image Classification](../tasks/image-classification.md)：大規模影像分類的 benchmark。
- 評估指標：CS231n 提到 AlexNet 的成績時用的是 **top-5 error** [CS231n convolutional-networks "Case studies"]。目前的來源沒有定義 top-5 error。

## 歷年成績（CNN 架構）

| 年份 | 架構 | 名次 | 備註 |
|---|---|---|---|
| 2012 | [AlexNet](../models/alexnet.md) | 第一（比第二名好很多） | top-5 error 16%，第二名 26% |
| 2013 | ZFNet | 冠軍 | 改良 AlexNet |
| 2014 | GoogLeNet | 冠軍 | 4M 參數 |
| 2014 | [VGGNet](../models/vggnet.md) | 亞軍 | 證明深度很重要 |
| 2015 | ResNet | 冠軍 | skip connections |

（表中內容依據 [CS231n convolutional-networks "Case studies"]。）

## 在 Wiki 中的使用

- [Gradient Descent](../concepts/gradient-descent.md)：CS231n 用 ILSVRC 說明為什麼需要 **mini-batch**。訓練資料多達百萬筆，只為了更新一步就算完整個 training set 的 loss，很浪費 [CS231n optimization-1 "Gradient Descent"]。
- （截至 CS231n 筆記撰寫時）當時 state of the art 的 ConvNets 在這個規模上訓練，典型的 batch 大小是 256 [CS231n optimization-1 "Gradient Descent"]。
- [CNN](../concepts/convolutional-neural-network.md)：CS231n 的實務建議是，直接使用（截至 CS231n 筆記撰寫時）在 ImageNet 上表現最好的預訓練模型，再用自己的資料 finetune [CS231n convolutional-networks "Layer Patterns"]。

## 和 CIFAR-10 的對比

| | [CIFAR-10](cifar-10.md) | ILSVRC |
|---|---|---|
| 訓練影像數 | 50,000 [CS231n classification "Nearest Neighbor Classifier"] | 1.2 million [CS231n optimization-1 "Gradient Descent"] |
| 類別數 | 10 [CS231n classification "Nearest Neighbor Classifier"] | 1000（推得，見上方） |
| 常見輸入大小 | 32 × 32 [CS231n convolutional-networks "Layer Sizing Patterns"] | 224 × 224 [CS231n convolutional-networks "Layer Sizing Patterns"] |
| CS231n 的定位 | toy dataset [CS231n classification "Nearest Neighbor Classifier"] | 大規模應用的例子 [CS231n optimization-1 "Gradient Descent"] |

## 限制與注意事項

- 本頁只依據 CS231n 筆記中順帶提到的資訊，內容不完整。特別是 ILSVRC 和 ImageNet 的確切關係、資料集的建立方式，都還沒有來源可以引用。
