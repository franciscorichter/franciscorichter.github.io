---
title: 'Probability and Frequency: Simulating Coin Tosses with LCG'
date: 2024-10-13
permalink: /posts/2024/10/probability-frequency-lcg/
tags:
  - probability
  - random number generation
  - python
---

In this post, we explore the a practical example of simulating a coin toss experiment with a **Linear Congruential Generator (LCG)**, a well-known random number generator (RNG). We’ll illustrate how the probabilities of heads and tails converge to 0.5 as the number of tosses increases, validating the frequency approach to probability.


## The Experiment: Simulating Coin Tosses with LCG

The Linear Congruential Generator is defined by the recurrence relation:

$$
X_{n+1} = (1664525 \times X_n + 1013904223) \mod 2^{32}
$$

LCG produces a sequence of pseudo-random numbers uniformly distributed over its range. For this experiment, we map numbers below \( \frac{2^{32}}{2} \) to **Heads** (H) and those above it to **Tails** (T). 

### Python Code

We implement this simulation in Python and analyze how the proportions of heads and tails converge to 0.5 as the number of tosses increases.







  <pre><code>
import numpy as np
import matplotlib.pyplot as plt

# Linear Congruential Generator parameters
a = 1664525
c = 1013904223
m = 2**32

# Initialize the LCG
def LCG(seed, n):
    X = np.zeros(n, dtype=np.uint32)
    X[0] = seed
    for i in range(1, n):
        X[i] = (a * X[i-1] + c) % m
    return X

# Simulate the coin toss experiment
def coin_toss_lcg(n, seed=0):
    X = LCG(seed, n)
    # Map values below 2**31 to Heads (0), and values above to Tails (1)
    tosses = (X >= m // 2).astype(int)
    return tosses

# Number of trials
N = 10000
seed = 12345  # Starting seed

# Perform the experiment
tosses = coin_toss_lcg(N, seed)

# Calculate cumulative proportions of heads and tails
cumulative_heads = np.cumsum(tosses == 0) / np.arange(1, N+1)
cumulative_tails = np.cumsum(tosses == 1) / np.arange(1, N+1)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(cumulative_heads, label="Heads (H)", color="blue")
plt.plot(cumulative_tails, label="Tails (T)", color="green")
plt.axhline(y=0.5, color="red", linestyle="--", label="Theoretical 0.5")
plt.xlabel("Number of Tosses")
plt.ylabel("Proportion")
plt.title("Convergence of Heads and Tails to 0.5 Using LCG")
plt.legend()
plt.grid(True)
plt.show()
  </code></pre>

### Results

As shown in the plot below, the cumulative proportions of heads and tails approach the theoretical value of 0.5 as the number of tosses increases. This empirical result reinforces the uniformity and reliability of the LCG in simulating coin tosses.

![Convergence of Heads and Tails to 0.5 Using LCG](/images/coin.png)

The key takeaway is that the random numbers generated by the LCG, when mapped to heads or tails, display a consistent pattern where both outcomes occur with equal likelihood over a large number of trials.
