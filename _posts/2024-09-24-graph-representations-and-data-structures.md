---
title: 'Lecture Notes 2: Graph Representations and Data Structures'
date: 2024-09-24
permalink: /posts/2024/09/graph-representations-and-data-structures/
tags:
  - social networks
  - graph theory
  - data structures
  - network analysis
---

In this post, we explore the various ways to represent graphs and the data structures frequently used in social network analysis. Choosing the right representation is key, as it impacts memory efficiency, computational complexity, and algorithm performance.

## Introduction to Graph Representation

When working with social networks, we often deal with sparse graphs, where the number of edges is significantly smaller than \( n^2 \), the maximum possible number of edges for a graph with \( n \) nodes. Therefore, selecting an efficient graph representation becomes crucial. Different representations offer varying trade-offs in terms of memory usage and performance.

## Adjacency Matrix

An **adjacency matrix** is a square matrix \( A \in \mathbb{R}^{n \times n} \), where \( n \) is the number of nodes in the graph. The element \( A_{ij} \) indicates whether there is an edge between nodes \( v_i \) and \( v_j \):

$$
A_{ij} = 
\begin{cases} 
w_{ij}, & \text{if } (v_i, v_j) \in \mathcal{E}, \\
0, & \text{otherwise}.
\end{cases}
$$

Where \( w_{ij} \) represents the weight of the edge, or 1 for unweighted graphs.

### Example: Facebook Friendships

In a **Facebook-like network**, where each node represents a person, and an edge represents a friendship, the adjacency matrix would be used to check quickly if two people are friends. For a small group of friends, say 3 people (nodes), the adjacency matrix could look like:

\[
A = \begin{bmatrix} 
0 & 1 & 0 \\
1 & 0 & 1 \\
0 & 1 & 0 
\end{bmatrix}
\]

This matrix shows that person 1 is friends with person 2, and person 2 is friends with person 3.

### Space Complexity

The adjacency matrix uses \( O(n^2) \) space, which can be inefficient for large, sparse networks.

### Advantages:
- Constant-time \( O(1) \) lookup for edges between nodes.
- Useful for **dense graphs** where \( m \approx n^2 \).

### Disadvantages:
- High memory usage for sparse graphs, where most entries are 0.
- Inefficient for traversing the graph when there are few edges relative to nodes.

### Real-World Use Case:
Dense graphs like **fully connected networks** (e.g., some types of computer networks) might benefit from adjacency matrices. However, for large social networks with many users but fewer connections, adjacency matrices can be wasteful.

## Adjacency List

An **adjacency list** is a more efficient structure for sparse graphs. Each node stores a list of its neighbors, which represent the edges.

### Example: Twitter Follows

For a **Twitter-like network**, where users follow others, the adjacency list representation for 3 users, with user 1 following user 2 and user 2 following both user 1 and user 3, would be:

\[
\{ 1: [2], 2: [1, 3], 3: [2] \}
\]

### Space Complexity

The adjacency list requires \( O(n + m) \) space, where \( n \) is the number of nodes and \( m \) is the number of edges. This makes it suitable for **sparse graphs**.

### Advantages:
- Space-efficient for sparse graphs.
- Traversing all edges takes \( O(m) \) time.

### Disadvantages:
- Checking if a specific edge exists requires \( O(\text{deg}(v)) \), where \( \text{deg}(v) \) is the degree of the node.

### Real-World Use Case:
In social networks like **Twitter**, where users follow a relatively small fraction of others, adjacency lists provide a space-efficient way to store and query the network.

## Incidence Matrix

An **incidence matrix** represents the relationships between nodes and edges. It is a matrix \( B \in \mathbb{R}^{n \times m} \), where \( n \) is the number of nodes, and \( m \) is the number of edges.

$$
B_{ij} = 
\begin{cases} 
1, & \text{if node } v_i \text{ is incident to edge } e_j, \\
0, & \text{otherwise}.
\end{cases}
$$

### Example: Biological Networks

In **protein-protein interaction networks**, where multiple proteins interact with each other (with multiple edges between nodes), incidence matrices help represent these multiple connections effectively.

### Space Complexity

