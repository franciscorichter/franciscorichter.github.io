---
title: 'Lecture notes 3: Machine Learning for Network Analysis'
date: 2024-10-22
permalink: /posts/2024/10/machine-learning-network-analysis/
tags:
  - social networks
  - machine learning
  - graph theory
  - network analysis
---

Machine learning (ML) techniques have become a cornerstone in the analysis of social networks, enabling us to leverage the structural complexity of networks to perform tasks such as node classification, link prediction, and community detection. By embedding graph structures into vector spaces, ML algorithms can process these representations to uncover insights that are otherwise hidden in high-dimensional, non-Euclidean data.

## Machine Learning in Social Networks

Social networks represent intricate relationships between entities, which are typically modeled as graphs $G = (V, E)$, where $V$ is the set of nodes (users, entities) and $E$ is the set of edges (relationships). To apply machine learning algorithms, which expect data in a tabular or vectorized form, it is essential to transform this complex structure into a **low-dimensional embedding**. The goal of **network representation learning** is to generate these embeddings while preserving the inherent graph properties such as connectivity, proximity, and community structure.

### Network Representation Learning

The fundamental problem in network representation learning is to map each node $v \in V$ to a point $\mathbf{z}_v \in \mathbb{R}^d$, where $d$ is much smaller than the number of nodes $n$, typically $d \ll n$. This embedding space enables the application of machine learning techniques for tasks such as classification and clustering.

#### Random Walk-Based Embeddings

One of the most effective approaches for network representation learning is through **random walks**. A random walk on the graph generates sequences of nodes that encode the local neighborhood structure. Algorithms like **DeepWalk** and **node2vec** rely on this principle to produce embeddings.

Given a graph $G$, a random walk starting at node $v$ generates a sequence of nodes $\{v_1, v_2, ..., v_t\}$, which can be treated as analogous to a sentence in a corpus. Using the skip-gram model, we learn embeddings that maximize the co-occurrence probability of nodes appearing in the same walk. 

**node2vec** extends DeepWalk by allowing flexible random walks. The walk can be biased using parameters $p$ and $q$, controlling whether the random walk behaves more like a **depth-first search (DFS)** or **breadth-first search (BFS)**.

For more details, see [DeepWalk](https://arxiv.org/pdf/1403.6652) and [node2vec](https://snap.stanford.edu/node2vec/).

#### Matrix Factorization-Based Approaches

Matrix factorization methods such as **Singular Value Decomposition (SVD)** offer a more global perspective by factoring the graph's adjacency matrix $A$ into a lower-dimensional approximation. This is formalized as:

$$
A \approx U \Sigma V^T
$$

where:
- $A \in \mathbb{R}^{n \times n}$ is the adjacency matrix of the graph,
- $U \in \mathbb{R}^{n \times d}$ and $V \in $\mathbb{R}^{n \times d}$ are orthogonal matrices representing the embeddings of the nodes,
- $\Sigma \in \mathbb{R}^{d \times d}$ is a diagonal matrix of singular values capturing the most significant structural information.

SVD provides embeddings that preserve both local and global relationships in the graph, enabling efficient learning for downstream tasks.

#### Graph Neural Networks (GNNs)

The emergence of **Graph Neural Networks (GNNs)** has transformed how we handle graph-structured data. GNNs generalize traditional neural networks by allowing them to operate directly on the graph's structure. In GNNs, the embedding of a node $v$ is updated based on the features of its neighbors through a message-passing mechanism.

The update rule for a **Graph Convolutional Network (GCN)**, for example, is typically written as:

$$
H^{(l+1)} = \sigma\left( D^{-1/2} A D^{-1/2} H^{(l)} W^{(l)} \right)
$$

where:
- $H^{(l)}$ represents the node embeddings at layer $l$,
- $A$ is the adjacency matrix,
- $D$ is the degree matrix,
- $W^{(l)}$ are trainable weight matrices, and
- $\sigma$ is a non-linear activation function.

This iterative process allows nodes to aggregate information from their neighbors, producing embeddings that are highly informed by both node features and graph structure.

### Machine Learning Tasks on Networks

Once node embeddings are learned, we can apply them to several machine learning tasks relevant to social network analysis:

#### Node Classification

The goal of **node classification** is to predict the label of a node, such as categorizing users as "influencers" or "casual users." Given a set of embeddings $\mathbf{z}_v$, a classifier such as **logistic regression** or **support vector machines (SVM)** can be trained to assign labels to nodes:

$$
\hat{y}_v = \text{softmax}(W \mathbf{z}_v)
$$

where $W$ is a weight matrix learned by the classifier, and $\hat{y}_v$ is the predicted label for node $v$.

#### Link Prediction

**Link prediction** aims to infer the existence of edges between nodes, predicting whether two nodes will form a new connection in the future or whether there are missing edges in the current graph. A common approach is to compute the similarity between two node embeddings $\mathbf{z}_u$ and $\mathbf{z}_v$, often using metrics such as the **dot product**:

$$
\text{score}(u, v) = \mathbf{z}_u^T \mathbf{z}_v
$$

A higher score indicates a higher likelihood that an edge exists between nodes $u$ and $v$.

#### Clustering and Community Detection

In **community detection**, we aim to group nodes into clusters that exhibit high internal connectivity. Once embeddings are computed, nodes that are close in the embedding space can be clustered using traditional clustering algorithms such as **k-means**:

$$
\min_{C} \sum_{v \in V} \|\mathbf{z}_v - \mu_{C(v)}\|^2
$$

where $C(v)$ is the cluster assignment of node $v$, and $\mu_{C(v)}$ is the centroid of the cluster.

This allows for the discovery of cohesive groups in social networks, providing insights into social dynamics and influence patterns.

#### Visualization of Embeddings

Finally, embeddings can be visualized by reducing their dimensionality to 2D or 3D using techniques like **t-SNE** or **PCA**. Visualization helps in understanding the overall structure of the network, highlighting clusters, communities, and potential outliers.

---

By embedding graph data into vector spaces, machine learning models can harness the underlying structure of social networks for predictive tasks such as classification and link prediction. Techniques like random walks, matrix factorization, and graph neural networks provide a robust foundation for tackling increasingly complex social network data. As networks continue to grow, these machine learning approaches will remain central to unlocking insights hidden within their intricate webs of relationships.
