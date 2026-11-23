---
title: k-Nearest Neighbor (KNN)
type: concept
first_introduced: unknown
aliases: [KNN, k-近鄰, Nearest Neighbor Classifier, NN classifier, 最近鄰分類器]
tags: [classifier, baseline, non-parametric]
sources: [CS231n]
related:
  - tasks/image-classification.md
  - concepts/hyperparameter-tuning.md
  - datasets/cifar-10.md
  - concepts/linear-classifier.md
  - concepts/data-preprocessing.md
created: 2026-11-22
updated: 2026-11-23
---

# k-Nearest Neighbor（KNN，k-近鄰分類器）

## 一句話說明

要判斷一張新圖片是什麼，就去訓練資料裡找**最像它的 k 張圖**，讓它們投票決定標籤。

## 直觀理解

想像你不認識某種水果，於是翻開一本有標註的水果圖鑑，找出跟手上這顆長得最像的幾張照片，看它們大多叫什麼名字。KNN 就是這樣運作的：**它不真正「學」任何東西，只是把所有訓練資料記下來，等到要預測時再去比對**。

CS231n 用它當作第一個方法，原因不是它好用。筆記直接說它跟 CNN 無關，在實務上也很少使用。用它的目的是讓讀者先理解影像分類問題的基本做法 [CS231n classification "Nearest Neighbor Classifier"]。

## 技術細節

### Nearest Neighbor（k = 1）

- **訓練**：只是把所有訓練影像和標籤存起來 [CS231n classification "Nearest Neighbor Classifier"]。
- **預測**：把測試影像跟**每一張**訓練影像比較，採用距離最近的那一張的標籤 [CS231n classification "Nearest Neighbor Classifier"]。

所有分類器都遵守同一個介面：`train(X, y)` 從資料和標籤學習，`predict(X)` 對新資料預測標籤 [CS231n classification "Nearest Neighbor Classifier"]。

### 距離怎麼算：L1 與 L2

把兩張影像都攤平成向量 $I_1, I_2$，逐個像素相減：

- **L1 距離**：$d_1(I_1, I_2) = \sum_p |I_1^p - I_2^p|$。也就是把每個像素差的絕對值全部加起來。兩張圖完全一樣時，結果是 0；差異越大，數字越大 [CS231n classification "Nearest Neighbor Classifier"]。
- **L2 距離**：$d_2(I_1, I_2) = \sqrt{\sum_p (I_1^p - I_2^p)^2}$。也就是幾何上的歐氏距離 [CS231n classification "Nearest Neighbor Classifier"]。
  - 實際使用時可以省略開根號。開根號是單調函數，不會改變距離的大小順序，所以找到的最近鄰居還是一樣 [CS231n classification "Nearest Neighbor Classifier"]。

**L1 與 L2 的差別**：L2 對差異「更不寬容」。它寧可接受很多個中等的差異，也不願意接受一個很大的差異，因為差異被平方之後，大的差異會被放大。L1 和 L2 都是 p-norm 的特例 [CS231n classification "Nearest Neighbor Classifier"]。

| 距離 | CIFAR-10 accuracy（NN，k = 1） |
|---|---|
| L1 | 38.6% [CS231n classification "Nearest Neighbor Classifier"] |
| L2 | 35.4% [CS231n classification "Nearest Neighbor Classifier"] |

### 從 NN 到 KNN

只看最近的一張圖，很容易被異常值帶偏。KNN 改成找最近的 **k** 張，讓它們投票。k = 1 時就是原本的 NN [CS231n classification "k - Nearest Neighbor Classifier"]。

k 越大，決策邊界越平滑，越不容易被異常值影響。筆記的示意圖比較了 NN 和 5-NN：NN 會因為一個混在藍色群中的綠點，形成一小塊錯誤的「孤島」；5-NN 則會把這種不規則抹平，泛化能力可能比較好 [CS231n classification "k - Nearest Neighbor Classifier" 圖]。

CS231n 的建議是，實務上幾乎都應該用 KNN，而不是 NN [CS231n classification "k - Nearest Neighbor Classifier"]。至於 k 要設多少、用哪種距離，這些 **hyperparameter** 要用 validation set 來決定，詳見 [Hyperparameter Tuning](../concepts/hyperparameter-tuning.md)。

