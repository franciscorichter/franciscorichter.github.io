"""
Lecture 5: Direct Methods for Linear Systems
Educational Python Code with Comprehensive Demonstrations

Topics Covered:
1. Gaussian Elimination and LU Decomposition
2. Pivoting Strategies (Partial and Complete)
3. Cholesky Decomposition
4. Stability Analysis and Growth Factors
5. Special Matrix Structures (Tridiagonal, Band)
6. Iterative Refinement

Author: Francisco Richter Mendoza
Course: Numerical Computing
Institution: Università della Svizzera Italiana
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.linalg import lu, cholesky, solve_triangular, lu_factor, lu_solve
from scipy.sparse import diags
import warnings
warnings.filterwarnings('ignore')

# Set style for professional plots
plt.style.use('default')
sns.set_palette("husl")

def create_direct_methods_figures():
    """Generate comprehensive figures for direct methods lecture"""
    
    # Create figure with 4 subplots
    fig = plt.figure(figsize=(16, 12))
    
    # Figure 1: LU Decomposition Process Visualization
    ax1 = plt.subplot(2, 2, 1)
    
    # Create a sample matrix for LU decomposition
    np.random.seed(42)
    A = np.array([[4, 3, 2], [3, 4, 1], [2, 1, 3]], dtype=float)
    
    # Perform LU decomposition
    P, L, U = lu(A)
    
    # Create visualization of LU decomposition
    matrices = [A, L, U, L @ U]
    titles = ['Original Matrix A', 'Lower L', 'Upper U', 'Reconstruction L×U']
    
    for i, (matrix, title) in enumerate(zip(matrices, titles)):
        ax_sub = plt.subplot(4, 4, i + 1)
        im = ax_sub.imshow(matrix, cmap='RdBu_r', aspect='equal')
        ax_sub.set_title(title, fontsize=10, fontweight='bold')
        
        # Add numerical values
        for row in range(matrix.shape[0]):
            for col in range(matrix.shape[1]):
                ax_sub.text(col, row, f'{matrix[row, col]:.2f}', 
                           ha='center', va='center', fontweight='bold')
        
        ax_sub.set_xticks([])
        ax_sub.set_yticks([])
        plt.colorbar(im, ax=ax_sub, shrink=0.6)
    
    ax1.text(0.5, 0.95, 'LU Decomposition: A = L × U', 
             transform=ax1.transAxes, ha='center', va='top',
             fontsize=14, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    ax1.axis('off')
    
    # Figure 2: Pivoting Strategy Comparison
    ax2 = plt.subplot(2, 2, 2)
    
    # Create matrices that demonstrate pivoting benefits
    sizes = np.arange(3, 21)
    growth_no_pivot = []
    growth_partial_pivot = []
    
    for n in sizes:
        # Create a matrix that grows exponentially without pivoting
        A_bad = np.ones((n, n))
        A_bad[np.tril_indices(n, -1)] = -1
        A_bad[np.diag_indices(n)] = 1
        
        # Compute growth factors
        try:
            # Without pivoting (theoretical worst case)
            growth_no_pivot.append(2**(n-1))
            
            # With partial pivoting (empirical)
            P, L, U = lu(A_bad)
            growth_partial_pivot.append(np.max(np.abs(U)) / np.max(np.abs(A_bad)))
        except:
            growth_no_pivot.append(np.nan)
            growth_partial_pivot.append(np.nan)
    
    ax2.semilogy(sizes, growth_no_pivot, 'r-o', label='No Pivoting (Worst Case)', linewidth=2, markersize=6)
    ax2.semilogy(sizes, growth_partial_pivot, 'b-s', label='Partial Pivoting', linewidth=2, markersize=6)
    ax2.set_xlabel('Matrix Size n', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Growth Factor', fontsize=12, fontweight='bold')
    ax2.set_title('Growth Factor Comparison:\nPivoting vs No Pivoting', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # Add annotations
    ax2.annotate('Exponential Growth\nwithout Pivoting', 
                xy=(15, 2**14), xytext=(12, 1e6),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=11, fontweight='bold', color='red')
    ax2.annotate('Controlled Growth\nwith Pivoting', 
                xy=(18, growth_partial_pivot[-3]), xytext=(15, 1e2),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                fontsize=11, fontweight='bold', color='blue')
    
    # Figure 3: Cholesky vs LU Efficiency
    ax3 = plt.subplot(2, 2, 3)
    
    sizes = np.logspace(1, 3, 20).astype(int)
    cholesky_ops = []
    lu_ops = []
    
    for n in sizes:
        # Theoretical operation counts
        cholesky_ops.append(n**3 / 3)
        lu_ops.append(2 * n**3 / 3)
    
    ax3.loglog(sizes, cholesky_ops, 'g-o', label='Cholesky: n³/3', linewidth=3, markersize=8)
    ax3.loglog(sizes, lu_ops, 'r-s', label='LU: 2n³/3', linewidth=3, markersize=8)
    ax3.set_xlabel('Matrix Size n', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Operation Count', fontsize=12, fontweight='bold')
    ax3.set_title('Computational Complexity:\nCholesky vs LU Decomposition', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=12)
    ax3.grid(True, alpha=0.3)
    
    # Add efficiency annotation
    ax3.text(0.6, 0.3, 'Cholesky is 2× faster\nfor SPD matrices', 
             transform=ax3.transAxes, fontsize=12, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.8))
    
    # Figure 4: Condition Number and Stability
    ax4 = plt.subplot(2, 2, 4)
    
    # Generate matrices with different condition numbers
    condition_numbers = np.logspace(1, 12, 50)
    relative_errors = []
    
    np.random.seed(123)
    for kappa in condition_numbers:
        # Create matrix with specified condition number
        n = 10
        U, _, Vt = np.linalg.svd(np.random.randn(n, n))
        s = np.logspace(0, -np.log10(kappa), n)
        A = U @ np.diag(s) @ Vt
        
        # True solution
        x_true = np.random.randn(n)
        b = A @ x_true
        
        # Solve with LU
        try:
            x_computed = np.linalg.solve(A, b)
            rel_error = np.linalg.norm(x_computed - x_true) / np.linalg.norm(x_true)
            relative_errors.append(rel_error)
        except:
            relative_errors.append(np.nan)
    
    # Theoretical bound
    machine_eps = np.finfo(float).eps
    theoretical_bound = condition_numbers * machine_eps
    
    ax4.loglog(condition_numbers, relative_errors, 'bo', alpha=0.7, markersize=6, label='Computed Error')
    ax4.loglog(condition_numbers, theoretical_bound, 'r--', linewidth=3, label='Theoretical Bound: κ(A)εₘₐₓ')
    ax4.set_xlabel('Condition Number κ(A)', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Relative Error', fontsize=12, fontweight='bold')
    ax4.set_title('Error vs Condition Number:\nStability Analysis', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=11)
    ax4.grid(True, alpha=0.3)
    
    # Add stability regions
    ax4.axvline(x=1e12, color='orange', linestyle=':', linewidth=2, alpha=0.8)
    ax4.text(1e13, 1e-10, 'Ill-conditioned\nRegion', fontsize=11, fontweight='bold', 
             color='orange', rotation=90, va='center')
    
    plt.tight_layout()
    plt.savefig('figures/direct_methods_comprehensive.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Generated: direct_methods_comprehensive.png")

def create_special_structures_figure():
    """Generate figure showing special matrix structures and their properties"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Figure 1: Tridiagonal Matrix Structure
    ax1 = axes[0, 0]
    
    n = 8
    # Create tridiagonal matrix
    a = np.ones(n-1) * (-1)  # sub-diagonal
    b = np.ones(n) * 2       # diagonal
    c = np.ones(n-1) * (-1)  # super-diagonal
    
    A_tri = diags([a, b, c], [-1, 0, 1], shape=(n, n)).toarray()
    
    im1 = ax1.imshow(A_tri, cmap='RdBu_r', aspect='equal')
    ax1.set_title('Tridiagonal Matrix Structure\n(Bandwidth = 3)', fontsize=14, fontweight='bold')
    
    # Highlight the band structure
    for i in range(n):
        for j in range(n):
            if abs(i - j) <= 1:
                ax1.add_patch(plt.Rectangle((j-0.4, i-0.4), 0.8, 0.8, 
                                          fill=False, edgecolor='black', linewidth=2))
    
    ax1.set_xticks(range(n))
    ax1.set_yticks(range(n))
    plt.colorbar(im1, ax=ax1, shrink=0.8)
    
    # Add complexity annotation
    ax1.text(0.5, -0.15, f'Thomas Algorithm: O(n) operations\nStandard LU: O(n³) operations', 
             transform=ax1.transAxes, ha='center', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
    
    # Figure 2: Band Matrix Visualization
    ax2 = axes[0, 1]
    
    n = 10
    bandwidth = 3
    A_band = np.zeros((n, n))
    
    for i in range(n):
        for j in range(max(0, i-bandwidth), min(n, i+bandwidth+1)):
            A_band[i, j] = np.random.randn() * np.exp(-abs(i-j))
    
    im2 = ax2.imshow(A_band, cmap='RdBu_r', aspect='equal')
    ax2.set_title(f'Band Matrix\n(Bandwidth = {2*bandwidth+1})', fontsize=14, fontweight='bold')
    
    # Highlight band structure
    for i in range(n):
        for j in range(n):
            if abs(i - j) <= bandwidth:
                ax2.add_patch(plt.Rectangle((j-0.4, i-0.4), 0.8, 0.8, 
                                          fill=False, edgecolor='red', linewidth=1.5))
    
    ax2.set_xticks(range(n))
    ax2.set_yticks(range(n))
    plt.colorbar(im2, ax=ax2, shrink=0.8)
    
    # Add complexity annotation
    ax2.text(0.5, -0.15, f'Band LU: O(n·p²) operations\np = bandwidth', 
             transform=ax2.transAxes, ha='center', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcyan"))
    
    # Figure 3: Cholesky Decomposition Visualization
    ax3 = axes[1, 0]
    
    # Create symmetric positive definite matrix
    np.random.seed(42)
    n = 6
    A_temp = np.random.randn(n, n)
    A_spd = A_temp @ A_temp.T + np.eye(n)  # Ensure SPD
    
    # Compute Cholesky decomposition
    L_chol = cholesky(A_spd, lower=True)
    
    # Create side-by-side visualization
    combined = np.zeros((n, 2*n + 1))
    combined[:, :n] = A_spd
    combined[:, n+1:] = L_chol @ L_chol.T
    
    im3 = ax3.imshow(combined, cmap='RdBu_r', aspect='equal')
    ax3.set_title('Cholesky Decomposition: A = L·Lᵀ', fontsize=14, fontweight='bold')
    
    # Add separator line
    ax3.axvline(x=n-0.5, color='black', linewidth=3)
    
    # Add labels
    ax3.text(n/2-0.5, -0.8, 'Original A\n(SPD)', ha='center', fontsize=12, fontweight='bold')
    ax3.text(1.5*n, -0.8, 'Reconstructed\nL·Lᵀ', ha='center', fontsize=12, fontweight='bold')
    
    ax3.set_xticks([])
    ax3.set_yticks([])
    plt.colorbar(im3, ax=ax3, shrink=0.8)
    
    # Figure 4: Iterative Refinement Convergence
    ax4 = axes[1, 1]
    
    # Simulate iterative refinement for different condition numbers
    condition_numbers = [1e2, 1e6, 1e10, 1e14]
    colors = ['green', 'blue', 'orange', 'red']
    
    for i, kappa in enumerate(condition_numbers):
        # Create matrix with specified condition number
        n = 10
        U, _, Vt = np.linalg.svd(np.random.randn(n, n))
        s = np.logspace(0, -np.log10(kappa), n)
        A = U @ np.diag(s) @ Vt
        
        # True solution and RHS
        x_true = np.ones(n)
        b = A @ x_true
        
        # Initial solution (with some error)
        x = np.linalg.solve(A, b) + 1e-10 * np.random.randn(n)
        
        errors = []
        for iteration in range(10):
            residual = b - A @ x
            correction = np.linalg.solve(A, residual)
            x = x + correction
            
            error = np.linalg.norm(x - x_true) / np.linalg.norm(x_true)
            errors.append(error)
            
            if error < 1e-15:
                break
        
        iterations = range(len(errors))
        ax4.semilogy(iterations, errors, 'o-', color=colors[i], linewidth=2, 
                    markersize=6, label=f'κ = {kappa:.0e}')
    
    ax4.set_xlabel('Iteration', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Relative Error', fontsize=12, fontweight='bold')
    ax4.set_title('Iterative Refinement Convergence', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    # Add convergence annotation
    ax4.axhline(y=np.finfo(float).eps, color='gray', linestyle='--', alpha=0.7)
    ax4.text(0.6, 0.8, 'Machine Precision', transform=ax4.transAxes, 
             fontsize=10, color='gray', rotation=0)
    
    plt.tight_layout()
    plt.savefig('figures/special_matrix_structures.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Generated: special_matrix_structures.png")

def create_stability_analysis_figure():
    """Generate comprehensive stability analysis visualization"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Figure 1: Growth Factor Analysis
    ax1 = axes[0, 0]
    
    # Compare different matrix types
    sizes = np.arange(5, 31, 2)
    
    # Random matrices
    growth_random = []
    # Hilbert matrices  
    growth_hilbert = []
    # Worst-case matrices
    growth_worst = []
    
    np.random.seed(42)
    for n in sizes:
        # Random matrix
        A_rand = np.random.randn(n, n)
        P, L, U = lu(A_rand)
        growth_random.append(np.max(np.abs(U)) / np.max(np.abs(A_rand)))
        
        # Hilbert matrix
        A_hilb = np.array([[1/(i+j+1) for j in range(n)] for i in range(n)])
        try:
            P, L, U = lu(A_hilb)
            growth_hilbert.append(np.max(np.abs(U)) / np.max(np.abs(A_hilb)))
        except:
            growth_hilbert.append(np.nan)
        
        # Worst-case matrix (exponential growth)
        growth_worst.append(2**(n-1))
    
    ax1.semilogy(sizes, growth_random, 'b-o', label='Random Matrices', linewidth=2, markersize=6)
    ax1.semilogy(sizes, growth_hilbert, 'g-s', label='Hilbert Matrices', linewidth=2, markersize=6)
    ax1.semilogy(sizes, growth_worst, 'r--', label='Worst Case (Theoretical)', linewidth=2, alpha=0.7)
    
    ax1.set_xlabel('Matrix Size n', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Growth Factor ρ', fontsize=12, fontweight='bold')
    ax1.set_title('Growth Factor Analysis:\nDifferent Matrix Types', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Add stability threshold
    ax1.axhline(y=1e12, color='orange', linestyle=':', linewidth=2, alpha=0.8)
    ax1.text(0.7, 0.8, 'Stability\nThreshold', transform=ax1.transAxes, 
             fontsize=11, fontweight='bold', color='orange')
    
    # Figure 2: Backward Error Analysis
    ax2 = axes[0, 1]
    
    # Simulate backward errors for different algorithms
    condition_numbers = np.logspace(1, 14, 30)
    
    # Gaussian elimination with partial pivoting
    backward_errors_gepp = condition_numbers * np.finfo(float).eps * 10
    
    # Gaussian elimination without pivoting (unstable)
    backward_errors_ge = condition_numbers**1.5 * np.finfo(float).eps * 100
    
    # Cholesky (for SPD matrices)
    backward_errors_chol = condition_numbers * np.finfo(float).eps * 5
    
    ax2.loglog(condition_numbers, backward_errors_gepp, 'b-', linewidth=3, 
              label='GE with Partial Pivoting')
    ax2.loglog(condition_numbers, backward_errors_ge, 'r--', linewidth=3, 
              label='GE without Pivoting')
    ax2.loglog(condition_numbers, backward_errors_chol, 'g-', linewidth=3, 
              label='Cholesky Decomposition')
    
    # Machine precision line
    ax2.axhline(y=np.finfo(float).eps, color='gray', linestyle=':', linewidth=2)
    ax2.text(1e2, 2*np.finfo(float).eps, 'Machine Precision', fontsize=10, color='gray')
    
    ax2.set_xlabel('Condition Number κ(A)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Backward Error ||ΔA||/||A||', fontsize=12, fontweight='bold')
    ax2.set_title('Backward Error Analysis:\nAlgorithm Comparison', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # Figure 3: Forward Error vs Condition Number
    ax3 = axes[1, 0]
    
    # Generate data for forward error analysis
    kappa_values = np.logspace(1, 15, 50)
    forward_errors = []
    
    np.random.seed(123)
    for kappa in kappa_values:
        n = 8
        # Create matrix with specified condition number
        U, _, Vt = np.linalg.svd(np.random.randn(n, n))
        s = np.logspace(0, -np.log10(kappa), n)
        A = U @ np.diag(s) @ Vt
        
        # Solve system multiple times and average error
        errors = []
        for _ in range(5):
            x_true = np.random.randn(n)
            b = A @ x_true
            
            try:
                x_computed = np.linalg.solve(A, b)
                error = np.linalg.norm(x_computed - x_true) / np.linalg.norm(x_true)
                errors.append(error)
            except:
                errors.append(np.nan)
        
        forward_errors.append(np.nanmean(errors))
    
    # Theoretical bounds
    theoretical_bound = kappa_values * np.finfo(float).eps
    
    ax3.loglog(kappa_values, forward_errors, 'bo', alpha=0.6, markersize=5, label='Computed Errors')
    ax3.loglog(kappa_values, theoretical_bound, 'r-', linewidth=3, label='Theoretical Bound')
    
    ax3.set_xlabel('Condition Number κ(A)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Relative Forward Error', fontsize=12, fontweight='bold')
    ax3.set_title('Forward Error Analysis:\nTheory vs Practice', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=11)
    ax3.grid(True, alpha=0.3)
    
    # Add conditioning regions
    ax3.axvspan(1, 1e3, alpha=0.2, color='green', label='Well-conditioned')
    ax3.axvspan(1e3, 1e12, alpha=0.2, color='yellow', label='Moderately conditioned')
    ax3.axvspan(1e12, 1e15, alpha=0.2, color='red', label='Ill-conditioned')
    
    # Figure 4: Residual vs Error Relationship
    ax4 = axes[1, 1]
    
    # Generate matrices with different properties
    n = 10
    residuals = []
    errors = []
    condition_numbers_scatter = []
    
    np.random.seed(456)
    for _ in range(100):
        # Random condition number
        kappa = 10**np.random.uniform(1, 12)
        
        # Create matrix
        U, _, Vt = np.linalg.svd(np.random.randn(n, n))
        s = np.logspace(0, -np.log10(kappa), n)
        A = U @ np.diag(s) @ Vt
        
        # True solution and solve
        x_true = np.random.randn(n)
        b = A @ x_true
        
        try:
            x_computed = np.linalg.solve(A, b)
            
            # Compute residual and error
            residual = np.linalg.norm(b - A @ x_computed) / np.linalg.norm(b)
            error = np.linalg.norm(x_computed - x_true) / np.linalg.norm(x_true)
            
            residuals.append(residual)
            errors.append(error)
            condition_numbers_scatter.append(kappa)
        except:
            continue
    
    # Color by condition number
    scatter = ax4.scatter(residuals, errors, c=np.log10(condition_numbers_scatter), 
                         cmap='viridis', alpha=0.7, s=50)
    
    # Add diagonal lines showing relationship
    res_range = np.logspace(-16, -1, 100)
    ax4.loglog(res_range, res_range, 'k--', alpha=0.5, label='Error = Residual')
    ax4.loglog(res_range, res_range * 1e12, 'r--', alpha=0.5, label='Error = κ(A) × Residual')
    
    ax4.set_xlabel('Relative Residual ||b - Ax̃||/||b||', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Relative Error ||x̃ - x||/||x||', fontsize=12, fontweight='bold')
    ax4.set_title('Residual vs Error Relationship', fontsize=14, fontweight='bold')
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax4)
    cbar.set_label('log₁₀(κ(A))', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/stability_analysis_comprehensive.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Generated: stability_analysis_comprehensive.png")

def create_computational_complexity_figure():
    """Generate computational complexity comparison figure"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Figure 1: Operation Count Comparison
    ax1 = axes[0, 0]
    
    sizes = np.logspace(1, 3.5, 30).astype(int)
    
    # Different algorithms
    dense_lu = 2 * sizes**3 / 3
    cholesky = sizes**3 / 3
    tridiagonal = 5 * sizes
    band_width_5 = sizes * 25  # bandwidth = 5
    
    ax1.loglog(sizes, dense_lu, 'r-', linewidth=3, label='Dense LU: 2n³/3')
    ax1.loglog(sizes, cholesky, 'g-', linewidth=3, label='Cholesky: n³/3')
    ax1.loglog(sizes, band_width_5, 'b-', linewidth=3, label='Band (p=5): 25n')
    ax1.loglog(sizes, tridiagonal, 'm-', linewidth=3, label='Tridiagonal: 5n')
    
    ax1.set_xlabel('Matrix Size n', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Operation Count', fontsize=12, fontweight='bold')
    ax1.set_title('Computational Complexity:\nDifferent Matrix Types', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Add complexity annotations
    ax1.text(0.7, 0.8, 'O(n³)', transform=ax1.transAxes, fontsize=12, 
             fontweight='bold', color='red')
    ax1.text(0.7, 0.6, 'O(n³)', transform=ax1.transAxes, fontsize=12, 
             fontweight='bold', color='green')
    ax1.text(0.7, 0.4, 'O(n)', transform=ax1.transAxes, fontsize=12, 
             fontweight='bold', color='blue')
    ax1.text(0.7, 0.2, 'O(n)', transform=ax1.transAxes, fontsize=12, 
             fontweight='bold', color='magenta')
    
    # Figure 2: Memory Requirements
    ax2 = axes[0, 1]
    
    # Memory requirements for different storage schemes
    dense_memory = sizes**2
    band_memory = sizes * 11  # bandwidth = 5, so 2*5+1 = 11 diagonals
    tridiagonal_memory = 3 * sizes
    
    ax2.loglog(sizes, dense_memory, 'r-', linewidth=3, label='Dense: n²')
    ax2.loglog(sizes, band_memory, 'b-', linewidth=3, label='Band: (2p+1)n')
    ax2.loglog(sizes, tridiagonal_memory, 'm-', linewidth=3, label='Tridiagonal: 3n')
    
    ax2.set_xlabel('Matrix Size n', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Memory Requirements', fontsize=12, fontweight='bold')
    ax2.set_title('Memory Usage:\nStorage Schemes', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # Figure 3: Timing Comparison (Simulated)
    ax3 = axes[1, 0]
    
    # Simulate timing data
    sizes_timing = np.array([10, 20, 50, 100, 200, 500, 1000])
    
    # Simulated timings (normalized)
    dense_times = (sizes_timing/10)**3 * 0.001
    cholesky_times = (sizes_timing/10)**3 * 0.0005
    band_times = (sizes_timing/10) * 0.01
    tridiagonal_times = (sizes_timing/10) * 0.001
    
    ax3.loglog(sizes_timing, dense_times, 'ro-', linewidth=2, markersize=8, label='Dense LU')
    ax3.loglog(sizes_timing, cholesky_times, 'go-', linewidth=2, markersize=8, label='Cholesky')
    ax3.loglog(sizes_timing, band_times, 'bo-', linewidth=2, markersize=8, label='Band Matrix')
    ax3.loglog(sizes_timing, tridiagonal_times, 'mo-', linewidth=2, markersize=8, label='Tridiagonal')
    
    ax3.set_xlabel('Matrix Size n', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
    ax3.set_title('Performance Comparison:\nExecution Times', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=11)
    ax3.grid(True, alpha=0.3)
    
    # Figure 4: Scalability Analysis
    ax4 = axes[1, 1]
    
    # Show how different methods scale
    problem_sizes = np.array([100, 1000, 10000])
    methods = ['Dense LU', 'Cholesky', 'Band (p=10)', 'Tridiagonal']
    
    # Relative times (normalized to smallest problem)
    times_100 = np.array([1, 0.5, 0.1, 0.01])
    times_1000 = np.array([1000, 500, 10, 0.1])
    times_10000 = np.array([1e6, 5e5, 100, 1])
    
    x = np.arange(len(methods))
    width = 0.25
    
    bars1 = ax4.bar(x - width, times_100, width, label='n = 100', alpha=0.8)
    bars2 = ax4.bar(x, times_1000, width, label='n = 1,000', alpha=0.8)
    bars3 = ax4.bar(x + width, times_10000, width, label='n = 10,000', alpha=0.8)
    
    ax4.set_yscale('log')
    ax4.set_xlabel('Method', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Relative Time', fontsize=12, fontweight='bold')
    ax4.set_title('Scalability Analysis:\nRelative Performance', fontsize=14, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(methods, rotation=45, ha='right')
    ax4.legend(fontsize=11)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax4.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.0e}' if height >= 1000 else f'{height:.2f}',
                        ha='center', va='bottom', fontsize=8, rotation=90)
    
    plt.tight_layout()
    plt.savefig('figures/computational_complexity_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Generated: computational_complexity_analysis.png")

def demonstrate_thomas_algorithm():
    """Demonstrate Thomas algorithm for tridiagonal systems"""
    
    print("\n" + "="*60)
    print("THOMAS ALGORITHM DEMONSTRATION")
    print("="*60)
    
    # Create a tridiagonal system
    n = 6
    a = np.array([0, -1, -1, -1, -1, -1])  # sub-diagonal (first element unused)
    b = np.array([2, 2, 2, 2, 2, 2])      # diagonal
    c = np.array([-1, -1, -1, -1, -1, 0]) # super-diagonal (last element unused)
    
    # Right-hand side
    d = np.array([1, 1, 1, 1, 1, 1])
    
    print(f"Solving tridiagonal system of size {n}x{n}")
    print(f"Sub-diagonal: {a[1:]}")
    print(f"Diagonal:     {b}")
    print(f"Super-diagonal: {c[:-1]}")
    print(f"RHS:          {d}")
    
    # Thomas algorithm implementation
    def thomas_algorithm(a, b, c, d):
        n = len(d)
        
        # Forward elimination
        c_prime = np.zeros(n-1)
        d_prime = np.zeros(n)
        
        c_prime[0] = c[0] / b[0]
        d_prime[0] = d[0] / b[0]
        
        for i in range(1, n-1):
            c_prime[i] = c[i] / (b[i] - a[i] * c_prime[i-1])
        
        for i in range(1, n):
            d_prime[i] = (d[i] - a[i] * d_prime[i-1]) / (b[i] - a[i] * c_prime[i-1])
        
        # Back substitution
        x = np.zeros(n)
        x[n-1] = d_prime[n-1]
        
        for i in range(n-2, -1, -1):
            x[i] = d_prime[i] - c_prime[i] * x[i+1]
        
        return x
    
    # Solve using Thomas algorithm
    x_thomas = thomas_algorithm(a, b, c, d)
    
    # Verify using scipy
    A_full = diags([a[1:], b, c[:-1]], [-1, 0, 1], shape=(n, n)).toarray()
    x_scipy = np.linalg.solve(A_full, d)
    
    print(f"\nSolution (Thomas):  {x_thomas}")
    print(f"Solution (SciPy):   {x_scipy}")
    print(f"Difference:         {np.abs(x_thomas - x_scipy)}")
    print(f"Max difference:     {np.max(np.abs(x_thomas - x_scipy)):.2e}")
    
    # Verify solution
    residual = A_full @ x_thomas - d
    print(f"Residual norm:      {np.linalg.norm(residual):.2e}")
    
    return x_thomas, x_scipy

def demonstrate_iterative_refinement():
    """Demonstrate iterative refinement process"""
    
    print("\n" + "="*60)
    print("ITERATIVE REFINEMENT DEMONSTRATION")
    print("="*60)
    
    # Create an ill-conditioned system
    n = 8
    np.random.seed(42)
    
    # Create matrix with specified condition number
    kappa = 1e8
    U, _, Vt = np.linalg.svd(np.random.randn(n, n))
    s = np.logspace(0, -np.log10(kappa), n)
    A = U @ np.diag(s) @ Vt
    
    print(f"Matrix size: {n}x{n}")
    print(f"Condition number: {np.linalg.cond(A):.2e}")
    
    # True solution and RHS
    x_true = np.ones(n)
    b = A @ x_true
    
    # Initial solution (standard solve)
    x = np.linalg.solve(A, b)
    
    print(f"\nInitial relative error: {np.linalg.norm(x - x_true)/np.linalg.norm(x_true):.2e}")
    
    # Iterative refinement
    print("\nIterative Refinement Process:")
    print("Iter  Residual Norm    Relative Error")
    print("-" * 40)
    
    for iteration in range(8):
        # Compute residual
        residual = b - A @ x
        residual_norm = np.linalg.norm(residual)
        
        # Compute relative error
        rel_error = np.linalg.norm(x - x_true) / np.linalg.norm(x_true)
        
        print(f"{iteration:2d}    {residual_norm:.2e}      {rel_error:.2e}")
        
        # Check convergence
        if residual_norm < 1e-14:
            break
        
        # Solve correction equation
        try:
            correction = np.linalg.solve(A, residual)
            x = x + correction
        except:
            print("Refinement failed - matrix too ill-conditioned")
            break
    
    print(f"\nFinal relative error: {np.linalg.norm(x - x_true)/np.linalg.norm(x_true):.2e}")
    
    return x, x_true

if __name__ == "__main__":
    print("Generating Lecture 5: Direct Methods for Linear Systems")
    print("=" * 60)
    
    # Create figures directory
    import os
    os.makedirs('figures', exist_ok=True)
    
    # Generate all figures
    create_direct_methods_figures()
    create_special_structures_figure()
    create_stability_analysis_figure()
    create_computational_complexity_figure()
    
    # Run demonstrations
    demonstrate_thomas_algorithm()
    demonstrate_iterative_refinement()
    
    print("\n" + "="*60)
    print("✅ ALL FIGURES AND DEMONSTRATIONS COMPLETED")
    print("="*60)
    print("\nGenerated files:")
    print("- figures/direct_methods_comprehensive.png")
    print("- figures/special_matrix_structures.png") 
    print("- figures/stability_analysis_comprehensive.png")
    print("- figures/computational_complexity_analysis.png")
    print("\nKey Educational Results:")
    print("- LU decomposition visualization with numerical values")
    print("- Growth factor comparison: exponential vs controlled")
    print("- Cholesky efficiency: 2× faster than LU for SPD matrices")
    print("- Thomas algorithm: O(n) vs O(n³) for tridiagonal systems")
    print("- Iterative refinement convergence analysis")
    print("- Stability analysis across different condition numbers")
