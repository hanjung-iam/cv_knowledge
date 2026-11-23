---
title: Regularization
type: concept
first_introduced: unknown
aliases: [正規化（regularization）, 正則化, L2 regularization, regularization penalty, regularization strength]
tags: [training, generalization, foundation]
sources: [CS231n]
related:
  - concepts/loss-function.md
  - concepts/linear-classifier.md
  - concepts/softmax-cross-entropy.md
  - concepts/hyperparameter-tuning.md
created: 2026-11-23
updated: 2026-11-23
---

# Regularization（正規化）

> **用語提醒**：本 Wiki 中「正規化」可能指 **regularization**（本頁）或 **normalization**（例如資料前處理、softmax 的歸一化）。為了區分，「正規化」出現時一律附上英文。

## 一句話說明

在 loss 裡額外加上一項**只跟權重有關的懲罰** $R(W)$，表示我們偏好某一種權重，最常見的是偏好「小而分散」的權重 [CS231n linear-classify "Multiclass Support Vector Machine loss"]。

## 直觀理解

假設兩個學生考試都拿了滿分。一個是每一科都理解了；另一個是只靠背某幾題的答案。如果只看分數，兩個人沒有差別；但遇到新題目時，前者比較可靠。

Regularization 就是在「答對訓練資料」之外，再加一條偏好：**不要過度依賴少數幾個特徵，要把注意力平均分配**。這樣做通常能讓模型在沒看過的資料上表現更好。

## 技術細節

### 動機一：讓 W 有唯一的偏好

假設某組 W 已經把所有訓練樣本分對，每個 $L_i = 0$。問題是這組 W **並不唯一**：把 W 乘上任何 $\lambda > 1$，所有分數之間的差距都會等比例放大，loss 仍然是 0。例如正確類別和最接近的錯誤類別差了 15，把 W 乘以 2 之後就差 30 [CS231n linear-classify "Multiclass Support Vector Machine loss"]。

所以我們需要表達**對某些 W 的偏好**，消除這種不確定性，做法就是加上 regularization penalty [CS231n linear-classify "Multiclass Support Vector Machine loss"]。

### L2 regularization

最常見的是平方 L2 norm，也就是把 W 的每個元素平方之後全部加起來 [CS231n linear-classify "Multiclass Support Vector Machine loss"]：

$$
R(W) = \sum_k \sum_l W_{k,l}^2
$$

它不是資料的函數，只看權重本身 [CS231n linear-classify "Multiclass Support Vector Machine loss"]。加進 loss 之後：

$$
L = \frac{1}{N}\sum_i L_i + \lambda R(W)
$$

> **符號說明**：本 Wiki 統一用 $\lambda$ 表示 regularization strength，和 linear-classify 筆記一致 [CS231n linear-classify "Multiclass Support Vector Machine loss"]。optimization-1 筆記把同一個 loss 寫成 $\ldots + \alpha R(W)$，用的是 $\alpha$ [CS231n optimization-1 "Introduction"]。兩者指的是同一件事。

$\lambda$（regularization strength）是 hyperparameter，**沒有簡單的設定方式，通常用 cross-validation 決定** [CS231n linear-classify "Multiclass Support Vector Machine loss"]，詳見 [Hyperparameter Tuning](hyperparameter-tuning.md)。

### 動機二：小而分散的權重，泛化比較好

CS231n 認為這是 regularization **最吸引人的性質**：懲罰大權重，可以避免任何單一輸入維度獨自對分數產生很大的影響，因此往往能改善泛化 [CS231n linear-classify "Multiclass Support Vector Machine loss"]。

**範例** [CS231n linear-classify "Multiclass Support Vector Machine loss"]：輸入 $x = (1, 1, 1, 1)$，有兩組權重：

| 權重 | 和 x 的內積 | L2 penalty |
|---|---|---|
| $w_1 = (1, 0, 0, 0)$：只看第一個維度 | 1 | 1.0 |
| $w_2 = (0.25, 0.25, 0.25, 0.25)$：平均看所有維度 | 1 | 0.25 |

兩者的預測完全一樣，但 L2 penalty 偏好 $w_2$。這樣的分類器會**每個輸入維度都考慮一點**，而不是只強烈依賴少數幾個維度。這可以改善在 test 影像上的泛化表現，減少 **overfitting** [CS231n linear-classify "Multiclass Support Vector Machine loss"]。

### 其他性質

- 在 SVM 中，加上 L2 penalty 會帶來 **max margin** 的性質，細節見 CS229 的講義 [CS231n linear-classify "Multiclass Support Vector Machine loss"]。
- 從機率的觀點來看，regularization 項可以解讀成 W 上的 **Gaussian prior**，整體變成 MAP 估計 [CS231n linear-classify "Softmax classifier"]，詳見 [Softmax／Cross-Entropy](softmax-cross-entropy.md)。
- 加上 regularization 之後，loss **永遠不可能剛好是 0.0**，除非 W = 0 這種病態情況 [CS231n linear-classify "Multiclass Support Vector Machine loss"]。
- $\lambda$ 會影響 Softmax 輸出「機率」的集中程度：$\lambda$ 越大，權重越小，「機率」越分散 [CS231n linear-classify "SVM vs. Softmax"]。

### 要不要 regularize bias？

bias 不控制輸入維度的影響力，所以沒有同樣的效果。常見做法是**只 regularize W，不 regularize b**，不過實務上兩種做法的差別通常可以忽略 [CS231n linear-classify "Multiclass Support Vector Machine loss"]。

### 和 SVM 的 margin Δ 的關係

SVM 的 margin $\Delta$ 和 $\lambda$ 控制的是**同一個取捨**：data loss 和 regularization loss 之間的平衡。因此 $\Delta$ 可以固定成 1.0，真正要調的只有 $\lambda$ [CS231n linear-classify "Practical Considerations"]。詳見 [Loss Function](loss-function.md)。

## 出現在哪些地方

- [Loss Function](loss-function.md)：完整 loss = data loss + regularization loss
- [Linear Classifier](linear-classifier.md)：限制 W 的大小
- [Softmax／Cross-Entropy](softmax-cross-entropy.md)：MAP 詮釋、對輸出「機率」的影響
- [Hyperparameter Tuning](hyperparameter-tuning.md)：$\lambda$ 是典型的 hyperparameter

## 常見誤解

- **「Regularization 是為了讓 training loss 更低」**：剛好相反。它會讓 training loss 沒辦法降到 0 [CS231n linear-classify "Multiclass Support Vector Machine loss"]。它的目的是改善在沒看過的資料上的表現。