# Global Review Report (2026-11-23)

頁面數：23

## 1. 跨頁數字（出現在 ≥2 個非 source 頁面）

逐一確認：各頁的數字是否相同、條件（資料集、設定）是否寫清楚。

- `38.6%`：concepts/hyperparameter-tuning.md, concepts/k-nearest-neighbor.md, datasets/cifar-10.md, overview.md, tasks/image-classification.md
- `0.01`：concepts/activation-function.md, concepts/overfitting.md, concepts/regularization.md, concepts/softmax-cross-entropy.md
- `0.25`：concepts/activation-function.md, concepts/hyperparameter-tuning.md, concepts/linear-classifier.md, concepts/regularization.md
- `1.0`：concepts/backpropagation.md, concepts/hyperparameter-tuning.md, concepts/loss-function.md, concepts/regularization.md
- `10%`：concepts/optimization.md, datasets/cifar-10.md, overview.md, tasks/image-classification.md
- `15.5%`：concepts/linear-classifier.md, concepts/optimization.md, datasets/cifar-10.md, tasks/image-classification.md
- `16%`：concepts/convolutional-neural-network.md, datasets/ilsvrc.md, models/alexnet.md, tasks/image-classification.md
- `21.4%`：concepts/linear-classifier.md, concepts/optimization.md, datasets/cifar-10.md, tasks/image-classification.md
- `26%`：concepts/convolutional-neural-network.md, datasets/ilsvrc.md, models/alexnet.md, tasks/image-classification.md
- `90%`：concepts/convolutional-neural-network.md, concepts/hyperparameter-tuning.md, concepts/softmax-cross-entropy.md, tasks/image-classification.md
- `0.1`：concepts/linear-classifier.md, concepts/overfitting.md, concepts/regularization.md
- `0.5`：concepts/linear-classifier.md, concepts/neural-network.md, concepts/softmax-cross-entropy.md
- `105,705,600`：concepts/convolutional-layer.md, models/alexnet.md, overview.md
- `30,730`：concepts/gradient-descent.md, concepts/optimization.md, datasets/cifar-10.md
- `34,944`：concepts/convolutional-layer.md, models/alexnet.md, overview.md
- `35.4%`：concepts/k-nearest-neighbor.md, datasets/cifar-10.md, tasks/image-classification.md
- `50,000`：concepts/linear-classifier.md, datasets/cifar-10.md, datasets/ilsvrc.md
- `94%`：datasets/cifar-10.md, overview.md, tasks/image-classification.md
- `0.0`：concepts/linear-classifier.md, concepts/regularization.md
- `0.001`：concepts/overfitting.md, concepts/regularization.md
- `0.2`：concepts/backpropagation.md, concepts/linear-classifier.md
- `0.28`：concepts/loss-function.md, concepts/softmax-cross-entropy.md
- `0.86`：concepts/loss-function.md, concepts/softmax-cross-entropy.md
- `1,000`：concepts/hyperparameter-tuning.md, datasets/cifar-10.md
- `1.04`：concepts/loss-function.md, concepts/softmax-cross-entropy.md
- `1.2`：concepts/linear-classifier.md, datasets/ilsvrc.md
- `2.85`：concepts/loss-function.md, concepts/softmax-cross-entropy.md
- `3,072`：concepts/convolutional-neural-network.md, datasets/cifar-10.md
- `40%`：concepts/activation-function.md, concepts/gradient-descent.md
- `437.9`：concepts/linear-classifier.md, concepts/loss-function.md
- `49,000`：concepts/hyperparameter-tuning.md, datasets/cifar-10.md
- `61.95`：concepts/linear-classifier.md, concepts/loss-function.md
- `95%`：datasets/cifar-10.md, tasks/image-classification.md
- `96.8`：concepts/linear-classifier.md, concepts/loss-function.md

## 2. 未連結的提及

A 頁提到了 B 頁的標題或英文別名，但全頁都沒有連到 B 頁。不一定要修，請判斷是否該加連結。

- `concepts/loss-function.md` 提到 kernel，但沒有連到 `concepts/convolutional-layer.md`

## 3. 候選新頁面

在 ≥3 個頁面被粗體強調、但不是任何頁面標題或別名的英文術語。是否建頁仍要看來源是否有足夠內容。

（無）

## 4. 數學符號

各頁使用的希臘字母。同一概念在不同頁面用了不同符號時要統一（或註明）。

