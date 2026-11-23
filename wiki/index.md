# CV Wiki Index

Computer Vision 知識庫總目錄。每次 ingest 或新增頁面時更新。

## Overview

- [Overview — Computer Vision 的演進主線](overview.md) — Wiki 入口：從比對像素、學習參數，到學習表示（sources: 1）

## Models

- [AlexNet](models/alexnet.md) — ILSVRC 2012，讓 CNN 流行起來；第一層 11×11、stride 4（sources: 1）
- [VGGNet](models/vggnet.md) — ILSVRC 2014 亞軍，證明深度很重要；全部 3×3 conv，138M 參數（sources: 1）

## Tasks

- [Image Classification](tasks/image-classification.md) — 從固定類別中為影像選一個標籤；難點、data-driven 流程、方法演進（sources: 1）

## Concepts

- [k-Nearest Neighbor (KNN)](concepts/k-nearest-neighbor.md) — 第一個 baseline；L1/L2 距離；pixel 距離不等於語意（sources: 1）
- [Linear Classifier](concepts/linear-classifier.md) — score function Wx + b；加權總和、幾何、template matching 三種理解；一類一個模板的極限（sources: 1）
- [Loss Function](concepts/loss-function.md) — data loss + regularization loss；Multiclass SVM（hinge）loss；SVM vs Softmax（sources: 1）
- [Softmax and Cross-Entropy Loss](concepts/softmax-cross-entropy.md) — 分數轉「機率」；資訊理論與 MLE 詮釋；數值穩定（sources: 1）
- [Regularization](concepts/regularization.md) — L2 penalty；消除 W 的不唯一性；小而分散的權重泛化較好（sources: 1）
- [Optimization](concepts/optimization.md) — loss landscape、convex 與 non-convex、三種策略、iterative refinement（sources: 1）
- [Gradient Descent](concepts/gradient-descent.md) — numerical 與 analytic gradient、gradient check、learning rate、mini-batch／SGD（sources: 1）
- [Backpropagation](concepts/backpropagation.md) — chain rule、電路圖、local gradient、add／max／mul 的模式、staged computation（sources: 1）
- [Data Preprocessing](concepts/data-preprocessing.md) — centering、縮放；資料尺度會影響 gradient 與 learning rate（sources: 1）
- [Neural Network](concepts/neural-network.md) — 疊起來的 linear classifier 加上非線性；層狀組織、universal approximator、深度（sources: 1）
- [Activation Function](concepts/activation-function.md) — sigmoid、tanh、ReLU、Leaky ReLU、Maxout；「用 ReLU，不要用 sigmoid」（sources: 1）
- [Overfitting](concepts/overfitting.md) — capacity、generalization；用大網路加 regularization，而不是縮小網路（sources: 1）
- [Convolutional Neural Network (CNN)](concepts/convolutional-neural-network.md) — 為影像設計的神經網路；3D volume、層的排列模式、經典架構演進（sources: 1）
- [Convolutional Layer](concepts/convolutional-layer.md) — local connectivity、輸出大小公式、parameter sharing、im2col（sources: 1）
- [Pooling Layer](concepts/pooling-layer.md) — max pooling、downsampling、backward 的 switches（sources: 1）
- [Hyperparameter Tuning](concepts/hyperparameter-tuning.md) — validation set、cross-validation、test set 只用一次；λ 要調、Δ 不用調；learning rate、batch size（sources: 1）

## Datasets

- [CIFAR-10](datasets/cifar-10.md) — 60,000 張 32×32 影像、10 類的入門資料集（sources: 1）
- [ILSVRC](datasets/ilsvrc.md) — ImageNet 的大規模影像分類挑戰賽，約 120 萬張訓練影像；歷年 CNN 冠軍（sources: 1）

## Comparisons

（尚無）

## Sources

| cite key | 頁面 | 說明 |
|---|---|---|
| `CS231n` | [CS231n 課程筆記](sources/cs231n.md) | Stanford CS231n 課程筆記（已 ingest：classification、linear-classify、optimization-1、optimization-2、neural-networks-1、convolutional-networks） |
