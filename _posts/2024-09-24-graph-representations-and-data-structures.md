---
title: 'Lecture notes 2: Graph Representations and Data Structures'
date: 2024-09-24
permalink: /posts/2024/09/graph-representations-and-data-structures/
tags:
  - social networks
  - graph theory
  - data structures
  - network analysis
---

In this post, we will explore the various ways to represent graphs and the data structures frequently used in social network analysis. Selecting the appropriate graph representation is crucial, as it significantly impacts memory usage, computational efficiency, and the complexity of algorithm implementation.

## Introduction to Graph Representation

When analyzing social networks, the way we represent the graph can change the efficiency of operations like traversal, edge lookup, and node degree calculation. Graph representations vary based on the structure of the network and the types of queries or analysis we aim to perform.

In social networks, most graphs are **sparse**, meaning the number of edges is far smaller than the maximum possible number of edges \( n^2 \). Thus, efficient graph representation and traversal are critical.

## Adjacency Matrix

An **adjacency matrix** is a square matrix \( A \in \mathbb{R}^{n \times n} \), where \( n \) represents the number of nodes in the graph. The element \( A_{ij} \) indicates whether there is an edge between nodes \( v_i \) and \( v_j \):

$$
A_{ij} = 
\begin{cases} 
w_{ij}, & \text{if } (v_i, v_j) \in \mathcal{E}, \\
0, & \text{otherwise}.
\end{cases}
$$

### Space Complexity

The adjacency matrix requires \( O(n^2) \) space. For **dense graphs**, where many connections exist between nodes, this representation works well. However, for **sparse graphs** with far fewer edges, it becomes inefficient.

### Advantages:
- Efficient for **dense graphs**.
- Constant-time \( O(1) \) lookup to check if an edge exists between two nodes.

### Disadvantages:
- Memory usage grows quadratically \( O(n^2) \), which can be impractical for large, sparse graphs.
- Traversing all edges requires \( O(n^2) \) time, inefficient for sparse graphs.

### Real-World Use Case:
In social networks like **Facebook**, where connections are plentiful within certain sub-communities, but overall the graph remains sparse, an adjacency matrix could be computationally heavy.

## Adjacency List

An **adjacency list** is a more memory-efficient way to store sparse graphs. Each node in the graph is associated with a list of its neighboring nodes, representing the edges.

For example, for a graph with three nodes and edges \( (1, 2) \) and \( (2, 3) \), the adjacency list looks like:

\[
\{ 1: [2], 2: [1, 3], 3: [2] \}
\]

### Space Complexity

The adjacency list uses \( O(n + m) \) space, where \( n \) is the number of nodes and \( m \) is the number of edges. This makes it highly suitable for **sparse graphs**.

### Advantages:
- Space-efficient for sparse graphs with \( m \ll n^2 \).
- Traversing all edges is efficient, requiring \( O(m) \) time.

### Disadvantages:
- Checking for the existence of a specific edge can take up to \( O(\text{deg}(v)) \) time, where \( \text{deg}(v) \) is the degree of the node.

### Real-World Use Case:
Social networks like **Twitter**, where most users follow only a small fraction of others, are highly sparse. Adjacency lists provide an efficient way to store and traverse such graphs.

## Incidence Matrix

An **incidence matrix** \( B \in \mathbb{R}^{n \times m} \) is a matrix that represents the relationships between nodes and edges. Each row corresponds to a node, and each column corresponds to an edge.

$$
B_{ij} = 
\begin{cases} 
1, & \text{if node } v_i \text{ is incident to edge } e_j, \\
0, & \text{otherwise}.
\end{cases}
$$

### Space Complexity

The incidence matrix requires \( O(n \times m) \) space, making it a middle-ground in terms of memory efficiency.

### Advantages:
- Effective for representing **multigraphs** (graphs with multiple edges between the same pair of nodes).

### Disadvantages:
- Inefficient for graphs with many edges.
- More complex to extract node-specific information such as degree or neighbors.

### Real-World Use Case:
In **biological networks** where interactions between proteins or genes can be represented as multiple edges between the same entities, incidence matrices offer a useful representation.

## Matrix Factorization-Based Representations

Matrix factorization techniques decompose the adjacency matrix into lower-dimensional representations that capture important structural relationships in the graph. These representations are essential for dimensionality reduction and the creation of graph embeddings, allowing for tasks like node classification and link prediction.

### Singular Value Decomposition (SVD)

SVD decomposes the adjacency matrix \( A \) into the product of three matrices:

$$
A = U \Sigma V^T
$$

where:
- \( U \) and \( V \) are orthogonal matrices containing node embeddings.
- \( \Sigma \) is a diagonal matrix of singular values, representing the importance of each dimension.

### Advantages:
- Captures latent structural properties in the network.
- Useful for **node embeddings**, which allow complex graph analysis tasks such as clustering and classification.

### Real-World Use Case:
In **recommendation systems** like those used by **Netflix** or **Spotify**, matrix factorization techniques can predict links (e.g., suggesting connections or songs) based on existing relationships.

## Graph Embeddings and Applications

Graph embeddings transform nodes into vector spaces, making it easier to apply machine learning algorithms. Popular techniques include **node2vec**, **DeepWalk**, and **graph convolutional networks** (GCNs).

Embeddings are crucial for tasks such as:
- **Node Classification**: Predicting attributes of nodes based on their structural properties.
- **Link Prediction**: Inferring potential connections in a social network.
- **Clustering**: Grouping similar nodes together.
- **Community Detection**: Identifying clusters or communities within social networks.

## Graph Generation: Erdős–Rényi Model

The **Erdős–Rényi model** is a probabilistic method used to generate random graphs. In this model, each pair of nodes has a fixed probability \( p \) of having an edge between them.

For example, for a graph \( G(n, p) \):
- \( n \) is the number of nodes.
- Each edge exists independently with probability \( p \).

The Erdős–Rényi model is useful for testing graph algorithms and understanding how graph properties change as the number of nodes increases.

## Experiment Setup

### Objective

To explore how memory consumption of different graph representations scales as the number of nodes increases. The question we want to answer is: _How does the choice of graph representation impact memory efficiency as the graph grows?_

### Methodology

1. **Graph Sizes**: We generated graphs with 10, 50, 100, and 500 nodes using the Erdős–Rényi model, with edge probability \( p = 0.5 \).
2. **Memory Measurement**: For each graph size, we computed the memory usage for the adjacency matrix, adjacency list, and incidence matrix representations.

### Results

| Nodes | Adjacency Matrix (Bytes) | Adjacency List (Bytes) | Incidence Matrix (Bytes) |
|-------|--------------------------|------------------------|--------------------------|
| 10    | 928                      | 352                    | 2128                     |
| 50    | 20128                    | 2264                   | 234128                   |
| 100   | 80128                    | 4688                   | 2013728                  |

### Analysis

- The **Adjacency Matrix** grows quadratically with \( n \), making it impractical for large graphs.
- The **Adjacency List** scales linearly, demonstrating efficiency for sparse graphs.
- The **Incidence Matrix** grows more slowly than the adjacency matrix but is still less efficient than the adjacency list.

## Conclusion

Choosing the right graph representation is crucial for optimizing memory usage and computational efficiency. The adjacency list is typically the most memory-efficient for sparse social networks, while the adjacency matrix is better suited for dense graphs. Matrix factorization and embeddings provide powerful tools for uncovering hidden patterns and making predictions in networks. Understanding these trade-offs is critical for efficiently analyzing large-scale social networks and complex systems.
