---
title: Data Preprocessing
type: concept
first_introduced: unknown
aliases: [資料前處理, preprocessing, image data preprocessing, mean subtraction, mean image, centering, 正規化（normalization）]
tags: [data, training, practice]
sources: [CS231n]
related:
  - concepts/linear-classifier.md
  - concepts/k-nearest-neighbor.md
  - concepts/backpropagation.md
  - concepts/gradient-descent.md
  - concepts/activation-function.md
created: 2026-11-23
updated: 2026-11-23
---

# Data Preprocessing（資料前處理）

## 一句話說明

在把資料送進模型之前，先調整每個特徵的**中心位置**和**尺度**，最常見的是減去平均值（centering），再縮放到固定的範圍。

## 直觀理解

原始像素值的範圍是 0～255。對人來說沒差，但對模型來說，數字的大小和偏移會直接影響訓練過程。

這一頁整合了三篇 CS231n 筆記各自提到的前處理內容。它們從不同角度回答同一個問題：**為什麼要前處理？**

| 筆記 | 角度 |
|---|---|
| classification | kNN 的實務建議：先把特徵正規化（normalization） |
| linear-classify | 影像前處理的具體做法：mean subtraction 和縮放 |
| optimization-2 | 從 backprop 的角度：**資料的尺度會影響 gradient 的大小** |

## 技術細節

### 做法一：Centering（中心化）／Mean subtraction

- 在機器學習中，對輸入特徵做正規化（normalization）是非常普遍的做法。對影像來說，每個像素都被視為一個特徵 [CS231n linear-classify "Interpreting a linear classifier"]。
- 特別重要的是**把資料中心化**：每個特徵都減去它的平均值。對影像來說，就是先算出所有訓練影像的 **mean image（平均影像）**，再從每張影像減掉它，像素範圍大約變成 −127～127 [CS231n linear-classify "Interpreting a linear classifier"]。

### 做法二：Scaling（縮放）

- 更進一步的常見做法，是把每個輸入特徵縮放到 −1～1 的範圍 [CS231n linear-classify "Interpreting a linear classifier"]。
- kNN 的實務建議則是把特徵正規化（normalization）成**平均值 0、變異數 1** [CS231n classification "Summary: Applying kNN in practice"]。

兩者之中，zero mean centering 可以說比較重要 [CS231n linear-classify "Interpreting a linear classifier"]。

### 為什麼尺度重要：從 backprop 來看

[Backpropagation](backpropagation.md) 中的 **mul gate**，local gradient 是「另一個輸入的值」。所以在 [linear classifier](linear-classifier.md) 中，權重和輸入做內積 $w^T x_i$ 時，**資料的尺度會直接影響權重 gradient 的大小** [CS231n optimization-2 "Patterns in backward flow"]：

- 如果前處理時把所有輸入 $x_i$ 都乘以 1000，權重的 gradient 也會變成 1000 倍 [CS231n optimization-2 "Patterns in backward flow"]。
- 這時就必須把 [learning rate](gradient-descent.md) 調小同樣的倍數來補償 [CS231n optimization-2 "Patterns in backward flow"]。

筆記的結論：**這就是為什麼前處理很重要，而且有時候影響的方式很隱微**。對 gradient 怎麼流動有直觀的理解，可以幫助 debug 這類問題 [CS231n optimization-2 "Patterns in backward flow"]。

> **一個伏筆的回收**：linear-classify 說 zero mean centering 比較重要，但「原因要等理解 gradient descent 的動態之後才能解釋」[CS231n linear-classify "Interpreting a linear classifier"]。
> - optimization-2 解釋了資料的**尺度**為什麼會影響 gradient [CS231n optimization-2 "Patterns in backward flow"]。
> - neural-networks-1 在討論 [sigmoid](activation-function.md) 的缺點時說明：如果**輸入一個 neuron 的資料都是正的**，backprop 時權重的 gradient 會全部同號（全正或全負），讓 gradient 更新「之字形」前進 [CS231n neural-networks-1 "Commonly used activation functions"]。
>
> 原始像素值 0～255 全部是正數，所以第二點很可能就是「為什麼要中心化」的答案：減去平均之後，輸入有正有負，就不會出現權重 gradient 全部同號的情況（綜合推論，依據 [CS231n linear-classify "Interpreting a linear classifier"; CS231n neural-networks-1 "Commonly used activation functions"]）。不過 neural-networks-1 談的是 sigmoid 的輸出，並沒有直接把這個論點套用到輸入資料的前處理上。

### 影像資料的特殊之處

在 kNN 的那一講，CS231n 選擇**不深入**討論資料正規化（normalization），理由是影像的像素通常分布相近，不會有差異很大的分布，所以比較不需要正規化（normalization）[CS231n classification "Summary: Applying kNN in practice"]。但到了 linear classifier，筆記又說對輸入特徵做正規化（normalization）是「非常普遍的做法」，並建議做 mean subtraction [CS231n linear-classify "Interpreting a linear classifier"]。

這兩個說法沒有矛盾：前者說的是「像素之間的分布差異不大」，後者說的是「整體仍然需要中心化和縮放」。而 optimization-2 從 gradient 的角度說明了，即使分布相近，**整體的尺度**仍然會影響訓練（綜合推論，依據 [CS231n classification "Summary: Applying kNN in practice"; CS231n linear-classify "Interpreting a linear classifier"; CS231n optimization-2 "Patterns in backward flow"]）。

### 其他前處理：降維

kNN 的實務建議也提到，資料維度很高時，可以考慮先降維，例如 PCA、NCA、Random Projections [CS231n classification "Summary: Applying kNN in practice"]。

## 出現在哪些地方

- [k-Nearest Neighbor](k-nearest-neighbor.md)：實務建議的第一步就是正規化（normalization）
- [Linear Classifier](linear-classifier.md)：mean subtraction 與縮放
- [Backpropagation](backpropagation.md)：mul gate 說明了尺度的影響
- [Gradient Descent](gradient-descent.md)：資料尺度會影響 learning rate 的設定

## 常見誤解

- **「影像像素都在 0～255，所以不需要前處理」**：像素之間分布相近，確實可以少做一些處理 [CS231n classification "Summary: Applying kNN in practice"]，但中心化仍然是常見做法 [CS231n linear-classify "Interpreting a linear classifier"]，而且整體的尺度會影響 gradient 和 learning rate [CS231n optimization-2 "Patterns in backward flow"]。
