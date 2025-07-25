---
title: "Stochastic Methods"
collection: teaching
type: "2025-spring"
permalink: /teaching/2025-spring-stochastic-methods
venue: "Università della Svizzera italiana, Faculty of Informatics"
date: 2025-02-03
location: "Lugano, Switzerland"
---

This course covers foundational and advanced topics in **stochastic processes**, focusing on both theoretical principles and practical applications. Students learn to **model randomness in systems, analyze probabilistic phenomena, and apply stochastic methods** in various domains, including **optimization, inference, networks, and simulation**.

## Course Overview

The course covers a **broad range of stochastic techniques**, structured into **thirteen main topics**, each with corresponding **lecture notes**:

### **1. Randomness**  
📄 [Lecture 1: Randomness](https://github.com/franciscorichter/franciscorichter.github.io/blob/master/files/Notes/week1.pdf)  
- Random number generators (RNGs) and their properties
- Pseudorandom number generation: Linear Congruential Generators (LCG), PCG64
- Probability distributions: uniform, discrete, continuous
- Inverse transform sampling

### **2. Random Variables**  
📄 [Lecture 2: Random Variables](https://github.com/franciscorichter/franciscorichter.github.io/blob/master/files/Notes/week2.pdf)  
- Discrete vs. continuous random variables
- Probability mass functions (PMF) and probability density functions (PDF)
- Cumulative distribution functions (CDF) and their properties
- Binomial, Poisson, and normal distributions

### **3. Expectation & Limit Theorems**  
📄 [Lecture 3: Expectation](https://github.com/franciscorichter/franciscorichter.github.io/blob/master/files/Notes/week3.pdf)  
- Definition of expectation and its properties
- Linearity of expectation
- The **Law of Large Numbers (LLN)**
- The **Central Limit Theorem (CLT)** and its implications
- Monte Carlo simulation for numerical approximations

### **4. Variance & Monte Carlo Methods**  
📄 [Lecture 4: Variance](https://github.com/franciscorichter/franciscorichter.github.io/blob/master/files/Notes/week4.pdf)  
- Monte Carlo integration and importance sampling
- Variance reduction techniques (stratified sampling, control variates, antithetic variates)
- Rejection sampling and proof of correctness
- Dependence and independence of random variables
- Bayesian inference and Bayes' theorem

### **5. Networks & Random Graphs**  
📄 [Lecture 5: Networks](https://github.com/franciscorichter/franciscorichter.github.io/blob/master/files/Notes/week5.pdf)  
- Introduction to **random networks**
- Graph theory: adjacency matrices and connectivity
- Erdős–Rényi random graphs
- Structural Equation Models (SEM) and causality in networks
- Applications in epidemiology and network analysis

### **6. Markov Processes**  
📄 [Lecture 6: Markov Processes](https://github.com/franciscorichter/franciscorichter.github.io/blob/master/files/Notes/week6.pdf)  
- **Markov chains**: transition matrices, Chapman-Kolmogorov equation
- Random walks and applications in financial models
- Stationary distributions and **ergodicity**
- Multi-step transition probabilities and long-term behavior
- Applications in **epidemiology and finance**

### **7. Stochastic Simulation**  
📄 [Lecture 7: Stochastic Simulation](https://github.com/franciscorichter/franciscorichter.github.io/blob/master/files/Notes/week7.pdf)  
- Stochastic Cellular Automata and probabilistic grid-based models
- Agent-Based Modeling (ABM) and emergent behavior
- Example: **Forest fire model** (spread of wildfire simulation)
- Example: **Ant foraging simulation** (pheromone-based search strategies)

### **8. Stochastic Inference**  
📄 [Lecture 8: Stochastic Inference](https://github.com/franciscorichter/franciscorichter.github.io/blob/master/files/Notes/week8.pdf)  
- **Linear Regression** and least squares estimation
- **Logistic Regression** and Maximum Likelihood Estimation (MLE)
- **Support Vector Machines (SVMs)** for classification
- **Neural networks** and stochastic optimization methods

### **9. Stochastic Optimization**  
📄 [Lecture 9: Stochastic Optimization](https://github.com/franciscorichter/franciscorichter.github.io/blob/master/files/Notes/week9.pdf)  
- **Evolutionary algorithms**: Genetic algorithms (GA) & Differential Evolution (DE)
- **Stochastic Gradient Descent (SGD)** and its variants
- **ADAM optimizer**: adaptive learning rates for optimization
- **Expectation-Maximization (EM) algorithm** and Monte Carlo EM
- **Markov Chain Monte Carlo (MCMC)** methods

### **10. Stochastic Systems & Multi-Agent Models**  
📄 [Lecture 10: Stochastic Systems](https://github.com/franciscorichter/franciscorichter.github.io/blob/master/files/Notes/week10.pdf)  
- **Multi-agent stochastic systems**: Defining agents, tasks, tools, and processes
- **Markov Decision Processes (MDP)**
- Process optimization: sequential, parallel, hierarchical, and event-driven systems
- Randomness in AI-generated outputs and bias in language models

### **11. Advanced Stochastic Optimization**  
📄 [Lecture 11: Advanced Optimization](https://github.com/franciscorichter/franciscorichter.github.io/blob/master/files/Notes/week11.pdf)  
- Advanced optimization techniques for stochastic systems
- Reinforcement learning algorithms and applications
- Multi-objective optimization under uncertainty
- Bayesian optimization methods

### **12. Stochastic Optimization Methods**  
📄 [Lecture 12: Optimization Methods](https://github.com/franciscorichter/franciscorichter.github.io/blob/master/files/Notes/week12.pdf)  
- Building upon foundational concepts of stochastic optimization
- Advanced gradient-based methods
- Constraint handling in stochastic optimization
- Real-world applications and case studies

### **13. Decision-Making and Collaboration**  
📄 [Lecture 13: Multi-Agent Decision-Making](https://github.com/franciscorichter/franciscorichter.github.io/blob/master/files/Notes/week13.pdf)  
- Multi-agent systems and autonomous agents
- Collaborative decision-making under uncertainty
- Game theory in stochastic environments
- Emergent behaviors in complex systems

---

## **Key Learning Objectives**
1. **Master Probability & Stochastic Concepts**: Develop a strong foundation in probability theory, random variables, and stochastic modeling.
2. **Analyze Markov Processes & Networks**: Construct and analyze Markov Chains and random networks, understanding long-term behaviors.
3. **Simulate & Optimize Stochastic Systems**: Apply Monte Carlo methods, agent-based models, and stochastic gradient descent for practical applications.
4. **Explore Stochastic Optimization**: Learn techniques like **evolutionary algorithms, SGD, and MCMC** for solving complex problems.
5. **Work with Multi-Agent Stochastic Models**: Understand stochastic decision-making, AI-generated randomness, and process optimization.


## **References**
<ul>
    <li><i>Introduction to Probability Models</i> by Sheldon M. Ross</li>
    <li><i>Stochastic Processes</i> by Sheldon M. Ross</li>
    <li><i>Probability Models for Computer Science</i> by Sheldon M. Ross</li>
    <li><i>First-order and Stochastic Optimization Methods for Machine Learning</i> by Guanghui Lan</li>
    <li><i>Basic Stochastic Processes</i> by Zdzisław Brzeźniak and Tomasz Zastawniak</li>
</ul>
