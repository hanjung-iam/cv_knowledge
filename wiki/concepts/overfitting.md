---
title: Overfitting
type: concept
first_introduced: unknown
aliases: [過擬合, 過度擬合, generalization, 泛化, capacity, model capacity, outliers]
tags: [generalization, training, foundation]
sources: [CS231n]
related:
  - concepts/regularization.md
  - concepts/hyperparameter-tuning.md
  - concepts/neural-network.md
  - concepts/convolutional-neural-network.md
  - concepts/pooling-layer.md
  - concepts/convolutional-layer.md
  - concepts/gradient-descent.md
  - concepts/loss-function.md
created: 2026-11-23
updated: 2026-11-23
---

# Overfitting（過擬合）與 Generalization（泛化）

## 一句話說明

**Overfitting** 是模型擬合到資料中的**雜訊**，而不是背後真正的關係，結果在訓練資料上表現很好，在新資料上卻變差 [CS231n neural-networks-1 "Setting number of layers and their sizes"]。**Generalization** 則是模型在沒看過的資料上的表現 [CS231n classification "Validation sets for Hyperparameter tuning"]。

## 直觀理解

想像你在背考古題：如果你連題目裡的錯字都背下來了，遇到新的題目反而不會做。模型也一樣，能力太強（capacity 太大）又缺乏約束時，它會連資料裡的雜訊、例外都記下來。

這一頁整合了四篇 CS231n 筆記中關於 overfitting 的內容：

| 筆記 | 角度 |
|---|---|
| classification | 調參數時對 **test set** overfitting |
| linear-classify | regularization 可以減少 overfitting |
| convolutional-networks | **參數太多**會導致 overfitting；pooling 可以控制 overfitting |
| neural-networks-1 | **capacity** 與 overfitting 的關係；應該用 regularization 而不是縮小網路 |

## 技術細節

### Capacity：模型能表達多複雜的函數

網路越大、層數越多，**capacity** 越大，也就是能表達的函數空間越大，因為更多 neuron 可以合作表達各種不同的函數 [CS231n neural-networks-1 "Setting number of layers and their sizes"]。

筆記用一個二維的二元分類問題，比較三個各有一層 hidden layer、大小不同的網路 [CS231n neural-networks-1 "Setting number of layers and their sizes" 圖]：

| hidden neuron 數 | 決策區域 |
|---|---|
| 3 | 大致切成兩大塊，只能粗略地分類 |
| 6 | 開始出現比較複雜的邊界 |
| 20 | 擬合所有訓練資料，但把空間切成很多分散的紅綠區域 |

更多 neuron 可以表達更複雜的函數。這**既是好處**（能分類更複雜的資料），**也是壞處**（更容易 overfit 訓練資料）[CS231n neural-networks-1 "Setting number of layers and their sizes"]。

### Overfitting 的例子

- 20 個 hidden neuron 的模型擬合了**所有**訓練資料，代價是把空間切成很多分散的區域 [CS231n neural-networks-1 "Setting number of layers and their sizes"]。
- 3 個 hidden neuron 的模型只有足夠的表達能力做粗略的分類：它把資料看成兩大團，並把綠色區域中的少數紅點視為 **outliers**（雜訊）。實務上，這**可能**在 test set 上有更好的 generalization [CS231n neural-networks-1 "Setting number of layers and their sizes"]。

### 但不要用小網路來避免 overfitting

看了上面的例子，似乎資料不夠複雜時，應該選比較小的網路。**CS231n 說這是錯的** [CS231n neural-networks-1 "Setting number of layers and their sizes"]：