## 優點與缺點

| | 內容 |
|---|---|
| ✅ 簡單 | 很容易實作和理解 [CS231n classification "Pros and Cons of Nearest Neighbor classifier"] |
| ✅ 不用訓練 | 訓練時間是零，只需要儲存資料 [CS231n classification "Pros and Cons of Nearest Neighbor classifier"] |
| ❌ 預測很慢 | 每次預測都要跟全部訓練資料比對。實務上我們更在乎預測速度，所以這個取捨方向是**反的** [CS231n classification "Pros and Cons of Nearest Neighbor classifier"] |
| ❌ 要存全部資料 | 預測時必須保留整個 training set [CS231n classification "Summary"] |
| ❌ Pixel 距離沒有語意 | 見下一節 |

深度神經網路的取捨剛好相反：**訓練很貴，但訓練完之後分類新影像很便宜**，而這是實務上比較理想的模式 [CS231n classification "Pros and Cons of Nearest Neighbor classifier"]。

預測太慢時，可以用 Approximate Nearest Neighbor（ANN）函式庫加速，例如 FLANN，代價是犧牲一點準確度 [CS231n classification "Pros and Cons of Nearest Neighbor classifier"]。

## 根本問題：pixel 距離不等於語意相似

這是 KNN 這一頁對整個 Wiki 最重要的一課。

- 筆記展示了一張人臉原圖，旁邊三張圖分別是**平移過的（shifted）**、**用黑塊遮住眼睛和嘴巴的（messed up）**，以及**整體調暗的（darkened）**。這三張跟原圖的 **L2 pixel 距離都一樣**，但對人來說，平移和調暗的圖明明還是同一張臉，被遮住的那張卻差很多。換句話說，pixel 距離和人感受到的相似度、語意上的相似度幾乎無關 [CS231n classification "Pros and Cons of Nearest Neighbor classifier" 圖]。
- 用 t-SNE 把 CIFAR-10 依 L2 pixel 距離排成二維圖之後，可以看到影像主要是按照**整體色調和背景**聚在一起，而不是按照類別。例如狗和青蛙會因為都在白色背景上而靠得很近 [CS231n classification "Pros and Cons of Nearest Neighbor classifier"]。
- 在 NN 的示範中，10 張測試圖大約只有 3 張找到同類別的最近鄰。其中一張馬頭的圖，最近鄰是一輛紅色的車，原因推測是兩者都有很強的黑色背景 [CS231n classification "Nearest Neighbor Classifier"]。

**結論**：要讓同類別的影像聚在一起、不受背景等無關因素干擾，就必須**超越 raw pixel** [CS231n classification "Pros and Cons of Nearest Neighbor classifier"]。這正是後來「從資料中學習特徵表示」（例如 CNN）要解決的問題。

## 實務使用建議

CS231n 建議，如果真的要用 KNN（最好不是用在影像上，或只當作 baseline），步驟如下 [CS231n classification "Summary: Applying kNN in practice"]：

1. 把特徵正規化（normalization）成平均值 0、變異數 1。不過影像的像素通常分布相近，所以這一講沒有深入討論。詳見 [Data Preprocessing](data-preprocessing.md)。
2. 維度很高時，考慮先降維，例如 PCA、NCA、Random Projections。
3. 把資料隨機切成 train 和 val，必要時改用 cross-validation。
4. 在 validation data 上嘗試多種 k 和距離（L1、L2）。
5. 太慢的話，改用 ANN 函式庫。
6. 記下最好的 hyperparameter，最後在 test set 上評估一次並回報結果。

## 和 Linear Classifier 的關係

[Linear classifier](linear-classifier.md) 可以看成 KNN 的「壓縮版」：它**仍然是在做 Nearest Neighbor**，只是每個類別只保留**一張學出來的模板**，而不是幾千張訓練圖片，距離也改用（負的）內積 [CS231n linear-classify "Interpreting a linear classifier"]。

這解決了 KNN 的兩個缺點：要存全部訓練資料，以及預測時要逐一比對 [CS231n linear-classify "Linear Classification"]。

## 出現在哪些地方

- [Image Classification](../tasks/image-classification.md)：作為第一個 baseline
- [CIFAR-10](../datasets/cifar-10.md)：CS231n 的實驗資料集
