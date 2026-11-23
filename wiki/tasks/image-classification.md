---
title: Image Classification
type: task
metrics: [accuracy]
aliases: [影像分類, 圖像分類]
tags: [task, core-problem]
sources: [CS231n]
related:
  - concepts/k-nearest-neighbor.md
  - concepts/linear-classifier.md
  - concepts/loss-function.md
  - concepts/hyperparameter-tuning.md
  - datasets/cifar-10.md
  - concepts/optimization.md
  - concepts/gradient-descent.md
created: 2026-11-22
updated: 2026-11-23
---

# Image Classification（影像分類）

## 一句話說明

給電腦一張圖片，讓它從一組**事先固定好的類別**中，選出最符合的一個標籤 [CS231n classification "Image Classification"]。

## 直觀理解

人看到一張貓的照片，一眼就知道那是貓。但電腦「看到」的不是貓，而是一大片數字。

CS231n 的例子：一張寬 248、高 400 像素的彩色貓咪照片，對電腦來說是 248 × 400 × 3 個數字（3 代表紅、綠、藍三個顏色通道），總共 297,600 個數字。每個數字都是 0（黑）到 255（白）之間的整數。影像分類的任務，就是把這二十幾萬個數字變成一個標籤，例如「cat」[CS231n classification "Image Classification"]。

模型通常不只輸出一個答案，而是對每個類別給出一個機率，表示它有多確定。筆記的示意圖中，模型對這張貓的輸出是 82% cat、15% dog、2% hat、1% mug [CS231n classification "Image Classification" 圖]。

為什麼要先學分類？CS231n 指出，分類雖然簡單，卻是 Computer Vision 的核心問題之一，有大量實際應用，而且許多看起來不一樣的任務，例如 object detection、segmentation，都可以化約成分類問題 [CS231n classification "Image Classification"]。

## 輸入與輸出

| | 內容 |
|---|---|
| 輸入 | 一張影像：寬 × 高 × 3 的數字陣列，數值範圍 0～255 [CS231n classification "Image Classification"] |
| 輸出 | 一個類別標籤，或是在所有類別上的機率分布 [CS231n classification "Image Classification" 圖] |

## 為什麼這件事對電腦很難

CS231n 列出的難點如下。它強調這份清單並不完整 [CS231n classification "Image Classification"]。下表用筆記示意圖中的例子說明：

| 難點 | 意思 | 筆記示意圖的例子 |
|---|---|---|
| Viewpoint variation（視角變化） | 同一個物體從不同角度拍，看起來完全不同 | 同一座雕像的三個角度 |
| Scale variation（尺度變化） | 同一類物體的實際大小差異很大 | 高矮差距很大的兩個人都拿著筆電 |
| Deformation（形變） | 很多物體不是剛體，可以扭曲變形 | 姿勢誇張的貓 |
| Occlusion（遮蔽） | 物體可能只露出一小部分 | 只從牆後露出頭頂的貓 |
| Illumination conditions（光照） | 光線變化在像素層級的影響非常劇烈 | 不同打光下的同一組企鵝模型 |
| Background clutter（背景雜亂） | 物體可能和背景融在一起 | 花紋和背景很像的豹紋貓 |
| Intra-class variation（類內差異） | 同一類別的成員外觀差很多 | 各種造型的椅子 |

（示意圖的描述依據 [CS231n classification "Image Classification" 圖]。）

一個好的分類模型，必須**對這些變化的各種組合都保持不變（invariant）**，同時**對不同類別之間的差異保持敏感** [CS231n classification "Image Classification"]。

## 解法的思路：Data-driven Approach（資料驅動方法）

排序數字可以寫成明確的演算法，但「怎麼辨認貓」很難寫成程式規則。因此 CS231n 採取的做法，就像教小孩一樣：**給電腦看很多每個類別的範例，讓學習演算法自己學出每個類別長什麼樣子**。這種方法依賴先蒐集一個有標籤的 training dataset，所以叫做 data-driven approach [CS231n classification "Image Classification"]。