- 有很多更好的方法可以防止 overfitting，例如 [L2 regularization](regularization.md)、dropout、input noise。實務上，用這些方法控制 overfitting，**永遠比**減少 neuron 數更好。
- **原因**：小網路比較難用 [gradient descent](gradient-descent.md) 這種局部方法訓練。它的 [loss function](loss-function.md) 的 local minima 比較少，但其中很多**很容易收斂到，而且是不好的**（loss 很高）。大網路的 local minima 多得多，但這些 minima 的實際 loss 好得多 [CS231n neural-networks-1 "Setting number of layers and their sizes"]。
- 實務上的現象：訓練小網路時，最終的 loss 變異很大，有時運氣好收斂到好的地方，有時卡在不好的 minima；訓練大網路時，會得到很多不同的解，但最終 loss 的變異小得多，**所有解都差不多好**，比較不依賴隨機初始化的運氣 [CS231n neural-networks-1 "Setting number of layers and their sizes"]。

> CS231n 的結論：不應該因為害怕 overfitting 就用比較小的網路。應該**在計算資源允許的範圍內用越大的網路越好**，再用 regularization 等技巧控制 overfitting [CS231n neural-networks-1 "Setting number of layers and their sizes"]。

### 用 regularization strength 控制 overfitting

regularization strength 是控制神經網路 overfitting 的**首選方法** [CS231n neural-networks-1 "Setting number of layers and their sizes"]。筆記的圖比較了同樣 20 個 hidden neuron 的網路，在三種 $\lambda$ 下的決策區域 [CS231n neural-networks-1 "Setting number of layers and their sizes" 圖]：

| $\lambda$ | 決策區域 |
|---|---|
| 0.001 | 很破碎，有很多細長的區域 |
| 0.01 | 比較平滑 |
| 0.1 | 接近一條平滑的分界線 |

regularization 越強，最終的決策區域越平滑 [CS231n neural-networks-1 "Setting number of layers and their sizes" 圖]。詳見 [Regularization](regularization.md)。

### 其他和 overfitting 有關的內容

- **參數太多會 overfitting**：一般神經網路用在影像上時，全連接結構的參數量太大，很快就會導致 overfitting [CS231n convolutional-networks "Architecture Overview"]。CNN 的 [parameter sharing](convolutional-layer.md) 和 [pooling layer](pooling-layer.md) 都能減少參數量；CS231n 明確說 pooling 層的作用之一就是控制 overfitting [CS231n convolutional-networks "Pooling Layer"]。
- **偏好小而分散的權重**：L2 regularization 讓分類器把每個輸入維度都考慮一點，而不是強烈依賴少數維度，這可以改善泛化表現、減少 overfitting [CS231n linear-classify "Multiclass Support Vector Machine loss"]。
- **對 test set overfitting**：如果拿 test set 來調整 hyperparameter，就等於對 test set overfitting，測出來的成績會過度樂觀。test set 只在最後用一次，才能作為 generalization 的可靠指標 [CS231n classification "Validation sets for Hyperparameter tuning"]。詳見 [Hyperparameter Tuning](hyperparameter-tuning.md)。
- **KNN 的 k**：k 越大，決策邊界越平滑，越不容易被異常值影響，可能帶來更好的 generalization [CS231n classification "k - Nearest Neighbor Classifier" 圖]。詳見 [k-Nearest Neighbor](k-nearest-neighbor.md)。

## 出現在哪些地方

- [Regularization](regularization.md)：控制 overfitting 的首選方法
- [Neural Network](neural-network.md)：網路大小與 capacity
- [CNN](convolutional-neural-network.md)、[Pooling Layer](pooling-layer.md)：減少參數以控制 overfitting
- [Hyperparameter Tuning](hyperparameter-tuning.md)：對 test set overfitting
- [k-Nearest Neighbor](k-nearest-neighbor.md)：k 的平滑效果

## 常見誤解

- **「怕 overfitting，就用小一點的模型」**：CS231n 明確說這是錯的，應該用大網路加上 regularization [CS231n neural-networks-1 "Setting number of layers and their sizes"]。
- **「training loss 越低越好」**：training loss 很低，可能只是擬合到了雜訊。真正要看的是模型在沒看過的資料上的表現 [CS231n neural-networks-1 "Setting number of layers and their sizes"; CS231n classification "Validation sets for Hyperparameter tuning"]。
