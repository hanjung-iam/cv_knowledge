---
title: Backpropagation
type: concept
first_introduced: unknown
aliases: [反向傳播, backprop, chain rule, 連鎖律, forward pass, backward pass, local gradient, staged computation]
tags: [training, gradient, foundation]
sources: [CS231n]
related:
  - concepts/gradient-descent.md
  - concepts/optimization.md
  - concepts/loss-function.md
  - concepts/data-preprocessing.md
  - concepts/linear-classifier.md
created: 2026-11-23
updated: 2026-11-23
---

# Backpropagation（反向傳播）

## 一句話說明

反覆套用微積分的 **chain rule（連鎖律）**，從輸出往回，有效率地算出整個運算式對每個輸入的 gradient [CS231n optimization-2 "Introduction"]。

## 直觀理解

[Gradient descent](gradient-descent.md) 需要知道 loss 對每個權重的 gradient。那一頁介紹了兩種算法：numerical gradient 太慢，analytic gradient 又容易推導錯誤。Backpropagation 解決了這個兩難：**不需要寫出完整的 gradient 公式**，只要把運算拆成很多個小步驟，每一步各自算出簡單的局部導數，再從後往前一路相乘就好 [CS231n optimization-2 "Summary"]。

CS231n 用**電路**來比喻：運算式是一個由許多「gate」（加法、乘法、max…）組成的電路 [CS231n optimization-2 "Compound expressions with chain rule"]。

- **Forward pass（前向傳遞）**：數值從輸入流向輸出。
- **Backward pass（反向傳遞）**：gradient 從輸出往回流，一路傳到每個輸入。

可以把它想成 gate 之間在**互相傳話**：透過 gradient 告訴上一個 gate「我希望你的輸出變大還是變小、程度有多強」，目的是讓最後的輸出變大 [CS231n optimization-2 "Intuitive understanding of backpropagation"]。

CS231n 認為，理解這個過程和它的細節，對理解、開發、設計和 debug 神經網路都非常關鍵 [CS231n optimization-2 "Introduction"]。

## 技術細節

### 要解決的問題

給定一個函數 $f(x)$，其中 $x$ 是輸入向量，要算出 $\nabla f(x)$。在神經網路中，$f$ 就是 [loss function](loss-function.md) $L$，輸入包括訓練資料和權重 [CS231n optimization-2 "Introduction"]。

訓練資料是固定的，所以實務上**通常只算權重的 gradient**，用來更新參數。不過輸入資料 $x_i$ 的 gradient 有時也有用，例如用來視覺化、理解神經網路在做什麼 [CS231n optimization-2 "Introduction"]。

### Gradient 的意義：敏感度

**每個變數的導數，代表整個運算式對這個變數的值有多敏感** [CS231n optimization-2 "Simple expressions and interpretation of the gradient"]。

例如 $f(x, y) = xy$，所以 $\partial f/\partial x = y$、$\partial f/\partial y = x$。當 $x = 4$、$y = -3$ 時，$f = -12$ [CS231n optimization-2 "Simple expressions and interpretation of the gradient"]：

- $\partial f/\partial x = -3$：x 增加一點點 h，f 會**減少** 3h。
- $\partial f/\partial y = 4$：y 增加一點點 h，f 會**增加** 4h。

注意：導數只描述**無限小**的變化會帶來的影響，不能拿來預測大幅改變輸入時會發生什麼事 [CS231n optimization-2 "Simple expressions and interpretation of the gradient"]。

三種基本運算的 local gradient [CS231n optimization-2 "Simple expressions and interpretation of the gradient"]：

| 運算 | 對 x 的導數 | 對 y 的導數 |
|---|---|---|
| $f = xy$ | $y$ | $x$ |
| $f = x + y$ | 1 | 1 |
| $f = \max(x, y)$ | $\mathbb{1}(x \ge y)$ | $\mathbb{1}(y \ge x)$ |

max 的 (sub)gradient：較大的那個輸入是 1，另一個是 0。

### Chain rule：把 gradient 串起來

以 $f(x, y, z) = (x + y) z$ 為例，拆成 $q = x + y$ 和 $f = qz$ 兩步。**chain rule** 說，把各段的 gradient 串起來的方法是**相乘**：$\frac{\partial f}{\partial x} = \frac{\partial f}{\partial q} \frac{\partial q}{\partial x}$ [CS231n optimization-2 "Compound expressions with chain rule"]。

代入 $x = -2$、$y = 5$、$z = -4$ [CS231n optimization-2 "Compound expressions with chain rule"]：

