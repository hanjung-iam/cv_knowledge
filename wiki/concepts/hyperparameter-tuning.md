---
title: Hyperparameter Tuning
type: concept
first_introduced: unknown
aliases: [超參數調整, validation set, 驗證集, cross-validation, 交叉驗證, train/val/test split]
tags: [ml-fundamentals, evaluation]
sources: [CS231n]
related:
  - concepts/k-nearest-neighbor.md
  - tasks/image-classification.md
  - datasets/cifar-10.md
created: 2026-11-22
updated: 2026-11-22
---

# Hyperparameter Tuning（超參數調整）與資料切分

## 一句話說明

模型有些設定無法從資料中直接學到，必須由人來選，這些設定叫做 hyperparameter。選擇時要用從 training set 切出來的 **validation set**，**絕對不能用 test set**。

## 直觀理解

把 test set 想成期末考，validation set 想成模擬考。

如果你反覆看期末考考卷，再依考卷內容調整讀書方法，最後考高分也不代表你真的學會了，只代表你「背了考卷」。正確的做法是用模擬考調整讀書方法，期末考只考一次，這樣分數才真的反映你的能力。

## 技術細節

### 什麼是 hyperparameter

以 [kNN](k-nearest-neighbor.md) 為例，k 要設多少、要用 L1 還是 L2 距離，這些選擇就是 hyperparameter。它們在許多機器學習演算法中都會出現，而且通常沒有明顯的正確答案 [CS231n classification "Validation sets for Hyperparameter tuning"]。

### 為什麼不能用 test set 調參數

最直覺的做法是「多試幾個值，看哪個效果最好」。這個想法沒錯，但**不能在 test set 上試** [CS231n classification "Validation sets for Hyperparameter tuning"]：

- 如果依照 test set 的表現調整 hyperparameter，就等於**把 test set 當成 training set 在用**，這叫做 overfit to the test set。
- 這樣測出來的成績會**過度樂觀**，真正部署之後，表現可能明顯變差。
- test set 只在最後用一次，才能作為衡量**泛化能力（generalization）**的可靠指標。

> 原則：test set 只在最後評估一次 [CS231n classification "Validation sets for Hyperparameter tuning"]。

### 正確做法：Validation Set（驗證集）

把 training set 再切成兩份：一份比較小的 training set，加上一份 **validation set**。validation set 的作用就像一個「假的 test set」，專門用來調整 hyperparameter [CS231n classification "Validation sets for Hyperparameter tuning"]。

以 [CIFAR-10](../datasets/cifar-10.md) 為例：拿 49,000 張來訓練，留 1,000 張當作 validation [CS231n classification "Validation sets for Hyperparameter tuning"]。接著對每個候選的 k，例如 1、3、5、10、20、50、100，都在 validation set 上評估，選出最好的 k，最後只在 test set 上跑一次 [CS231n classification "Validation sets for Hyperparameter tuning"]。

### Cross-validation（交叉驗證）

當訓練資料很少時，只切一份 validation set 的結果會很不穩定。Cross-validation 的做法是 [CS231n classification "Validation sets for Hyperparameter tuning"]：

- 以 **5-fold** 為例：把訓練資料平均分成 5 份，用其中 4 份訓練、1 份驗證。
- 輪流讓每一份都當一次驗證集，最後把 5 次的表現取平均。
- 這樣估計出來的結果比較穩定，雜訊比較少。

筆記附了一張 5-fold cross-validation 選 k 的圖：每個 k 都有 5 個驗證結果（點），趨勢線經過平均值，誤差棒表示標準差。圖說指出，**在這個資料上 k ≈ 7 最好** [CS231n classification "Validation sets for Hyperparameter tuning" 圖]。圖上的 accuracy 大約落在 0.25～0.31 [CS231n classification "Validation sets for Hyperparameter tuning" 圖]，明顯低於內文 NN 在完整 CIFAR-10 上的 38.6%，但原文沒有說明這張圖的實驗設定，所以兩者不能直接比較。

### 實務上怎麼選

- 因為 cross-validation 的計算成本高，實務上大家比較常用**單一 validation split** [CS231n classification "Validation sets for Hyperparameter tuning"]。
- Fold 數常見是 3、5 或 10 [CS231n classification "Validation sets for Hyperparameter tuning"]。
- **validation set 要切多大**，同一份筆記裡有兩種說法：
  - 「In practice」段落說，常見做法是用 training data 的 50%～90% 訓練，其餘當作 validation [CS231n classification "Validation sets for Hyperparameter tuning"]。
  - 「Summary: Applying kNN in practice」則說 rule of thumb 是 70%～90% 用來訓練 [CS231n classification "Summary: Applying kNN in practice"]。
  - 兩段的共同點是：hyperparameter 越多，validation set 應該越大；validation set 太小時（例如只有幾百筆），改用 cross-validation 比較安全 [CS231n classification "Validation sets for Hyperparameter tuning"]。
- 調整完之後，要不要把 validation data 併回去重新訓練？CS231n 認為比較乾淨的做法是不併回，把 validation data 視為已經「燒掉」了 [CS231n classification "Summary: Applying kNN in practice"]。

## 出現在哪些地方

- [k-Nearest Neighbor](k-nearest-neighbor.md)：用來選擇 k 和距離函數
- [Image Classification](../tasks/image-classification.md)：所有分類方法的評估流程都適用
- 之後所有深度學習模型的 learning rate、層數等 hyperparameter，也遵循同樣的原則（綜合推論，依據 [CS231n classification "Validation sets for Hyperparameter tuning"]：原文說 hyperparameter「come up very often in the design of many Machine Learning algorithms」）

## 常見誤解

- **「validation set 的成績就是模型的成績」**：不對。validation set 已經用來做選擇，會帶有偏差，要回報的應該是 test set 的成績。
- **「多看幾次 test set 沒關係」**：每看一次，就多一分對 test set 的 overfit。
