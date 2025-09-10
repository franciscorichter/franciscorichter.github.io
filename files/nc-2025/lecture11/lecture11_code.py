"""
LECTURE 11: ORDINARY DIFFERENTIAL EQUATIONS (IVPs)
Generates educational figures saved into ../images/ at 300 DPI.

Figures:
- euler_vs_rk4_solution.png
- stability_regions_euler_trap.png
- stiff_euler_instability.png
- embedded_rk_error_control.png
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(2)


def f_vdp(t, y, mu=1.0):
    # Van der Pol in relaxation regime (mu moderate for demo)
    x, v = y
    dx = v
    dv = mu * (1 - x**2) * v - x
    return np.array([dx, dv])


def rk4_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + 0.5*h, y + 0.5*h*k1)
    k3 = f(t + 0.5*h, y + 0.5*h*k2)
    k4 = f(t + h, y + h*k3)
    return y + (h/6.0) * (k1 + 2*k2 + 2*k3 + k4)


def euler_step(f, t, y, h):
    return y + h * f(t, y)


def figure_euler_vs_rk4_solution():
    # Simple harmonic oscillator y'' + y = 0 -> system
    def f(t, y):
        return np.array([y[1], -y[0]])

    t0, T = 0.0, 20.0
    h = 0.1
    n = int((T - t0) / h)
    t = np.linspace(t0, T, n+1)
    y_e = np.zeros((n+1, 2))
    y_r = np.zeros((n+1, 2))
    y_e[0] = np.array([1.0, 0.0])
    y_r[0] = np.array([1.0, 0.0])

    for i in range(n):
        y_e[i+1] = euler_step(f, t[i], y_e[i], h)
        y_r[i+1] = rk4_step(f, t[i], y_r[i], h)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(t, y_e[:, 0], label='Euler', color='#d62728')
    axes[0].plot(t, y_r[:, 0], label='RK4', color='#1f77b4')
    axes[0].set_title('Solution component x(t)')
    axes[0].set_xlabel('t')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(y_e[:, 0], y_e[:, 1], label='Euler', color='#d62728')
    axes[1].plot(y_r[:, 0], y_r[:, 1], label='RK4', color='#1f77b4')
    axes[1].set_title('Phase portrait (x, v)')
    axes[1].set_xlabel('x')
    axes[1].set_ylabel('v')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    plt.tight_layout()
    plt.savefig('../images/euler_vs_rk4_solution.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


def figure_stability_regions_euler_trap():
    # Stability regions for Euler (explicit) and Trapezoidal (implicit midpoint)
    x = np.linspace(-4, 2, 400)
    y = np.linspace(-3, 3, 400)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j*Y

    R_euler = 1 + Z  # forward Euler
    R_trap = (1 + Z/2) / (1 - Z/2)  # trapezoidal rule

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    axes[0].contourf(X, Y, np.abs(R_euler) <= 1, levels=1, cmap='Blues')
    axes[0].set_title('Stability region: Forward Euler')
    axes[0].set_xlabel('Re(z)')
    axes[0].set_ylabel('Im(z)')
    axes[0].axvline(0, color='k', linewidth=0.5)
    axes[0].axhline(0, color='k', linewidth=0.5)

    axes[1].contourf(X, Y, np.abs(R_trap) <= 1, levels=1, cmap='Greens')
    axes[1].set_title('Stability region: Trapezoidal (A-stable)')
    axes[1].set_xlabel('Re(z)')
    axes[1].axvline(0, color='k', linewidth=0.5)
    axes[1].axhline(0, color='k', linewidth=0.5)

    plt.tight_layout()
    plt.savefig('../images/stability_regions_euler_trap.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


def figure_stiff_euler_instability():
    # Stiff equation y' = -lambda y with large lambda
    lam = 50.0
    f = lambda t, y: -lam * y
    t0, T = 0.0, 1.0
    h_explicit = 0.05  # unstable for Euler if h*lam > 2
    h_implicit = 0.2   # stable for trapezoidal

    # Explicit Euler
    nE = int((T - t0) / h_explicit)
    tE = np.linspace(t0, T, nE+1)
    yE = np.zeros(nE+1)
    yE[0] = 1.0
    for i in range(nE):
        yE[i+1] = yE[i] + h_explicit * f(tE[i], yE[i])

    # Trapezoidal (implicit midpoint) for scalar linear f
    nT = int((T - t0) / h_implicit)
    tT = np.linspace(t0, T, nT+1)
    yT = np.zeros(nT+1)
    yT[0] = 1.0
    # update: y_{n+1} = y_n + h*(-lam*(y_{n+1}+y_n)/2) -> (1 + h*lam/2) y_{n+1} = (1 - h*lam/2) y_n
    a = (1 - h_implicit*lam/2) / (1 + h_implicit*lam/2)
    for i in range(nT):
        yT[i+1] = a * yT[i]

    t_true = np.linspace(t0, T, 400)
    y_true = np.exp(-lam * t_true)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t_true, y_true, 'k--', label='Exact')
    ax.plot(tE, yE, 'o-', label='Explicit Euler (unstable)')
    ax.plot(tT, yT, 's-', label='Trapezoidal (stable)')
    ax.set_title("Stiff ODE: Stability matters")
    ax.set_xlabel('t')
    ax.set_ylabel('y')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig('../images/stiff_euler_instability.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


def figure_embedded_rk_error_control():
    # Demonstrate error estimate trend for an embedded method (synthetic)
    # Use RK4 as reference solution and simulate error estimates decreasing with step refinement.
    f = lambda t, y: -y + np.sin(t)
    t0, T = 0.0, 10.0
    hs = np.array([1.0, 0.5, 0.25, 0.125, 0.0625])
    errs = []
    for h in hs:
        n = int(np.ceil((T - t0) / h))
        t = t0
        y = 0.0
        for _ in range(n):
            y = rk4_step(lambda tt, yy: np.array([f(tt, yy[0])]), t, np.array([y]), h)[0]
            t += h
        # Use difference to a refined step as a proxy
        h2 = h / 2
        n2 = int(np.ceil((T - t0) / h2))
        t2 = t0
        y2 = 0.0
        for _ in range(n2):
            y2 = rk4_step(lambda tt, yy: np.array([f(tt, yy[0])]), t2, np.array([y2]), h2)[0]
            t2 += h2
        errs.append(abs(y2 - y))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.loglog(hs, errs, 'o-', label='Estimated error')
    ax.loglog(hs, errs[0]*(hs/hs[0])**4, '--', color='gray', label='~ h^4')
    ax.set_xlabel('Step size h (log scale)')
    ax.set_ylabel('Error estimate (log scale)')
    ax.set_title('Embedded RK Error Control Trend (Illustrative)')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig('../images/embedded_rk_error_control.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    figure_euler_vs_rk4_solution()
    figure_stability_regions_euler_trap()
    figure_stiff_euler_instability()
    figure_embedded_rk_error_control()
    print('Lecture 11 figures generated in ../images/')
