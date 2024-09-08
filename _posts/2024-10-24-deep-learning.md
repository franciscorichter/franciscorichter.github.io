---
title: 'Deep Learning for Network Analysis'
date: 2024-10-24
permalink: /posts/2024/09/deep-learning/
tags:
  - deep learning
  - graph neural networks
  - node embeddings
---

## Introduction

Deep learning has transformed many fields by enabling the automatic learning of data representations. In network analysis, deep learning has significantly impacted **representation learning**, allowing machines to learn useful features from graphs for tasks like classification, clustering, and link prediction.

## Neural Networks

### Perceptron

The **perceptron** is one of the earliest models for binary classification. It classifies data by applying weights to input features. The model is represented as:

$$
y = \text{sgn} \left( \sum_{i=1}^{n} w_i x_i + b \right)
$$

where:
- \( w_i \) are the weights,
- \( x_i \) are the input features,
- \( b \) is the bias.

### Multilayer Perceptron Networks

A **Multilayer Perceptron (MLP)** extends the basic perceptron by adding hidden layers and applying an activation function to introduce non-linearity. A common activation function is **ReLU**:

$$
f(x) = \max(0, x)
$$

Training MLPs involves **backpropagation**, which updates weights based on the error gradients:

$$
w \leftarrow w - \eta \frac{\partial L}{\partial w}
$$

where \( \eta \) is the learning rate and \( L \) is the loss function.

## Convolutional Neural Networks (CNNs)

CNNs are designed for tasks like image recognition but can also be applied to graph data. The convolution operation for an image is defined as:

$$
O(i, j) = f \left( \sum_{m=1}^{M} \sum_{n=1}^{N} I(i + m - 1, j + n - 1)T(m, n) \right)
$$

where:
- \( T \) is the filter (kernel),
- \( I \) is the input image (or graph),
- \( f \) is the activation function.

CNNs apply these filters across the data, capturing important patterns.

## Recurrent Neural Networks (RNNs)

**RNNs** are designed for sequence data, allowing the model to retain information across time steps. The hidden state at time \( t \) is updated as:

$$
h_t = \sigma(W_h h_{t-1} + W_x x_t + b)
$$

### Long Short-Term Memory (LSTM)

LSTMs improve RNNs by adding **gates** to control memory retention and updates. The **forget gate** is defined as:

$$
f_t = \sigma(W_f [h_{t-1}, x_t] + b_f)
$$

## Autoencoders

**Autoencoders** are used for unsupervised learning. They compress input data and then reconstruct it. The loss function for an autoencoder is:

$$
\text{Loss} = \frac{1}{2} \sum_{i=1}^{n} |x_i - \hat{z}_i|^2
$$

Variants include **denoising autoencoders** and **sparse autoencoders**.

## Conclusion

Deep learning provides powerful tools for network analysis, including models like MLPs, CNNs, RNNs, LSTMs, and autoencoders. These techniques enable representation learning and are essential for solving complex tasks in graph data.
