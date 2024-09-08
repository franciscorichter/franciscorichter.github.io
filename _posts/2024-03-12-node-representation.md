---
title: 'Node Representation'
date: 2024-03-12
permalink: /posts/2012/08/blog-post-4/
tags:
  - cool posts
  - category1
  - category2
---

# Chapter 4: Node Representations

## 4.1 Introduction
One of the key challenges in machine learning tasks is the **dimensionality** of the data. High-dimensional data is difficult to process, particularly when the number of training examples is relatively small. In network analysis, the data is often represented as an **adjacency matrix** of size \(N \times N\), where \(N\) is the number of nodes in the network graph. This makes the dimensionality problem especially challenging.

Applications of network data include tasks like friend recommendation in social networks, clustering papers in citation networks, and identifying communities in user interest networks. For these tasks, we need low-dimensional representations of the nodes in the network, also known as **embeddings**. These embeddings are crucial for downstream tasks such as classification, clustering, and visualization.

## 4.2 Random Walk-Based Approaches

### 4.2.1 DeepWalk: Online Learning of Social Representations
**DeepWalk** is a popular unsupervised technique for learning node embeddings based on random walks. The idea is to treat random walks in a graph like sentences in a language and apply models like **skip-gram** to learn node representations.

Given a graph \(G = (V, E)\), DeepWalk first performs random walks for each node. Each walk is a sequence of nodes starting from a root node. The sequence captures local structure, and the skip-gram model is used to learn representations for each node by predicting its neighboring nodes in the walk.

The objective function for DeepWalk is as follows:

\[
\min_g -\log \Pr(\{v_{i-k}, \dots, v_{i+k} \} \mid g(v_i))
\]

Where the window size \(k\) defines the neighborhood of a node in a random walk. The function \(g(v_i)\) gives the embedding of node \(v_i\), and the goal is to maximize the probability of observing neighboring nodes given the embedding of the root node.

### 4.2.2 Scalable Feature Learning for Networks: Node2Vec
**Node2Vec** improves upon DeepWalk by introducing a **biased random walk** that can transition between **breadth-first** and **depth-first** searches. This allows Node2Vec to learn representations that capture both **local** and **global** structures in the network.

Node2Vec introduces two parameters:
- **p** controls the likelihood of revisiting a node, allowing for deeper exploration of local neighborhoods.
- **q** biases the random walk to either explore outward (depth-first) or stay near the root (breadth-first).

Like DeepWalk, Node2Vec uses the **skip-gram** model to learn node embeddings. The optimization problem is similar:

\[
\min_g -\sum_{v_j \in N(v_i)} \log \Pr(v_j \mid g(v_i))
\]

Where \(N(v_i)\) is the neighborhood of node \(v_i\), and the probability of observing a node \(v_j\) given the embedding of \(v_i\) is modeled using a softmax function.

## 4.3 Matrix Factorization-Based Algorithms

### 4.3.1 Network Representation Learning with Rich Text Information
Some node embedding methods, such as **Text-Associated DeepWalk (TADW)**, integrate node features (e.g., textual attributes) with network structure to improve node representations. TADW reformulates DeepWalk as a **matrix factorization** problem:

\[
\min_{Z, S} \|P - Z^T S\|_F^2 + \lambda (\|Z\|_F^2 + \|S\|_F^2)
\]

Where \(P\) is a matrix of transition probabilities between nodes, \(Z\) and \(S\) are matrices containing node embeddings, and \(\lambda\) is a regularization term to avoid overfitting. TADW extends this by incorporating text features into the factorization process.

### 4.3.2 GraRep: Learning Graph Representations with Global Structural Information
**GraRep** focuses on learning representations that capture long-range dependencies between nodes by considering **k-step** relations. For each value of \(k\), GraRep computes the **k-step transition matrix** \(A^k\) and solves an optimization problem similar to skip-gram:

\[
L_k = \sum_{i \in V} \sum_{j \in V} \log \sigma( \mathbf{v}_i \cdot \mathbf{v}_j ) - \gamma \mathbb{E}_{j' \sim P_k(V)} [\log \sigma(- \mathbf{v}_i \cdot \mathbf{v}_{j'})]
\]

Where \(\sigma\) is the sigmoid function, \(\gamma\) controls the number of negative samples, and \(P_k(V)\) is a distribution over nodes used for negative sampling.

## 4.4 Graph Neural Networks

### 4.4.1 Semi-Supervised Classification with Graph Convolutional Networks (GCNs)
GCNs are a powerful approach for semi-supervised learning on graphs. The key idea is to apply **convolutional filters** directly to graph data. For a graph \(G = (V, E)\) with node features \(X\), a GCN layer is defined as:

\[
H^{(l+1)} = \sigma(\tilde{D}^{-1/2} \tilde{A} \tilde{D}^{-1/2} H^{(l)} W^{(l)})
\]

Where \(\tilde{A} = A + I\) is the adjacency matrix with added self-loops, \(\tilde{D}\) is the degree matrix, \(W^{(l)}\) is the layer-specific weight matrix, and \(\sigma\) is a non-linear activation function.

### 4.4.2 Graph Attention Networks (GAT)
**Graph Attention Networks (GATs)** improve on GCNs by incorporating an **attention mechanism** to weight the importance of neighboring nodes. In GAT, the hidden state of a node \(i\) is computed as:

\[
h_i' = \sigma \left( \sum_{j \in \mathcal{N}(i)} \alpha_{ij} W h_j \right)
\]

Where \(\alpha_{ij}\) is the attention coefficient that determines the importance of node \(j\) for node \(i\), and \(W\) is a learned weight matrix.

## 4.5 Experimental Evaluation

### 4.5.1 Node Classification
Node embeddings can be evaluated by their performance on node classification tasks. Supervised methods like GCN often outperform unsupervised methods like DeepWalk because they can leverage label information during training.

### 4.5.2 Node Clustering
Unsupervised methods like DeepWalk and Node2Vec are typically evaluated using clustering accuracy. The embeddings are passed to a clustering algorithm like **K-Means**, and the quality of the clusters is measured using **clustering accuracy**.

### 4.5.3 Visualization
The learned node embeddings can be visualized using techniques like **t-SNE** to project the embeddings into a 2D space. This allows us to see how well the embeddings capture the structure of the graph.

## 4.6 Summary
In this chapter, we explored several methods for learning node embeddings. These methods include random walk-based approaches like DeepWalk and Node2Vec, matrix factorization methods like TADW and GraRep, and deep learning approaches like GCNs and GATs. Node embeddings are crucial for tasks such as node classification, clustering, and visualization.


