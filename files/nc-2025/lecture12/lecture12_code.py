"""
LECTURE 12: PARTIAL DIFFERENTIAL EQUATIONS
Generates educational figures saved into ../images/ at 300 DPI.

Figures:
- heat_fe_stability_region.png
- wave_cfl_diagram.png
- poisson_five_point_stencil.png
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

np.random.seed(3)


def heat_fe_stability_region():
    # Von Neumann amplification for heat FE: xi = 1 - 4 r sin^2(beta/2)
    r = np.linspace(0.0, 1.0, 400)
    beta = np.linspace(0.0, np.pi, 401)
    R, B = np.meshgrid(r, beta)
    xi = 1.0 - 4.0 * R * np.sin(B / 2.0) ** 2
    abs_xi = np.abs(xi)

    fig, ax = plt.subplots(figsize=(10, 6))
    cs = ax.contourf(R, B, abs_xi, levels=[0.0, 1.0, 1.5, 2.0], colors=["#63b2ee", "#f8d568", "#e06666"], alpha=0.85)
    cbar = fig.colorbar(cs, ax=ax)
    cbar.set_label(r"$|\xi(\beta)|$")
    ax.axvline(0.5, color="k", linestyle="--", linewidth=1.2, label=r"$r=1/2$ (stability limit)")
    ax.set_xlabel(r"$r = \alpha\,\Delta t/(\Delta x)^2$")
    ax.set_ylabel(r"$\beta$ (wavenumber)")
    ax.set_title("Heat Equation (Forward Euler): Stability Region", fontsize=14, fontweight="bold")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig("../images/heat_fe_stability_region.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def wave_cfl_diagram():
    # Stable region for leapfrog scheme: c * dt / dx <= 1
    s = np.linspace(0, 1.5, 400)
    c_vals = np.linspace(0, 2.0, 401)
    S, C = np.meshgrid(s, c_vals)

    stable = (S <= 1.0).astype(float)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.contourf(S, C, stable, levels=[-0.1, 0.1, 1.1], colors=["#e06666", "#63b2ee"], alpha=0.9)
    ax.axvline(1.0, color="k", linestyle="--", linewidth=1.2)
    ax.text(1.02, 0.05, r"CFL: $c\,\Delta t/\Delta x \leq 1$", transform=ax.get_yaxis_transform(), fontsize=11)
    ax.set_xlabel(r"$\sigma = c\,\Delta t/\Delta x$")
    ax.set_ylabel(r"$c$ (wave speed)")
    ax.set_title("Wave Equation (Leapfrog): CFL Stability Diagram", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig("../images/wave_cfl_diagram.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def poisson_five_point_stencil():
    # Draw a small grid and highlight five-point stencil
    fig, ax = plt.subplots(figsize=(6, 6))
    n = 5
    # draw grid
    for i in range(n):
        ax.plot([0, n - 1], [i, i], color="#999999", linewidth=0.8)
        ax.plot([i, i], [0, n - 1], color="#999999", linewidth=0.8)

    # center point
    cx, cy = 2, 2
    # neighbors
    points = {
        (cx, cy): ("C", "#1f77b4"),
        (cx + 1, cy): ("E", "#2ca02c"),
        (cx - 1, cy): ("W", "#2ca02c"),
        (cx, cy + 1): ("N", "#2ca02c"),
        (cx, cy - 1): ("S", "#2ca02c"),
    }

    for (x, y), (label, color) in points.items():
        ax.add_patch(Rectangle((x - 0.45, y - 0.45), 0.9, 0.9, facecolor=color, alpha=0.3, edgecolor=color))
        ax.text(x, y, label, ha="center", va="center", fontsize=12, color="k")

    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(-0.5, n - 0.5)
    ax.set_aspect("equal")
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_title("Five-Point Stencil for $-\nabla^2 u = f$", fontsize=14, fontweight="bold")
    ax.grid(False)
    plt.tight_layout()
    plt.savefig("../images/poisson_five_point_stencil.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    heat_fe_stability_region()
    wave_cfl_diagram()
    poisson_five_point_stencil()
    print("Lecture 12 figures generated in ../images/")
