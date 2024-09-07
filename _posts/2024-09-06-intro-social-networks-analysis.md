---
title: 'Introduction to Social Networks Analysis'
date: 2024-09-06
permalink: /posts/2024/09/intro-social-networks-analysis/
tags:
  - social networks
  - graph theory
  - network analysis
---

In this post, we'll explore the fascinating world of Social Networks Analysis, focusing on the fundamental concepts introduced in Chapter 1 of our lecture notes.

## What are Networks and Graphs?

At its core, a network is a collection of objects (nodes or vertices) connected by relationships (edges or links). The mathematical study of these structures is known as graph theory, which has applications across various disciplines, including sociology, biology, computer science, and economics.

Mathematically, we represent a network as a graph G = (V, E), where:
- V = {v₁, v₂, ..., vₙ} is the set of nodes
- E = {e₁, e₂, ..., eₘ} is the set of edges

## Types of Networks

Networks can be classified into two main categories:
1. **Explicit networks**: Relationships between nodes are clearly defined (e.g., friendships on social media)
2. **Implicit networks**: Connections are inferred from data (e.g., co-purchase behavior in e-commerce)

## Applications of Network Analysis

Network analysis is crucial for detecting hidden patterns and dependencies in various domains:
- Social Networks: Understanding human relationships and social structures
- Biological Networks: Studying protein-protein interactions or genetic networks
- Technological Networks: Examining the structure of the Internet or power grids

## Basic Notations and Definitions

Let's dive into some key concepts:
- **Directed vs Undirected**: Edges can have direction (directed) or not (undirected)
- **Weighted vs Unweighted**: Edges can have associated weights or be uniform
- **Adjacency Matrix**: A matrix representation of the graph, where A[i][j] indicates an edge between nodes i and j

## Key Equations in Network Analysis

1. **Degree of a Node**: For an undirected graph, k[i] = Σ[j] A[i][j]
2. **Clustering Coefficient**: C[i] = 2e[i] / (k[i](k[i] - 1))
3. **Average Path Length**: L = (1 / (n(n-1))) * Σ[i≠j] d(v[i], v[j])

## Challenges in Network Data

Analyzing network data comes with several challenges:
- High dimensionality
- Data sparsity
- Dynamic networks
- Heterogeneous networks

## Network Embeddings

To address these challenges, we use Network Representation Learning (NRL) to convert network data into low-dimensional vector embeddings. Some popular approaches include:
- Random Walk-Based (e.g., DeepWalk, Node2vec)
- Matrix Factorization
- Deep Learning (e.g., Graph Neural Networks)

In the next post, we'll delve deeper into these embedding techniques and their applications in social network analysis.