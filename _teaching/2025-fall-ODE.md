---
title: "Introduction to Ordinary Differential Equations"
collection: teaching
type: "2025-fall"
permalink: /teaching/2025-fall-intro-ode
venue: "Università della Svizzera italiana, Faculty of Informatics"
date: 2025-09-19
location: "Lugano, Switzerland"
instructor: "Francisco Richter"
degree_program: "Master of Science in Artificial Intelligence / Computational Science, 1st-2nd year"
---

This course introduces the fundamental concepts and techniques of ordinary differential equations (ODEs), with a focus on applications in artificial intelligence and computational science. We connect modeling and analysis (existence, stability, qualitative behavior) with computation (numerical initial-value solvers, stiffness) and modern ODE-based learning (Neural ODEs, sparse discovery, and multiscale/network dynamics).

For up-to-date information on schedule and lecture room, visit the [official USI course page](https://search.usi.ch/it/corsi/35275460/introduction-to-ordinary-differential-equations).

## Schedule (14 weeks)

- **Format:** 1 lecture per week on Fridays. After every two lectures there is an _Exercises + Quiz_ session (first half TA Q&A, second half quiz). After Quiz 4 there is one last lecture and a final Exercises session before the exam.

| Week | Date       | Topic                                                  | Materials                                   | Notes            |
|:-----|:-----------|:-------------------------------------------------------|:--------------------------------------------|:-----------------|
| 1    | 2025-09-19 | Lecture 1: Introduction and First-Order Equations      | [Notes](/files/ode-2025/lecture01.pdf)      |                  |
| 2    | 2025-09-26 | Lecture 2: Systems of First-Order Equations            | [Notes](/files/ode-2025/lecture02.pdf)      |                  |
| 3    | 2025-10-03 | Exercises + Quiz 1                                     |                                             | TA Q&A + Quiz    |
| 4    | 2025-10-10 | Lecture 3: Linear Systems and Matrix Methods           | [Notes](/files/ode-2025/lecture03.pdf)      |                  |
| 5    | 2025-10-17 | Lecture 4: Eigenvalue Methods and Diagonalization      | [Notes](/files/ode-2025/lecture04.pdf)      |                  |
| 6    | 2025-10-24 | Exercises + Quiz 2                                     |                                             | TA Q&A + Quiz    |
| 7    | 2025-10-31 | Lecture 5: Nonlinear Dynamics and Phase Plane Analysis | [Notes](/files/ode-2025/lecture05.pdf)      |                  |
| 8    | 2025-11-07 | Lecture 6: Stability Theory and Lyapunov Methods       | [Notes](/files/ode-2025/lecture06.pdf)      |                  |
| 9    | 2025-11-14 | Exercises + Quiz 3                                     |                                             | TA Q&A + Quiz    |
| 10   | 2025-11-21 | Lecture 7: Numerical Methods for Differential Equations| [Notes](/files/ode-2025/lecture07.pdf)      |                  |
| 11   | 2025-11-28 | Lecture 8: Applications in Science and Engineering     | [Notes](/files/ode-2025/lecture08.pdf)      |                  |
| 12   | 2025-12-05 | Exercises + Quiz 4                                     |                                             | TA Q&A + Quiz    |
| 13   | 2025-12-12 | Lecture 9: Advanced Topics and Current Research        | [Notes](/files/ode-2025/lecture09.pdf)      |                  |
| 14   | 2025-12-19 | Final Exercises & Q&A (exam preparation)               |                                             | No quiz          |

_Slight adjustments may occur; any changes will be announced here and in class._

## Course Outline (Lectures 1–9)

1.  **Lecture 1 — Introduction and First-Order Equations:** Basic concepts, classification of ODEs, direction fields, isoclines, separable equations, and linear first-order equations with integrating factors.
2.  **Lecture 2 — Systems of First-Order Equations:** Reduction of higher-order equations, phase space, trajectories, nullclines, and linearization for analyzing equilibria in systems like predator-prey models.
3.  **Lecture 3 — Linear Systems and Matrix Methods:** The matrix exponential, eigenvalue analysis for classifying 2D systems (nodes, saddles, spirals), fundamental matrices, and nonhomogeneous systems.
4.  **Lecture 4 — Eigenvalue Methods and Diagonalization:** Solving systems via diagonalization and modal coordinates, handling complex and repeated eigenvalues, and applications to mechanical systems.
5.  **Lecture 5 — Nonlinear Dynamics and Phase Plane Analysis:** In-depth analysis of nonlinear systems, limit cycles, Poincaré-Bendixson theorem, and local bifurcations (saddle-node, transcritical, pitchfork, Hopf).
6.  **Lecture 6 — Stability Theory and Lyapunov Methods:** Rigorous definitions of stability, Lyapunov's direct method, LaSalle's invariance principle, estimating basins of attraction, and stability of periodic orbits.
7.  **Lecture 7 — Numerical Methods for Differential Equations:** Euler's method, Runge-Kutta methods, multi-step methods, local vs. global error, stability regions, stiffness, adaptive step-size control, and geometric integration.
8.  **Lecture 8 — Applications in Science and Engineering:** Broad survey of ODE modeling in mechanics, population dynamics (logistic growth, SIR models), biochemical networks, and coupled oscillator systems.
9.  **Lecture 9 — Advanced Topics and Current Research:** Modern developments including Neural ODEs with adjoint sensitivity, sparse discovery of dynamics (SINDy), consensus on graphs, multiscale methods, and continuous normalizing flows.
