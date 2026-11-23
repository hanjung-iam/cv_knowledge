---
title: Convolutional Neural Network (CNN)
type: concept
first_introduced: unknown
aliases: [CNN, ConvNet, 卷積神經網路, Convolutional Neural Networks]
tags: [architecture, cnn, foundation]
sources: [CS231n]
related:
  - concepts/convolutional-layer.md
  - concepts/pooling-layer.md
  - models/alexnet.md
  - models/vggnet.md
  - concepts/linear-classifier.md
  - concepts/backpropagation.md
  - concepts/loss-function.md
  - datasets/ilsvrc.md
  - concepts/neural-network.md
  - concepts/activation-function.md
  - concepts/overfitting.md
created: 2026-11-23
updated: 2026-11-23
---

# Convolutional Neural Network（CNN，卷積神經網路）

## 一句話說明

一種**專門為影像設計**的神經網路：利用「輸入是影像」這個前提，讓每個 neuron 只看影像的一小塊區域，而且在不同位置共用同一組權重，因此參數大幅減少 [CS231n convolutional-networks "Convolutional Neural Networks (CNNs / ConvNets)"]。

## 直觀理解

前面的 Wiki 已經走過一條路：[kNN](k-nearest-neighbor.md) 直接比對像素，行不通；[linear classifier](linear-classifier.md) 每個類別只能學一個模板，太弱；[神經網路](neural-network.md)把 linear classifier 疊起來、中間插入非線性，解決了「一類一個模板」的問題，但它的全連接結構不適合影像（見下一節）。CNN 是這條路的下一站。

CNN 並沒有推翻前面學到的東西。CS231n 強調，它和一般的[神經網路](neural-network.md)非常相似 [CS231n convolutional-networks "Convolutional Neural Networks (CNNs / ConvNets)"]：

- 一樣由有可學習權重和 bias 的 neuron 組成；每個 neuron 做內積，再接一個非線性函數。
- 整個網路仍然是**一個可微分的 score function**，從原始像素一路算到類別分數。
- 最後一層一樣接 [loss function](loss-function.md)（例如 SVM 或 Softmax），訓練神經網路的技巧也都適用。

**那改變了什麼？** CNN 明確假設**輸入是影像**，並把這個假設寫進架構裡。這讓 forward 運算更有效率，也**大幅減少了參數量** [CS231n convolutional-networks "Convolutional Neural Networks (CNNs / ConvNets)"]。

一個直覺的比喻：與其讓每個 neuron 盯著整張圖（全部像素），不如讓它只看一個小窗口，並且讓同一個「偵測器」在整張圖上滑動、到處找同樣的特徵，例如某個方向的邊緣（綜合推論，依據 [CS231n convolutional-networks "Convolutional Layer"]）。

## 為什麼一般的神經網路不適合處理影像

一般的神經網路中，每個 hidden layer 的 neuron 都和上一層的**所有** neuron 相連（fully connected）[CS231n convolutional-networks "Architecture Overview"]。這在影像上會出問題 [CS231n convolutional-networks "Architecture Overview"]：

| 影像大小 | 第一層**一個** fully-connected neuron 的權重數 |
|---|---|
| 32 × 32 × 3（[CIFAR-10](../datasets/cifar-10.md)） | 3,072 |
| 200 × 200 × 3 | 120,000 |

（依據 [CS231n convolutional-networks "Architecture Overview"]。）

而且我們一定會需要很多個這樣的 neuron，參數量會迅速爆增。這種全連接的結構很浪費，而且大量的參數很快就會導致 **[overfitting](overfitting.md)** [CS231n convolutional-networks "Architecture Overview"]。

## 技術細節

### 3D volume：neuron 排成三維

CNN 每一層的 neuron 排成三個維度：**width、height、depth** [CS231n convolutional-networks "Architecture Overview"]。

