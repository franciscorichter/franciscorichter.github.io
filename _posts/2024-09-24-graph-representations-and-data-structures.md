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

In this post, we'll dive into the various ways to represent graphs and the data structures used in social network analysis. The choice of representation can significantly impact both memory usage and computational efficiency.

## Introduction to Graph Representation

When analyzing networks, selecting the appropriate data structure is crucial. Different representations have their own strengths and weaknesses, affecting how efficiently we can perform various operations on the graph.

## Adjacency Matrix

An adjacency matrix is a square matrix $A \in \mathbb{R}^{n \times n}$ where $n$ is the number of nodes in the graph. The element $A_{ij}$ indicates the presence or absence of an edge between nodes $v_i$ and $v_j$:

$$
A_{ij} = 
\begin{cases} 
w_{ij}, & \text{if } (v_i, v_j) \in \mathcal{E}, \\
0, & \text{otherwise}.
\end{cases}
$$

### Space Complexity
The adjacency matrix requires $O(n^2)$ space, making it efficient for dense graphs but inefficient for sparse graphs.

### Advantages:
- Efficient for dense graphs
- Constant-time $O(1)$ lookup for edge existence

### Disadvantages:
- Inefficient $O(n^2)$ space usage for sparse graphs
- Inefficient $O(n^2)$ time for edge traversal in large graphs

## Adjacency List

An adjacency list stores each node's neighbors in a list or array. It's particularly efficient for sparse graphs where $m \ll n^2$ (m is the number of edges, n is the number of nodes).

### Space Complexity
The adjacency list requires $O(n + m)$ space, making it suitable for sparse graphs.

### Advantages:
- Space-efficient for sparse graphs
- $O(m)$ time for traversing all edges

### Disadvantages:
- $O(\text{deg}(v))$ time to check for a specific edge's existence

## Incidence Matrix

An incidence matrix $B \in \mathbb{R}^{n \times m}$ represents the relationship between nodes and edges:

$$
B_{ij} = 
\begin{cases} 
1, & \text{if node } v_i \text{ is incident to edge } e_j, \\
0, & \text{otherwise}.
\end{cases}
$$

### Space Complexity
The incidence matrix requires $O(n \times m)$ space.

### Advantages:
- Suitable for graphs with few edges compared to nodes

### Disadvantages:
- Inefficient for graphs with many edges

## Matrix Factorization-Based Representations

Matrix factorization techniques decompose the adjacency matrix into lower-dimensional representations, capturing important structural relationships in the graph.

### Singular Value Decomposition (SVD)

SVD decomposes the adjacency matrix $A$ into the product of three matrices:

$$
A = U \Sigma V^T
$$

where $U$ and $V$ are orthogonal matrices containing node embeddings, and $\Sigma$ is a diagonal matrix of singular values.

## Graph Embeddings and Applications

Embeddings generated using matrix factorization and other methods allow the network's nodes to be represented in a vector space. These embeddings are crucial for:

- Node Classification
- Link Prediction
- Clustering and Community Detection

## Practical Examples

- Social Networks: Adjacency lists are often more efficient due to the sparsity of connections.
- Biological Networks: Matrix factorization can reveal hidden biological patterns through dimensionality reduction.


## Graph Representations

### 1. Adjacency Matrix

An **Adjacency Matrix** \(A\) is a square matrix of size \(n \times n\), where \(n\) is the number of nodes in the graph. Each element \(A_{ij}\) is defined as follows:

\[
A_{ij} = 
\begin{cases} 
1, & \text{if there is an edge between node } i \text{ and node } j, \\
0, & \text{otherwise.}
\end{cases}
\]

The memory complexity of the adjacency matrix is \(O(n^2)\), making it inefficient for large, sparse graphs.

### 2. Adjacency List

An **Adjacency List** is a dictionary or list where each node is associated with a list of its neighboring nodes. For example, the adjacency list for a graph with three nodes and edges \((1, 2)\) and \((2, 3)\) would look like this:

