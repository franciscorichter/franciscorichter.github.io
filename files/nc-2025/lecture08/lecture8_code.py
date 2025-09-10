"""
LECTURE 8: EIGENVALUE PROBLEMS
Educational Python code to generate figures for the Numerical Computing course.

Figures generated (saved to ../images/ at 300 DPI):
- power_method_convergence.png
- qr_algorithm_convergence.png
- eigenvalue_perturbation.png
- lanczos_ritz_convergence.png
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)


def power_method_convergence():
    """Simulate power method convergence rate for matrices with varying |lambda2/lambda1|."""
    ratios = [0.9, 0.7, 0.5, 0.3]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

    fig, ax = plt.subplots(figsize=(10, 6))
    k = np.arange(0, 30)
    for r, c in zip(ratios, colors):
        err = r ** k
        ax.semilogy(k, err, label=f"|λ2/λ1|={r}", color=c, linewidth=2)

    ax.set_xlabel("Iteration k", fontsize=12)
    ax.set_ylabel("Error ~ |λ2/λ1|^k", fontsize=12)
    ax.set_title("Power Method Convergence vs. Spectral Gap", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)

    plt.tight_layout()
    plt.savefig("../images/power_method_convergence.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


ess = np.finfo(float).eps


def qr_algorithm_convergence():
    """Illustrative QR convergence by tracking off-diagonal Frobenius norm during implicit iterations."""
    # Create a symmetric matrix with distinct eigenvalues
    n = 20
    A = np.random.randn(n, n)
    A = (A + A.T) / 2.0

    def offdiag_norm(M):
        return np.linalg.norm(M - np.diag(np.diag(M)), ord="fro")

    max_iter = 50
    norms = []
    H = A.copy()
    for _ in range(max_iter):
        # Basic unshifted QR (illustrative)
        Q, R = np.linalg.qr(H)
        H = R @ Q
        norms.append(offdiag_norm(H) + ess)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.semilogy(norms, linewidth=2, color="#9467bd")
    ax.set_xlabel("Iteration", fontsize=12)
    ax.set_ylabel("Off-diagonal Frobenius norm", fontsize=12)
    ax.set_title("QR Algorithm: Off-diagonal Decay (Illustrative)", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("../images/qr_algorithm_convergence.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def eigenvalue_perturbation():
    """Visualize Bauer–Fike style sensitivity by perturbing a diagonalizable matrix."""
    n = 6
    # Create a diagonalizable matrix A = X Λ X^{-1}
    eigvals = np.linspace(1, 6, n)
    X, _ = np.linalg.qr(np.random.randn(n, n))
    A = X @ np.diag(eigvals) @ np.linalg.inv(X)

    # Perturbations
    deltas = np.logspace(-6, -1, 10)
    max_shifts = []

    for d in deltas:
        E = d * np.random.randn(n, n)
        lam_A = np.linalg.eigvals(A)
        lam_AE = np.linalg.eigvals(A + E)
        # Maximum distance from each perturbed eigenvalue to the closest original
        shifts = []
        for lam in lam_AE:
            shifts.append(np.min(np.abs(lam - lam_A)))
        max_shifts.append(np.max(shifts))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.loglog(deltas, max_shifts, 'o-', color="#8c564b", linewidth=2, markersize=6, label="Observed")

    # Rough Bauer–Fike bound line: κ(X) * ||E||
    kappa_X = np.linalg.cond(X)
    bound = kappa_X * deltas
    ax.loglog(deltas, bound, '--', color="#17becf", linewidth=2, label=r"κ(X) \|E\|")

    ax.set_xlabel(r"\|E\| (log scale)", fontsize=12)
    ax.set_ylabel("Eigenvalue shift (max)", fontsize=12)
    ax.set_title("Eigenvalue Perturbation (Bauer–Fike intuition)", fontsize=14, fontweight="bold")
    ax.grid(True, which='both', alpha=0.3)
    ax.legend(fontsize=11)

    plt.tight_layout()
    plt.savefig("../images/eigenvalue_perturbation.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def lanczos_ritz_convergence():
    """Demonstrate Ritz value convergence using a simple Lanczos-like projection (without SciPy)."""
    n = 80
    A = np.random.randn(n, n)
    A = (A + A.T) / 2.0  # symmetric

    m = 20  # subspace size
    q = np.random.randn(n)
    q = q / np.linalg.norm(q)

    Q = np.zeros((n, m))
    alpha = np.zeros(m)
    beta = np.zeros(m-1)

    q_prev = np.zeros_like(q)
    for j in range(m):
        Q[:, j] = q
        z = A @ q
        alpha[j] = np.dot(q, z)
        if j > 0:
            z = z - beta[j-1] * q_prev
        z = z - alpha[j] * q
        # Re-orthogonalize a bit (one step)
        if j > 0:
            z = z - np.dot(Q[:, :j], np.dot(Q[:, :j].T, z))
        beta_j = np.linalg.norm(z)
        if j < m-1:
            beta[j] = beta_j
        if beta_j < 1e-14:
            break
        q_prev = q
        q = z / beta_j

    # Tridiagonal T
    T = np.diag(alpha)
    for j in range(m-1):
        T[j, j+1] = beta[j]
        T[j+1, j] = beta[j]

    # Ritz eigenvalues
    ritz = np.linalg.eigvalsh(T)
    true_vals = np.linalg.eigvalsh(A)

    # Track convergence of extremal Ritz values against true extremals
    ritz_min = np.min(ritz)
    ritz_max = np.max(ritz)
    true_min = np.min(true_vals)
    true_max = np.max(true_vals)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axhline(true_min, color="#2ca02c", linestyle=":", label="True min eig")
    ax.axhline(true_max, color="#d62728", linestyle=":", label="True max eig")
    ax.plot([m], [ritz_min], 'o', color="#2ca02c", label="Ritz min (m)")
    ax.plot([m], [ritz_max], 'o', color="#d62728", label="Ritz max (m)")

    ax.set_xlabel("Subspace size m", fontsize=12)
    ax.set_ylabel("Eigenvalue", fontsize=12)
    ax.set_title("Lanczos Ritz Values vs True Extremal Eigenvalues", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig("../images/lanczos_ritz_convergence.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    power_method_convergence()
    qr_algorithm_convergence()
    eigenvalue_perturbation()
    lanczos_ritz_convergence()
    print("Figures generated in ../images/")