The incidence matrix requires \( O(n \times m) \) space, a middle ground in memory efficiency.

### Advantages:
- Effective for representing multigraphs.
- Can handle multiple edges between node pairs.

### Disadvantages:
- Inefficient for extracting neighbor information.
- More complex for analyzing individual nodes' properties.

### Real-World Use Case:
In **biological networks**, where nodes represent proteins and edges represent interactions, the incidence matrix can capture complex relationships with multiple connections.

## Matrix Factorization for Graph Representations

Matrix factorization methods provide an alternative way to represent graphs by decomposing the adjacency matrix into lower-dimensional matrices. This is especially useful for embedding nodes into vector spaces for machine learning tasks like clustering or link prediction.

### Singular Value Decomposition (SVD)

SVD decomposes the adjacency matrix \( A \) as follows:

$$
A = U \Sigma V^T
$$

Where:
- \( U \) and \( V \) are orthogonal matrices representing the nodes' embeddings.
- \( \Sigma \) is a diagonal matrix of singular values that captures important structural information in the network.

### Example: Netflix Recommendation System

In **recommendation systems** like Netflix, SVD helps predict user preferences by decomposing the user-item interaction matrix into latent factors. Similarly, in social networks, SVD helps uncover hidden community structures and latent features.

### Advantages:
- Captures latent features that are not immediately visible from the graph structure.
- Reduces dimensionality, making large graphs more manageable for algorithms.

### Real-World Use Case:
Graph factorization is widely used in **recommendation systems** to predict user behaviors and in social networks for tasks like community detection and link prediction.

## Graph Embeddings

**Graph embeddings** transform nodes into low-dimensional vectors, allowing the application of machine learning algorithms like classification, clustering, and link prediction. Techniques like **DeepWalk**, **node2vec**, and **Graph Convolutional Networks (GCNs)** are commonly used for this purpose.

### DeepWalk

DeepWalk uses random walks on the graph to capture neighborhood structures and embed nodes into a lower-dimensional space. The embedding objective is to maximize the probability of seeing a node’s neighborhood given its embedding:

$$
\max_Z \sum_{(i,j) \in V} \log P(v_j | v_i)
$$

Where the conditional probability is defined as:

$$
P(v_j | v_i) = \frac{\exp(\mathbf{z}_i^T \mathbf{z}_j)}{\sum_{v_k \in V} \exp(\mathbf{z}_i^T \mathbf{z}_k)}
$$

### Example: Community Detection in Social Networks

For **community detection**, DeepWalk finds embeddings where nodes within the same community are close in the embedding space. The random walks ensure that nodes frequently traversed together will have similar embeddings.

### node2vec

node2vec extends DeepWalk by allowing flexible random walks that can transition between **breadth-first search (BFS)** and **depth-first search (DFS)** behaviors. This allows node2vec to capture both local and global structures.

The probability of transitioning between nodes during a random walk is controlled by parameters \( p \) and \( q \), affecting the walk's exploration strategy.

### Example: Node Classification in Citation Networks

In **citation networks**, where papers cite other papers, node2vec can be used to classify papers based on their citation patterns. Papers cited by similar sources will have similar embeddings.

### Real-World Use Case:
Graph embeddings are widely used in **fraud detection** and **recommendation engines**, where understanding relationships between entities is critical.

## Graph Generation: Erdős–Rényi Model

The **Erdős–Rényi model** is used to generate random graphs, with each pair of nodes having a fixed probability \( p \) of having an edge between them.

In a graph \( G(n, p) \):
- \( n \) is the number of nodes.
- Each edge exists independently with probability \( p \).

This model helps us understand how graph properties evolve as the number of nodes or edges increases.

### Example: Network Testing

In experiments with social networks, Erdős–Rényi graphs are often used to test algorithms' behavior on random graph structures.

## Conclusion

Choosing the right graph representation is critical for balancing memory usage, computational efficiency, and the complexity of graph algorithms. The adjacency list is typically the best choice for sparse social networks, while the adjacency matrix works better for dense graphs. Matrix factorization and graph embeddings allow us to uncover hidden patterns in large networks and apply machine learning algorithms effectively. Understanding these representations and their trade-offs enables efficient analysis of real-world social networks.

