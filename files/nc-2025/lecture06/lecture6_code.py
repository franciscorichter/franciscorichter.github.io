"""
LECTURE 6: LEAST SQUARES AND QR DECOMPOSITION
Educational Python Code for Numerical Computing Course

Author: Francisco Richter Mendoza
Institution: Università della Svizzera Italiana
Course: Numerical Computing

This module demonstrates:
1. Linear least squares problems and geometric interpretation
2. Normal equations vs QR decomposition methods
3. QR decomposition algorithms (Gram-Schmidt, Householder)
4. Numerical stability analysis and conditioning
5. Applications to data fitting and overdetermined systems
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import qr, lstsq, norm, svd
from scipy.sparse import random
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

def create_least_squares_comprehensive_figure():
    """Create comprehensive least squares visualization"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Geometric interpretation of least squares
    # Create overdetermined system
    m, n = 20, 2
    A = np.random.randn(m, n)
    x_true = np.array([2, -1])
    noise = 0.3 * np.random.randn(m)
    b = A @ x_true + noise
    
    # Solve using normal equations and QR
    x_normal = np.linalg.solve(A.T @ A, A.T @ b)
    x_qr = np.linalg.lstsq(A, b, rcond=None)[0]
    
    # Plot data and fits
    t = np.linspace(0, 1, m)
    A_plot = np.column_stack([np.ones(m), t])
    b_plot = A_plot @ x_true + 0.3 * np.random.randn(m)
    
    x_fit_normal = np.linalg.solve(A_plot.T @ A_plot, A_plot.T @ b_plot)
    x_fit_qr = np.linalg.lstsq(A_plot, b_plot, rcond=None)[0]
    
    t_fine = np.linspace(0, 1, 100)
    A_fine = np.column_stack([np.ones(100), t_fine])
    
    ax1.scatter(t, b_plot, alpha=0.7, color='blue', s=50, label='Data points')
    ax1.plot(t_fine, A_fine @ x_true, 'g--', linewidth=2, label='True function')
    ax1.plot(t_fine, A_fine @ x_fit_normal, 'r-', linewidth=2, label='Normal equations fit')
    ax1.plot(t_fine, A_fine @ x_fit_qr, 'orange', linestyle=':', linewidth=3, label='QR decomposition fit')
    
    # Add residual visualization
    residual = b_plot - A_plot @ x_fit_qr
    for i in range(0, m, 3):
        ax1.plot([t[i], t[i]], [b_plot[i], A_plot[i] @ x_fit_qr], 'k--', alpha=0.5, linewidth=1)
    
    ax1.set_xlabel('t', fontsize=12)
    ax1.set_ylabel('y', fontsize=12)
    ax1.set_title('Least Squares Data Fitting\nOverdetermined System (m=20, n=2)', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Add text with numerical results
    residual_norm = np.linalg.norm(residual)
    ax1.text(0.05, 0.95, f'Residual norm: {residual_norm:.3f}\nCondition number: {np.linalg.cond(A_plot):.2f}', 
             transform=ax1.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # 2. QR decomposition visualization
    # Create matrix for QR demo
    A_qr = np.array([[1, 2], [1, 1], [1, 0], [0, 1]], dtype=float)
    Q, R = qr(A_qr)
    
    # Plot original matrix columns and Q matrix columns
    colors = ['red', 'blue']
    for i in range(2):
        ax2.arrow(0, 0, A_qr[0, i], A_qr[1, i], head_width=0.1, head_length=0.1, 
                 fc=colors[i], ec=colors[i], linewidth=2, label=f'$a_{i+1}$')
        ax2.arrow(0, 0, Q[0, i], Q[1, i], head_width=0.1, head_length=0.1, 
                 fc=colors[i], ec=colors[i], linestyle='--', linewidth=2, alpha=0.7, label=f'$q_{i+1}$')
    
    # Draw unit circle
    theta = np.linspace(0, 2*np.pi, 100)
    ax2.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3, linewidth=1)
    
    ax2.set_xlim(-1.5, 2.5)
    ax2.set_ylim(-1.5, 2.5)
    ax2.set_xlabel('x₁', fontsize=12)
    ax2.set_ylabel('x₂', fontsize=12)
    ax2.set_title('QR Decomposition: A = QR\nOrthogonalization Process', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')
    
    # Add QR matrices as text
    ax2.text(0.02, 0.98, f'Q = \n{Q[:2, :2].round(3)}\n\nR = \n{R[:2, :2].round(3)}', 
             transform=ax2.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # 3. Stability comparison: Normal equations vs QR
    condition_numbers = np.logspace(1, 12, 20)
    errors_normal = []
    errors_qr = []
    
    for kappa in condition_numbers:
        # Create ill-conditioned matrix with specified condition number
        U, _, Vt = svd(np.random.randn(10, 5))
        s = np.logspace(0, -np.log10(kappa), 5)
        A_test = U[:, :5] @ np.diag(s) @ Vt
        
        x_true_test = np.random.randn(5)
        b_test = A_test @ x_true_test
        
        # Add small perturbation
        b_pert = b_test + 1e-12 * np.random.randn(10)
        
        # Solve using both methods
        try:
            x_normal_test = np.linalg.solve(A_test.T @ A_test, A_test.T @ b_pert)
            error_normal = np.linalg.norm(x_normal_test - x_true_test) / np.linalg.norm(x_true_test)
        except:
            error_normal = np.inf
        
        x_qr_test = np.linalg.lstsq(A_test, b_pert, rcond=None)[0]
        error_qr = np.linalg.norm(x_qr_test - x_true_test) / np.linalg.norm(x_true_test)
        
        errors_normal.append(error_normal)
        errors_qr.append(error_qr)
    
    ax3.loglog(condition_numbers, errors_normal, 'r-o', linewidth=2, markersize=6, label='Normal equations')
    ax3.loglog(condition_numbers, errors_qr, 'b-s', linewidth=2, markersize=6, label='QR decomposition')
    ax3.loglog(condition_numbers, condition_numbers * 1e-16, 'k--', alpha=0.7, label='κ(A) × εₘₐₓ')
    
    ax3.set_xlabel('Condition Number κ(A)', fontsize=12)
    ax3.set_ylabel('Relative Error', fontsize=12)
    ax3.set_title('Numerical Stability Comparison\nNormal Equations vs QR Decomposition', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # Add annotation
    ax3.annotate('QR is more stable\nfor ill-conditioned problems', 
                xy=(1e8, 1e-4), xytext=(1e4, 1e-2),
                arrowprops=dict(arrowstyle='->', color='black', alpha=0.7),
                fontsize=10, ha='center',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # 4. Computational complexity analysis
    matrix_sizes = np.array([50, 100, 200, 400, 800])
    times_normal = []
    times_qr = []
    times_householder = []
    
    for n in matrix_sizes:
        m = int(1.5 * n)  # Overdetermined system
        A_timing = np.random.randn(m, n)
        b_timing = np.random.randn(m)
        
        # Time normal equations
        import time
        start = time.time()
        for _ in range(10):
            x_normal_timing = np.linalg.solve(A_timing.T @ A_timing, A_timing.T @ b_timing)
        times_normal.append((time.time() - start) / 10)
        
        # Time QR decomposition
        start = time.time()
        for _ in range(10):
            x_qr_timing = np.linalg.lstsq(A_timing, b_timing, rcond=None)[0]
        times_qr.append((time.time() - start) / 10)
        
        # Time Householder QR
        start = time.time()
        for _ in range(10):
            Q_h, R_h = qr(A_timing)
            x_house = np.linalg.solve(R_h[:n, :n], Q_h[:m, :n].T @ b_timing)
        times_householder.append((time.time() - start) / 10)
    
    ax4.loglog(matrix_sizes, times_normal, 'r-o', linewidth=2, markersize=6, label='Normal equations O(n³)')
    ax4.loglog(matrix_sizes, times_qr, 'b-s', linewidth=2, markersize=6, label='QR (NumPy) O(mn²)')
    ax4.loglog(matrix_sizes, times_householder, 'g-^', linewidth=2, markersize=6, label='Householder QR O(mn²)')
    
    # Add theoretical complexity lines
    ax4.loglog(matrix_sizes, 1e-8 * matrix_sizes**3, 'r--', alpha=0.5, label='n³ scaling')
    ax4.loglog(matrix_sizes, 2e-8 * matrix_sizes**2 * (1.5 * matrix_sizes), 'b--', alpha=0.5, label='mn² scaling')
    
    ax4.set_xlabel('Matrix Size n', fontsize=12)
    ax4.set_ylabel('Computation Time (seconds)', fontsize=12)
    ax4.set_title('Computational Complexity Comparison\nLeast Squares Methods', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figures/least_squares_comprehensive.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'condition_number': np.linalg.cond(A_plot),
        'residual_norm': residual_norm,
        'qr_matrices': (Q[:2, :2], R[:2, :2]),
        'stability_improvement': np.mean(np.array(errors_normal) / np.array(errors_qr))
    }

def create_qr_algorithms_comparison():
    """Create QR algorithms comparison visualization"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Classical vs Modified Gram-Schmidt
    def classical_gram_schmidt(A):
        m, n = A.shape
        Q = np.zeros((m, n))
        R = np.zeros((n, n))
        
        for j in range(n):
            v = A[:, j].copy()
            for i in range(j):
                R[i, j] = Q[:, i].T @ A[:, j]
                v = v - R[i, j] * Q[:, i]
            R[j, j] = np.linalg.norm(v)
            Q[:, j] = v / R[j, j]
        
        return Q, R
    
    def modified_gram_schmidt(A):
        m, n = A.shape
        Q = np.zeros((m, n))
        R = np.zeros((n, n))
        V = A.copy()
        
        for i in range(n):
            R[i, i] = np.linalg.norm(V[:, i])
            Q[:, i] = V[:, i] / R[i, i]
            for j in range(i + 1, n):
                R[i, j] = Q[:, i].T @ V[:, j]
                V[:, j] = V[:, j] - R[i, j] * Q[:, i]
        
        return Q, R
    
    # Test orthogonality loss
    condition_numbers = np.logspace(1, 10, 15)
    orthogonality_cgs = []
    orthogonality_mgs = []
    orthogonality_householder = []
    
    for kappa in condition_numbers:
        # Create ill-conditioned matrix
        U, _, Vt = svd(np.random.randn(20, 10))
        s = np.logspace(0, -np.log10(kappa), 10)
        A_test = U[:, :10] @ np.diag(s) @ Vt
        
        # Classical Gram-Schmidt
        Q_cgs, _ = classical_gram_schmidt(A_test)
        orth_cgs = np.linalg.norm(Q_cgs.T @ Q_cgs - np.eye(10), 'fro')
        orthogonality_cgs.append(orth_cgs)
        
        # Modified Gram-Schmidt
        Q_mgs, _ = modified_gram_schmidt(A_test)
        orth_mgs = np.linalg.norm(Q_mgs.T @ Q_mgs - np.eye(10), 'fro')
        orthogonality_mgs.append(orth_mgs)
        
        # Householder QR
        Q_house, _ = qr(A_test)
        orth_house = np.linalg.norm(Q_house[:, :10].T @ Q_house[:, :10] - np.eye(10), 'fro')
        orthogonality_householder.append(orth_house)
    
    ax1.loglog(condition_numbers, orthogonality_cgs, 'r-o', linewidth=2, markersize=6, label='Classical Gram-Schmidt')
    ax1.loglog(condition_numbers, orthogonality_mgs, 'b-s', linewidth=2, markersize=6, label='Modified Gram-Schmidt')
    ax1.loglog(condition_numbers, orthogonality_householder, 'g-^', linewidth=2, markersize=6, label='Householder QR')
    ax1.loglog(condition_numbers, condition_numbers * 1e-16, 'k--', alpha=0.7, label='κ(A) × εₘₐₓ')
    
    ax1.set_xlabel('Condition Number κ(A)', fontsize=12)
    ax1.set_ylabel('||QᵀQ - I||_F', fontsize=12)
    ax1.set_title('Orthogonality Loss in QR Algorithms\nNumerical Stability Comparison', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # 2. Householder reflection visualization
    # Create example vector and its reflection
    x = np.array([3, 2])
    e1 = np.array([1, 0])
    
    # Householder vector
    v = x + np.sign(x[0]) * np.linalg.norm(x) * e1
    v = v / np.linalg.norm(v)
    
    # Householder matrix
    H = np.eye(2) - 2 * np.outer(v, v)
    
    # Reflected vector
    x_reflected = H @ x
    
    # Plot
    ax2.arrow(0, 0, x[0], x[1], head_width=0.2, head_length=0.2, fc='blue', ec='blue', linewidth=3, label='Original vector x')
    ax2.arrow(0, 0, x_reflected[0], x_reflected[1], head_width=0.2, head_length=0.2, fc='red', ec='red', linewidth=3, label='Reflected vector Hx')
    ax2.arrow(0, 0, v[0], v[1], head_width=0.15, head_length=0.15, fc='green', ec='green', linewidth=2, label='Householder vector v')
    
    # Draw reflection line (perpendicular to v)
    t_line = np.linspace(-4, 4, 100)
    perp_v = np.array([-v[1], v[0]])
    reflection_line = np.outer(t_line, perp_v)
    ax2.plot(reflection_line[:, 0], reflection_line[:, 1], 'k--', alpha=0.5, linewidth=1, label='Reflection hyperplane')
    
    ax2.set_xlim(-4, 4)
    ax2.set_ylim(-1, 3)
    ax2.set_xlabel('x₁', fontsize=12)
    ax2.set_ylabel('x₂', fontsize=12)
    ax2.set_title('Householder Reflection\nH = I - 2vvᵀ/||v||²', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')
    
    # Add matrix representation
    ax2.text(0.02, 0.98, f'H = \n{H.round(3)}', 
             transform=ax2.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # 3. QR decomposition step-by-step
    A_demo = np.array([[1, 2, 1], [1, 1, 2], [1, 0, 1], [0, 1, 1]], dtype=float)
    
    # Show original matrix and QR result
    Q_demo, R_demo = qr(A_demo)
    
    # Create visualization of the decomposition
    im1 = ax3.imshow(A_demo, cmap='RdBu', aspect='auto', interpolation='nearest')
    ax3.set_title('Original Matrix A\n(4×3 overdetermined)', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Column index', fontsize=12)
    ax3.set_ylabel('Row index', fontsize=12)
    
    # Add values as text
    for i in range(A_demo.shape[0]):
        for j in range(A_demo.shape[1]):
            ax3.text(j, i, f'{A_demo[i, j]:.1f}', ha='center', va='center', fontsize=10, fontweight='bold')
    
    plt.colorbar(im1, ax=ax3, shrink=0.6)
    
    # 4. Show Q and R matrices
    # Plot Q matrix
    ax4_left = plt.subplot2grid((2, 4), (1, 2))
    im2 = ax4_left.imshow(Q_demo, cmap='RdBu', aspect='auto', interpolation='nearest')
    ax4_left.set_title('Q Matrix\n(Orthogonal)', fontsize=12, fontweight='bold')
    ax4_left.set_xlabel('Column', fontsize=10)
    ax4_left.set_ylabel('Row', fontsize=10)
    
    for i in range(Q_demo.shape[0]):
        for j in range(Q_demo.shape[1]):
            ax4_left.text(j, i, f'{Q_demo[i, j]:.2f}', ha='center', va='center', fontsize=8)
    
    # Plot R matrix
    ax4_right = plt.subplot2grid((2, 4), (1, 3))
    im3 = ax4_right.imshow(R_demo, cmap='RdBu', aspect='auto', interpolation='nearest')
    ax4_right.set_title('R Matrix\n(Upper Triangular)', fontsize=12, fontweight='bold')
    ax4_right.set_xlabel('Column', fontsize=10)
    ax4_right.set_ylabel('Row', fontsize=10)
    
    for i in range(R_demo.shape[0]):
        for j in range(R_demo.shape[1]):
            ax4_right.text(j, i, f'{R_demo[i, j]:.2f}', ha='center', va='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('figures/qr_algorithms_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'orthogonality_improvement': np.mean(np.array(orthogonality_cgs) / np.array(orthogonality_householder)),
        'householder_matrix': H,
        'qr_decomposition': (Q_demo, R_demo)
    }

def create_applications_and_conditioning():
    """Create applications and conditioning analysis"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Polynomial fitting application
    # Generate noisy polynomial data
    np.random.seed(123)
    t = np.linspace(0, 1, 20)
    true_coeffs = [1, -2, 3, -1]  # cubic polynomial
    y_true = np.polyval(true_coeffs, t)
    noise = 0.2 * np.random.randn(len(t))
    y_data = y_true + noise
    
    # Fit polynomials of different degrees
    degrees = [1, 2, 3, 5, 8]
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    
    t_fine = np.linspace(0, 1, 100)
    
    ax1.scatter(t, y_data, color='black', s=50, alpha=0.7, label='Noisy data', zorder=5)
    ax1.plot(t_fine, np.polyval(true_coeffs, t_fine), 'k--', linewidth=2, label='True polynomial', zorder=4)
    
    residual_norms = []
    condition_numbers = []
    
    for i, deg in enumerate(degrees):
        # Create Vandermonde matrix
        A_poly = np.vander(t, deg + 1, increasing=True)
        
        # Solve using QR
        coeffs = np.linalg.lstsq(A_poly, y_data, rcond=None)[0]
        
        # Evaluate fitted polynomial
        A_fine = np.vander(t_fine, deg + 1, increasing=True)
        y_fit = A_fine @ coeffs
        
        ax1.plot(t_fine, y_fit, color=colors[i], linewidth=2, label=f'Degree {deg}', alpha=0.8)
        
        # Compute residual norm and condition number
        residual = np.linalg.norm(A_poly @ coeffs - y_data)
        cond_num = np.linalg.cond(A_poly)
        
        residual_norms.append(residual)
        condition_numbers.append(cond_num)
    
    ax1.set_xlabel('t', fontsize=12)
    ax1.set_ylabel('y', fontsize=12)
    ax1.set_title('Polynomial Fitting with Different Degrees\nOverfitting vs Underfitting', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # 2. Residual norms and condition numbers
    ax2.semilogy(degrees, residual_norms, 'bo-', linewidth=2, markersize=8, label='Residual norm')
    ax2_twin = ax2.twinx()
    ax2_twin.semilogy(degrees, condition_numbers, 'rs-', linewidth=2, markersize=8, label='Condition number')
    
    ax2.set_xlabel('Polynomial Degree', fontsize=12)
    ax2.set_ylabel('Residual Norm', fontsize=12, color='blue')
    ax2_twin.set_ylabel('Condition Number', fontsize=12, color='red')
    ax2.set_title('Trade-off: Residual vs Conditioning\nVandermonde Matrix Properties', fontsize=14, fontweight='bold')
    
    ax2.tick_params(axis='y', labelcolor='blue')
    ax2_twin.tick_params(axis='y', labelcolor='red')
    ax2.grid(True, alpha=0.3)
    
    # Add annotations
    ax2.annotate('Lower residual\nbut ill-conditioned', 
                xy=(8, residual_norms[-1]), xytext=(6, residual_norms[2]),
                arrowprops=dict(arrowstyle='->', color='blue', alpha=0.7),
                fontsize=10, color='blue')
    
    # 3. Rank-deficient least squares
    # Create rank-deficient matrix
    A_rank = np.random.randn(15, 8)
    # Make it rank deficient by setting last columns as linear combinations
    A_rank[:, 6] = 2 * A_rank[:, 0] + A_rank[:, 1]
    A_rank[:, 7] = A_rank[:, 2] - A_rank[:, 3]
    
    b_rank = np.random.randn(15)
    
    # SVD analysis
    U, s, Vt = svd(A_rank)
    
    ax3.semilogy(range(1, len(s) + 1), s, 'bo-', linewidth=2, markersize=8, label='Singular values')
    ax3.axhline(y=1e-12, color='red', linestyle='--', linewidth=2, label='Machine precision threshold')
    
    # Identify numerical rank
    tol = 1e-12
    rank = np.sum(s > tol)
    ax3.axvline(x=rank + 0.5, color='green', linestyle=':', linewidth=2, label=f'Numerical rank = {rank}')
    
    ax3.set_xlabel('Index', fontsize=12)
    ax3.set_ylabel('Singular Value', fontsize=12)
    ax3.set_title('Singular Value Decomposition\nRank-Deficient Matrix Analysis', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # Add text with matrix properties
    ax3.text(0.02, 0.98, f'Matrix size: {A_rank.shape}\nTheoretical rank: 6\nNumerical rank: {rank}\nCondition number: {np.linalg.cond(A_rank):.2e}', 
             transform=ax3.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
    
    # 4. Regularization effects
    # Ridge regression comparison
    lambda_values = np.logspace(-6, 2, 50)
    solution_norms = []
    residual_norms_reg = []
    
    # Create ill-conditioned problem
    A_reg = np.random.randn(20, 10)
    U_reg, s_reg, Vt_reg = svd(A_reg)
    s_reg = np.logspace(0, -8, 10)  # Make ill-conditioned
    A_reg = U_reg[:, :10] @ np.diag(s_reg) @ Vt_reg
    
    x_true_reg = np.random.randn(10)
    b_reg = A_reg @ x_true_reg + 0.01 * np.random.randn(20)
    
    for lam in lambda_values:
        # Ridge regression: min ||Ax - b||² + λ||x||²
        A_aug = np.vstack([A_reg, np.sqrt(lam) * np.eye(10)])
        b_aug = np.hstack([b_reg, np.zeros(10)])
        
        x_ridge = np.linalg.lstsq(A_aug, b_aug, rcond=None)[0]
        
        solution_norms.append(np.linalg.norm(x_ridge))
        residual_norms_reg.append(np.linalg.norm(A_reg @ x_ridge - b_reg))
    
    ax4.loglog(lambda_values, solution_norms, 'b-', linewidth=2, label='||x||₂ (solution norm)')
    ax4.loglog(lambda_values, residual_norms_reg, 'r-', linewidth=2, label='||Ax - b||₂ (residual norm)')
    
    # Find L-curve corner (optimal regularization)
    curvature = []
    for i in range(1, len(lambda_values) - 1):
        # Approximate curvature
        x1, y1 = np.log(residual_norms_reg[i-1]), np.log(solution_norms[i-1])
        x2, y2 = np.log(residual_norms_reg[i]), np.log(solution_norms[i])
        x3, y3 = np.log(residual_norms_reg[i+1]), np.log(solution_norms[i+1])
        
        # Curvature approximation
        k = 2 * abs((x2-x1)*(y3-y1) - (y2-y1)*(x3-x1)) / ((x2-x1)**2 + (y2-y1)**2)**1.5
        curvature.append(k)
    
    optimal_idx = np.argmax(curvature) + 1
    optimal_lambda = lambda_values[optimal_idx]
    
    ax4.axvline(x=optimal_lambda, color='green', linestyle='--', linewidth=2, 
               label=f'Optimal λ = {optimal_lambda:.2e}')
    
    ax4.set_xlabel('Regularization Parameter λ', fontsize=12)
    ax4.set_ylabel('Norm', fontsize=12)
    ax4.set_title('Ridge Regression L-Curve\nRegularization Parameter Selection', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figures/applications_and_conditioning.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'polynomial_degrees': degrees,
        'condition_numbers': condition_numbers,
        'numerical_rank': rank,
        'optimal_lambda': optimal_lambda
    }

def create_computational_methods_comparison():
    """Create computational methods comparison"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Memory usage comparison
    matrix_sizes = np.array([100, 200, 500, 1000, 2000])
    
    # Memory for different methods (in MB)
    memory_normal = (matrix_sizes**2 * 8) / (1024**2)  # A^T A storage
    memory_qr_full = (matrix_sizes * matrix_sizes * 8) / (1024**2)  # Full Q matrix
    memory_qr_reduced = (matrix_sizes * matrix_sizes * 0.5 * 8) / (1024**2)  # Reduced QR
    memory_householder = (matrix_sizes * 100 * 8) / (1024**2)  # Only store Householder vectors
    
    ax1.loglog(matrix_sizes, memory_normal, 'r-o', linewidth=2, markersize=6, label='Normal equations (AᵀA)')
    ax1.loglog(matrix_sizes, memory_qr_full, 'b-s', linewidth=2, markersize=6, label='Full QR decomposition')
    ax1.loglog(matrix_sizes, memory_qr_reduced, 'g-^', linewidth=2, markersize=6, label='Reduced QR decomposition')
    ax1.loglog(matrix_sizes, memory_householder, 'm-d', linewidth=2, markersize=6, label='Householder vectors only')
    
    ax1.set_xlabel('Matrix Size n (square matrices)', fontsize=12)
    ax1.set_ylabel('Memory Usage (MB)', fontsize=12)
    ax1.set_title('Memory Requirements Comparison\nDifferent Least Squares Methods', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Add memory limit line
    ax1.axhline(y=1000, color='red', linestyle='--', alpha=0.7, label='1GB memory limit')
    
    # 2. Accuracy vs condition number
    condition_numbers = np.logspace(1, 14, 25)
    accuracies_normal = []
    accuracies_qr = []
    accuracies_svd = []
    
    for kappa in condition_numbers:
        # Create test problem
        U, _, Vt = svd(np.random.randn(50, 20))
        s = np.logspace(0, -np.log10(kappa), 20)
        A_test = U[:, :20] @ np.diag(s) @ Vt
        
        x_true = np.random.randn(20)
        b_test = A_test @ x_true
        b_noisy = b_test + 1e-14 * np.random.randn(50)
        
        # Normal equations
        try:
            x_normal = np.linalg.solve(A_test.T @ A_test, A_test.T @ b_noisy)
            acc_normal = -np.log10(np.linalg.norm(x_normal - x_true) / np.linalg.norm(x_true))
        except:
            acc_normal = 0
        
        # QR decomposition
        x_qr = np.linalg.lstsq(A_test, b_noisy, rcond=None)[0]
        acc_qr = -np.log10(np.linalg.norm(x_qr - x_true) / np.linalg.norm(x_true))
        
        # SVD (most stable)
        U_svd, s_svd, Vt_svd = svd(A_test, full_matrices=False)
        x_svd = Vt_svd.T @ (np.diag(1/s_svd) @ (U_svd.T @ b_noisy))
        acc_svd = -np.log10(np.linalg.norm(x_svd - x_true) / np.linalg.norm(x_true))
        
        accuracies_normal.append(max(0, acc_normal))
        accuracies_qr.append(max(0, acc_qr))
        accuracies_svd.append(max(0, acc_svd))
    
    ax2.semilogx(condition_numbers, accuracies_normal, 'r-o', linewidth=2, markersize=4, label='Normal equations')
    ax2.semilogx(condition_numbers, accuracies_qr, 'b-s', linewidth=2, markersize=4, label='QR decomposition')
    ax2.semilogx(condition_numbers, accuracies_svd, 'g-^', linewidth=2, markersize=4, label='SVD')
    
    # Theoretical limit
    theoretical_limit = 16 - np.log10(condition_numbers)
    ax2.semilogx(condition_numbers, np.maximum(0, theoretical_limit), 'k--', alpha=0.7, label='Theoretical limit')
    
    ax2.set_xlabel('Condition Number κ(A)', fontsize=12)
    ax2.set_ylabel('Digits of Accuracy', fontsize=12)
    ax2.set_title('Accuracy vs Conditioning\nMethod Comparison', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 16)
    
    # 3. Computational cost breakdown
    operations = ['Matrix multiply\n(AᵀA)', 'Cholesky\nfactorization', 'QR\ndecomposition', 'Back\nsubstitution', 'SVD\ndecomposition']
    costs_normal = [2, 1/3, 0, 1, 0]  # Relative costs (n³ units)
    costs_qr = [0, 0, 2, 1, 0]
    costs_svd = [0, 0, 0, 1, 4]
    
    x_pos = np.arange(len(operations))
    width = 0.25
    
    bars1 = ax3.bar(x_pos - width, costs_normal, width, label='Normal equations', color='red', alpha=0.7)
    bars2 = ax3.bar(x_pos, costs_qr, width, label='QR decomposition', color='blue', alpha=0.7)
    bars3 = ax3.bar(x_pos + width, costs_svd, width, label='SVD', color='green', alpha=0.7)
    
    ax3.set_xlabel('Operation', fontsize=12)
    ax3.set_ylabel('Relative Cost (n³ units)', fontsize=12)
    ax3.set_title('Computational Cost Breakdown\nOperation-by-Operation Analysis', fontsize=14, fontweight='bold')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(operations, fontsize=10)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Add total cost annotations
    total_normal = sum(costs_normal)
    total_qr = sum(costs_qr)
    total_svd = sum(costs_svd)
    
    ax3.text(0.02, 0.98, f'Total costs:\nNormal: {total_normal:.1f}n³\nQR: {total_qr:.1f}n³\nSVD: {total_svd:.1f}n³', 
             transform=ax3.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # 4. Parallel scalability
    num_cores = np.array([1, 2, 4, 8, 16, 32])
    
    # Theoretical speedup (Amdahl's law with different parallel fractions)
    parallel_fraction_normal = 0.7  # Matrix multiply is highly parallel
    parallel_fraction_qr = 0.6     # QR has some sequential parts
    parallel_fraction_svd = 0.8    # SVD is highly parallel
    
    speedup_normal = 1 / ((1 - parallel_fraction_normal) + parallel_fraction_normal / num_cores)
    speedup_qr = 1 / ((1 - parallel_fraction_qr) + parallel_fraction_qr / num_cores)
    speedup_svd = 1 / ((1 - parallel_fraction_svd) + parallel_fraction_svd / num_cores)
    
    ax4.plot(num_cores, speedup_normal, 'r-o', linewidth=2, markersize=6, label='Normal equations')
    ax4.plot(num_cores, speedup_qr, 'b-s', linewidth=2, markersize=6, label='QR decomposition')
    ax4.plot(num_cores, speedup_svd, 'g-^', linewidth=2, markersize=6, label='SVD')
    ax4.plot(num_cores, num_cores, 'k--', alpha=0.7, label='Perfect scaling')
    
    ax4.set_xlabel('Number of Cores', fontsize=12)
    ax4.set_ylabel('Speedup Factor', fontsize=12)
    ax4.set_title('Parallel Scalability\nAmdahl\'s Law Analysis', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(1, 32)
    ax4.set_ylim(1, 32)
    
    # Add efficiency annotations
    efficiency_32_normal = speedup_normal[-1] / 32 * 100
    efficiency_32_qr = speedup_qr[-1] / 32 * 100
    efficiency_32_svd = speedup_svd[-1] / 32 * 100
    
    ax4.text(0.02, 0.98, f'32-core efficiency:\nNormal: {efficiency_32_normal:.1f}%\nQR: {efficiency_32_qr:.1f}%\nSVD: {efficiency_32_svd:.1f}%', 
             transform=ax4.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('figures/computational_methods_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'memory_savings_qr': memory_qr_reduced[-1] / memory_normal[-1],
        'accuracy_improvement': np.mean(np.array(accuracies_qr) / np.maximum(np.array(accuracies_normal), 0.1)),
        'cost_comparison': (total_normal, total_qr, total_svd),
        'parallel_efficiency': (efficiency_32_normal, efficiency_32_qr, efficiency_32_svd)
    }

# Main execution
if __name__ == "__main__":
    print("Generating Lecture 6: Least Squares and QR Decomposition")
    print("=" * 60)
    
    # Create figures directory
    import os
    os.makedirs('figures', exist_ok=True)
    
    # Generate all figures and demonstrations
    print("✅ Generating comprehensive least squares analysis...")
    results1 = create_least_squares_comprehensive_figure()
    
    print("✅ Generating QR algorithms comparison...")
    results2 = create_qr_algorithms_comparison()
    
    print("✅ Generating applications and conditioning analysis...")
    results3 = create_applications_and_conditioning()
    
    print("✅ Generating computational methods comparison...")
    results4 = create_computational_methods_comparison()
    
    print("=" * 60)
    print("LEAST SQUARES AND QR DECOMPOSITION ANALYSIS")
    print("=" * 60)
    
    print(f"📊 Least Squares Problem Analysis:")
    print(f"   • Data fitting condition number: {results1['condition_number']:.2f}")
    print(f"   • Residual norm: {results1['residual_norm']:.3f}")
    print(f"   • Stability improvement (QR vs Normal): {results1['stability_improvement']:.1f}×")
    
    print(f"\n🔧 QR Algorithm Comparison:")
    print(f"   • Orthogonality improvement (Householder vs CGS): {results2['orthogonality_improvement']:.1e}×")
    print(f"   • Householder matrix condition: {np.linalg.cond(results2['householder_matrix']):.2f}")
    
    print(f"\n📈 Applications and Conditioning:")
    print(f"   • Polynomial fitting degrees tested: {results3['polynomial_degrees']}")
    print(f"   • Highest condition number: {max(results3['condition_numbers']):.2e}")
    print(f"   • Numerical rank detection: {results3['numerical_rank']}")
    print(f"   • Optimal regularization parameter: {results3['optimal_lambda']:.2e}")
    
    print(f"\n⚡ Computational Performance:")
    print(f"   • Memory savings (QR vs Normal): {results4['memory_savings_qr']:.1f}×")
    print(f"   • Accuracy improvement: {results4['accuracy_improvement']:.1f}×")
    print(f"   • Cost comparison (Normal/QR/SVD): {results4['cost_comparison']}")
    print(f"   • 32-core parallel efficiency: {results4['parallel_efficiency']}")
    
    print("=" * 60)
    print("✅ ALL FIGURES AND DEMONSTRATIONS COMPLETED")
    print("=" * 60)
    print("Generated files:")
    print("- figures/least_squares_comprehensive.png")
    print("- figures/qr_algorithms_comparison.png") 
    print("- figures/applications_and_conditioning.png")
    print("- figures/computational_methods_comparison.png")
    
    print("\nKey Educational Results:")
    print("- Geometric interpretation of least squares projection")
    print("- QR decomposition stability advantages over normal equations")
    print("- Householder reflections provide optimal numerical stability")
    print("- Condition number effects on accuracy and method selection")
    print("- Trade-offs between computational cost and numerical stability")
    print("- Applications to polynomial fitting and regularization")
