---
title: 'Lecture notes 5: Node Representations in Network Analysis'
date: 2024-12-05
permalink: /posts/2024/12/node-representations/
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

-----------------------------------

In network analysis, representing nodes in a meaningful way is crucial for understanding the structure and relationships within graphs. **Node representation learning** refers to the process of converting high-dimensional, complex network data into a low-dimensional space where essential structural information is preserved. These embeddings simplify tasks such as node classification, link prediction, clustering, and community detection.

## Key Properties of Node Representations

For node embeddings to be effective, they must encode several key aspects of the graph's structure:

- **First-order proximity**: Nodes that are directly connected in the graph should be close in the embedding space.
- **Higher-order proximity**: Embeddings should reflect multi-hop relationships, capturing more global structures beyond immediate neighbors.
- **Community structure**: Nodes within the same community or cluster should have similar embeddings, reflecting homophily.
- **Structural roles**: Nodes with similar roles (e.g., hubs or bridges) should have similar embeddings, even if they are not directly connected.

## Approaches to Node Representation Learning

### Random Walk-Based Approaches

**Random walk-based methods** generate sequences of nodes by simulating random walks over the graph, which are then treated as "sentences" in natural language processing. The **skip-gram** model is applied to learn embeddings from these walks. Two widely-used methods are **DeepWalk** and **node2vec**.

#### DeepWalk

DeepWalk performs uniform random walks on a graph to capture the local neighborhood structure of each node. These walks are analogous to sentences, and the skip-gram model is used to maximize the likelihood that nearby nodes in a walk are predicted to be in each other's context. The goal is to learn embeddings that reflect both local and global relationships.

The objective function in DeepWalk is designed to maximize the probability of observing a node's neighbors in the walk:

$$
\sum_{v \in V} \sum_{u \in N(v)} \log P(u | v)
$$

where \(N(v)\) represents the set of nodes neighboring \(v\) in the random walks.

#### Node2Vec

Node2Vec extends DeepWalk by introducing a biased random walk mechanism, allowing for control over the walk strategy. It uses two parameters:

- **p**: Controls the likelihood of revisiting a node (return parameter).
- **q**: Controls the likelihood of exploring outward from the starting node (in-out parameter).

With these two parameters, Node2Vec can balance between breadth-first search (capturing homophily) and depth-first search (capturing structural equivalence). This flexibility allows Node2Vec to capture both local and global relationships.

### Matrix Factorization-Based Approaches

Matrix factorization-based methods aim to reduce the dimensionality of large matrices that represent node relationships. These methods often focus on factorizing the **adjacency matrix** or its transformations, preserving important structural information.

#### GraRep

GraRep (Graph Representation) is a matrix factorization approach that captures multi-hop relationships by factorizing higher-order proximity matrices. It factorizes multiple powers of the adjacency matrix, representing k-step transitions between nodes. By combining the embeddings learned at different steps, GraRep captures both local and global structures.

The objective function for GraRep is:

$$
L_k = \sum_{i \in V} \sum_{j \in V} \log P(j | i)
$$

where \(P(j | i)\) represents the probability of transitioning from node \(i\) to node \(j\) in a k-step walk. By considering different values of \(k\), GraRep can capture the structure across multiple scales.

### Deep Learning-Based Approaches

Deep learning methods for node representation learning include **Graph Neural Networks (GNNs)**, which directly learn node embeddings from both the graph's structure and node features.

#### Graph Convolutional Networks (GCNs)

GCNs are an extension of traditional convolutional neural networks to graphs. Instead of applying convolutions to grids (such as images), GCNs apply convolutions to the local neighborhoods of nodes. Each node aggregates information from its neighbors, learning embeddings that incorporate both local and global information.

The update rule in a GCN is:

$$
H^{l+1} = \sigma(D^{-1/2} A D^{-1/2} H^l W^l)
$$

where:
- \(A\) is the adjacency matrix,
- \(D\) is the degree matrix,
- \(H^l\) is the node embedding at layer \(l\),
- \(W^l\) is the learnable weight matrix,
- \(\sigma\) is a non-linear activation function (like ReLU).

By stacking multiple layers, GCNs capture information from farther-away neighbors, allowing for more comprehensive node representations.

#### Graph Attention Networks (GATs)

GATs improve upon GCNs by incorporating attention mechanisms, where each node learns to weigh the importance of its neighbors. This attention mechanism allows GATs to focus on the most relevant neighbors during the aggregation process.

The attention coefficient between two nodes \(i\) and \(j\) is calculated as:

$$
\alpha_{ij} = \frac{\exp(\text{LeakyReLU}(a^T [Wh_i \parallel Wh_j]))}{\sum_{k \in N(i)} \exp(\text{LeakyReLU}(a^T [Wh_i \parallel Wh_k]))}
$$