| 變數 | forward 的值 | backward 的 gradient |
|---|---|---|
| x | −2 | −4 |
| y | 5 | −4 |
| z | −4 | 3 |
| q = x + y | 3 | −4 |
| f = q × z | −12 | 1 |

（表中數值依據 [CS231n optimization-2 "Compound expressions with chain rule" 圖]。）

計算順序：先算 $f = qz$ 的 local gradient：$\partial f/\partial z = q = 3$、$\partial f/\partial q = z = -4$。再往回經過 $q = x + y$，local gradient 都是 1，乘上 −4，得到 x 和 y 的 gradient 都是 −4。

### 為什麼說 backprop 是「局部」的

每個 gate 拿到輸入之後，可以**立刻、獨立地**算出兩件事：自己的輸出值，以及自己輸出對輸入的 **local gradient**。它完全不需要知道整個電路長什麼樣子 [CS231n optimization-2 "Intuitive understanding of backpropagation"]。

forward 結束後，在 backward pass 中，gate 會收到「自己的輸出對最終結果的 gradient」，然後依照 chain rule，把它**乘上**自己對每個輸入的 local gradient，再往回傳 [CS231n optimization-2 "Intuitive understanding of backpropagation"]。

> 筆記的說法：chain rule 帶來的這個額外乘法，可以讓一個單獨看起來沒什麼用的 gate，變成整個神經網路這種複雜電路中的一個齒輪 [CS231n optimization-2 "Intuitive understanding of backpropagation"]。

以上面的例子來說，add gate 的 local gradient 是 +1。它在 backward 時得知自己輸出的 gradient 是 −4，意思是電路「希望」它的輸出**變小**，力道是 4。它把 −4 乘上 1，傳給 x 和 y。如果 x、y 照著負的 gradient 變小，add gate 的輸出就會變小，multiply gate 的輸出（因為 z 是負的）就會變大 [CS231n optimization-2 "Intuitive understanding of backpropagation"]。

### 三種常見 gate 的模式

筆記用一個電路示範 add、mul、max 三種最常見的 gate 在 backward 時的行為 [CS231n optimization-2 "Patterns in backward flow"]：

| Gate | backward 時做什麼 | 例子中的情況 |
|---|---|---|
| **add** | 把輸出的 gradient **原封不動地分給所有輸入**，因為 local gradient 是 +1 | + gate 把 2.00 分別傳給兩個輸入 |
| **max** | 把 gradient **只傳給** forward 時值最大的那個輸入，其他輸入的 gradient 是 0 | z = 2 比 w = −1 大，所以 z 拿到 2.00，w 是 0 |
| **mul** | local gradient 是**另一個輸入的值**（兩者對調），再乘上輸出的 gradient | x 的 gradient = −4.00 × 2.00 = −8.00 |

（表中數值依據 [CS231n optimization-2 "Patterns in backward flow" 圖]。）

**mul gate 的反直覺效果**：如果一個輸入很小、另一個很大，mul gate 會給小的輸入很大的 gradient，給大的輸入很小的 gradient [CS231n optimization-2 "Patterns in backward flow"]。這代表**資料的尺度會影響權重 gradient 的大小**，詳見 [Data Preprocessing](data-preprocessing.md)。

### Modularity：任何可微分的函數都可以當 gate

gate 的劃分其實很隨意：**任何可微分的函數都可以當作一個 gate**，可以把多個 gate 合併成一個，也可以把一個函數拆成多個 gate，怎麼方便怎麼做 [CS231n optimization-2 "Modularity: Sigmoid example"]。

**範例：Sigmoid neuron**

$$
f(w, x) = \frac{1}{1 + e^{-(w_0 x_0 + w_1 x_1 + w_2)}}
$$

筆記說，這個運算式描述的是一個使用 **sigmoid activation** 的 2 維 neuron，之後的課程會再介紹 [CS231n optimization-2 "Modularity: Sigmoid example"]。這裡先把它當成一個普通的函數，拆成乘法、加法、乘以 −1、exp、加 1、取倒數等 gate。

**sigmoid 函數** $\sigma(x) = \frac{1}{1 + e^{-x}}$ 的導數可以化簡成一個很簡單的形式 [CS231n optimization-2 "Modularity: Sigmoid example"]：

$$
\frac{d\sigma(x)}{dx} = (1 - \sigma(x))\,\sigma(x)
$$

所以實務上，最好把整串 sigmoid 運算**合併成一個 gate**：只用一個簡單的式子就能算出 local gradient，效率更高，數值問題也更少 [CS231n optimization-2 "Modularity: Sigmoid example"]。