- 這裡的 **depth** 指的是 activation volume 的第三個維度，**不是**網路的層數 [CS231n convolutional-networks "Architecture Overview"]。
- 例如 CIFAR-10 的輸入影像是 32 × 32 × 3 的 volume（3 是 RGB 三個通道）；最後的輸出層是 1 × 1 × 10，也就是沿著 depth 排列的 10 個類別分數 [CS231n convolutional-networks "Architecture Overview"]。

> CS231n 的總結：ConvNet 由一層層的 layer 組成。每一層都有一個簡單的介面：用一個可微分的函數，把輸入的 3D volume 轉成輸出的 3D volume，這個函數可能有參數，也可能沒有 [CS231n convolutional-networks "Architecture Overview"]。

### 組成 CNN 的層

主要有三種層：**Convolutional layer**、**Pooling layer**、**Fully-connected layer** [CS231n convolutional-networks "Layers used to build ConvNets"]，另外通常把 ReLU 激活函數也寫成一層 [CS231n convolutional-networks "ConvNet Architectures"]。

| 層 | 做什麼 | 有參數嗎 | 有 hyperparameter 嗎 | 詳見 |
|---|---|---|---|---|
| CONV | 每個 neuron 只連到輸入的一小塊區域，計算權重和該區域的內積 | 有 | 有 | [Convolutional Layer](convolutional-layer.md) |
| RELU | 逐元素套用[激活函數](activation-function.md)，例如 $\max(0, x)$；volume 大小不變 | 沒有 | 沒有 | |
| POOL | 在空間維度（width、height）上做 downsampling | 沒有 | 有 | [Pooling Layer](pooling-layer.md) |
| FC | 和一般神經網路一樣，連到上一層的所有數值，算出類別分數 | 有 | 有 | |

（依據 [CS231n convolutional-networks "Layers used to build ConvNets"]。）

CONV 和 FC 層的參數用 [gradient descent](gradient-descent.md) 訓練，讓算出的類別分數和訓練標籤一致 [CS231n convolutional-networks "Layers used to build ConvNets"]。

**一個簡單的 CIFAR-10 範例架構** `INPUT → CONV → RELU → POOL → FC` [CS231n convolutional-networks "Layers used to build ConvNets"]：

| 層 | 輸出的 volume |
|---|---|
| INPUT | 32 × 32 × 3（原始像素） |
| CONV（12 個 filter） | 32 × 32 × 12 |
| RELU | 32 × 32 × 12（大小不變） |
| POOL | 16 × 16 × 12 |
| FC | 1 × 1 × 10（10 個類別分數） |

（依據 [CS231n convolutional-networks "Layers used to build ConvNets"]。）

筆記的示意圖畫出一個小型 VGG Net 處理一張汽車照片的過程：一欄欄的 CONV、RELU、POOL activation 由左至右，最右邊的 FC 輸出前 5 名分數，第一名是 car，接著是 truck、airplane、ship、horse [CS231n convolutional-networks "Layers used to build ConvNets" 圖]。

### Normalization layer

曾經有很多種正規化（normalization）層被提出來，有些是為了模仿生物大腦中觀察到的抑制機制。但因為實務上的貢獻很小，甚至沒有貢獻，（截至 CS231n 筆記撰寫時）這類層已經不再流行 [CS231n convolutional-networks "Normalization Layer"]。

### 常見的層排列模式

最常見的 CNN 架構模式是 [CS231n convolutional-networks "Layer Patterns"]：

`INPUT -> [[CONV -> RELU]*N -> POOL?]*M -> [FC -> RELU]*K -> FC`

其中 `*` 表示重複，`POOL?` 表示可有可無；通常 `N <= 3`、`K < 3`。幾個例子 [CS231n convolutional-networks "Layer Patterns"]：

- `INPUT -> FC`：N = M = K = 0，**這就是 [linear classifier](linear-classifier.md)**。
- `INPUT -> [CONV -> RELU -> POOL]*2 -> FC -> RELU -> FC`
- `INPUT -> [CONV -> RELU -> CONV -> RELU -> POOL]*3 -> [FC -> RELU]*2 -> FC`：每次 pooling 之前先疊兩層 conv，對比較大、比較深的網路通常是好主意，因為在具破壞性的 pooling 之前，多層 conv 可以先學出更複雜的特徵。