where \(h_i\) and \(h_j\) are the hidden states of nodes \(i\) and \(j\), \(a\) is the attention vector, and \(\parallel\) denotes concatenation. The attention scores allow the model to assign more importance to certain neighbors, improving performance on tasks like node classification and link prediction.

## Applications of Node Representations

Once learned, node representations can be applied to a variety of tasks in network analysis:

### Node Classification

In **node classification**, embeddings are used as features to predict labels for unlabeled nodes. The embeddings capture structural properties of the nodes, which can be leveraged by classifiers such as logistic regression:

$$
\hat{y}_v = \text{softmax}(W z_v)
$$

where \(z_v\) is the learned embedding for node \(v\), and \(W\) is a weight matrix learned during training.

### Link Prediction

In **link prediction**, the task is to predict whether an edge will form between two nodes. This can be done by computing a similarity score between the embeddings of the two nodes, typically using the dot product:

$$
\text{score}(u, v) = z_u^T z_v
$$

Higher scores indicate a higher likelihood that a link exists between nodes \(u\) and \(v\).

### Clustering and Community Detection

Node embeddings can also be used for **clustering** and **community detection**. Nodes with similar embeddings are likely to belong to the same community, and clustering algorithms like **k-means** can be applied directly to the embeddings to identify these communities.


---------------------------

Node representation learning is central to network analysis, as it converts high-dimensional, sparse network data into low-dimensional vectors that are easy to process. These embeddings preserve critical structural information, making downstream tasks like node classification, link prediction, and community detection feasible and effective. In this lecture, we expand on techniques not previously covered, emphasizing **graph kernels**, **graph-level representations**, and **pooling techniques** for embedding entire graphs.

### Graph-Level Representations

Beyond individual nodes, it's essential to represent entire graphs in a way that captures their global structure. **Graph embedding** seeks to create a low-dimensional vector for an entire graph, which enables tasks such as graph classification and comparison. This is particularly useful in applications like drug discovery, where the objective might be to predict the biological activity of molecules, or in social networks, where the goal is to classify communities or network behavior.

Graph kernels play a critical role in this task. These kernels compute the similarity between graphs based on various graph properties.

- **Weisfeiler-Lehman Subtree Kernel**: This graph kernel compares subtree patterns across graphs, determining their similarity by counting common substructures. It is widely used for tasks requiring the comparison of graphs based on node and edge patterns.
  
- **Random Walk Kernel**: This kernel counts the number of common random walks between two graphs, providing a similarity measure based on the paths traversed by random walks across nodes in different graphs.

### Graph Pooling and Aggregation Techniques

For graph-level tasks, pooling methods are used to aggregate node representations into a single vector that captures the entire graph's structure. These operations are vital for reducing the graph's complexity while retaining essential information.

- **DIFFPOOL**: DiffPool is a differentiable pooling mechanism that clusters nodes based on learned soft assignments, progressively pooling the graph into a coarser structure. This technique enables the model to preserve hierarchical graph structures, which is useful for tasks like graph classification.

  The pooling operation is mathematically defined as:

  \[
  Z^{(l+1)} = \text{softmax}(A^{(l)} \cdot P^{(l)})
  \]

  where \(P^{(l)}\) represents the learned soft assignment matrix at layer \(l\), and \(A^{(l)}\) is the adjacency matrix of the graph at layer \(l\).

- **SAGPool**: Self-Attention Graph Pooling (SAGPool) employs self-attention mechanisms to select the most informative nodes during pooling. By incorporating attention scores, it learns to downsample the graph while focusing on the most critical nodes.

### Advanced Graph Embedding Methods

Recent methods for graph embeddings have focused on using **Graph Neural Networks (GNNs)** to learn both node and graph-level representations:

1. **Graph Isomorphism Network (GIN)**: GIN is a powerful GNN variant that achieves maximal expressiveness by using a more flexible aggregation function. GIN captures both local neighborhood information and node attributes, making it highly effective for tasks like graph classification.

2. **Graph U-Nets**: These architectures mimic the U-Net structure from convolutional neural networks, where downsampling (pooling) and upsampling layers are used to encode and then reconstruct graph features. **Graph U-Nets** have proven effective in node classification tasks by allowing for multi-scale feature extraction and reconstruction across different graph resolutions.

### Applications of Node Representations

Once node embeddings are learned, they can be applied to various tasks. Some of these include:

1. **Graph Classification**: With node and graph embeddings, classifiers can predict the category of an entire graph. This is particularly relevant in fields like bioinformatics, where graphs represent molecules or proteins, and the task is to predict their function or behavior.

2. **Graph Clustering**: Clustering techniques applied to node or graph embeddings help identify communities or substructures within networks. This can be applied to detect cohesive subgroups in social networks or to group molecules with similar properties in chemistry.

3. **Visualization**: Embeddings allow for the projection of high-dimensional graph data into 2D or 3D spaces for visualization. This is often done using dimensionality reduction techniques like **t-SNE** or **PCA** to observe clusters or patterns in the data visually.
