# Global Review Report (2026-11-23)

頁面數：13

## 1. 跨頁數字（出現在 ≥2 個非 source 頁面）

逐一確認：各頁的數字是否相同、條件（資料集、設定）是否寫清楚。

- `38.6%`：concepts/hyperparameter-tuning.md, concepts/k-nearest-neighbor.md, datasets/cifar-10.md, overview.md, tasks/image-classification.md
- `10%`：concepts/optimization.md, datasets/cifar-10.md, overview.md, tasks/image-classification.md
- `15.5%`：concepts/linear-classifier.md, concepts/optimization.md, datasets/cifar-10.md, tasks/image-classification.md
- `21.4%`：concepts/linear-classifier.md, concepts/optimization.md, datasets/cifar-10.md, tasks/image-classification.md
- `0.25`：concepts/hyperparameter-tuning.md, concepts/linear-classifier.md, concepts/regularization.md
- `1.0`：concepts/hyperparameter-tuning.md, concepts/loss-function.md, concepts/regularization.md
- `30,730`：concepts/gradient-descent.md, concepts/optimization.md, datasets/cifar-10.md
- `35.4%`：concepts/k-nearest-neighbor.md, datasets/cifar-10.md, tasks/image-classification.md
- `50,000`：concepts/linear-classifier.md, datasets/cifar-10.md, datasets/ilsvrc.md
- `90%`：concepts/hyperparameter-tuning.md, concepts/softmax-cross-entropy.md, tasks/image-classification.md
- `94%`：datasets/cifar-10.md, overview.md, tasks/image-classification.md
- `0.0`：concepts/linear-classifier.md, concepts/regularization.md
- `0.28`：concepts/loss-function.md, concepts/softmax-cross-entropy.md
- `0.5`：concepts/linear-classifier.md, concepts/softmax-cross-entropy.md
- `0.86`：concepts/loss-function.md, concepts/softmax-cross-entropy.md
- `1,000`：concepts/hyperparameter-tuning.md, datasets/cifar-10.md
- `1.04`：concepts/loss-function.md, concepts/softmax-cross-entropy.md
- `1.2`：concepts/linear-classifier.md, datasets/ilsvrc.md
- `2.85`：concepts/loss-function.md, concepts/softmax-cross-entropy.md
- `437.9`：concepts/linear-classifier.md, concepts/loss-function.md
- `49,000`：concepts/hyperparameter-tuning.md, datasets/cifar-10.md
- `61.95`：concepts/linear-classifier.md, concepts/loss-function.md
- `95%`：datasets/cifar-10.md, tasks/image-classification.md
- `96.8`：concepts/linear-classifier.md, concepts/loss-function.md

## 2. 未連結的提及

A 頁提到了 B 頁的標題或英文別名，但全頁都沒有連到 B 頁。不一定要修，請判斷是否該加連結。

（無）

## 3. 候選新頁面

在 ≥3 個頁面被粗體強調、但不是任何頁面標題或別名的英文術語。是否建頁仍要看來源是否有足夠內容。

（無）

## 4. 數學符號

各頁使用的希臘字母。同一概念在不同頁面用了不同符號時要統一（或註明）。

- `\alpha`：concepts/regularization.md(2)
- `\delta`：concepts/optimization.md(1)
- `\Delta`：concepts/gradient-descent.md(2), concepts/hyperparameter-tuning.md(3), concepts/loss-function.md(8), concepts/regularization.md(2)
- `\lambda`：concepts/hyperparameter-tuning.md(3), concepts/loss-function.md(6), concepts/regularization.md(9), concepts/softmax-cross-entropy.md(2)

## 5. 待重新檢視的段落

（綜合推論）和前瞻性用語，在新來源加入後可能已經過時或被修正。

- `concepts/gradient-descent.md:134`（前瞻性用語）：## 下一步：Backpropagation…
- `concepts/hyperparameter-tuning.md:87`（綜合推論）：這說明了一件事：先理解 hyperparameter 之間的關係，可以減少需要搜尋的組合（綜合推論，依據 [CS231n linear-classify "Pr…
- `concepts/linear-classifier.md:82`（綜合推論）：> **圖中數字的驗算**：用圖上的 W、x、b 實際計算，cat = 0.2×56 − 0.5×231 + 0.1×24 + 2.0×2 + 1.1 = −9…
- `concepts/linear-classifier.md:146`（前瞻性用語）：這兩個數字只反映**很差的最佳化方法**，不是 linear classifier 的能力上限。用 gradient descent 訓練的結果，目前收錄的來源…
- `datasets/ilsvrc.md:35`（綜合推論）：類別數的依據：筆記的思想實驗說，假設 120 萬張影像其實是「1000 張不同影像，每類一張」的複本，每張各有 1200 份 [CS231n optimizat…
- `overview.md:68`（前瞻性用語）：### 下一站（待補）…
- `overview.md:70`（前瞻性用語）：依照 CS231n 的脈絡，下一步是 **backpropagation**（用 chain rule 有效率地算出 gradient），然後是神經網路和 CN…
- `overview.md:81`（前瞻性用語）：| **方法** | kNN（baseline）→ Linear classifier | （待補） | （待補） |…
- `overview.md:82`（前瞻性用語）：| **資料集** | [CIFAR-10](datasets/cifar-10.md)、[ILSVRC](datasets/ilsvrc.md) | （待補）…