完整流程分成三步 [CS231n classification "Image Classification"]：

1. **Input**：N 張影像，每張標有 K 個類別中的一個，這就是 training set。
2. **Learning**：用 training set 學出每個類別的樣子，稱為 training a classifier 或 learning a model。
3. **Evaluation**：讓分類器預測一批**它從沒看過的新影像**，再和真正的標籤（ground truth）比對。

## 評估指標

- **Accuracy**：預測正確的比例。這是影像分類最常用的評估標準 [CS231n classification "Nearest Neighbor Classifier"]。
- 評估必須在沒看過的資料上進行，而且 test set 只能在最後用一次，詳見 [Hyperparameter Tuning](../concepts/hyperparameter-tuning.md)。

## 方法演進

之後隨著來源增加會持續補充。

| 方法 | 核心想法 | 成績（資料集、指標） | 頁面 |
|---|---|---|---|
| Nearest Neighbor（L1 距離） | 找訓練集中最像的那張圖，直接沿用它的標籤 | CIFAR-10 accuracy 38.6% [CS231n classification "Nearest Neighbor Classifier"] | [k-Nearest Neighbor](../concepts/k-nearest-neighbor.md) |
| Nearest Neighbor（L2 距離） | 同上，換成歐氏距離 | CIFAR-10 accuracy 35.4% [CS231n classification "Nearest Neighbor Classifier"] | [k-Nearest Neighbor](../concepts/k-nearest-neighbor.md) |
| Linear classifier（SVM loss） | 學出一組權重 W，每個類別一個「模板」，分數 = Wx + b | CIFAR-10 accuracy：用 random search 訓練約 15.5%；用 random local search 訓練 21.4%（只反映很差的最佳化方法）[CS231n optimization-1 "Strategy #1: A first very bad idea solution: Random search"; CS231n optimization-1 "Strategy #2: Random Local Search"] | [Linear Classifier](../concepts/linear-classifier.md) |
| CNN：[AlexNet](../models/alexnet.md)（2012） | 用 conv 層學出局部特徵，並在不同位置共用參數 | ILSVRC 2012 top-5 error 16%（第二名 26%）[CS231n convolutional-networks "Case studies"] | [CNN](../concepts/convolutional-neural-network.md) |

表中的成績來自**不同的資料集和指標**，不能直接互相比較。

CIFAR-10 的參考線：

- 隨機猜測：10%（10 個類別）[CS231n classification "Nearest Neighbor Classifier"]
- 人類：估計約 94% [CS231n classification "Nearest Neighbor Classifier"]
- （截至 CS231n 筆記撰寫時）state-of-the-art CNN：約 95%，與人類相當 [CS231n classification "Nearest Neighbor Classifier"]

### 第一步：kNN 的教訓 — 必須超越 raw pixel

kNN 的失敗點出了這個領域的核心問題：直接比較像素，反映的是**背景和顏色分布**，而不是物體**是什麼**。例如狗和青蛙，只因為都在白色背景上，就被判定為相近 [CS231n classification "Pros and Cons of Nearest Neighbor classifier"]。CS231n 的結論是：要讓同一類別的影像聚在一起、不受背景等無關因素影響，就**必須超越 raw pixel** [CS231n classification "Pros and Cons of Nearest Neighbor classifier"]。

CS231n 也預告，後續課程的方法可以做到：
- 約 90% 的 accuracy [CS231n classification "Summary"]
- 學完之後就可以丟掉 training set [CS231n classification "Summary"]
- 每張測試影像不到一毫秒就能分類完 [CS231n classification "Summary"]

### 第二步：Parametric approach — Linear classifier

[Linear classifier](../concepts/linear-classifier.md) 先解決了 kNN 的兩個實務問題 [CS231n linear-classify "Summary"]：
- 學完參數之後就可以**丟掉訓練資料**，不用把整個 training set 留在身邊。
- 預測一張圖只需要**一次矩陣乘法**，不用跟每張訓練圖片比對。

