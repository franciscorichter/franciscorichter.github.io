"""
LECTURE 9: INTERPOLATION AND APPROXIMATION
Generates educational figures saved into ../images/ at 300 DPI.

Figures:
- runge_phenomenon.png
- chebyshev_nodes.png
- least_squares_fit.png
- vandermonde_conditioning.png
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)


def runge_phenomenon():
    def f(x):
        return 1.0 / (1 + 25 * x**2)

    xs = np.linspace(-1, 1, 400)
    ys = f(xs)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Equally spaced nodes
    for n, ax in zip([8, 16], axes):
        nodes = np.linspace(-1, 1, n+1)
        values = f(nodes)
        coeffs = np.polyfit(nodes, values, n)
        p = np.poly1d(coeffs)
        ax.plot(xs, ys, 'k-', label='f(x)')
        ax.plot(xs, p(xs), label=f'Interp deg {n}', linewidth=2)
        ax.plot(nodes, values, 'o', ms=4, label='nodes')
        ax.set_title(f'Equispaced nodes, degree {n}')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig('../images/runge_phenomenon.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


def chebyshev_nodes():
    def f(x):
        return 1.0 / (1 + 25 * x**2)

    xs = np.linspace(-1, 1, 400)
    ys = f(xs)

    n = 16
    # Equispaced
    nodes_e = np.linspace(-1, 1, n+1)
    values_e = f(nodes_e)
    p_e = np.poly1d(np.polyfit(nodes_e, values_e, n))

    # Chebyshev
    k = np.arange(0, n+1)
    nodes_c = np.cos((2*k+1) * np.pi / (2*(n+1)))
    values_c = f(nodes_c)
    p_c = np.poly1d(np.polyfit(nodes_c, values_c, n))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(xs, ys, 'k-', label='f(x)')
    ax.plot(xs, p_e(xs), '--', label='Equispaced interp (deg 16)')
    ax.plot(xs, p_c(xs), '-', label='Chebyshev interp (deg 16)')
    ax.plot(nodes_e, values_e, 'o', ms=4, label='Equispaced nodes')
    ax.plot(nodes_c, values_c, 's', ms=4, label='Chebyshev nodes')
    ax.set_title('Chebyshev vs Equispaced Interpolation', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9)

    plt.tight_layout()
    plt.savefig('../images/chebyshev_nodes.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


def least_squares_fit():
    # Generate noisy quadratic data
    m = 40
    x = np.linspace(-2, 2, m)
    y_true = 0.5 * x**2 - x + 1
    y = y_true + 0.3 * np.random.randn(m)

    # Fit polynomials of degree 1, 2, 5
    degrees = [1, 2, 5]
    xx = np.linspace(-2, 2, 400)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y, s=16, color='#1f77b4', alpha=0.7, label='Noisy data')
    ax.plot(xx, y_true := 0.5 * xx**2 - xx + 1, 'k--', label='True model')

    for d in degrees:
        coeffs = np.polyfit(x, y, d)
        p = np.poly1d(coeffs)
        ax.plot(xx, p(xx), linewidth=2, label=f'Least squares deg {d}')

    ax.set_title('Least Squares Polynomial Fits', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9)

    plt.tight_layout()
    plt.savefig('../images/least_squares_fit.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


def vandermonde_conditioning():
    # Condition numbers for Vandermonde with equispaced vs Chebyshev nodes
    sizes = np.arange(5, 41, 5)
    cond_e = []
    cond_c = []
    for n in sizes:
        nodes_e = np.linspace(-1, 1, n)
        V_e = np.vander(nodes_e, N=n, increasing=True)
        cond_e.append(np.linalg.cond(V_e))

        k = np.arange(0, n)
        nodes_c = np.cos((2*k+1) * np.pi / (2*n))
        V_c = np.vander(nodes_c, N=n, increasing=True)
        cond_c.append(np.linalg.cond(V_c))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.semilogy(sizes, cond_e, 'o-', label='Equispaced nodes')
    ax.semilogy(sizes, cond_c, 's-', label='Chebyshev nodes')
    ax.set_xlabel('Number of nodes n', fontsize=12)
    ax.set_ylabel('cond(V)', fontsize=12)
    ax.set_title('Vandermonde Conditioning', fontsize=14, fontweight='bold')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend(fontsize=9)

    plt.tight_layout()
    plt.savefig('../images/vandermonde_conditioning.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    runge_phenomenon()
    chebyshev_nodes()
    least_squares_fit()
    vandermonde_conditioning()
    print('Lecture 9 figures generated in ../images/')