範例中，權重是 (2, −3, −3)、輸入是 (−1, −2)，內積加上 bias 之後是 1.0，sigmoid 的輸出是 0.73，local gradient 是 (1 − 0.73) × 0.73 ≈ 0.2 [CS231n optimization-2 "Modularity: Sigmoid example"]。這和把 sigmoid 拆成好幾個 gate、逐一 backprop 算出來的結果相同 [CS231n optimization-2 "Modularity: Sigmoid example" 圖]。

### 實作：Staged computation（分段計算）

筆記用一個「完全沒用、只是為了示範」的複雜函數說明 [CS231n optimization-2 "Backprop in practice: Staged computation"]：

$$
f(x, y) = \frac{x + \sigma(y)}{\sigma(x) + (x + y)^2}
$$

如果直接對 x 或 y 微分，會得到非常龐大複雜的式子。但**完全沒必要這樣做**：我們不需要寫出 gradient 的明確公式，只需要**知道怎麼算**它 [CS231n optimization-2 "Backprop in practice: Staged computation"]。

做法 [CS231n optimization-2 "Backprop in practice: Staged computation"]：

1. **Forward**：把運算拆成很多個中間變數，每個都是 local gradient 已知的簡單運算（例如 `sigy`、`num`、`den`、`invden`）。
2. **Backward**：依**相反順序**，對每個中間變數算出對應的 gradient 變數（例如 `dnum`、`dden`）。每一步都是「local gradient × 上游傳來的 gradient」。

兩個要注意的地方 [CS231n optimization-2 "Backprop in practice: Staged computation"]：

- **Cache forward 的中間值**：backward 時會用到 forward 算過的變數，所以要把它們存起來。重新計算也可以，但很浪費。
- **分岔處的 gradient 要相加**：同一個變數在運算式中被用到好幾次時，往回流的 gradient 要**累加**（用 `+=`，不能用 `=` 覆蓋）。這是微積分中 multivariable chain rule 的結果。

### 矩陣運算的 gradient

所有概念都可以直接推廣到矩陣和向量運算，只是要特別注意維度和轉置 [CS231n optimization-2 "Gradients for vectorized operations"]。最棘手的是矩陣乘法 $D = WX$：

- $dW$ = `dD.dot(X.T)`
- $dX$ = `W.T.dot(dD)`

**技巧：用維度分析推導**，不必背公式 [CS231n optimization-2 "Gradients for vectorized operations"]。$dW$ 的形狀一定要和 $W$ 一樣，而且一定是 $X$ 和 $dD$ 的矩陣乘法。例如 $X$ 是 10 × 3、$dD$ 是 5 × 3、$W$ 是 5 × 10，那麼唯一能讓維度對上的寫法就是 `dD.dot(X.T)`。

另一個建議：先寫出一個**最小的具體例子**，在紙上推導 gradient，再推廣到向量化的形式 [CS231n optimization-2 "Gradients for vectorized operations"]。

## 在學習流程中的位置

| 步驟 | 負責的頁面 |
|---|---|
| 算出分數 | [Linear classifier](linear-classifier.md) 等 score function（forward pass） |
| 衡量好壞 | [Loss function](loss-function.md) |
| **算出 loss 對權重的 gradient** | **Backpropagation**（backward pass） |
| 更新權重 | [Gradient descent](gradient-descent.md) |

CS231n 的結論：有了 backprop，就能有效率地算出 loss 對參數的 gradient，也就準備好訓練神經網路了。「課程中觀念上最難的部分已經過去了，ConvNets 只差一小步」[CS231n optimization-2 "Summary"]。

## 出現在哪些地方

- [Gradient Descent](gradient-descent.md)：backprop 算出的 gradient 就是用來做 gradient descent
- [Data Preprocessing](data-preprocessing.md)：mul gate 的特性說明了資料尺度為什麼重要
- 之後的神經網路和 CNN：用 backprop 計算 gradient [CS231n optimization-2 "Summary"]

## 常見誤解

- **「backprop 要先推導出完整的 gradient 公式」**：剛好相反。CS231n 強調幾乎**永遠不需要**在紙上把整個式子完整地符號微分；只要分段，每段各自算 local gradient 就好 [CS231n optimization-2 "Summary"]。
- **「backprop 和 gradient descent 是同一件事」**：不是。backprop 負責**計算** gradient，gradient descent 負責**使用** gradient 來更新參數（綜合推論，依據 [CS231n optimization-2 "Summary"; CS231n optimization-1 "Gradient Descent"]）。