更重要的是，它建立了之後的神經網路和 CNN 都沿用的框架：**score function**（像素 → 分數）加上 **[loss function](../concepts/loss-function.md)**（衡量分數好不好），再把學習變成「讓 loss 最小」的最佳化問題 [CS231n linear-classify "Linear Classification"]。

但它還沒有真正「超越 raw pixel」：每個類別只有**一個模板**，所以朝左和朝右的馬會被混成一匹兩個頭的馬，各種顏色的車會被混成一輛紅色的車 [CS231n linear-classify "Interpreting a linear classifier"]。CS231n 預告，神經網路可以用多個中間神經元分別偵測不同類型的物體，再把它們組合起來 [CS231n linear-classify "Interpreting a linear classifier"]。

### 第三步：學習的閉環 — Optimization

有了 score function 和 loss，還需要找到讓 loss 最小的參數。CS231n 的做法是 **iterative refinement**：從隨機的 W 出發，用 [gradient descent](../concepts/gradient-descent.md) 一步一步改進 [CS231n optimization-1 "Strategy #1: A first very bad idea solution: Random search"; CS231n optimization-1 "Gradient Descent"]。詳見 [Optimization](../concepts/optimization.md)。

到這裡，「score function + loss function + optimization」三個元件都到齊了。CS231n 預告，接下來只要把 score function 換成神經網路、CNN，loss 和最佳化的過程大致不變 [CS231n optimization-1 "Introduction"]。

### 第四步：CNN — 為影像量身打造的 score function

[CNN](../concepts/convolutional-neural-network.md) 沿用 loss、optimization、[backprop](../concepts/backpropagation.md)，換掉的只有 score function [CS231n convolutional-networks "Convolutional Neural Networks (CNNs / ConvNets)"]。它利用「輸入是影像」這個前提，讓每個 neuron 只看一小塊區域（[conv layer](../concepts/convolutional-layer.md)），並在不同位置共用同一組權重，所以參數大幅減少 [CS231n convolutional-networks "Convolutional Layer"]。

網路學出來的 filter，在第一層是各種方向的邊緣和色塊，到了較高的層則是更複雜的圖案 [CS231n convolutional-networks "Convolutional Layer"]。這正是 kNN 那一步得出的結論「必須超越 raw pixel」的答案：**不再比對像素，而是學出特徵**（綜合推論，依據 [CS231n classification "Pros and Cons of Nearest Neighbor classifier"; CS231n convolutional-networks "Convolutional Layer"]）。

2012 年，[AlexNet](../models/alexnet.md) 在 [ILSVRC](../datasets/ilsvrc.md) 上大幅領先，讓 CNN 在 Computer Vision 中流行起來；之後 [VGGNet](../models/vggnet.md) 證明了深度的重要性，ResNet 則用 skip connections 繼續推進 [CS231n convolutional-networks "Case studies"]。

**中間少了一步**：CNN 是建立在一般「神經網路」之上的，但目前 Wiki 還沒有收錄介紹神經網路的來源。

## 相關概念

- [k-Nearest Neighbor](../concepts/k-nearest-neighbor.md)：第一個 baseline
- [Linear Classifier](../concepts/linear-classifier.md)：第一個 parametric 方法
- [Loss Function](../concepts/loss-function.md)、[Softmax／Cross-Entropy](../concepts/softmax-cross-entropy.md)、[Regularization](../concepts/regularization.md)：訓練用的框架
- [Optimization](../concepts/optimization.md)、[Gradient Descent](../concepts/gradient-descent.md)：如何找到好的參數
- [Hyperparameter Tuning](../concepts/hyperparameter-tuning.md)：如何正確地調整與評估
- [CNN](../concepts/convolutional-neural-network.md)、[Convolutional Layer](../concepts/convolutional-layer.md)、[Pooling Layer](../concepts/pooling-layer.md)：CNN 與它的組成元件
- [CIFAR-10](../datasets/cifar-10.md)：入門常用的資料集
- [ILSVRC](../datasets/ilsvrc.md)：大規模的資料集
