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


Networks are everywhere, spanning across diverse fields, and their analysis is vital for uncovering hidden patterns and dependencies. These applications appear in many areas, including:

- **Technical/Engineering Networks**: Focus on connectivity, reachability, and efficiency in systems like the Internet, power grids, or transportation systems.
- **Mathematical Networks**: Studying the formal properties and theoretical underpinnings of networks to better understand their structure and behavior.
- **Communication and Media Networks**: Understanding the spread of information in platforms like blogs, Twitter, and other forms of social media.
- **Physics Networks**: Investigating phenomena such as community detection, "small world" effects, modularity, and multilayer networks.
- **Economic Networks**: Mapping world trade connections and exploring the networks that drive economic development.
- **Biological Networks**: Studying interactions between proteins, gene regulatory networks, and motifs that form the building blocks of life.
- **Sociological Networks**: Analyzing social movements, development, education, and access within a population.



![Graph Representation of the Adjacency Matrix](/images/nets.png)

The image above illustrates four distinct network types, each from a unique domain:

- **Top Left: Caltech Facebook Network**  
  This graph represents friendships between users in the Caltech Facebook network. Each node corresponds to an individual, and the edges depict social ties. By analyzing this network, we can identify patterns of social cohesion, community formation, and influential individuals within a university setting.

- **Top Right: Historical Network of Russian Trade Routes (12th-13th Century)**  
  This network visualizes trade routes connecting major cities in medieval Russia. Nodes represent cities or trading posts, while edges reflect the trade pathways. Studying this historical network helps us understand economic dependencies and the geopolitical landscape of the time.

- **Bottom Left: Soccer Match Pass Network**  
  This network shows passes between players in a soccer match, where nodes are the players and edges represent successful passes. Analyzing this network reveals team dynamics, key players, and overall passing strategy, offering insights into how teams organize and function during a game.

- **Bottom Right: Protein-Protein Interaction Network**  
  This biological network visualizes interactions between proteins within an organism. Each node is a protein, and edges signify interactions between them. By examining this network, researchers can identify essential proteins and functional modules involved in cellular processes.

Analyzing networks allows us to achieve the following objectives:

- **Description**: Identifying and describing hidden community structures, clusters of closely related nodes, and general patterns in the network.
- **Explanation**: Providing insights into the underlying mechanisms or structural dependencies within the system (e.g., who influences whom in a social network, or how entities are interrelated in a technological network).
- **Prediction**: Forecasting future interactions or behaviors within the network, such as predicting the emergence of new relationships, or the likely behavior of system components based on current trends.


The process of analyzing networks typically follows a structured pipeline, as illustrated in the diagram below:

<img src="/images/diagram1.png" alt="Pipeline Diagram" width="400"/>

It begins with a clear **problem statement**, where the primary research question or challenge is identified. This is followed by the development of a **theoretical framework**, which provides the necessary background and context for understanding the network's behavior. Based on this theory, **hypotheses** are formulated, offering testable predictions about the relationships and structures within the network.

Once the hypotheses are set, a **research design** is created, outlining the methods and tools that will be used to gather and analyze the data. The next step is **data collection**, where relevant network data is gathered from various sources, whether social, biological, or technological.

With the data in hand, the exploration and **analysis** phase begins. This step involves applying network analysis techniques to uncover hidden patterns, clusters, or dependencies within the network. Finally, the findings are brought together in the **interpretation and presentation** stage, where results are visualized and communicated to provide actionable insights or conclusions.




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



<img src="/images/graph1.png" alt="Graph Representation of the Adjacency Matrix">


<details>
  <summary>Click to show the R code</summary>

  <pre><code>
# Load necessary library
library(igraph)

# Define the adjacency matrix
adj_matrix <- matrix(c(0, 1, 1, 0, 0, 0,
                       1, 0, 1, 0, 0, 0,
                       1, 1, 0, 1, 0, 0,
                       0, 0, 1, 0, 1, 0,
                       0, 0, 0, 1, 0, 1,
                       0, 0, 0, 1, 1, 0),
                     nrow = 6, ncol = 6, byrow = TRUE)

# Create a graph object from the adjacency matrix
graph <- graph_from_adjacency_matrix(adj_matrix, mode = "undirected")

# Plot the graph
plot(graph, vertex.label = c("v1", "v2", "v3", "v4", "v5", "v6"),
     vertex.size = 30, 
     vertex.color = "lightblue", 
     edge.arrow.size = 0.5, 
     main = "Graph Representation of the Adjacency Matrix")
  </code></pre>

</details>

<details>
  <summary>Click to show the Python code</summary>

  <pre><code>
# Import necessary libraries
import networkx as nx
import matplotlib.pyplot as plt

# Define the adjacency matrix as a list of lists
adj_matrix = [
    [0, 1, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1],
    [0, 0, 0, 1, 1, 0]
]

# Create a graph object from the adjacency matrix
G = nx.Graph(adj_matrix)

# Plot the graph
nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, font_weight='bold')
plt.title('Graph Representation of the Adjacency Matrix')
plt.show()
  </code></pre>

</details>


## Challenges in Network Data

Analyzing network data presents several challenges:

- **High Dimensionality**: Networks can have millions of nodes and edges, making computational analysis difficult.
- **Data Sparsity**: Despite their large size, most nodes in a real-world network may not be directly connected.
- **Dynamic Networks**: Networks change over time, and algorithms need to account for these changes.
- **Heterogeneous Networks**: Some networks include multiple types of nodes and edges, adding complexity to their analysis.



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

