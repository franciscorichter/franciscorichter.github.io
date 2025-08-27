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


| Week | Date       | Topic                                                                 | Materials                                   | Notes            |
|------|------------|------------------------------------------------------------------------|---------------------------------------------|------------------|
| 1    | 2025-09-19 | Lecture 1: Introduction, modeling, IVPs                                | [Notes](/files/ode-2025/lecture01.pdf)      |                  |
| 2    | 2025-09-26 | Lecture 2: First-order ODEs                                            | [Notes](/files/ode-2025/lecture02.pdf)      |                  |
| 3    | 2025-10-03 | Exercises + Quiz 1                                                     |                                             | TA Q&A + Quiz    |
| 4    | 2025-10-10 | Lecture 3: Linear ODEs (higher order)                                  | [Notes](/files/ode-2025/lecture03.pdf)      |                  |
| 5    | 2025-10-17 | Lecture 4: Systems of ODEs                                             | [Notes](/files/ode-2025/lecture04.pdf)      |                  |
| 6    | 2025-10-24 | Exercises + Quiz 2                                                     |                                             | TA Q&A + Quiz    |
| 7    | 2025-10-31 | Lecture 5: Qualitative analysis, phase plane                           | [Notes](/files/ode-2025/lecture05.pdf)      |                  |
| 8    | 2025-11-07 | Lecture 6: Numerical methods for IVPs                                  | [Notes](/files/ode-2025/lecture06.pdf)      |                  |
| 9    | 2025-11-14 | Exercises + Quiz 3                                                     |                                             | TA Q&A + Quiz    |
| 10   | 2025-11-21 | Lecture 7: Laplace transforms                                          | [Notes](/files/ode-2025/lecture07.pdf)      |                  |
| 11   | 2025-11-28 | Lecture 8: Parameter estimation & inference for ODEs                   | [Notes](/files/ode-2025/lecture08.pdf)      |                  |
| 12   | 2025-12-05 | Exercises + Quiz 4                                                     |                                             | TA Q&A + Quiz    |
| 13   | 2025-12-12 | Lecture 9: Modern ODE modeling & learning (Neural ODEs, SINDy, networks, multiscale, CNFs) | [Notes](/files/ode-2025/lecture09.pdf) |                  |
| 14   | 2025-12-19 | Final Exercises & Q&A (exam preparation)                               |                                             | No quiz          |

_Slight adjustments may occur; any changes will be announced here and in class._

## Course Outline (Lectures 1–9)

1. **Lecture 1 — First steps:** modeling from balances; initial value problems; direction fields; separable equations; autonomous dynamics and phase lines.  
2. **Lecture 2 — Existence and tools:** Lipschitz conditions; Picard iterations; Grönwall inequality; comparison principles; maximal interval of existence and blow-up tests.  
3. **Lecture 3 — Linear higher-order ODEs:** reduction to first-order systems; fundamental solutions; constant-coefficient cases; resonance and forcing.  
4. **Lecture 4 — Linear systems:** eigenstructure; Jordan cases; decoupling; planar phase portraits; stability classification; response to inputs.  
5. **Lecture 5 — Nonlinear systems:** linearization; Lyapunov functions; invariant sets; local bifurcations (saddle-node, transcritical, pitchfork); examples.  
6. **Lecture 6 — Numerical IVP solvers:** Euler and Runge–Kutta families; local/global error; stability regions; stiffness; implicit methods; step-size control.  
7. **Lecture 7 — Laplace transforms:** transforms and inversion; step/impulse responses; transfer functions; convolution; solving linear ODEs with discontinuous/impulsive inputs.  
8. **Lecture 8 — Parameter estimation & inference for ODEs:** least squares and collocation; identifiability; residual penalties; regularization; validation on withheld trajectories.  
9. **Lecture 9 — Modern ODE modeling & learning:** Neural ODEs and adjoint sensitivity; sparse discovery (SINDy, weak forms); ODEs on graphs (consensus/synchronization); fast–slow reduction; continuous normalizing flows; computational/stability considerations.