### 用多個小 filter 取代一個大 filter

疊三層 3×3 的 conv（中間有非線性），第三層的每個 neuron 對原始輸入的「視野」是 7×7，和一層 7×7 conv 相同。但三層 3×3 有兩個優點 [CS231n convolutional-networks "Layer Patterns"]：

| | 一層 7×7 | 三層 3×3 |
|---|---|---|
| 非線性 | 沒有，只是輸入的線性函數 | 有，特徵的表達能力更強 |
| 參數量（每層都是 C 個通道） | $49C^2$ | $27C^2$ |

（依據 [CS231n convolutional-networks "Layer Patterns"]。）

缺點是：如果要做 backprop，需要更多記憶體來存中間層的結果 [CS231n convolutional-networks "Layer Patterns"]。

### 尺寸規則（rules of thumb）

- **輸入層**：大小要能被 2 整除很多次，常見的有 32（例如 CIFAR-10）、64、96（例如 STL-10）、224（常見的 ImageNet ConvNets）、384、512 [CS231n convolutional-networks "Layer Sizing Patterns"]。
- **Conv 層**：用小 filter（3×3，最多 5×5）、stride 1，並用 zero-padding 讓輸出大小和輸入相同（F = 3 時 P = 1，F = 5 時 P = 2）。比較大的 filter（例如 7×7）通常只出現在第一層 [CS231n convolutional-networks "Layer Sizing Patterns"]。
- **Pool 層**：負責縮小空間尺寸。最常見的是 2×2、stride 2 的 max pooling [CS231n convolutional-networks "Layer Sizing Patterns"]。

這個方案的好處是：**conv 層都維持空間尺寸，只有 pool 層負責縮小**，所以不必費心追蹤每一層的尺寸是否「對得上」[CS231n convolutional-networks "Layer Sizing Patterns"]。

- **為什麼 conv 用 stride 1？** 實務上小 stride 效果比較好，而且可以把所有空間上的縮小都交給 pool 層 [CS231n convolutional-networks "Layer Sizing Patterns"]。
- **為什麼要 padding？** 除了維持尺寸，padding 實際上也能**提升效能**。如果不 padding，每過一層 conv，volume 就會縮小一點，邊緣的資訊會太快被「洗掉」[CS231n convolutional-networks "Layer Sizing Patterns"]。

### 實務建議：Don't be a hero

CS231n 說，在 90% 以上的應用中，其實**不需要自己煩惱架構設計**：與其自己設計架構，不如找一個（截至 CS231n 筆記撰寫時）在 ImageNet 上表現最好的架構，**下載預訓練好的模型，再用自己的資料 finetune**。幾乎不需要從頭訓練或從頭設計一個 ConvNet [CS231n convolutional-networks "Layer Patterns"]。

### FC 層與 Conv 層可以互相轉換

FC 層和 CONV 層唯一的差別，是 CONV 的 neuron 只連到局部區域、而且共用參數；兩者都是在算內積，形式完全相同，所以可以互相轉換 [CS231n convolutional-networks "Converting FC layers to CONV layers"]：

- 任何 CONV 層都可以寫成一個 FC 層，權重矩陣大部分是 0，非 0 的區塊中也有很多相同的權重。
- 任何 FC 層也可以寫成 CONV 層：只要把 filter 大小設成和輸入 volume 一樣大。例如看著 7 × 7 × 512 輸入的 4096 個 FC neuron，等同於 F = 7、P = 0、S = 1、K = 4096 的 CONV 層 [CS231n convolutional-networks "Converting FC layers to CONV layers"]。