\[
\{ 1: [2], 2: [1, 3], 3: [2] \}
\]

The memory complexity of the adjacency list is \(O(n + m)\), where \(m\) is the number of edges. This makes it more space-efficient for sparse graphs.

### 3. Incidence Matrix

An **Incidence Matrix** \(I\) is a matrix of size \(n \times m\), where \(n\) is the number of nodes and \(m\) is the number of edges. Each element \(I_{ij}\) is defined as:

\[
I_{ij} = 
\begin{cases} 
1, & \text{if node } i \text{ is incident to edge } j, \\
0, & \text{otherwise.}
\end{cases}
\]

The memory complexity of the incidence matrix is \(O(n \times m)\).

## Graph Generation: Erdős–Rényi Model

The **Erdős–Rényi model** is a probabilistic method used to generate random graphs. In this model, each pair of nodes has a fixed probability \(p\) of having an edge between them. For our experiment, we used \(p = 0.5\), meaning each pair of nodes has a 50% chance of being connected.

The model is defined as follows:
1. Let \(G(n, p)\) represent a random graph with \(n\) nodes and edge probability \(p\).
2. For each pair of nodes \(i\) and \(j\), an edge is added with probability \(p\), independent of other edges.

This model is particularly useful for understanding how graph properties (such as memory usage) scale with the number of nodes.

## Experiment Setup

### Objective

The objective of this experiment is to evaluate how the memory consumption of different graph representations scales as the number of nodes increases. The key research question is: _How does the choice of graph representation affect memory efficiency, particularly as graph size grows?_

### Methodology

1. **Graph Sizes**: We generated graphs with 10, 50, 100, and 500 nodes using the Erdős–Rényi model, with an edge probability \(p = 0.5\).
2. **Memory Measurement**: For each graph size, we computed the memory usage for the adjacency matrix, adjacency list, and incidence matrix representations.
3. **Python Code**: The graphs were generated, and memory was measured using the Python code detailed in the earlier sections.

The Python script uses `sys.getsizeof()` to calculate memory usage, ensuring an accurate comparison of memory consumption across different representations.

## Results

### Memory Usage vs. Number of Nodes

The following table summarizes the memory usage for each graph representation as the number of nodes increases:

| Nodes | Adjacency Matrix (Bytes) | Adjacency List (Bytes) | Incidence Matrix (Bytes) |
|-------|--------------------------|------------------------|--------------------------|
| 10    | 928                      | 352                    | 2128                     |
| 50    | 20128                    | 2264                   | 234128                   |
| 100   | 80128                    | 4688                   | 2013728                  |

As seen in the table, the memory usage grows rapidly for the adjacency matrix as the number of nodes increases, while the adjacency list and incidence matrix scale more efficiently.

### Visualizing the Results

The following plot illustrates how memory usage scales with the number of nodes for each graph representation:

![Memory Usage Plot](https://github.com/franciscorichter/franciscorichter.github.io/blob/master/_posts/images/memory.png)

In this plot, we observe that:
- The **Adjacency Matrix** exhibits quadratic growth, consistent with its \(O(n^2)\) complexity.
- The **Adjacency List** grows linearly, making it the most memory-efficient representation for sparse graphs.
- The **Incidence Matrix** shows a hybrid behavior, growing more slowly than the adjacency matrix but faster than the adjacency list as the number of edges increases with node count.

## Conclusion

This experiment provides a clear comparison of the memory consumption associated with different graph representations. The key takeaways are:
- The **Adjacency Matrix** is most appropriate for dense graphs, but its memory requirements grow quadratically with the number of nodes, making it inefficient for large, sparse graphs.
- The **Adjacency List** is the most memory-efficient representation, especially for sparse graphs, due to its linear scaling with the number of edges.
- The **Incidence Matrix** offers a compromise between the two, but its memory usage becomes significant as the number of edges grows.

These findings highlight the importance of choosing the right graph representation based on the specific properties of the graph and the tasks at hand.
