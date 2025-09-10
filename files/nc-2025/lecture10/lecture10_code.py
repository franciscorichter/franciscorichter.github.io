"""
LECTURE 10: NUMERICAL INTEGRATION
Generates educational figures saved into ../images/ at 300 DPI.

Figures:
- trapezoid_vs_simpson_convergence.png
- gaussian_quadrature_performance.png
- adaptive_simpson_subdivision.png
- newton_cotes_nodes.png
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.legendre import leggauss

np.random.seed(1)

def true_integral(f, a, b):
    # High-accuracy reference via Gauss-Legendre with many points
    x, w = leggauss(200)
    # map [-1,1] -> [a,b]
    t = 0.5 * (x + 1) * (b - a) + a
    return 0.5 * (b - a) * np.sum(w * f(t))


def composite_trapezoid(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    y = f(x)
    return h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1])


def composite_simpson(f, a, b, n2):
    # n2 must be even number of subintervals; n2 = 2n
    if n2 % 2 == 1:
        n2 += 1
    x = np.linspace(a, b, n2 + 1)
    h = (b - a) / n2
    y = f(x)
    S = y[0] + y[-1] + 4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2])
    return h * S / 3.0


def figure_trapezoid_vs_simpson():
    f = np.exp
    a, b = 0.0, 1.0
    I = true_integral(f, a, b)

    Ns = np.array([2, 4, 8, 16, 32, 64, 128])
    err_T = []
    err_S = []
    for n in Ns:
        T = composite_trapezoid(f, a, b, n)
        S = composite_simpson(f, a, b, 2 * n)
        err_T.append(abs(I - T))
        err_S.append(abs(I - S))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.loglog(Ns, err_T, 'o-', label='Composite Trapezoid (O(h^2))')
    ax.loglog(Ns, err_S, 's-', label='Composite Simpson (O(h^4))')

    # Reference slopes
    ax.loglog(Ns, err_T[0] * (Ns[0] / Ns) ** 2, '--', color='gray', label='~ h^2')
    ax.loglog(Ns, err_S[0] * (Ns[0] / Ns) ** 4, '--', color='black', label='~ h^4')

    ax.set_xlabel('Number of subintervals N (log scale)', fontsize=12)
    ax.set_ylabel('Absolute error (log scale)', fontsize=12)
    ax.set_title('Convergence: Composite Trapezoid vs Simpson (f(x)=e^x)', fontsize=14, fontweight='bold')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig('../images/trapezoid_vs_simpson_convergence.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


def figure_gaussian_quadrature_performance():
    f = lambda x: np.cos(5 * x) * np.exp(-x)
    a, b = -1.0, 1.0
    I = true_integral(f, a, b)

    ns = np.arange(1, 9)
    err_GL = []
    err_S = []
    for n in ns:
        # Gauss-Legendre n points
        xg, wg = leggauss(n)
        # map [-1,1] -> [a,b]
        tg = 0.5 * (xg + 1) * (b - a) + a
        Ig = 0.5 * (b - a) * np.sum(wg * f(tg))
        err_GL.append(abs(I - Ig))

        # Simpson with roughly comparable evaluations (2n subintervals -> ~2n+1 evals)
        S = composite_simpson(f, a, b, max(2, 2 * n))
        err_S.append(abs(I - S))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.semilogy(ns, err_GL, 'o-', label='Gauss-Legendre (n points)')
    ax.semilogy(ns, err_S, 's-', label='Composite Simpson (~2n+1 evals)')
    ax.set_xlabel('n (points / half subintervals)', fontsize=12)
    ax.set_ylabel('Absolute error (log scale)', fontsize=12)
    ax.set_title('Gaussian Quadrature vs Composite Simpson', fontsize=14, fontweight='bold')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig('../images/gaussian_quadrature_performance.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


def figure_adaptive_simpson_subdivision():
    # Illustrate refinement concentration on sharp feature
    f = lambda x: 1.0 / (1 + 400 * (x - 0.3) ** 2) + 0.2 * np.sin(8 * x)
    a, b = 0.0, 1.0

    # Construct a simple refinement: start with few intervals; refine where curvature proxy is large
    x = np.linspace(a, b, 17)
    for _ in range(3):
        y = f(x)
        # curvature proxy: second finite difference magnitude
        curv = np.abs(np.diff(y, 2))
        # mark segments with largest curvature
        idx = np.argsort(curv)[-8:]
        new_pts = 0.5 * (x[idx + 1] + x[idx + 2])
        x = np.sort(np.concatenate([x, new_pts]))

    xs = np.linspace(a, b, 800)
    ys = f(xs)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(xs, ys, 'k-', label='f(x)')
    ax.vlines(x, ymin=min(ys), ymax=max(ys), colors='gray', alpha=0.2, label='Refined subintervals')
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_title('Adaptive Simpson: Subdivision Concentrates Near Sharp Features (Illustrative)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig('../images/adaptive_simpson_subdivision.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


def figure_newton_cotes_nodes():
    a, b = -1.0, 1.0
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)

    # Midpoint (open n=1)
    x_mid = np.array([(a + b) / 2])
    axes[0].axhline(0, color='k', linewidth=0.5)
    axes[0].scatter(x_mid, np.zeros_like(x_mid), s=60)
    axes[0].set_title('Midpoint rule (open)')

    # Trapezoid (closed n=1)
    x_trap = np.array([a, b])
    axes[1].axhline(0, color='k', linewidth=0.5)
    axes[1].scatter(x_trap, np.zeros_like(x_trap), s=60)
    axes[1].set_title("Trapezoidal rule (closed)")

    # Simpson (closed n=2)
    x_simp = np.array([a, 0.5 * (a + b), b])
    axes[2].axhline(0, color='k', linewidth=0.5)
    axes[2].scatter(x_simp, np.zeros_like(x_simp), s=60)
    axes[2].set_title("Simpson's rule (closed)")

    for ax in axes:
        ax.set_xlim(a - 0.1, b + 0.1)
        ax.set_xticks(np.linspace(a, b, 5))
        ax.set_yticks([])
        ax.grid(True, alpha=0.2)

    fig.suptitle('Newton–Cotes Nodes (Illustrative)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('../images/newton_cotes_nodes.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    figure_trapezoid_vs_simpson()
    figure_gaussian_quadrature_performance()
    figure_adaptive_simpson_subdivision()
    figure_newton_cotes_nodes()
    print('Lecture 10 figures generated in ../images/')
