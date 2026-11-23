---
title: ILSVRC
type: dataset
year: unknown
size: 1.2 million training images
num_classes: "1000"
tasks: [image-classification]
aliases: [ILSVRC challenge]
tags: [dataset, large-scale, classification]
sources: [CS231n]
related:
  - concepts/gradient-descent.md
  - tasks/image-classification.md
created: 2026-11-23
updated: 2026-11-23
---

# ILSVRC

> 這一頁目前**內容很少**：只依據 CS231n optimization-1 中順帶提到的資訊建立。之後有來源詳細介紹這個資料集或比賽時，再補充。
> 依照 schema，目前的來源**沒有提到「ImageNet」這個名稱**，所以這頁暫時不寫 ILSVRC 和 ImageNet 的關係。

## 一句話說明

CS231n 用來舉例的**大規模**影像分類挑戰賽，訓練資料約有 120 萬張影像 [CS231n optimization-1 "Gradient Descent"]。

## 規模與組成

| 項目 | 數值 |
|---|---|
| 訓練影像數 | 1.2 million [CS231n optimization-1 "Gradient Descent"] |
| 類別數 | 1000 |
| 其他（解析度、val／test 切分、年份） | unknown（目前的來源沒有提供） |

類別數的依據：筆記的思想實驗說，假設 120 萬張影像其實是「1000 張不同影像，每類一張」的複本，每張各有 1200 份 [CS231n optimization-1 "Gradient Descent"]。「每類一張、共 1000 張」代表有 1000 個類別。原文沒有直接寫「1000 個類別」，這是從思想實驗的敘述推得的（綜合推論，依據 [CS231n optimization-1 "Gradient Descent"]）。

## 用途

- [Image Classification](../tasks/image-classification.md)：大規模影像分類。

## 在 Wiki 中的使用

- [Gradient Descent](../concepts/gradient-descent.md)：CS231n 用 ILSVRC 說明為什麼需要 **mini-batch**。訓練資料多達百萬筆，只為了更新一步就算完整個 training set 的 loss，很浪費 [CS231n optimization-1 "Gradient Descent"]。
- （截至 CS231n 筆記撰寫時）當時 state of the art 的 ConvNets 在這個規模上訓練，典型的 batch 大小是 256 [CS231n optimization-1 "Gradient Descent"]。

## 和 CIFAR-10 的對比

| | [CIFAR-10](cifar-10.md) | ILSVRC |
|---|---|---|
| 訓練影像數 | 50,000 [CS231n classification "Nearest Neighbor Classifier"] | 1.2 million [CS231n optimization-1 "Gradient Descent"] |
| 類別數 | 10 [CS231n classification "Nearest Neighbor Classifier"] | 1000（推得，見上方） |
| CS231n 的定位 | toy dataset [CS231n classification "Nearest Neighbor Classifier"] | 大規模應用的例子 [CS231n optimization-1 "Gradient Descent"] |

## 限制與注意事項

- 本頁只依據一份來源中順帶提到的資訊，內容很不完整。
