---
title: 'Lecture notes 4: Deep Learning for Network Analysis'
date: 2024-10-24
permalink: /posts/2024/10/deep-learning/
tags:
  - deep learning
  - graph neural networks
  - node embeddings
---

Deep learning has transformed many fields by enabling machines to automatically learn data representations. In network analysis, deep learning plays a pivotal role in **representation learning**, facilitating the extraction of meaningful features from graphs for tasks such as classification, clustering, and link prediction.

## Neural Networks

### Perceptron

A **perceptron** is a fundamental model used for binary classification. The model applies a linear combination of weights to input features and then classifies the result using a sign function. Mathematically, the perceptron can be written as:

$$
y = \text{sgn} \left( \sum_{i=1}^{n} w_i x_i + b \right)
$$

where:
- $w_i$ represents the weights,
- $x_i$ are the input features,
- $b$ is the bias term.

While simple, the perceptron model struggles with non-linear patterns, leading to the development of more complex architectures such as the **Multilayer Perceptron (MLP)**.

### Multilayer Perceptron (MLP)

An **MLP** consists of multiple layers of neurons, including hidden layers that introduce non-linearity through activation functions like **ReLU**:

$$
f(x) = \max(0, x)
$$

Training MLPs involves the **backpropagation** algorithm, which adjusts the weights to minimize the error using gradient descent:

$$
w \leftarrow w - \eta \frac{\partial L}{\partial w}
$$

where $ \eta $ is the learning rate and $ L $ is the loss function. This iterative process updates the weights to improve the model's predictions.

## Graph Neural Networks (GNNs)

While traditional neural networks are highly effective for Euclidean data such as images or text, graphs are non-Euclidean structures, requiring specialized architectures. **Graph Neural Networks (GNNs)** generalize neural networks to graph data by allowing nodes to aggregate information from their neighbors, effectively learning graph-structured representations.

### Graph Convolutional Networks (GCNs)

A **Graph Convolutional Network (GCN)** extends the convolutional operation from grids (like pixels in an image) to graphs. The key idea is that each node aggregates features from its neighbors to update its representation. The update rule for a GCN layer can be expressed as:

$$
H^{(l+1)} = \sigma \left( D^{-1/2} A D^{-1/2} H^{(l)} W^{(l)} \right)
$$

where:
- $H^{(l)}$ are the node embeddings at layer $l$,
- $A$ is the adjacency matrix of the graph,
- $D$ is the degree matrix,
- $W^{(l)}$ is the layer's weight matrix,
- $ \sigma $ is an activation function (e.g., ReLU).

This allows each node to combine information from its neighbors, progressively learning higher-level representations through multiple layers.

### Graph Attention Networks (GATs)

**Graph Attention Networks (GATs)** build upon GCNs by incorporating an attention mechanism, which enables the model to learn different importance weights for each neighbor. The attention coefficient $\alpha_{ij}$ between nodes $i$ and $j$ is computed as:

$$
\alpha_{ij} = \frac{\exp \left( \text{LeakyReLU} \left( a^T [W h_i \parallel W h_j] \right) \right)}{\sum_{k \in \mathcal{N}(i)} \exp \left( \text{LeakyReLU} \left( a^T [W h_i \parallel W h_k] \right) \right)}
$$

where:
- $ h_i $ is the hidden state of node $ i $,
- $ W $ is a learnable weight matrix,
- $ a $ is the attention vector,
- $ \parallel $ denotes concatenation.

This mechanism allows the model to focus on the most important neighbors, improving performance on tasks where different neighbors contribute differently to node classification or link prediction.

## Autoencoders for Graphs

**Autoencoders** are used for unsupervised learning of graph embeddings. They consist of an encoder, which compresses the graph's structure into a low-dimensional latent space, and a decoder, which attempts to reconstruct the original graph from these embeddings. The reconstruction loss is typically formulated as:

$$
\text{Loss} = \frac{1}{2} \sum_{i,j} \left( A_{ij} - \hat{A}_{ij} \right)^2
$$

where $A_{ij}$ represents the adjacency matrix of the graph, and $\hat{A}_{ij}$ is the reconstructed matrix from the decoder. **Variational Graph Autoencoders (VGAEs)** extend this model by incorporating probabilistic latent variables, making them robust to noise.

## DeepWalk and Node2Vec

For network embedding, **DeepWalk** and **Node2Vec** are pivotal algorithms based on random walks. They generate sequences of nodes by simulating random walks over the graph, and treat these sequences as "sentences" in a corpus, applying the **word2vec** algorithm to obtain node embeddings.

- **DeepWalk** performs uniform random walks to capture the local neighborhood of each node.
- **Node2Vec** introduces parameters $p$ and $q$ to bias the random walks towards breadth-first or depth-first search, thus capturing both homophily and structural equivalence.

The learned embeddings can be used for downstream tasks such as classification, link prediction, or clustering.

## Application to Social Networks

The embeddings learned through GNNs or random walk-based methods can be applied to various tasks in social network analysis:

### Node Classification

Given a graph with partially labeled nodes, **node classification** predicts the labels of the unlabeled nodes. The learned embeddings serve as features for classifiers like logistic regression:

$$
\hat{y}_v = \text{softmax} (W \mathbf{z}_v)
$$

where $ \mathbf{z}_v $ is the embedding of node $ v $ and $ W $ is a trainable weight matrix.

### Link Prediction

In **link prediction**, the task is to predict whether an edge exists between two nodes. This can be achieved by calculating the similarity between their embeddings, typically using the dot product or cosine similarity:

$$
\text{score} (u, v) = \mathbf{z}_u^T \mathbf{z}_v
$$

A higher score implies a higher likelihood of a future connection between nodes $u$ and $v$.
