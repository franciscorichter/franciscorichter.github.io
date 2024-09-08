---
title: 'Introduction to Social Networks Analysis'
date: 2024-09-19
permalink: /posts/2024/09/intro-social-networks-analysis/
tags:
  - social networks
  - graph theory
  - network analysis
---



A **network** is a collection of objects, known as *nodes* (or *vertices*), connected by relationships called *edges* (or *links*). The study of networks, also referred to as *graph theory*, has applications in multiple disciplines, including sociology, biology, computer science, and economics.

A network can be mathematically represented by a **graph**:

$$
G = (\mathcal{V}, \mathcal{E})
$$

where:

- $$\mathcal{V} = \{v_1, v_2, \dots, v_n\}$$ is the set of nodes (or vertices),
- $$\mathcal{E} = \{e_1, e_2, \dots, e_m\}$$ is the set of edges (or links).

Graphs can be used to represent various real-world systems:

- In a **social network**, nodes could represent individuals, and edges could represent relationships (e.g., friendships).
- In a **biological network**, nodes could represent proteins, and edges could represent interactions between them.

## Explicit vs Implicit Networks

Networks can be classified into two categories:

- **Explicit networks**: Relationships between nodes are explicitly defined (e.g., friendships in social networks).
- **Implicit networks**: Connections are inferred from data (e.g., co-purchase behavior in an e-commerce setting).

## Applications of Network Analysis

Networks are ubiquitous in various domains, and their analysis is crucial for detecting hidden patterns and dependencies. Some applications include:

- **Social Networks**: Understanding human relationships and social structures (e.g., Facebook, LinkedIn).
- **Biological Networks**: Studying protein-protein interactions or genetic networks.
- **Technological Networks**: Examining the structure of the Internet or power grids.

Analyzing networks allows us to uncover:

- **Latent content**: Hidden community structures or clusters of closely related nodes.
- **Structural dependencies**: Understanding how entities in the system are interrelated (e.g., who influences whom in a social network).

## Basic Notations and Definitions

Let $$G = (\mathcal{V}, \mathcal{E})$$ be a graph:

- A *node* (or *vertex*) $$v_i \in \mathcal{V}$$ represents an entity in the network.
- An *edge* $$e_{ij} = (v_i, v_j) \in \mathcal{E}$$ represents a relationship between two nodes.

A graph can be:

- **Directed**: Each edge has a direction from $$v_i$$ to $$v_j$$.
- **Undirected**: Edges do not have direction.
- **Weighted**: Edges are associated with weights $$w_{ij}$$.

## Matrix Representation

The **adjacency matrix** $$A \in \mathbb{R}^{n \times n}$$ of a graph is defined as:

$$
A_{ij} = 
\begin{cases} 
w_{ij}, & \text{if there is an edge from } v_i \text{ to } v_j \\
0, & \text{otherwise}.
\end{cases}
$$

For undirected graphs, $$A$$ is symmetric. For example, the adjacency matrix for a 6-node network is:

$$
A =
\begin{bmatrix}
0 & 1 & 1 & 0 & 0 & 0 \\
1 & 0 & 1 & 0 & 0 & 0 \\
1 & 1 & 0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 & 1 & 0 \\
0 & 0 & 0 & 1 & 0 & 1 \\
0 & 0 & 0 & 1 & 1 & 0 \\
\end{bmatrix}
$$

## Key Equations

### Degree of a Node

The degree of a node $$v_i$$ is defined as the number of edges connected to $$v_i$$. For an undirected graph:

$$
k_i = \sum_{j} A_{ij}
$$

For directed graphs, we define:

- **In-degree**: $$k_i^{\text{in}} = \sum_j A_{ji}$$
- **Out-degree**: $$k_i^{\text{out}} = \sum_j A_{ij}$$

### Clustering Coefficient

The clustering coefficient $$C_i$$ measures how interconnected the neighbors of node $$v_i$$ are:

$$
C_i = \frac{2e_i}{k_i(k_i - 1)}
$$

where $$e_i$$ is the number of edges between the neighbors of node $$v_i$$.

### Path Length

The shortest path between two nodes is often computed using algorithms such as Dijkstra’s or Floyd-Warshall. The average path length $$L$$ in a graph is given by:

$$
L = \frac{1}{n(n-1)} \sum_{i \neq j} d(v_i, v_j)
$$

where $$d(v_i, v_j)$$ is the shortest distance between nodes $$v_i$$ and $$v_j$$.

## Challenges in Network Data

Analyzing network data presents several challenges:

- **High Dimensionality**: Networks can have millions of nodes and edges, making computational analysis difficult.
- **Data Sparsity**: Despite their large size, most nodes in a real-world network may not be directly connected.
- **Dynamic Networks**: Networks change over time, and algorithms need to account for these changes.
- **Heterogeneous Networks**: Some networks include multiple types of nodes and edges, adding complexity to their analysis.
