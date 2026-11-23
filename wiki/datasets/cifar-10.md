---
title: CIFAR-10
type: dataset
year: unknown
size: 60,000 images
num_classes: 10
tasks: [image-classification]
aliases: [CIFAR10]
tags: [dataset, toy-dataset, classification]
sources: [CS231n]
related:
  - tasks/image-classification.md
  - concepts/k-nearest-neighbor.md
  - concepts/hyperparameter-tuning.md
  - concepts/linear-classifier.md
  - concepts/optimization.md
  - datasets/ilsvrc.md
created: 2026-11-22
updated: 2026-11-23
---

# CIFAR-10

## 一句話說明

一個常用的小型影像分類資料集，包含 10 個類別的 32 × 32 小圖。CS231n 稱它為「toy」資料集，適合拿來入門和快速做實驗 [CS231n classification "Nearest Neighbor Classifier"]。

## 規模與組成

| 項目 | 數值 |
|---|---|
| 影像總數 | 60,000 [CS231n classification "Nearest Neighbor Classifier"] |
| 解析度 | 32 × 32 像素，3 個顏色通道 [CS231n classification "Nearest Neighbor Classifier"] |
| 類別數 | 10 [CS231n classification "Nearest Neighbor Classifier"] |
| Training set | 50,000 張，每類 5,000 張 [CS231n classification "Nearest Neighbor Classifier"] |
| Test set | 10,000 張 [CS231n classification "Nearest Neighbor Classifier"] |
| 發布年份 | unknown（目前的來源沒有提供） |

10 個類別是 airplane、automobile、bird、cat、deer、dog、frog、horse、ship、truck [CS231n classification "Nearest Neighbor Classifier" 圖]。

攤平之後，每張影像是一個長度 32 × 32 × 3 = 3,072 的向量 [CS231n classification "Nearest Neighbor Classifier"]。

## 用途

- [Image Classification](../tasks/image-classification.md)：入門教學與方法比較的標準 benchmark。

## 在 Wiki 中的使用

| 方法 | 設定 | accuracy | 頁面 |
|---|---|---|---|
| 隨機猜測 | 10 類 | 10% [CS231n classification "Nearest Neighbor Classifier"] | |
| Nearest Neighbor | L1 距離 | 38.6% [CS231n classification "Nearest Neighbor Classifier"] | [kNN](../concepts/k-nearest-neighbor.md) |
| Nearest Neighbor | L2 距離 | 35.4% [CS231n classification "Nearest Neighbor Classifier"] | [kNN](../concepts/k-nearest-neighbor.md) |
| Linear classifier（SVM loss） | 用 random search 訓練（1000 次） | 約 15.5% [CS231n optimization-1 "Strategy #1: A first very bad idea solution: Random search"] | [Optimization](../concepts/optimization.md) |
| Linear classifier（SVM loss） | 用 random local search 訓練（1000 次） | 21.4% [CS231n optimization-1 "Strategy #2: Random Local Search"] | [Optimization](../concepts/optimization.md) |
| 人類 | 估計值 | 約 94% [CS231n classification "Nearest Neighbor Classifier"] | |
| CNN | （截至 CS231n 筆記撰寫時）state-of-the-art | 約 95% [CS231n classification "Nearest Neighbor Classifier"] | |

**Linear classifier 在 CIFAR-10 上的設定**：每張影像是 3072 × 1 的向量，W 是 10 × 3072，b 是 10 × 1；使用 bias trick 之後，分別變成 3073 × 1 和 10 × 3073 [CS231n linear-classify "Parameterized mapping from images to label scores"; CS231n linear-classify "Interpreting a linear classifier"]。W 加上 bias 共有 30,730 個參數 [CS231n optimization-1 "Visualizing the loss function"]。linear-classify 筆記**沒有提供** linear classifier 在 CIFAR-10 上的 accuracy；optimization-1 筆記則提供了用很差的最佳化方法訓練的結果，見下表。

**從學到的模板看資料集的特性**：linear classifier 學出的 car 模板是紅色的，這暗示 CIFAR-10 裡紅色的車比其他顏色多；horse 模板有兩個頭，反映資料中同時有朝左和朝右的馬 [CS231n linear-classify "Interpreting a linear classifier"]。詳見 [Linear Classifier](../concepts/linear-classifier.md)。

Validation 切分範例：從 50,000 張 training set 中取 1,000 張當 validation，用 49,000 張訓練 [CS231n classification "Validation sets for Hyperparameter tuning"]。詳見 [Hyperparameter Tuning](../concepts/hyperparameter-tuning.md)。

## 限制與注意事項

- 影像只有 32 × 32，解析度非常低，和真實世界的照片差距很大。CS231n 也明確稱它為 toy dataset [CS231n classification "Nearest Neighbor Classifier"]。
- 「人類約 94%」在原文中寫的是 "estimated at about 94%"，出處是原文連結的一篇部落格文章，不是正式論文 [CS231n classification "Nearest Neighbor Classifier"]。
- （截至 CS231n 筆記撰寫時）state-of-the-art 約 95% 這個數字，是引用當時一場 Kaggle 比賽的排行榜，有時效性，不能當作現在的最佳成績 [CS231n classification "Nearest Neighbor Classifier"]。
