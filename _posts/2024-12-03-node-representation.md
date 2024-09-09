---
title: 'Lecture Notes 5: Node Representations in Network Analysis'
date: 2024-12-03
permalink: /posts/2024/12/node-representations/
tags:
  - node embeddings
  - graph representation learning
  - GCN
---

**Node embeddings** are low-dimensional vector representations of nodes in a graph. These embeddings play a crucial role in tasks such as classification, clustering, and link prediction. Learning effective node representations involves preserving essential structural properties from the graph in a more compact, vectorized format. Several approaches to learning node embeddings exist, including random walk-based methods, matrix factorization, and deep learning techniques like Graph Neural Networks (GNNs).

## Key Properties of Node Representations

For node embeddings to be effective, they must encode several key aspects of the graph's structure:

- **First-order proximity**: Nodes that are directly connected in the graph should be close in the embedding space.
- **Higher-order proximity**: Embeddings should reflect multi-hop relationships, capturing more global structures beyond immediate neighbors.
- **Community structure**: Nodes within the same community or cluster should have similar embeddings, reflecting homophily.
- **Structural roles**: Nodes with similar roles (e.g., hubs or bridges) should have similar embeddings, even if they are not directly connected.

## Random Walk-Based Approaches

### DeepWalk

**DeepWalk** learns node embeddings by simulating random walks over the graph and treating the resulting sequences as "sentences" in natural language processing. The **skip-gram** model is then used to maximize the likelihood that nodes close in the walk are also close in the embedding space. This approach captures both local and global relationships.

The objective function is:

\[
\min_g - \log \Pr(\{v_{i-k}, \dots, v_{i+k} \} \mid g(v_i))
\]

where \( g(v_i) \) is the embedding of node \( v_i \), and the context nodes are those found in random walks around \( v_i \).

### Node2Vec

**Node2Vec** extends DeepWalk by introducing a biased random walk that allows control over the walk strategy. Two parameters, \( p \) and \( q \), control whether the random walk behaves more like breadth-first search (capturing homophily) or depth-first search (capturing structural equivalence). This flexibility enables Node2Vec to balance local and global structure more effectively.

## Matrix Factorization-Based Approaches

Matrix factorization methods aim to reduce the dimensionality of large matrices representing node relationships, preserving structural information while reducing complexity.

### GraRep

**GraRep** captures both local and global structures by factorizing k-step transition matrices. This approach generates embeddings by learning from multiple scales of node proximity, from immediate neighbors to more distant nodes.

The objective function for GraRep is:

\[
L_k = \sum_{i \in V} \sum_{j \in V} \log P(j \mid i)
\]

where \( P(j \mid i) \) represents the probability of transitioning from node \( i \) to node \( j \) in a k-step walk. GraRep captures both local and global structures by combining these embeddings across multiple steps.

### TADW (Text-Associated DeepWalk)

**TADW** integrates node features (such as text) into the embedding process. It extends DeepWalk by incorporating rich node attributes into the matrix factorization process, effectively learning both structural and feature-based embeddings.

## Deep Learning-Based Approaches

### Graph Neural Networks (GNNs)

**Graph Neural Networks (GNNs)** directly learn node embeddings from both the graph structure and node features. By applying convolutional operations to nodes and their neighbors, GNNs capture local patterns and propagate information across the graph. GNNs are particularly powerful for tasks like node classification, where both node features and the surrounding network context matter.

#### Graph Convolutional Networks (GCNs)

GCNs generalize the convolution operation to graphs. Each node aggregates features from its neighbors and updates its embedding. The update rule is:

\[
H^{(l+1)} = \sigma(D^{-1/2} A D^{-1/2} H^{(l)} W^{(l)})
\]

where:
- \( A \) is the adjacency matrix (with self-loops),
- \( D \) is the degree matrix,
- \( H^{(l)} \) represents the node embeddings at layer \( l \),
- \( W^{(l)} \) is the layer's weight matrix, and
- \( \sigma \) is a non-linear activation function (e.g., ReLU).

By stacking multiple layers, GCNs capture higher-order relationships in the graph.

#### Graph Attention Networks (GATs)

**Graph Attention Networks (GATs)** incorporate attention mechanisms to assign different importance weights to neighboring nodes. This approach allows GATs to learn which neighbors are most relevant to a node’s representation.

The hidden state of node \( i \) is computed as:

\[
h_i' = \sigma \left( \sum_{j \in \mathcal{N}(i)} \alpha_{ij} W h_j \right)
\]

where:
- \( \alpha_{ij} \) is the attention coefficient between nodes \( i \) and \( j \),
- \( W \) is a learnable weight matrix, and
- \( \sigma \) is an activation function.

By learning different attention weights for each neighbor, GATs improve the model's ability to focus on the most informative parts of the graph.

### Graph-Level Representations

In addition to node-level embeddings, it is sometimes necessary to represent entire graphs. **Graph embeddings** create low-dimensional vector representations for entire graphs, enabling tasks such as graph classification and comparison. This is particularly useful in applications like drug discovery, where graphs represent molecular structures.

Graph kernels, such as the **Weisfeiler-Lehman Subtree Kernel** and **Random Walk Kernel**, compute graph similarities by comparing substructures or paths across graphs.

### Graph Pooling and Aggregation Techniques

For graph-level tasks, pooling methods aggregate node embeddings into a single vector representing the entire graph. These techniques reduce the graph's complexity while retaining its essential information.

- **DIFFPOOL** clusters nodes into coarser representations through differentiable pooling, preserving hierarchical structures.
- **SAGPool** uses self-attention mechanisms to pool the most relevant nodes, focusing on important substructures.

## Applications of Node Representations

### Node Classification

In node classification, embeddings are used as features to predict labels for unlabeled nodes. For example, embeddings learned through GCNs or Node2Vec can be passed to a classifier like logistic regression to predict node labels.

\[
\hat{y}_v = \text{softmax}(W z_v)
\]

where \( z_v \) is the learned embedding for node \( v \).

### Link Prediction

Link prediction involves predicting the likelihood of an edge forming between two nodes. By using node embeddings, we can compute a similarity score (e.g., dot product) to assess whether a link should exist between two nodes:

\[
\text{score}(u, v) = z_u^T z_v
\]

Higher scores indicate a higher probability of a link between nodes \( u \) and \( v \).

### Clustering and Community Detection

Node embeddings can be used for clustering and community detection. Nodes with similar embeddings are grouped into clusters, representing communities or functional groups in the network. Clustering algorithms like **k-means** can be directly applied to the learned embeddings.

### Graph-Level Tasks

For tasks requiring whole-graph analysis, such as graph classification or clustering, the learned graph embeddings can be fed into downstream models. Pooling methods like DIFFPOOL or graph kernels provide effective ways to reduce entire graphs into meaningful representations.
