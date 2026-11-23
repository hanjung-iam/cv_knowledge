---
title: Optimization
type: concept
first_introduced: unknown
aliases: [最佳化, 優化, loss landscape, 損失地形, iterative refinement, random search]
tags: [training, foundation]
sources: [CS231n]
related:
  - concepts/gradient-descent.md
  - concepts/loss-function.md
  - concepts/linear-classifier.md
  - concepts/regularization.md
created: 2026-11-23
updated: 2026-11-23
---

# Optimization（最佳化）

## 一句話說明

找出讓 [loss function](loss-function.md) 最小的那組參數 W [CS231n optimization-1 "Introduction"]。

## 直觀理解

到這裡，學習的三個元件就到齊了 [CS231n optimization-1 "Introduction"]：

1. **Score function**：把像素變成分數，例如 [linear classifier](linear-classifier.md) 的 $Wx$。
2. **Loss function**：替一組參數打分數，分數越低代表越好。
3. **Optimization**：找出分數最低的那組參數。

CS231n 用一個比喻貫穿整個最佳化過程：**你被蒙上眼睛，站在一片丘陵上，目標是走到谷底** [CS231n optimization-1 "Strategy #1: A first very bad idea solution: Random search"]。

- 你站的位置，就是目前的參數 W。
- 腳下的高度，就是這組參數的 loss。
- 在 CIFAR-10 上，這片丘陵是 **30,730 維**的，因為 W 的大小是 10 × 3073。

CS231n 也預告：之後把 score function 換成神經網路、CNN 的時候，**loss function 和最佳化的過程大致不變**，換掉的只有第一個元件 [CS231n optimization-1 "Introduction"]。

## 技術細節

### 看看 loss 的地形

W 有 30,730 個參數，沒辦法直接畫出來。但可以從某個隨機的 W 出發，沿著一個隨機方向 $W_1$ 切一刀，畫出 $L(W + aW_1)$ 隨 $a$ 變化的曲線；或者沿著兩個方向切一個平面，畫出 $L(W + aW_1 + bW_2)$，用顏色表示 loss 的高低 [CS231n optimization-1 "Visualizing the loss function"]。

筆記在 CIFAR-10 上畫出 Multiclass SVM loss（沒有 regularization）的地形 [CS231n optimization-1 "Visualizing the loss function" 圖]：

- **只看一個樣本**：一維切面是由幾段直線組成的折線；二維切面也看得出分段線性的結構。
- **平均 100 個樣本**：二維切面變成一個平滑的**碗**，中間藍色（loss 低）、四周紅色（loss 高）。

**為什麼是分段線性？** 每個樣本的 SVM loss 是好幾個「在 0 截斷的線性函數」相加，所以每一項都是一條折線，加起來還是折線 [CS231n optimization-1 "Visualizing the loss function"]。很多樣本的 loss 取平均之後，就變成由很多個分段線性的碗疊成的大碗 [CS231n optimization-1 "Visualizing the loss function" 圖]。

### Convex 與 non-convex

- 碗狀的外觀暗示 SVM 的 loss 是一個 **convex function（凸函數）**。關於如何有效率地最小化這類函數，已經有大量的研究 [CS231n optimization-1 "Visualizing the loss function"]。
- 但等到 score function 換成神經網路，目標函數就會變成 **non-convex**，地形不再是一個碗，而是**複雜、凹凸不平的地形** [CS231n optimization-1 "Visualizing the loss function"]。
- 所以，雖然 SVM 這個例子是 convex 的，CS231n 在介紹最佳化時**刻意不使用 convex optimization 的工具**，因為最終的目標是神經網路，那些工具用不上 [CS231n optimization-1 "Optimization"]。

### 三種策略

| 策略 | 做法 | 蒙眼下山的比喻 | CIFAR-10 test accuracy |
|---|---|---|---|
| #1 Random search | 隨機產生 1000 組 W，留下 loss 最低的 | 隨便跳到 1000 個地方，記住最低的那個 | 約 15.5% |
| #2 Random local search | 從隨機的 W 出發，每次加上一個隨機擾動 $\delta W$，loss 變低才接受 | 往隨機方向伸出一隻腳試探，往下才走過去 | 21.4% |
| #3 Following the gradient | 算出最陡的下坡方向，往那裡走 | 用腳感覺地面的坡度，往最陡的方向往下走 | 這篇筆記沒有提供 |

（策略 #1 依據 [CS231n optimization-1 "Strategy #1: A first very bad idea solution: Random search"]；策略 #2 依據 [CS231n optimization-1 "Strategy #2: Random Local Search"]，它和 #1 一樣只評估 1000 次 loss；策略 #3 依據 [CS231n optimization-1 "Strategy #3: Following the Gradient"]。）

- 策略 #1 的程式碼回傳的是 0.1555，內文則寫「about 15.5%」[CS231n optimization-1 "Strategy #1: A first very bad idea solution: Random search"]。和隨機猜測的 10% 相比，這樣「腦死」的方法其實不算太差 [CS231n optimization-1 "Strategy #1: A first very bad idea solution: Random search"]。
- 策略 #2 比較好，但仍然浪費，計算成本也很高 [CS231n optimization-1 "Strategy #2: Random Local Search"]。
- 策略 #3 不需要隨機尋找方向：可以直接算出**最陡的下降方向**，至少在步伐趨近於 0 的極限下，數學上保證是最陡的 [CS231n optimization-1 "Strategy #3: Following the Gradient"]。這個方向和 loss 的 **gradient** 有關，詳見 [Gradient Descent](gradient-descent.md)。

### 核心想法：Iterative refinement（逐步改進）

**一次找到最好的 W 非常困難，甚至不可能**，尤其是當 W 是整個複雜神經網路的權重時。但「把目前這組 W 改得**稍微好一點**」就簡單得多 [CS231n optimization-1 "Strategy #1: A first very bad idea solution: Random search"]。

所以策略是：**從隨機的權重出發，一步一步改進，讓 loss 越來越低** [CS231n optimization-1 "Strategy #1: A first very bad idea solution: Random search"]。

## 出現在哪些地方

- [Gradient Descent](gradient-descent.md)：實際使用的最佳化方法
- [Loss Function](loss-function.md)：最佳化要最小化的目標
- [Linear Classifier](linear-classifier.md)：這篇筆記的範例對象
- 之後的神經網路和 CNN：loss 和最佳化的過程大致不變 [CS231n optimization-1 "Introduction"]

## 常見誤解

- **「random search 有 15.5%，代表 linear classifier 只有這個程度」**：不對。筆記在 random search 之後緊接著說「我們可以做得好得多」[CS231n optimization-1 "Strategy #1: A first very bad idea solution: Random search"]。15.5% 和 21.4% 反映的是**最佳化方法**很差，不是 linear classifier 的能力上限。
- **「SVM 的 loss 是碗狀，所以所有 loss 都很好最佳化」**：神經網路的 loss 是 non-convex 的 [CS231n optimization-1 "Visualizing the loss function"]。