**FC → CONV 的實用價值**：轉換之後，可以**只做一次 forward**，就讓整個網路在一張更大的影像上「滑動」[CS231n convolutional-networks "Converting FC layers to CONV layers"]。例如原本輸入 224 × 224 的網路，轉換後輸入 384 × 384 的影像，會得到 6 × 6 的類別分數陣列，等同於在 36 個位置分別跑一次原本的網路，但因為共用計算，效率高得多 [CS231n convolutional-networks "Converting FC layers to CONV layers"]。

### 記憶體是最大的瓶頸

建構 CNN 時，最需要注意的是**記憶體**。（截至 CS231n 筆記撰寫時）許多 GPU 只有 3/4/6GB 的記憶體，最好的大約 12GB [CS231n convolutional-networks "Computational Considerations"]。記憶體主要用在三個地方 [CS231n convolutional-networks "Computational Considerations"]：

1. **Activations**：每一層的中間 volume，以及它們的 gradient。大部分集中在前面幾層 conv。這些要保留下來給 backprop 用。
2. **Parameters**：參數本身、它們的 gradient，以及最佳化方法（例如 momentum、Adagrad、RMSProp）需要的暫存，所以通常至少要乘以 3。
3. **其他**：例如影像資料的 batch。

網路放不進記憶體時，常見的做法是**減小 batch size**，因為大部分記憶體通常被 activations 用掉 [CS231n convolutional-networks "Computational Considerations"]。

## 經典架構的演進

CS231n 列出的幾個有名字的 CNN 架構：

| 架構 | 年份／成績 | 重點 |
|---|---|---|
| **LeNet** | 1990 年代，Yann LeCun | CNN 第一批成功的應用，用來辨識郵遞區號、數字等 |
| **[AlexNet](../models/alexnet.md)** | ILSVRC 2012 | 第一個讓 CNN 在 Computer Vision 中流行起來的工作；top-5 error 16%，亞軍 26% |
| **ZFNet** | ILSVRC 2013 冠軍 | 調整 AlexNet 的 hyperparameter：中間的 conv 層變大，第一層的 stride 和 filter 變小 |
| **GoogLeNet** | ILSVRC 2014 冠軍 | 提出 Inception Module，參數量大幅減少（4M，AlexNet 是 60M）；頂端用 average pooling 取代 FC 層 |
| **[VGGNet](../models/vggnet.md)** | ILSVRC 2014 亞軍 | 證明**網路的深度是效能的關鍵**；全部只用 3×3 conv 和 2×2 pooling |
| **ResNet** | ILSVRC 2015 冠軍 | 特殊的 **skip connections**，大量使用 batch normalization，最後沒有 FC 層 |

（表中內容依據 [CS231n convolutional-networks "Case studies"]。）

- （截至 2016 年 5 月 10 日）ResNet 是 state of the art 的 CNN 模型，也是實務上使用 ConvNet 的預設選擇 [CS231n convolutional-networks "Case studies"]。
- 「一層接一層排成直線」的傳統架構，被 Google 的 Inception 架構和 Residual Networks 挑戰，兩者都有更複雜的連接結構 [CS231n convolutional-networks "Layer Patterns"]。

## 在學習框架中的位置

CNN 換掉的只是 **score function**，[loss function](loss-function.md)、[optimization](optimization.md)、[backpropagation](backpropagation.md) 都沿用前面的內容 [CS231n convolutional-networks "Convolutional Neural Networks (CNNs / ConvNets)"]。這也印證了 optimization-1 的預告：「把 score function 換成神經網路、CNN，loss 和最佳化的過程大致不變」[CS231n optimization-1 "Introduction"]。

## 出現在哪些地方

- [Convolutional Layer](convolutional-layer.md)、[Pooling Layer](pooling-layer.md)：CNN 的主要元件
- [AlexNet](../models/alexnet.md)、[VGGNet](../models/vggnet.md)：經典架構
- [Image Classification](../tasks/image-classification.md)：kNN、linear classifier 之後的方法
- [ILSVRC](../datasets/ilsvrc.md)：歷年冠軍都是 CNN