- `\alpha`：concepts/activation-function.md(1), concepts/regularization.md(2)
- `\delta`：concepts/optimization.md(1)
- `\Delta`：concepts/gradient-descent.md(2), concepts/hyperparameter-tuning.md(3), concepts/loss-function.md(8), concepts/regularization.md(2)
- `\epsilon`：concepts/neural-network.md(2)
- `\lambda`：concepts/hyperparameter-tuning.md(3), concepts/loss-function.md(6), concepts/overfitting.md(2), concepts/regularization.md(10), concepts/softmax-cross-entropy.md(2)
- `\sigma`：concepts/activation-function.md(3), concepts/backpropagation.md(6), concepts/neural-network.md(1), sources/cs231n.md(2)

## 5. 待重新檢視的段落

（綜合推論）和前瞻性用語，在新來源加入後可能已經過時或被修正。

- `concepts/activation-function.md:55`（綜合推論）：> **和資料前處理的關聯**：第 2 點說的是「**輸入一個 neuron 的資料**都是正的」會造成問題。原始像素值 0～255 也全部是正數，所以這很可能…
- `concepts/backpropagation.md:183`（綜合推論）：- [Convolutional Layer](convolutional-layer.md)：卷積的 backward 也是一個卷積（filter 在空間上翻…
- `concepts/backpropagation.md:189`（綜合推論）：- **「backprop 和 gradient descent 是同一件事」**：不是。backprop 負責**計算** gradient，gradient…
- `concepts/convolutional-neural-network.md:32`（前瞻性用語）：前面的 Wiki 已經走過一條路：[KNN](k-nearest-neighbor.md) 直接比對像素，行不通；[linear classifier](lin…
- `concepts/convolutional-neural-network.md:42`（綜合推論）：一個直覺的比喻：與其讓每個 neuron 盯著整張圖（全部像素），不如讓它只看一個小窗口，並且讓同一個「偵測器」在整張圖上滑動、到處找同樣的特徵，例如某個方向的…
- `concepts/data-preprocessing.md:64`（綜合推論）：> 原始像素值 0～255 全部是正數，所以第二點很可能就是「為什麼要中心化」的答案：減去平均之後，輸入有正有負，就不會出現權重 gradient 全部同號的情…
- `concepts/data-preprocessing.md:70`（綜合推論）：這兩個說法沒有矛盾：前者說的是「像素之間的分布差異不大」，後者說的是「整體仍然需要中心化和縮放」。而 optimization-2 從 gradient 的角度…
- `concepts/gradient-descent.md:150`（綜合推論）：backprop 負責**算出** gradient，gradient descent 負責**用** gradient 更新參數（綜合推論，依據 [CS231…
- `concepts/hyperparameter-tuning.md:102`（綜合推論）：這說明了一件事：先理解 hyperparameter 之間的關係，可以減少需要搜尋的組合（綜合推論，依據 [CS231n linear-classify "Pr…
- `concepts/linear-classifier.md:86`（綜合推論）：> **圖中數字的驗算**：用圖上的 W、x、b 實際計算，cat = 0.2×56 − 0.5×231 + 0.1×24 + 2.0×2 + 1.1 = −9…
- `concepts/linear-classifier.md:148`（前瞻性用語）：這兩個數字只反映**很差的最佳化方法**，不是 linear classifier 的能力上限。用 gradient descent 訓練的結果，目前收錄的來源…
- `datasets/ilsvrc.md:43`（綜合推論）：兩者都指向 1000 個類別（綜合推論，依據 [CS231n optimization-1 "Gradient Descent"; CS231n convolu…
- `models/alexnet.md:101`（綜合推論）：> 所以這一段描述的看起來比較像 VGGNet 的架構，而不是 AlexNet（綜合推論，依據 [CS231n convolutional-networks "…
- `models/vggnet.md:60`（綜合推論）：> **記憶體總量的驗算**：把表中每一層的 memory 逐一相加（150K + 2 × 3.2M + 800K + 2 × 1.6M + 400K + 3 …
- `overview.md:104`（綜合推論）：再加上 [pooling layer](concepts/pooling-layer.md) 逐步縮小尺寸，最後接 FC 層算出類別分數。網路學到的 filte…
- `overview.md:108`（前瞻性用語）：### 下一站（待補）…
- `overview.md:121`（前瞻性用語）：| **方法** | KNN（baseline）→ Linear classifier → Neural network → CNN | （待補） | （待補）…
- `overview.md:122`（前瞻性用語）：| **模型** | [AlexNet](models/alexnet.md) → [VGGNet](models/vggnet.md) | （待補） | （待…
- `overview.md:123`（前瞻性用語）：| **資料集** | [CIFAR-10](datasets/cifar-10.md)、[ILSVRC](datasets/ilsvrc.md) | （待補）…
- `tasks/image-classification.md:133`（綜合推論）：網路學出來的 filter，在第一層是各種方向的邊緣和色塊，到了較高的層則是更複雜的圖案 [CS231n convolutional-networks "Con…
