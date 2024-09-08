---
title: 'Node Representations in Network Analysis'
date: 2024-09-07
permalink: /posts/2024/09/node-representations/
tags:
  - node embeddings
  - graph representation learning
  - GCN
---



**Node embeddings** are low-dimensional vector representations of nodes in a graph. These embeddings are essential for tasks like classification, clustering, and link prediction. Various methods are used to learn node embeddings, including random walk-based approaches, matrix factorization, and deep learning techniques.

## Random Walk-Based Approaches

### DeepWalk

**DeepWalk** learns node embeddings by treating random walks as sentences and applying the **skip-gram** model to predict neighboring nodes. The objective function is:

$$
\min_g -\log \Pr(\{v_{i-k}, \dots, v_{i+k} \} \mid g(v_i))
$$

where \( g(v_i) \) is the embedding of node \( v_i \).

### Node2Vec

**Node2Vec** improves on DeepWalk by introducing a **biased random walk** that balances breadth-first and depth-first searches. It uses two parameters:
- \( p \): Controls the likelihood of revisiting nodes.
- \( q \): Biases towards outward exploration.

The objective function remains similar to DeepWalk.

## Matrix Factorization-Based Approaches

### TADW

**Text-Associated DeepWalk (TADW)** incorporates node features (e.g., text) into the embedding process. It solves the following optimization problem:

$$
\min_{Z, S} \|P - Z^T S\|_F^2 + \lambda (\|Z\|_F^2 + \|S\|_F^2)
$$

where \( P \) is the transition matrix, \( Z \) and \( S \) are embedding matrices, and \( \lambda \) is a regularization term.

### GraRep

**GraRep** captures global structural information by considering **k-step** transition matrices. The objective function is:

$$
L_k = \sum_{i \in V} \sum_{j \in V} \log \sigma( \mathbf{v}_i \cdot \mathbf{v}_j ) - \gamma \mathbb{E}_{j' \sim P_k(V)} [\log \sigma(- \mathbf{v}_i \cdot \mathbf{v}_{j'})]
$$

where \( \sigma \) is the sigmoid function.

## Graph Neural Networks

### Graph Convolutional Networks (GCN)

GCNs apply convolution directly to graph data. A GCN layer is defined as:

$$
H^{(l+1)} = \sigma(\tilde{D}^{-1/2} \tilde{A} \tilde{D}^{-1/2} H^{(l)} W^{(l)})
$$

where \( \tilde{A} = A + I \) is the adjacency matrix with self-loops.

### Graph Attention Networks (GAT)

GATs use an **attention mechanism** to weigh the importance of neighboring nodes. The hidden state of node \( i \) is:

$$
h_i' = \sigma \left( \sum_{j \in \mathcal{N}(i)} \alpha_{ij} W h_j \right)
$$

where \( \alpha_{ij} \) is the attention coefficient.

## Conclusion

In this chapter, we explored various methods for learning node embeddings, including random walk-based methods like DeepWalk and Node2Vec, matrix factorization approaches like TADW and GraRep, and deep learning models like GCNs and GATs.
