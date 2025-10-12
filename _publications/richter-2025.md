---
title: "Neural Causal Regularization: Extending Causal Invariance to Deep Models"
author: "Francisco Richter, Katerina Rigana, Ernst Wit"
year: 2025
collection: publications
pubtype: journals
booktitle: "Statistics for Innovation I"
editor: "Enrico di Bella, Vincenzo Gioia, Corrado Lagazio, Susanna Zaccarin"
publisher: "Springer Nature Switzerland"
address: "Cham"
pages: "97--102"
venue: "Statistics for Innovation I"
date: 2025-01-01
isbn: "978-3-031-96736-8"
abstract: |
  Learning predictors that remain accurate under dataset shift has long been a challenge in statistics and applied sciences---and remains crucial for reliable deployment in any setting where data distributions evolve. Recent work shows that exploiting causal invariances across training environments can improve out-of-distribution robustness, yet most existing approaches either rely on linear models or require difficult bi-level optimisation. We introduce Neural Causal Regularization (NCR), a simple invariance penalty that extends the causal regularization framework of Kania and Wit [3], to deep neural networks. NCR promotes robustness by penalising changes in a network's prediction under spurious transformations. When the two training environments differ only in the spurious factor, increasing the regularisation weight drives the risks toward equality, recovering the causal predictor in the limit. Empirically, on three bias-controlled variants of the Colored MNIST benchmark, NCR consistently improves out-of-distribution accuracy over empirical risk minimisation (ERM) and the variance-based REx penalty, while remaining easy to optimise.
permalink: /publication/2025-neural-causal-regularization
---

This paper was published in the volume "Statistics for Innovation I" (Springer Nature Switzerland, 2025), pp. 97--102.

**Authors:** Francisco Richter, Katerina Rigana, Ernst Wit

**Abstract:**
Learning predictors that remain accurate under dataset shift has long been a challenge in statistics and applied sciences---and remains crucial for reliable deployment in any setting where data distributions evolve. Recent work shows that exploiting causal invariances across training environments can improve out-of-distribution robustness, yet most existing approaches either rely on linear models or require difficult bi-level optimisation. We introduce Neural Causal Regularization (NCR), a simple invariance penalty that extends the causal regularization framework of Kania and Wit [3], to deep neural networks. NCR promotes robustness by penalising changes in a network's prediction under spurious transformations. When the two training environments differ only in the spurious factor, increasing the regularisation weight drives the risks toward equality, recovering the causal predictor in the limit. Empirically, on three bias-controlled variants of the Colored MNIST benchmark, NCR consistently improves out-of-distribution accuracy over empirical risk minimisation (ERM) and the variance-based REx penalty, while remaining easy to optimise.

