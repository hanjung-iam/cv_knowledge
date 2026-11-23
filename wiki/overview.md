---
title: Overview — Computer Vision 的演進主線
type: overview
aliases: [總覽, 綜述]
tags: [overview]
sources: [CS231n]
related:
  - tasks/image-classification.md
  - concepts/k-nearest-neighbor.md
  - concepts/linear-classifier.md
  - concepts/loss-function.md
  - concepts/softmax-cross-entropy.md
  - concepts/regularization.md
  - concepts/hyperparameter-tuning.md
  - datasets/cifar-10.md
created: 2026-11-22
updated: 2026-11-23
---

# Overview：Computer Vision 的演進主線

> 這頁是整個 Wiki 的入口，會隨著每次 ingest 更新。
> 目前收錄的來源：CS231n（classification、linear-classify）。

## Computer Vision 要解決什麼問題

對電腦來說，一張影像只是一大片 0～255 的數字。Computer Vision 的目標，是從這些數字中理解影像的內容：裡面**有什麼**（classification）、**在哪裡**（detection），以及**每個像素屬於什麼**（segmentation）。

其中 [Image Classification](tasks/image-classification.md) 是最核心的問題。許多看起來不同的任務，例如 object detection、segmentation，都可以化約成分類問題 [CS231n classification "Image Classification"]。所以這個 Wiki 從分類開始。

## 主線：從「比對像素」到「學習表示」

### 第一站：Data-driven approach

「貓長什麼樣子」很難寫成程式規則。因此現代 CV 的出發點是 **data-driven approach**：準備大量有標籤的範例，讓演算法自己學 [CS231n classification "Image Classification"]。

### 第二站：最簡單的 baseline — kNN

最直接的 data-driven 方法是 [k-Nearest Neighbor](concepts/k-nearest-neighbor.md)：記住所有訓練圖片，預測時找最像的幾張來投票。在 [CIFAR-10](datasets/cifar-10.md) 上只有 38.6%，比隨機猜測的 10% 好，但離人類的約 94% 還很遠 [CS231n classification "Nearest Neighbor Classifier"]。

它的失敗揭露了整個領域的核心問題：**pixel 距離反映的是背景和顏色，不是語意**，所以必須超越 raw pixel [CS231n classification "Pros and Cons of Nearest Neighbor classifier"]。

### 第三站：Score function + Loss function

[Linear classifier](concepts/linear-classifier.md) 引入了之後所有模型都沿用的框架 [CS231n linear-classify "Linear Classification"]：

1. **Score function**：把像素映射成類別分數。這裡是最簡單的 $f(x) = Wx + b$。
2. **[Loss function](concepts/loss-function.md)**：衡量分數和標籤有多吻合。常見的有 SVM（hinge）loss 和 [Softmax（cross-entropy）loss](concepts/softmax-cross-entropy.md)，再加上 [regularization](concepts/regularization.md)，表示偏好小而分散的權重。
3. **學習 = 最佳化**：找出讓 loss 最小的參數。

它用「學出來的參數」取代「記住所有資料」，解決了 kNN 儲存和速度上的問題 [CS231n linear-classify "Summary"]。但每個類別只有一個模板，所以兩個頭的馬、紅色的車，暴露出它**表達能力不足** [CS231n linear-classify "Interpreting a linear classifier"]。

CS231n 的伏筆是：CNN 從像素映射到分數的方式和這裡完全一樣，只是 $f$ 更複雜 [CS231n linear-classify "Parameterized mapping from images to label scores"]。

### 下一站（待補）

依照 CS231n 的脈絡，接下來是**最佳化**（怎麼找到讓 loss 最小的 W）、神經網路，然後是 CNN。這些內容會在對應來源 ingest 之後補上。

## 貫穿所有方法的紀律

- 評估一定要在**沒看過的資料**上進行。
- 用 validation set 調整 hyperparameter，**test set 只用一次** [CS231n classification "Validation sets for Hyperparameter tuning"]。詳見 [Hyperparameter Tuning](concepts/hyperparameter-tuning.md)。

## 兩軸地圖（目前狀態）

| | Classification | Detection | Segmentation |
|---|---|---|---|
| **方法** | kNN（baseline）→ Linear classifier | （待補） | （待補） |
| **資料集** | CIFAR-10 | （待補） | （待補） |
