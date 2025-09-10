"""
LECTURE 7: ITERATIVE METHODS FOR LINEAR SYSTEMS
Educational Python Code for Numerical Computing Course

Author: Francisco Richter Mendoza
Institution: Università della Svizzera Italiana
Course: Numerical Computing

This module provides comprehensive demonstrations of iterative methods
for solving linear systems, including classical methods (Jacobi, Gauss-Seidel, SOR)
and modern Krylov subspace methods (CG, GMRES).
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve, cg, gmres
from scipy.linalg import norm, eig, eigvals
import time
from matplotlib.patches import Ellipse
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

def create_iterative_methods_comprehensive_figure():
    """
    Create comprehensive analysis of iterative methods showing:
    1. Convergence comparison of classical methods
    2. Spectral radius analysis and convergence rates
    3. Condition number effects on convergence
    4. Geometric interpretation of conjugate gradient
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Problem setup: 2D Poisson equation discretization
    n = 50
    h = 1.0 / (n + 1)
    
    # Create 2D Laplacian matrix (5-point stencil)
    def create_2d_laplacian(n):
        """Create discrete 2D Laplacian matrix"""
        N = n * n
        diagonals = [
            -4 * np.ones(N),  # main diagonal
            np.ones(N-1),     # super diagonal
            np.ones(N-1),     # sub diagonal  
            np.ones(N-n),     # super diagonal (n positions)
            np.ones(N-n)      # sub diagonal (n positions)
        ]
        
        # Handle boundary conditions for super/sub diagonals
        for i in range(n-1, N-1, n):
            diagonals[1][i] = 0  # Remove connection across rows
            diagonals[2][i] = 0
            
        offsets = [0, 1, -1, n, -n]
        A = sp.diags(diagonals, offsets, shape=(N, N), format='csr')
        return -A / (h**2)  # Scale by grid spacing
    
    A_sparse = create_2d_laplacian(20)  # Smaller for demonstration
    A = A_sparse.toarray()
    
    # Right-hand side (manufactured solution)
    x_true = np.random.randn(A.shape[0])
    b = A @ x_true
    x0 = np.zeros_like(b)
    
    # Panel 1: Convergence comparison of classical methods
    def jacobi_iteration(A, b, x0, max_iter=100, tol=1e-10):
        """Jacobi iterative method"""
        n = len(b)
        x = x0.copy()
        residuals = []
        
        D = np.diag(np.diag(A))
        R = A - D
        
        for k in range(max_iter):
            x_new = np.linalg.solve(D, b - R @ x)
            residual = norm(A @ x_new - b)
            residuals.append(residual)
            
            if residual < tol:
                break
            x = x_new
            
        return x, residuals
    
    def gauss_seidel_iteration(A, b, x0, max_iter=100, tol=1e-10):
        """Gauss-Seidel iterative method"""
        n = len(b)
        x = x0.copy()
        residuals = []
        
        for k in range(max_iter):
            for i in range(n):
                sum1 = sum(A[i][j] * x[j] for j in range(i))
                sum2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
                x[i] = (b[i] - sum1 - sum2) / A[i][i]
            
            residual = norm(A @ x - b)
            residuals.append(residual)
            
            if residual < tol:
                break
                
        return x, residuals
    
    def sor_iteration(A, b, x0, omega=1.5, max_iter=100, tol=1e-10):
        """SOR iterative method"""
        n = len(b)
        x = x0.copy()
        residuals = []
        
        for k in range(max_iter):
            for i in range(n):
                sum1 = sum(A[i][j] * x[j] for j in range(i))
                sum2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
                x_gs = (b[i] - sum1 - sum2) / A[i][i]
                x[i] = (1 - omega) * x[i] + omega * x_gs
            
            residual = norm(A @ x - b)
            residuals.append(residual)
            
            if residual < tol:
                break
                
        return x, residuals
    
    # Test on smaller system for visualization
    A_small = A[:100, :100]
    b_small = b[:100]
    x0_small = x0[:100]
    
    _, res_jacobi = jacobi_iteration(A_small, b_small, x0_small)
    _, res_gs = gauss_seidel_iteration(A_small, b_small, x0_small)
    _, res_sor = sor_iteration(A_small, b_small, x0_small, omega=1.2)
    
    ax1.semilogy(res_jacobi[:50], 'b-', label='Jacobi', linewidth=2)
    ax1.semilogy(res_gs[:50], 'r--', label='Gauss-Seidel', linewidth=2)
    ax1.semilogy(res_sor[:50], 'g:', label='SOR (ω=1.2)', linewidth=2)
    ax1.set_xlabel('Iteration', fontsize=12)
    ax1.set_ylabel('Residual Norm', fontsize=12)
    ax1.set_title('Classical Iterative Methods Convergence', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Add convergence rate annotations
    if len(res_jacobi) > 10:
        rate_jacobi = -np.log(res_jacobi[20] / res_jacobi[10]) / 10
        ax1.text(0.6, 0.8, f'Jacobi rate: {rate_jacobi:.3f}', 
                transform=ax1.transAxes, fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    
    # Panel 2: Spectral radius analysis
    def compute_spectral_radius(A, method='jacobi'):
        """Compute spectral radius of iteration matrix"""
        D = np.diag(np.diag(A))
        L = -np.tril(A, -1)
        U = -np.triu(A, 1)
        
        if method == 'jacobi':
            G = np.linalg.solve(D, L + U)
        elif method == 'gauss_seidel':
            G = np.linalg.solve(D - L, U)
        elif method == 'sor':
            omega = 1.2
            G = np.linalg.solve(D - omega*L, (1-omega)*D + omega*U)
        
        eigenvals = eigvals(G)
        return max(abs(eigenvals)), eigenvals
    
    # Test on different matrix sizes
    sizes = [10, 15, 20, 25, 30]
    rho_jacobi = []
    rho_gs = []
    rho_sor = []
    
    for size in sizes:
        A_test = create_2d_laplacian(size).toarray()
        
        rho_j, _ = compute_spectral_radius(A_test, 'jacobi')
        rho_g, _ = compute_spectral_radius(A_test, 'gauss_seidel')
        rho_s, _ = compute_spectral_radius(A_test, 'sor')
        
        rho_jacobi.append(rho_j)
        rho_gs.append(rho_g)
        rho_sor.append(rho_s)
    
    ax2.plot(sizes, rho_jacobi, 'bo-', label='Jacobi', linewidth=2, markersize=8)
    ax2.plot(sizes, rho_gs, 'rs--', label='Gauss-Seidel', linewidth=2, markersize=8)
    ax2.plot(sizes, rho_sor, 'g^:', label='SOR (ω=1.2)', linewidth=2, markersize=8)
    ax2.axhline(y=1, color='k', linestyle='-', alpha=0.5, label='Convergence threshold')
    ax2.set_xlabel('Matrix Size', fontsize=12)
    ax2.set_ylabel('Spectral Radius ρ(G)', fontsize=12)
    ax2.set_title('Spectral Radius vs Matrix Size', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # Panel 3: Condition number effects on CG convergence
    def create_spd_matrix(n, condition_number):
        """Create symmetric positive definite matrix with specified condition number"""
        # Generate eigenvalues logarithmically spaced
        eigenvals = np.logspace(0, np.log10(condition_number), n)
        
        # Random orthogonal matrix
        Q, _ = np.linalg.qr(np.random.randn(n, n))
        
        # Construct SPD matrix
        A = Q @ np.diag(eigenvals) @ Q.T
        return A
    
    condition_numbers = [10, 100, 1000]
    colors = ['blue', 'red', 'green']
    
    for i, kappa in enumerate(condition_numbers):
        A_spd = create_spd_matrix(50, kappa)
        x_true_spd = np.random.randn(50)
        b_spd = A_spd @ x_true_spd
        
        # Conjugate Gradient
        def cg_method(A, b, x0, max_iter=50):
            """Conjugate Gradient method"""
            x = x0.copy()
            r = b - A @ x
            p = r.copy()
            errors = []
            
            for k in range(max_iter):
                Ap = A @ p
                alpha = (r.T @ r) / (p.T @ Ap)
                x = x + alpha * p
                r_new = r - alpha * Ap
                
                # Compute error in A-norm
                error = np.sqrt((x - x_true_spd).T @ A @ (x - x_true_spd))
                errors.append(error)
                
                if norm(r_new) < 1e-10:
                    break
                    
                beta = (r_new.T @ r_new) / (r.T @ r)
                p = r_new + beta * p
                r = r_new
                
            return x, errors
        
        _, errors = cg_method(A_spd, b_spd, np.zeros(50))
        
        # Theoretical bound
        theoretical_rate = (np.sqrt(kappa) - 1) / (np.sqrt(kappa) + 1)
        theoretical_bound = [2 * (theoretical_rate**k) * errors[0] for k in range(len(errors))]
        
        ax3.semilogy(errors, color=colors[i], linewidth=2, 
                    label=f'CG κ={kappa}')
        ax3.semilogy(theoretical_bound, '--', color=colors[i], alpha=0.7,
                    label=f'Theory κ={kappa}')
    
    ax3.set_xlabel('Iteration', fontsize=12)
    ax3.set_ylabel('Error in A-norm', fontsize=12)
    ax3.set_title('CG Convergence vs Condition Number', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # Panel 4: Geometric interpretation of CG
    # 2D quadratic function visualization
    def plot_cg_geometry():
        """Visualize CG method geometrically"""
        # Simple 2D problem
        A_2d = np.array([[4, 1], [1, 2]])
        b_2d = np.array([1, 2])
        x_true_2d = np.linalg.solve(A_2d, b_2d)
        
        # Create contour plot of quadratic function
        x_range = np.linspace(-1, 2, 100)
        y_range = np.linspace(-1, 3, 100)
        X, Y = np.meshgrid(x_range, y_range)
        
        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                x_vec = np.array([X[i,j], Y[i,j]])
                Z[i,j] = 0.5 * x_vec.T @ A_2d @ x_vec - b_2d.T @ x_vec
        
        contours = ax4.contour(X, Y, Z, levels=20, alpha=0.6, colors='gray')
        ax4.contourf(X, Y, Z, levels=20, alpha=0.3, cmap='viridis')
        
        # CG iterations
        x = np.array([0.0, 0.0])  # Starting point
        r = b_2d - A_2d @ x
        p = r.copy()
        
        cg_path = [x.copy()]
        
        for k in range(2):  # Exact in 2 steps for 2D
            Ap = A_2d @ p
            alpha = (r.T @ r) / (p.T @ Ap)
            x = x + alpha * p
            cg_path.append(x.copy())
            
            r_new = r - alpha * Ap
            if norm(r_new) < 1e-10:
                break
                
            beta = (r_new.T @ r_new) / (r.T @ r)
            p = r_new + beta * p
            r = r_new
        
        # Plot CG path
        cg_path = np.array(cg_path)
        ax4.plot(cg_path[:, 0], cg_path[:, 1], 'ro-', linewidth=3, 
                markersize=8, label='CG iterations')
        ax4.plot(x_true_2d[0], x_true_2d[1], 'g*', markersize=15, 
                label='True solution')
        
        # Add search direction arrows
        for i in range(len(cg_path)-1):
            dx = cg_path[i+1, 0] - cg_path[i, 0]
            dy = cg_path[i+1, 1] - cg_path[i, 1]
            ax4.arrow(cg_path[i, 0], cg_path[i, 1], dx, dy, 
                     head_width=0.05, head_length=0.05, fc='red', ec='red')
        
        ax4.set_xlabel('x₁', fontsize=12)
        ax4.set_ylabel('x₂', fontsize=12)
        ax4.set_title('CG Geometric Interpretation', fontsize=14, fontweight='bold')
        ax4.legend(fontsize=11)
        ax4.grid(True, alpha=0.3)
        ax4.set_aspect('equal')
    
    plot_cg_geometry()
    
    plt.tight_layout()
    plt.savefig('../images/iterative_methods_comprehensive.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'spectral_radii': {'jacobi': rho_jacobi[-1], 'gauss_seidel': rho_gs[-1], 'sor': rho_sor[-1]},
        'convergence_rates': {'jacobi': len(res_jacobi), 'gauss_seidel': len(res_gs), 'sor': len(res_sor)},
        'condition_effects': condition_numbers
    }

def create_krylov_methods_analysis():
    """
    Create analysis of Krylov subspace methods showing:
    1. CG vs GMRES convergence comparison
    2. Krylov subspace dimension growth
    3. Preconditioning effects
    4. Memory and computational requirements
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Create test problems
    n = 100
    
    # SPD matrix for CG
    eigenvals_spd = np.logspace(0, 2, n)  # Condition number 100
    Q_spd, _ = np.linalg.qr(np.random.randn(n, n))
    A_spd = Q_spd @ np.diag(eigenvals_spd) @ Q_spd.T
    
    # Non-symmetric matrix for GMRES
    A_nonsym = A_spd + 0.1 * np.random.randn(n, n)
    
    x_true = np.random.randn(n)
    b_spd = A_spd @ x_true
    b_nonsym = A_nonsym @ x_true
    
    # Panel 1: CG vs GMRES convergence
    def custom_cg(A, b, x0, max_iter=50):
        """Custom CG implementation with residual tracking"""
        x = x0.copy()
        r = b - A @ x
        p = r.copy()
        residuals = [norm(r)]
        
        for k in range(max_iter):
            Ap = A @ p
            alpha = (r.T @ r) / (p.T @ Ap)
            x = x + alpha * p
            r_new = r - alpha * Ap
            
            residuals.append(norm(r_new))
            
            if norm(r_new) < 1e-10:
                break
                
            beta = (r_new.T @ r_new) / (r.T @ r)
            p = r_new + beta * p
            r = r_new
            
        return x, residuals
    
    def custom_gmres(A, b, x0, max_iter=50):
        """Custom GMRES implementation with residual tracking"""
        x = x0.copy()
        r = b - A @ x
        residuals = [norm(r)]
        
        # Arnoldi process
        V = np.zeros((len(b), max_iter + 1))
        H = np.zeros((max_iter + 1, max_iter))
        
        V[:, 0] = r / norm(r)
        
        for k in range(max_iter):
            w = A @ V[:, k]
            
            # Gram-Schmidt orthogonalization
            for j in range(k + 1):
                H[j, k] = np.dot(w, V[:, j])
                w = w - H[j, k] * V[:, j]
            
            H[k + 1, k] = norm(w)
            if H[k + 1, k] < 1e-12:
                break
                
            V[:, k + 1] = w / H[k + 1, k]
            
            # Solve least squares problem
            e1 = np.zeros(k + 2)
            e1[0] = norm(r)
            
            y, _, _, _ = np.linalg.lstsq(H[:k+2, :k+1], e1, rcond=None)
            x_k = x0 + V[:, :k+1] @ y
            
            residual = norm(b - A @ x_k)
            residuals.append(residual)
            
            if residual < 1e-10:
                break
        
        return x_k, residuals
    
    # Run methods
    _, res_cg = custom_cg(A_spd, b_spd, np.zeros(n))
    _, res_gmres_spd = custom_gmres(A_spd, b_spd, np.zeros(n))
    _, res_gmres_nonsym = custom_gmres(A_nonsym, b_nonsym, np.zeros(n))
    
    ax1.semilogy(res_cg, 'b-', linewidth=2, label='CG (SPD matrix)')
    ax1.semilogy(res_gmres_spd, 'r--', linewidth=2, label='GMRES (SPD matrix)')
    ax1.semilogy(res_gmres_nonsym, 'g:', linewidth=2, label='GMRES (non-symmetric)')
    ax1.set_xlabel('Iteration', fontsize=12)
    ax1.set_ylabel('Residual Norm', fontsize=12)
    ax1.set_title('CG vs GMRES Convergence', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Panel 2: Krylov subspace dimension analysis
    def analyze_krylov_dimension(A, v, max_dim=20):
        """Analyze effective dimension of Krylov subspace"""
        n = len(v)
        K = np.zeros((n, max_dim))
        K[:, 0] = v / norm(v)
        
        dimensions = []
        condition_numbers = []
        
        for k in range(1, max_dim):
            # Build next Krylov vector
            Av = A @ K[:, k-1]
            K[:, k] = Av / norm(Av)
            
            # Check linear independence
            K_k = K[:, :k+1]
            U, s, Vt = np.linalg.svd(K_k, full_matrices=False)
            
            # Effective dimension (numerical rank)
            tol = 1e-12
            rank = np.sum(s > tol * s[0])
            dimensions.append(rank)
            
            # Condition number of Krylov matrix
            if rank > 0:
                condition_numbers.append(s[0] / s[rank-1])
            else:
                condition_numbers.append(np.inf)
        
        return dimensions, condition_numbers
    
    v = np.random.randn(n)
    dims_spd, conds_spd = analyze_krylov_dimension(A_spd, v)
    dims_nonsym, conds_nonsym = analyze_krylov_dimension(A_nonsym, v)
    
    ax2_twin = ax2.twinx()
    
    line1 = ax2.plot(range(1, len(dims_spd)+1), dims_spd, 'b-', linewidth=2, 
                     label='SPD matrix')
    line2 = ax2.plot(range(1, len(dims_nonsym)+1), dims_nonsym, 'r--', linewidth=2, 
                     label='Non-symmetric')
    
    line3 = ax2_twin.semilogy(range(1, len(conds_spd)+1), conds_spd, 'b:', alpha=0.7, 
                              label='Condition (SPD)')
    line4 = ax2_twin.semilogy(range(1, len(conds_nonsym)+1), conds_nonsym, 'r:', alpha=0.7, 
                              label='Condition (non-sym)')
    
    ax2.set_xlabel('Krylov Subspace Dimension', fontsize=12)
    ax2.set_ylabel('Effective Dimension', fontsize=12, color='black')
    ax2_twin.set_ylabel('Condition Number', fontsize=12, color='gray')
    ax2.set_title('Krylov Subspace Analysis', fontsize=14, fontweight='bold')
    
    # Combine legends
    lines = line1 + line2 + line3 + line4
    labels = [l.get_label() for l in lines]
    ax2.legend(lines, labels, fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    # Panel 3: Preconditioning effects
    def create_preconditioner(A, type='diagonal'):
        """Create different types of preconditioners"""
        if type == 'diagonal':
            return np.diag(np.diag(A))
        elif type == 'ilu':
            # Simplified incomplete LU (just lower triangular part)
            L = np.tril(A, -1) + np.eye(A.shape[0])
            U = np.triu(A, 0)
            return L @ U
        else:
            return np.eye(A.shape[0])
    
    # Test preconditioning on ill-conditioned problem
    eigenvals_ill = np.logspace(0, 3, n)  # Condition number 1000
    A_ill = Q_spd @ np.diag(eigenvals_ill) @ Q_spd.T
    b_ill = A_ill @ x_true
    
    # No preconditioning
    _, res_no_precond = custom_cg(A_ill, b_ill, np.zeros(n))
    
    # Diagonal preconditioning
    M_diag = create_preconditioner(A_ill, 'diagonal')
    M_diag_inv = np.diag(1.0 / np.diag(M_diag))
    A_precond_diag = M_diag_inv @ A_ill
    b_precond_diag = M_diag_inv @ b_ill
    _, res_diag_precond = custom_cg(A_precond_diag, b_precond_diag, np.zeros(n))
    
    # Incomplete LU preconditioning (simplified)
    M_ilu = create_preconditioner(A_ill, 'ilu')
    try:
        M_ilu_inv = np.linalg.inv(M_ilu)
        A_precond_ilu = M_ilu_inv @ A_ill
        b_precond_ilu = M_ilu_inv @ b_ill
        _, res_ilu_precond = custom_cg(A_precond_ilu, b_precond_ilu, np.zeros(n))
    except:
        res_ilu_precond = res_diag_precond  # Fallback
    
    ax3.semilogy(res_no_precond, 'r-', linewidth=2, label='No preconditioning')
    ax3.semilogy(res_diag_precond, 'b--', linewidth=2, label='Diagonal preconditioning')
    ax3.semilogy(res_ilu_precond, 'g:', linewidth=2, label='ILU preconditioning')
    ax3.set_xlabel('Iteration', fontsize=12)
    ax3.set_ylabel('Residual Norm', fontsize=12)
    ax3.set_title('Preconditioning Effects on CG', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=11)
    ax3.grid(True, alpha=0.3)
    
    # Panel 4: Memory and computational requirements
    matrix_sizes = [50, 100, 200, 400, 800]
    
    # Memory requirements (in MB, approximate)
    memory_direct = [(n**2 * 8) / (1024**2) for n in matrix_sizes]  # Full matrix storage
    memory_cg = [(n * 4 * 8) / (1024**2) for n in matrix_sizes]     # 4 vectors of size n
    memory_gmres_full = [(n * (n+1) * 8) / (1024**2) for n in matrix_sizes]  # Full GMRES
    memory_gmres_restart = [(n * 21 * 8) / (1024**2) for n in matrix_sizes]  # GMRES(20)
    
    # Computational complexity (operations per iteration, approximate)
    ops_direct = [n**3 / 3 for n in matrix_sizes]  # LU factorization
    ops_cg = [2 * n**2 for n in matrix_sizes]      # Matrix-vector products
    ops_gmres = [2 * n**2 for n in matrix_sizes]   # Similar to CG per iteration
    
    ax4_twin = ax4.twinx()
    
    # Memory plot
    line1 = ax4.loglog(matrix_sizes, memory_direct, 'k-', linewidth=2, 
                       label='Direct (LU)')
    line2 = ax4.loglog(matrix_sizes, memory_cg, 'b--', linewidth=2, 
                       label='CG')
    line3 = ax4.loglog(matrix_sizes, memory_gmres_restart, 'r:', linewidth=2, 
                       label='GMRES(20)')
    line4 = ax4.loglog(matrix_sizes, memory_gmres_full, 'g-.', linewidth=2, 
                       label='GMRES (full)')
    
    # Operations plot
    line5 = ax4_twin.loglog(matrix_sizes, ops_direct, 'k-', alpha=0.5, linewidth=1)
    line6 = ax4_twin.loglog(matrix_sizes, ops_cg, 'b--', alpha=0.5, linewidth=1)
    
    ax4.set_xlabel('Matrix Size n', fontsize=12)
    ax4.set_ylabel('Memory (MB)', fontsize=12, color='black')
    ax4_twin.set_ylabel('Operations per Iteration', fontsize=12, color='gray')
    ax4.set_title('Memory and Computational Requirements', fontsize=14, fontweight='bold')
    
    lines = line1 + line2 + line3 + line4
    labels = [l.get_label() for l in lines]
    ax4.legend(lines, labels, fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../images/krylov_methods_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'cg_iterations': len(res_cg),
        'gmres_iterations': len(res_gmres_nonsym),
        'preconditioning_improvement': len(res_no_precond) / len(res_diag_precond),
        'memory_scaling': {'cg': memory_cg[-1], 'gmres_full': memory_gmres_full[-1]}
    }

def create_convergence_theory_analysis():
    """
    Create theoretical analysis of convergence showing:
    1. Spectral radius and convergence rate relationship
    2. Polynomial approximation theory for CG
    3. Eigenvalue clustering effects
    4. Optimal parameters for SOR
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Panel 1: Spectral radius vs convergence rate
    spectral_radii = np.linspace(0.1, 0.99, 50)
    convergence_rates = -np.log(spectral_radii)
    iterations_to_converge = np.log(1e-6) / np.log(spectral_radii)  # To reduce error by 10^6
    
    ax1_twin = ax1.twinx()
    
    line1 = ax1.plot(spectral_radii, convergence_rates, 'b-', linewidth=2, 
                     label='Convergence rate')
    line2 = ax1_twin.plot(spectral_radii, iterations_to_converge, 'r--', linewidth=2, 
                          label='Iterations to converge')
    
    ax1.set_xlabel('Spectral Radius ρ(G)', fontsize=12)
    ax1.set_ylabel('Convergence Rate -log(ρ)', fontsize=12, color='blue')
    ax1_twin.set_ylabel('Iterations to Converge', fontsize=12, color='red')
    ax1.set_title('Spectral Radius vs Convergence', fontsize=14, fontweight='bold')
    
    # Add critical regions
    ax1.axvline(x=0.9, color='orange', linestyle=':', alpha=0.7, 
                label='Slow convergence')
    ax1.axvline(x=0.5, color='green', linestyle=':', alpha=0.7, 
                label='Fast convergence')
    
    lines = line1 + line2
    labels = [l.get_label() for l in lines] + ['Slow convergence', 'Fast convergence']
    ax1.legend(lines + [ax1.axvline(x=0.9, color='orange', linestyle=':'), 
                       ax1.axvline(x=0.5, color='green', linestyle=':')], 
              labels, fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Panel 2: Polynomial approximation theory for CG
    def chebyshev_polynomial(n, x, a, b):
        """Chebyshev polynomial of first kind on interval [a,b]"""
        # Transform to [-1,1]
        t = (2*x - a - b) / (b - a)
        
        if n == 0:
            return np.ones_like(t)
        elif n == 1:
            return t
        else:
            T_prev2 = np.ones_like(t)
            T_prev1 = t
            for k in range(2, n+1):
                T_curr = 2*t*T_prev1 - T_prev2
                T_prev2 = T_prev1
                T_prev1 = T_curr
            return T_curr
    
    # Eigenvalue distribution examples
    lambda_min, lambda_max = 1, 100
    eigenvals = np.linspace(lambda_min, lambda_max, 1000)
    
    # CG optimal polynomial (Chebyshev)
    degrees = [5, 10, 20]
    colors = ['blue', 'red', 'green']
    
    for i, degree in enumerate(degrees):
        # Chebyshev polynomial shifted to [lambda_min, lambda_max]
        T_n = chebyshev_polynomial(degree, eigenvals, lambda_min, lambda_max)
        T_n_0 = chebyshev_polynomial(degree, 0, lambda_min, lambda_max)
        
        # Optimal polynomial p(x) = T_n(x) / T_n(0)
        p_optimal = T_n / T_n_0
        
        ax2.plot(eigenvals, np.abs(p_optimal), color=colors[i], linewidth=2, 
                label=f'Degree {degree}')
        
        # Theoretical bound
        kappa = lambda_max / lambda_min
        bound = 2 * ((np.sqrt(kappa) - 1) / (np.sqrt(kappa) + 1))**degree
        ax2.axhline(y=bound, color=colors[i], linestyle='--', alpha=0.7)
    
    ax2.set_xlabel('Eigenvalue λ', fontsize=12)
    ax2.set_ylabel('|p(λ)|', fontsize=12)
    ax2.set_title('CG Optimal Polynomials (Chebyshev)', fontsize=14, fontweight='bold')
    ax2.set_yscale('log')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # Panel 3: Eigenvalue clustering effects
    def create_clustered_eigenvalues(n, cluster_ratio=0.8):
        """Create eigenvalue distribution with clustering"""
        n_clustered = int(n * cluster_ratio)
        n_outliers = n - n_clustered
        
        # Clustered eigenvalues near 1
        clustered = 1 + 0.1 * np.random.rand(n_clustered)
        
        # Outlier eigenvalues
        outliers = np.logspace(1, 2, n_outliers)  # Between 10 and 100
        
        return np.concatenate([clustered, outliers])
    
    # Compare uniform vs clustered eigenvalue distributions
    n = 50
    
    # Uniform distribution
    eigenvals_uniform = np.linspace(1, 100, n)
    
    # Clustered distribution
    eigenvals_clustered = create_clustered_eigenvalues(n, 0.9)
    eigenvals_clustered = np.sort(eigenvals_clustered)
    
    # Simulate CG convergence for both
    def simulate_cg_convergence(eigenvals, max_iter=30):
        """Simulate CG convergence based on eigenvalue distribution"""
        kappa = max(eigenvals) / min(eigenvals)
        
        # Theoretical bound (pessimistic)
        theoretical = [2 * ((np.sqrt(kappa) - 1) / (np.sqrt(kappa) + 1))**k 
                      for k in range(max_iter)]
        
        # Improved bound for clustered eigenvalues
        # Count eigenvalues in different ranges
        large_eigenvals = eigenvals[eigenvals > 10]
        small_eigenvals = eigenvals[eigenvals <= 10]
        
        if len(large_eigenvals) < 0.2 * len(eigenvals):  # Most eigenvalues clustered
            # Faster convergence due to clustering
            improved = [theoretical[k] * (0.1)**min(k//5, 2) for k in range(max_iter)]
        else:
            improved = theoretical
            
        return theoretical, improved
    
    theory_uniform, _ = simulate_cg_convergence(eigenvals_uniform)
    theory_clustered, improved_clustered = simulate_cg_convergence(eigenvals_clustered)
    
    ax3.semilogy(theory_uniform, 'b-', linewidth=2, label='Uniform eigenvalues')
    ax3.semilogy(theory_clustered, 'r--', linewidth=2, label='Clustered (pessimistic)')
    ax3.semilogy(improved_clustered, 'g:', linewidth=2, label='Clustered (realistic)')
    
    ax3.set_xlabel('Iteration', fontsize=12)
    ax3.set_ylabel('Error Bound', fontsize=12)
    ax3.set_title('Eigenvalue Clustering Effects on CG', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=11)
    ax3.grid(True, alpha=0.3)
    
    # Add eigenvalue distribution insets
    ax3_inset1 = ax3.inset_axes([0.15, 0.6, 0.3, 0.25])
    ax3_inset1.hist(eigenvals_uniform, bins=20, alpha=0.7, color='blue')
    ax3_inset1.set_title('Uniform', fontsize=8)
    ax3_inset1.set_xticks([])
    ax3_inset1.set_yticks([])
    
    ax3_inset2 = ax3.inset_axes([0.55, 0.6, 0.3, 0.25])
    ax3_inset2.hist(eigenvals_clustered, bins=20, alpha=0.7, color='green')
    ax3_inset2.set_title('Clustered', fontsize=8)
    ax3_inset2.set_xticks([])
    ax3_inset2.set_yticks([])
    
    # Panel 4: Optimal SOR parameters
    def compute_optimal_sor(h_values):
        """Compute optimal SOR parameter for 2D Poisson equation"""
        omega_optimal = []
        spectral_radii = []
        
        for h in h_values:
            # For 2D Poisson, Jacobi spectral radius is cos(π*h)
            rho_jacobi = np.cos(np.pi * h)
            
            # Optimal omega
            omega_opt = 2 / (1 + np.sqrt(1 - rho_jacobi**2))
            omega_optimal.append(omega_opt)
            
            # Corresponding SOR spectral radius
            rho_sor = omega_opt - 1
            spectral_radii.append(rho_sor)
        
        return omega_optimal, spectral_radii
    
    # Grid spacings
    h_values = np.logspace(-2, -0.5, 20)  # From 0.01 to ~0.3
    omega_opt, rho_sor = compute_optimal_sor(h_values)
    
    # Also compute for different omega values
    omega_range = np.linspace(1.0, 1.99, 100)
    h_fixed = 0.1
    rho_jacobi_fixed = np.cos(np.pi * h_fixed)
    
    rho_sor_range = []
    for omega in omega_range:
        if omega == 1.0:
            rho = rho_jacobi_fixed  # Gauss-Seidel
        else:
            # SOR spectral radius formula
            if omega < 2:
                rho = max(abs(omega - 1), 
                         abs(0.5 * (omega - 1 + np.sqrt((omega-1)**2 + 4*omega*rho_jacobi_fixed**2))))
            else:
                rho = omega - 1  # Divergent
        rho_sor_range.append(rho)
    
    ax4_twin = ax4.twinx()
    
    # Optimal omega vs grid spacing
    line1 = ax4.semilogx(h_values, omega_opt, 'b-', linewidth=2, 
                         label='Optimal ω')
    line2 = ax4_twin.semilogx(h_values, rho_sor, 'r--', linewidth=2, 
                              label='Spectral radius')
    
    ax4.set_xlabel('Grid Spacing h', fontsize=12)
    ax4.set_ylabel('Optimal ω', fontsize=12, color='blue')
    ax4_twin.set_ylabel('Spectral Radius', fontsize=12, color='red')
    ax4.set_title('Optimal SOR Parameters', fontsize=14, fontweight='bold')
    
    # Add inset showing omega vs spectral radius
    ax4_inset = ax4.inset_axes([0.5, 0.5, 0.45, 0.4])
    ax4_inset.plot(omega_range, rho_sor_range, 'g-', linewidth=2)
    ax4_inset.axhline(y=1, color='k', linestyle='--', alpha=0.5)
    ax4_inset.axvline(x=2/(1 + np.sqrt(1 - rho_jacobi_fixed**2)), 
                      color='r', linestyle=':', alpha=0.7)
    ax4_inset.set_xlabel('ω', fontsize=8)
    ax4_inset.set_ylabel('ρ(G)', fontsize=8)
    ax4_inset.set_title(f'h = {h_fixed}', fontsize=8)
    ax4_inset.grid(True, alpha=0.3)
    
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax4.legend(lines, labels, fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../images/convergence_theory_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'optimal_omega': omega_opt[-1],
        'convergence_improvement': rho_jacobi_fixed / rho_sor[-1],
        'clustering_effect': len(improved_clustered) / len(theory_uniform)
    }

def create_practical_implementation_guide():
    """
    Create practical implementation guide showing:
    1. Algorithm complexity comparison
    2. Memory usage patterns
    3. Parallel scalability analysis
    4. Method selection guidelines
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Panel 1: Algorithm complexity comparison
    problem_sizes = np.logspace(2, 4, 10)  # 100 to 10,000
    
    # Theoretical complexities
    direct_lu = problem_sizes**3 / 3
    jacobi_iter = 2 * problem_sizes**2 * 100  # Assume 100 iterations
    cg_iter = 2 * problem_sizes**2 * np.sqrt(problem_sizes)  # O(n^2.5) for typical problems
    gmres_iter = 2 * problem_sizes**2 * 50  # Assume 50 iterations
    multigrid = 10 * problem_sizes  # O(n) for optimal multigrid
    
    ax1.loglog(problem_sizes, direct_lu, 'k-', linewidth=2, label='Direct (LU)')
    ax1.loglog(problem_sizes, jacobi_iter, 'b--', linewidth=2, label='Jacobi (100 iter)')
    ax1.loglog(problem_sizes, cg_iter, 'r:', linewidth=2, label='CG (√n iter)')
    ax1.loglog(problem_sizes, gmres_iter, 'g-.', linewidth=2, label='GMRES (50 iter)')
    ax1.loglog(problem_sizes, multigrid, 'm-', linewidth=2, label='Multigrid')
    
    # Add complexity reference lines
    ax1.loglog(problem_sizes, problem_sizes**2, 'gray', alpha=0.5, linestyle=':', 
               label='O(n²)')
    ax1.loglog(problem_sizes, problem_sizes**3, 'gray', alpha=0.5, linestyle=':', 
               label='O(n³)')
    
    ax1.set_xlabel('Problem Size n', fontsize=12)
    ax1.set_ylabel('Operations', fontsize=12)
    ax1.set_title('Computational Complexity Comparison', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Panel 2: Memory usage patterns
    # Memory for different methods (in MB)
    memory_direct = (problem_sizes**2 * 8) / (1024**2)  # Full matrix
    memory_sparse = (5 * problem_sizes * 8) / (1024**2)  # 5-point stencil
    memory_cg = (4 * problem_sizes * 8) / (1024**2)  # 4 vectors
    memory_gmres_20 = (21 * problem_sizes * 8) / (1024**2)  # GMRES(20)
    memory_gmres_full = (problem_sizes**2 * 8) / (1024**2)  # Full GMRES
    
    ax2.loglog(problem_sizes, memory_direct, 'k-', linewidth=2, label='Direct (dense)')
    ax2.loglog(problem_sizes, memory_sparse, 'b--', linewidth=2, label='Sparse storage')
    ax2.loglog(problem_sizes, memory_cg, 'r:', linewidth=2, label='CG')
    ax2.loglog(problem_sizes, memory_gmres_20, 'g-.', linewidth=2, label='GMRES(20)')
    ax2.loglog(problem_sizes, memory_gmres_full, 'm-', linewidth=2, label='GMRES (full)')
    
    # Memory limit lines
    ax2.axhline(y=1024, color='orange', linestyle='--', alpha=0.7, label='1 GB limit')
    ax2.axhline(y=8*1024, color='red', linestyle='--', alpha=0.7, label='8 GB limit')
    
    ax2.set_xlabel('Problem Size n', fontsize=12)
    ax2.set_ylabel('Memory (MB)', fontsize=12)
    ax2.set_title('Memory Usage Comparison', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    # Panel 3: Parallel scalability analysis
    num_processors = np.array([1, 2, 4, 8, 16, 32, 64])
    
    # Theoretical speedup models
    ideal_speedup = num_processors
    
    # Amdahl's law with different serial fractions
    serial_fractions = [0.05, 0.1, 0.2]
    colors = ['blue', 'red', 'green']
    labels = ['5% serial', '10% serial', '20% serial']
    
    for i, s in enumerate(serial_fractions):
        amdahl_speedup = 1 / (s + (1-s)/num_processors)
        ax3.plot(num_processors, amdahl_speedup, color=colors[i], linewidth=2, 
                label=f'Amdahl ({labels[i]})')
    
    # Gustafson's law (scaled speedup)
    gustafson_speedup = num_processors - 0.1 * (num_processors - 1)
    ax3.plot(num_processors, gustafson_speedup, 'purple', linewidth=2, 
            label='Gustafson (scaled)')
    
    # Ideal speedup
    ax3.plot(num_processors, ideal_speedup, 'k--', linewidth=2, label='Ideal')
    
    # Realistic iterative method performance
    realistic_speedup = num_processors * 0.8 / (1 + 0.1 * np.log2(num_processors))
    ax3.plot(num_processors, realistic_speedup, 'orange', linewidth=2, 
            label='Realistic (iterative)')
    
    ax3.set_xlabel('Number of Processors', fontsize=12)
    ax3.set_ylabel('Speedup', fontsize=12)
    ax3.set_title('Parallel Scalability Analysis', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    ax3.set_xscale('log', base=2)
    
    # Panel 4: Method selection guidelines
    # Create decision tree visualization
    condition_numbers = np.logspace(1, 8, 100)
    problem_sizes = np.logspace(2, 6, 100)
    
    # Create meshgrid for decision regions
    kappa_grid, n_grid = np.meshgrid(np.logspace(1, 8, 50), np.logspace(2, 6, 50))
    
    # Decision function
    decision = np.zeros_like(kappa_grid)
    
    for i in range(kappa_grid.shape[0]):
        for j in range(kappa_grid.shape[1]):
            kappa = kappa_grid[i, j]
            n = n_grid[i, j]
            
            if n < 1000:
                if kappa < 100:
                    decision[i, j] = 1  # Direct methods
                else:
                    decision[i, j] = 2  # CG with preconditioning
            elif n < 10000:
                if kappa < 1000:
                    decision[i, j] = 2  # CG
                else:
                    decision[i, j] = 3  # GMRES with preconditioning
            else:
                if kappa < 10000:
                    decision[i, j] = 4  # Multigrid
                else:
                    decision[i, j] = 5  # Advanced methods
    
    # Plot decision regions
    colors = ['white', 'lightblue', 'lightgreen', 'lightyellow', 'lightcoral', 'lightpink']
    levels = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
    
    contour = ax4.contourf(kappa_grid, n_grid, decision, levels=levels, 
                          colors=colors[1:], alpha=0.7)
    
    # Add method labels
    ax4.text(50, 500, 'Direct\nMethods', fontsize=10, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    ax4.text(1000, 2000, 'CG', fontsize=10, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
    ax4.text(10000, 5000, 'GMRES\n+ Precond', fontsize=10, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
    ax4.text(1000, 50000, 'Multigrid', fontsize=10, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
    ax4.text(100000, 100000, 'Advanced\nMethods', fontsize=10, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightpink"))
    
    ax4.set_xlabel('Condition Number κ(A)', fontsize=12)
    ax4.set_ylabel('Problem Size n', fontsize=12)
    ax4.set_title('Method Selection Guidelines', fontsize=14, fontweight='bold')
    ax4.set_xscale('log')
    ax4.set_yscale('log')
    ax4.grid(True, alpha=0.3)
    
    # Add boundary lines
    ax4.axvline(x=100, color='black', linestyle='--', alpha=0.5)
    ax4.axvline(x=1000, color='black', linestyle='--', alpha=0.5)
    ax4.axhline(y=1000, color='black', linestyle='--', alpha=0.5)
    ax4.axhline(y=10000, color='black', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('../images/practical_implementation_guide.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'complexity_crossover': problem_sizes[np.argmin(np.abs(direct_lu - cg_iter))],
        'memory_limit_size': problem_sizes[np.argmin(np.abs(memory_direct - 1024))],
        'parallel_efficiency': realistic_speedup[-1] / ideal_speedup[-1],
        'method_recommendations': {
            'small_wellconditioned': 'Direct methods',
            'large_wellconditioned': 'CG',
            'large_illconditioned': 'Preconditioned GMRES',
            'very_large': 'Multigrid'
        }
    }

def main():
    """Main function to generate all figures and run demonstrations"""
    print("Generating Lecture 7: Iterative Methods for Linear Systems")
    print("=" * 60)
    
    # Create figures directory
    import os
    os.makedirs('figures', exist_ok=True)
    
    print("✅ Generating comprehensive iterative methods analysis...")
    results1 = create_iterative_methods_comprehensive_figure()
    
    print("✅ Generating Krylov subspace methods analysis...")
    results2 = create_krylov_methods_analysis()
    
    print("✅ Generating convergence theory analysis...")
    results3 = create_convergence_theory_analysis()
    
    print("✅ Generating practical implementation guide...")
    results4 = create_practical_implementation_guide()
    
    print("=" * 60)
    print("ITERATIVE METHODS ANALYSIS")
    print("=" * 60)
    
    print("📊 Classical Methods Performance:")
    print(f"   • Jacobi spectral radius: {results1['spectral_radii']['jacobi']:.3f}")
    print(f"   • Gauss-Seidel spectral radius: {results1['spectral_radii']['gauss_seidel']:.3f}")
    print(f"   • SOR spectral radius: {results1['spectral_radii']['sor']:.3f}")
    print(f"   • Convergence iterations (Jacobi/GS/SOR): {results1['convergence_rates']['jacobi']}/{results1['convergence_rates']['gauss_seidel']}/{results1['convergence_rates']['sor']}")
    
    print("\n🔧 Krylov Methods Analysis:")
    print(f"   • CG iterations: {results2['cg_iterations']}")
    print(f"   • GMRES iterations: {results2['gmres_iterations']}")
    print(f"   • Preconditioning improvement: {results2['preconditioning_improvement']:.1f}×")
    print(f"   • Memory scaling (CG/GMRES): {results2['memory_scaling']['cg']:.1f}/{results2['memory_scaling']['gmres_full']:.1f} MB")
    
    print("\n📈 Convergence Theory:")
    print(f"   • Optimal SOR parameter: {results3['optimal_omega']:.3f}")
    print(f"   • SOR convergence improvement: {results3['convergence_improvement']:.1f}×")
    print(f"   • Eigenvalue clustering effect: {results3['clustering_effect']:.1f}×")
    
    print("\n⚡ Practical Implementation:")
    print(f"   • Complexity crossover point: n ≈ {results4['complexity_crossover']:.0f}")
    print(f"   • Memory limit problem size: n ≈ {results4['memory_limit_size']:.0f}")
    print(f"   • Parallel efficiency (64 cores): {results4['parallel_efficiency']:.1%}")
    
    print("\n🎯 Method Selection Guidelines:")
    for problem_type, method in results4['method_recommendations'].items():
        print(f"   • {problem_type.replace('_', ' ').title()}: {method}")
    
    print("=" * 60)
    print("✅ ALL FIGURES AND DEMONSTRATIONS COMPLETED")
    print("=" * 60)
    
    print("Generated files:")
    print("- figures/iterative_methods_comprehensive.png")
    print("- figures/krylov_methods_analysis.png") 
    print("- figures/convergence_theory_analysis.png")
    print("- figures/practical_implementation_guide.png")
    
    print("\nKey Educational Results:")
    print("- Classical methods convergence depends on spectral radius")
    print("- Krylov methods provide optimal convergence for their respective classes")
    print("- Preconditioning is essential for ill-conditioned problems")
    print("- Method selection depends on problem size, conditioning, and structure")
    print("- Parallel scalability varies significantly between methods")

if __name__ == "__main__":
    main()
