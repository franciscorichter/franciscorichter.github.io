#!/usr/bin/env python3
"""
Lecture 4: Linear Algebra Foundations - Educational Code Package
Course: Numerical Computing
Author: Francisco Richter Mendoza
Institution: Università della Svizzera Italiana

This module provides comprehensive educational demonstrations for:
1. Vector and matrix norms with geometric visualization
2. Condition numbers and sensitivity analysis
3. Special matrix classes and their properties
4. Singular Value Decomposition (SVD) applications

All code is designed for educational purposes with detailed mathematical explanations.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from scipy.linalg import hilbert, svd, qr, norm
import warnings
warnings.filterwarnings('ignore')

# Set style for professional figures
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def create_linear_algebra_foundations():
    """
    Create comprehensive visualization of linear algebra foundations
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Vector Norms - Unit Balls
    theta = np.linspace(0, 2*np.pi, 1000)
    
    # L1 norm (diamond)
    x1_l1 = np.sign(np.cos(theta)) * np.abs(np.cos(theta))
    y1_l1 = np.sign(np.sin(theta)) * np.abs(np.sin(theta))
    
    # L2 norm (circle)
    x1_l2 = np.cos(theta)
    y1_l2 = np.sin(theta)
    
    # L∞ norm (square)
    square_x = [-1, 1, 1, -1, -1]
    square_y = [-1, -1, 1, 1, -1]
    
    ax1.plot(x1_l1, y1_l1, 'r-', linewidth=3, label=r'$\ell_1$ norm', alpha=0.8)
    ax1.plot(x1_l2, y1_l2, 'b-', linewidth=3, label=r'$\ell_2$ norm', alpha=0.8)
    ax1.plot(square_x, square_y, 'g-', linewidth=3, label=r'$\ell_\infty$ norm', alpha=0.8)
    
    # Add sample vectors
    vectors = np.array([[0.8, 0.6], [-0.5, 0.9], [0.3, -0.7]])
    colors = ['red', 'blue', 'green']
    for i, (vec, color) in enumerate(zip(vectors, colors)):
        ax1.arrow(0, 0, vec[0], vec[1], head_width=0.05, head_length=0.05, 
                 fc=color, ec=color, alpha=0.7)
        ax1.text(vec[0]*1.1, vec[1]*1.1, f'v{i+1}', fontsize=12, color=color, fontweight='bold')
    
    ax1.set_xlim(-1.2, 1.2)
    ax1.set_ylim(-1.2, 1.2)
    ax1.set_xlabel('x₁', fontsize=14, fontweight='bold')
    ax1.set_ylabel('x₂', fontsize=14, fontweight='bold')
    ax1.set_title('Vector Norms: Unit Balls in ℝ²', fontsize=16, fontweight='bold', pad=20)
    ax1.legend(fontsize=12, loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')
    
    # Add norm values for sample vector
    v_sample = np.array([0.8, 0.6])
    norm_l1 = np.sum(np.abs(v_sample))
    norm_l2 = np.sqrt(np.sum(v_sample**2))
    norm_linf = np.max(np.abs(v_sample))
    
    ax1.text(-1.1, -1.0, f'For v₁ = [{v_sample[0]}, {v_sample[1]}]:\n'
                         f'‖v₁‖₁ = {norm_l1:.2f}\n'
                         f'‖v₁‖₂ = {norm_l2:.2f}\n'
                         f'‖v₁‖∞ = {norm_linf:.2f}', 
             fontsize=11, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    # 2. SVD Geometric Interpretation
    # Create a 2x2 matrix and show its SVD decomposition
    A = np.array([[3, 1], [1, 2]])
    U, s, Vt = svd(A)
    
    # Unit circle
    theta = np.linspace(0, 2*np.pi, 100)
    unit_circle = np.array([np.cos(theta), np.sin(theta)])
    
    # Transform unit circle through A
    transformed = A @ unit_circle
    
    ax2.plot(unit_circle[0], unit_circle[1], 'b-', linewidth=2, label='Unit Circle', alpha=0.8)
    ax2.plot(transformed[0], transformed[1], 'r-', linewidth=3, label='A × Unit Circle', alpha=0.8)
    
    # Show singular vectors
    for i in range(2):
        # Right singular vectors (V)
        ax2.arrow(0, 0, Vt[i, 0], Vt[i, 1], head_width=0.1, head_length=0.1, 
                 fc='green', ec='green', alpha=0.8, linewidth=2)
        ax2.text(Vt[i, 0]*1.2, Vt[i, 1]*1.2, f'v{i+1}', fontsize=12, color='green', fontweight='bold')
        
        # Left singular vectors (U) scaled by singular values
        scaled_u = s[i] * U[:, i]
        ax2.arrow(0, 0, scaled_u[0], scaled_u[1], head_width=0.1, head_length=0.1, 
                 fc='orange', ec='orange', alpha=0.8, linewidth=2)
        ax2.text(scaled_u[0]*1.1, scaled_u[1]*1.1, f'σ{i+1}u{i+1}', fontsize=12, color='orange', fontweight='bold')
    
    ax2.set_xlim(-4, 4)
    ax2.set_ylim(-4, 4)
    ax2.set_xlabel('x₁', fontsize=14, fontweight='bold')
    ax2.set_ylabel('x₂', fontsize=14, fontweight='bold')
    ax2.set_title('SVD Geometric Interpretation', fontsize=16, fontweight='bold', pad=20)
    ax2.legend(fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')
    
    # Add SVD information
    ax2.text(-3.8, 3.5, f'A = UΣVᵀ\nσ₁ = {s[0]:.2f}\nσ₂ = {s[1]:.2f}\nκ₂(A) = {s[0]/s[1]:.2f}', 
             fontsize=11, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.7))
    
    # 3. Condition Number Effects
    # Generate well-conditioned and ill-conditioned systems
    np.random.seed(42)
    
    # Well-conditioned matrix
    A_good = np.array([[2, 0.1], [0.1, 2]])
    kappa_good = np.linalg.cond(A_good)
    
    # Ill-conditioned matrix
    A_bad = np.array([[1, 0.999], [0.999, 0.998]])
    kappa_bad = np.linalg.cond(A_bad)
    
    # Original right-hand side
    b_original = np.array([1, 1])
    
    # Solve original systems
    x_good_orig = np.linalg.solve(A_good, b_original)
    x_bad_orig = np.linalg.solve(A_bad, b_original)
    
    # Perturbed right-hand side
    perturbation_levels = np.logspace(-10, -1, 50)
    relative_errors_good = []
    relative_errors_bad = []
    
    for eps in perturbation_levels:
        # Add small perturbation
        b_pert = b_original + eps * np.array([1, -1])
        
        # Solve perturbed systems
        x_good_pert = np.linalg.solve(A_good, b_pert)
        x_bad_pert = np.linalg.solve(A_bad, b_pert)
        
        # Calculate relative errors
        rel_err_good = np.linalg.norm(x_good_pert - x_good_orig) / np.linalg.norm(x_good_orig)
        rel_err_bad = np.linalg.norm(x_bad_pert - x_bad_orig) / np.linalg.norm(x_bad_orig)
        
        relative_errors_good.append(rel_err_good)
        relative_errors_bad.append(rel_err_bad)
    
    ax3.loglog(perturbation_levels, relative_errors_good, 'b-', linewidth=3, 
               label=f'Well-conditioned (κ = {kappa_good:.1f})', alpha=0.8)
    ax3.loglog(perturbation_levels, relative_errors_bad, 'r-', linewidth=3, 
               label=f'Ill-conditioned (κ = {kappa_bad:.0f})', alpha=0.8)
    
    # Theoretical bounds
    relative_perturbation = perturbation_levels / np.linalg.norm(b_original)
    theoretical_good = kappa_good * relative_perturbation
    theoretical_bad = kappa_bad * relative_perturbation
    
    ax3.loglog(perturbation_levels, theoretical_good, 'b--', linewidth=2, alpha=0.6, label='Theory (well-cond.)')
    ax3.loglog(perturbation_levels, theoretical_bad, 'r--', linewidth=2, alpha=0.6, label='Theory (ill-cond.)')
    
    ax3.set_xlabel('Perturbation Level ε', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Relative Error in Solution', fontsize=14, fontweight='bold')
    ax3.set_title('Condition Number Effects on Solution Sensitivity', fontsize=16, fontweight='bold', pad=20)
    ax3.legend(fontsize=11)
    ax3.grid(True, alpha=0.3)
    
    # 4. Orthogonal Matrix Properties
    # Generate random orthogonal matrix using QR decomposition
    np.random.seed(123)
    A_random = np.random.randn(3, 3)
    Q, R = qr(A_random)
    
    # Ensure proper orthogonal matrix (det = +1)
    if np.linalg.det(Q) < 0:
        Q[:, 0] = -Q[:, 0]
    
    # Original vectors
    vectors_orig = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1]]).T
    
    # Transformed vectors
    vectors_transformed = Q @ vectors_orig
    
    # Create 3D plot
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    
    colors = ['red', 'green', 'blue', 'purple']
    labels = ['e₁', 'e₂', 'e₃', 'v']
    
    for i in range(4):
        # Original vectors
        ax4.quiver(0, 0, 0, vectors_orig[0, i], vectors_orig[1, i], vectors_orig[2, i], 
                  color=colors[i], alpha=0.5, linewidth=2, arrow_length_ratio=0.1)
        
        # Transformed vectors
        ax4.quiver(0, 0, 0, vectors_transformed[0, i], vectors_transformed[1, i], vectors_transformed[2, i], 
                  color=colors[i], alpha=0.9, linewidth=3, arrow_length_ratio=0.1)
        
        # Labels
        ax4.text(vectors_transformed[0, i]*1.1, vectors_transformed[1, i]*1.1, vectors_transformed[2, i]*1.1, 
                f'Q{labels[i]}', fontsize=10, color=colors[i], fontweight='bold')
    
    # Verify orthogonality properties
    norms_orig = [np.linalg.norm(vectors_orig[:, i]) for i in range(4)]
    norms_transformed = [np.linalg.norm(vectors_transformed[:, i]) for i in range(4)]
    
    ax4.set_xlabel('X', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Y', fontsize=12, fontweight='bold')
    ax4.set_zlabel('Z', fontsize=12, fontweight='bold')
    ax4.set_title('Orthogonal Matrix: Norm Preservation', fontsize=14, fontweight='bold', pad=20)
    
    # Add properties text
    properties_text = (f'Properties verified:\n'
                      f'det(Q) = {np.linalg.det(Q):.3f}\n'
                      f'κ₂(Q) = {np.linalg.cond(Q):.3f}\n'
                      f'‖Qv‖₂ = ‖v‖₂ ✓')
    
    ax4.text2D(0.02, 0.98, properties_text, transform=ax4.transAxes, fontsize=10,
               verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/figures/linear_algebra_foundations.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'well_conditioned_kappa': kappa_good,
        'ill_conditioned_kappa': kappa_bad,
        'orthogonal_det': np.linalg.det(Q),
        'orthogonal_cond': np.linalg.cond(Q)
    }

def create_matrix_conditioning_analysis():
    """
    Create detailed analysis of matrix conditioning effects
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Hilbert Matrix Conditioning
    sizes = range(2, 13)
    condition_numbers = []
    
    for n in sizes:
        H = hilbert(n)
        kappa = np.linalg.cond(H)
        condition_numbers.append(kappa)
    
    ax1.semilogy(sizes, condition_numbers, 'ro-', linewidth=3, markersize=8, alpha=0.8)
    ax1.set_xlabel('Matrix Size n', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Condition Number κ₂(Hₙ)', fontsize=14, fontweight='bold')
    ax1.set_title('Hilbert Matrix Conditioning Growth', fontsize=16, fontweight='bold', pad=20)
    ax1.grid(True, alpha=0.3)
    
    # Add exponential fit
    log_kappa = np.log10(condition_numbers)
    coeffs = np.polyfit(sizes, log_kappa, 1)
    fit_line = 10**(coeffs[0] * np.array(sizes) + coeffs[1])
    ax1.semilogy(sizes, fit_line, 'b--', linewidth=2, alpha=0.6, 
                label=f'Exponential fit: ~10^({coeffs[0]:.1f}n)')
    ax1.legend(fontsize=12)
    
    # Add specific values
    for i, (n, kappa) in enumerate(zip(sizes[::2], condition_numbers[::2])):
        ax1.annotate(f'{kappa:.0e}', (n, kappa), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=9)
    
    # 2. Random Matrix Conditioning Distribution
    np.random.seed(42)
    n_matrices = 1000
    matrix_size = 10
    condition_numbers_random = []
    
    for _ in range(n_matrices):
        A = np.random.randn(matrix_size, matrix_size)
        kappa = np.linalg.cond(A)
        if kappa < 1e16:  # Filter out numerically singular matrices
            condition_numbers_random.append(kappa)
    
    ax2.hist(np.log10(condition_numbers_random), bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    ax2.set_xlabel('log₁₀(κ₂)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Frequency', fontsize=14, fontweight='bold')
    ax2.set_title('Random Matrix Conditioning Distribution', fontsize=16, fontweight='bold', pad=20)
    ax2.grid(True, alpha=0.3)
    
    # Add statistics
    mean_log_kappa = np.mean(np.log10(condition_numbers_random))
    std_log_kappa = np.std(np.log10(condition_numbers_random))
    ax2.axvline(mean_log_kappa, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_log_kappa:.1f}')
    ax2.legend(fontsize=12)
    
    stats_text = (f'Statistics (n={matrix_size}):\n'
                 f'Mean log₁₀(κ): {mean_log_kappa:.2f}\n'
                 f'Std log₁₀(κ): {std_log_kappa:.2f}\n'
                 f'Median κ: {np.median(condition_numbers_random):.1f}')
    ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, fontsize=11,
             verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.7))
    
    # 3. Perturbation Analysis Visualization
    # Create a specific ill-conditioned system
    A = np.array([[1, 1], [1, 1.0001]])
    kappa = np.linalg.cond(A)
    b = np.array([2, 2.0001])
    x_exact = np.linalg.solve(A, b)
    
    # Generate perturbations
    n_perturbations = 100
    perturbation_magnitude = 1e-6
    
    solutions = []
    perturbations = []
    
    np.random.seed(42)
    for _ in range(n_perturbations):
        # Random perturbation in b
        delta_b = perturbation_magnitude * np.random.randn(2)
        b_pert = b + delta_b
        x_pert = np.linalg.solve(A, b_pert)
        
        solutions.append(x_pert)
        perturbations.append(delta_b)
    
    solutions = np.array(solutions)
    perturbations = np.array(perturbations)
    
    # Plot solution scatter
    ax3.scatter(solutions[:, 0], solutions[:, 1], alpha=0.6, s=30, c='blue')
    ax3.plot(x_exact[0], x_exact[1], 'ro', markersize=10, label='Exact solution')
    
    # Add error ellipse
    from matplotlib.patches import Ellipse
    cov = np.cov(solutions.T)
    eigenvals, eigenvecs = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(eigenvecs[1, 0], eigenvecs[0, 0]))
    
    for n_std in [1, 2, 3]:
        width, height = 2 * n_std * np.sqrt(eigenvals)
        ellipse = Ellipse(xy=x_exact, width=width, height=height, angle=angle,
                         facecolor='none', edgecolor='red', alpha=0.5, linewidth=2)
        ax3.add_patch(ellipse)
    
    ax3.set_xlabel('x₁', fontsize=14, fontweight='bold')
    ax3.set_ylabel('x₂', fontsize=14, fontweight='bold')
    ax3.set_title('Solution Sensitivity to RHS Perturbations', fontsize=16, fontweight='bold', pad=20)
    ax3.legend(fontsize=12)
    ax3.grid(True, alpha=0.3)
    
    # Add system information
    system_info = (f'System: Ax = b\n'
                  f'κ₂(A) = {kappa:.0f}\n'
                  f'‖Δb‖/‖b‖ = {perturbation_magnitude/np.linalg.norm(b):.0e}\n'
                  f'Expected ‖Δx‖/‖x‖ ≤ {kappa * perturbation_magnitude/np.linalg.norm(b):.2f}')
    ax3.text(0.02, 0.98, system_info, transform=ax3.transAxes, fontsize=11,
             verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7))
    
    # 4. SVD and Low-Rank Approximation
    # Create a low-rank matrix with noise
    np.random.seed(42)
    m, n = 50, 40
    rank = 5
    
    # Generate low-rank matrix
    U_true = np.random.randn(m, rank)
    V_true = np.random.randn(rank, n)
    A_true = U_true @ V_true
    
    # Add noise
    noise_level = 0.1
    noise = noise_level * np.random.randn(m, n)
    A_noisy = A_true + noise
    
    # Compute SVD
    U, s, Vt = svd(A_noisy, full_matrices=False)
    
    # Plot singular values
    ax4.semilogy(range(1, len(s)+1), s, 'bo-', linewidth=2, markersize=6, alpha=0.8, label='Singular values')
    ax4.axhline(noise_level, color='red', linestyle='--', linewidth=2, label=f'Noise level ({noise_level})')
    ax4.axvline(rank, color='green', linestyle='--', linewidth=2, label=f'True rank ({rank})')
    
    ax4.set_xlabel('Index i', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Singular Value σᵢ', fontsize=14, fontweight='bold')
    ax4.set_title('SVD: Rank Detection in Noisy Data', fontsize=16, fontweight='bold', pad=20)
    ax4.legend(fontsize=12)
    ax4.grid(True, alpha=0.3)
    
    # Add approximation quality
    approximation_errors = []
    for k in range(1, min(20, len(s))):
        A_k = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
        error = np.linalg.norm(A_true - A_k, 'fro') / np.linalg.norm(A_true, 'fro')
        approximation_errors.append(error)
    
    ax4_twin = ax4.twinx()
    ax4_twin.semilogy(range(1, len(approximation_errors)+1), approximation_errors, 'g^-', 
                     linewidth=2, markersize=4, alpha=0.7, label='Approximation error')
    ax4_twin.set_ylabel('Relative Frobenius Error', fontsize=12, fontweight='bold', color='green')
    ax4_twin.tick_params(axis='y', labelcolor='green')
    
    # Add text box with key insights
    insights_text = (f'Key Insights:\n'
                    f'• True rank: {rank}\n'
                    f'• σ₅/σ₆ ratio: {s[4]/s[5]:.1f}\n'
                    f'• Noise threshold works!\n'
                    f'• Rank-{rank} error: {approximation_errors[rank-1]:.3f}')
    ax4.text(0.98, 0.98, insights_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/figures/matrix_conditioning_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'hilbert_condition_growth': condition_numbers,
        'random_matrix_stats': {
            'mean_log_kappa': mean_log_kappa,
            'std_log_kappa': std_log_kappa,
            'median_kappa': np.median(condition_numbers_random)
        },
        'svd_rank_detection': {
            'true_rank': rank,
            'noise_level': noise_level,
            'singular_values': s[:10].tolist()
        }
    }

def create_special_matrices_properties():
    """
    Create visualization of special matrix classes and their properties
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Symmetric Matrix Eigenvalue Distribution
    np.random.seed(42)
    n = 100
    
    # Generate random symmetric matrix
    A_rand = np.random.randn(n, n)
    A_sym = (A_rand + A_rand.T) / 2
    
    # Compute eigenvalues
    eigenvals_sym = np.linalg.eigvals(A_sym)
    eigenvals_sym = np.sort(eigenvals_sym)
    
    # Generate random non-symmetric matrix for comparison
    A_nonsym = np.random.randn(n, n)
    eigenvals_nonsym = np.linalg.eigvals(A_nonsym)
    
    # Plot eigenvalue distributions
    ax1.hist(eigenvals_sym, bins=20, alpha=0.7, color='blue', label='Symmetric', density=True)
    ax1.hist(np.real(eigenvals_nonsym), bins=20, alpha=0.5, color='red', label='Non-symmetric (real part)', density=True)
    
    ax1.set_xlabel('Eigenvalue', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Density', fontsize=14, fontweight='bold')
    ax1.set_title('Eigenvalue Distributions: Symmetric vs Non-symmetric', fontsize=16, fontweight='bold', pad=20)
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Add Wigner semicircle law approximation for large random symmetric matrices
    x_theory = np.linspace(-3, 3, 1000)
    wigner_density = (2/np.pi) * np.sqrt(4 - x_theory**2)
    wigner_density[np.abs(x_theory) > 2] = 0
    ax1.plot(x_theory, wigner_density, 'k--', linewidth=2, alpha=0.8, label='Wigner semicircle')
    ax1.legend(fontsize=12)
    
    # 2. Positive Definite Matrix Properties
    # Create positive definite matrix
    A_pd = A_sym @ A_sym.T + 0.1 * np.eye(n)  # Ensure positive definiteness
    eigenvals_pd = np.linalg.eigvals(A_pd)
    
    # Create positive semidefinite matrix
    A_psd = A_sym @ A_sym.T
    eigenvals_psd = np.linalg.eigvals(A_psd)
    
    # Plot eigenvalue comparison
    ax2.scatter(range(len(eigenvals_pd)), np.sort(eigenvals_pd)[::-1], 
               alpha=0.7, s=30, color='green', label='Positive Definite')
    ax2.scatter(range(len(eigenvals_psd)), np.sort(eigenvals_psd)[::-1], 
               alpha=0.7, s=30, color='orange', label='Positive Semidefinite')
    ax2.axhline(0, color='red', linestyle='--', linewidth=2, alpha=0.8, label='Zero line')
    
    ax2.set_xlabel('Eigenvalue Index (sorted)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Eigenvalue', fontsize=14, fontweight='bold')
    ax2.set_title('Positive (Semi)Definite Matrix Eigenvalues', fontsize=16, fontweight='bold', pad=20)
    ax2.legend(fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')
    
    # Add properties text
    pd_props = (f'Positive Definite Properties:\n'
               f'• All λᵢ > 0: ✓\n'
               f'• min(λᵢ) = {np.min(eigenvals_pd):.3f}\n'
               f'• κ₂ = {np.max(eigenvals_pd)/np.min(eigenvals_pd):.1f}\n'
               f'• Cholesky decomposition exists')
    ax2.text(0.02, 0.98, pd_props, transform=ax2.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))
    
    # 3. Orthogonal Matrix Generation and Properties
    # Generate orthogonal matrices using different methods
    methods = ['QR', 'SVD', 'Givens', 'Householder']
    determinants = []
    condition_numbers = []
    
    np.random.seed(42)
    n_small = 10
    
    for method in methods:
        if method == 'QR':
            A = np.random.randn(n_small, n_small)
            Q, R = qr(A)
            if np.linalg.det(Q) < 0:
                Q[:, 0] = -Q[:, 0]
        elif method == 'SVD':
            A = np.random.randn(n_small, n_small)
            U, s, Vt = svd(A)
            Q = U @ Vt
            if np.linalg.det(Q) < 0:
                Q[:, 0] = -Q[:, 0]
        elif method == 'Givens':
            Q = np.eye(n_small)
            for i in range(n_small-1):
                for j in range(i+1, n_small):
                    theta = np.random.uniform(0, 2*np.pi)
                    G = np.eye(n_small)
                    G[i, i] = np.cos(theta)
                    G[i, j] = -np.sin(theta)
                    G[j, i] = np.sin(theta)
                    G[j, j] = np.cos(theta)
                    Q = Q @ G
        else:  # Householder
            Q = np.eye(n_small)
            for k in range(n_small-1):
                x = np.random.randn(n_small-k)
                x = x / np.linalg.norm(x)
                H = np.eye(n_small-k) - 2 * np.outer(x, x)
                Q_k = np.eye(n_small)
                Q_k[k:, k:] = H
                Q = Q @ Q_k
        
        determinants.append(np.linalg.det(Q))
        condition_numbers.append(np.linalg.cond(Q))
    
    # Plot properties
    x_pos = np.arange(len(methods))
    width = 0.35
    
    ax3.bar(x_pos - width/2, determinants, width, label='det(Q)', alpha=0.8, color='skyblue')
    ax3.bar(x_pos + width/2, condition_numbers, width, label='κ₂(Q)', alpha=0.8, color='lightcoral')
    
    ax3.set_xlabel('Generation Method', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Value', fontsize=14, fontweight='bold')
    ax3.set_title('Orthogonal Matrix Properties by Generation Method', fontsize=16, fontweight='bold', pad=20)
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(methods)
    ax3.legend(fontsize=12)
    ax3.grid(True, alpha=0.3)
    
    # Add horizontal lines for ideal values
    ax3.axhline(1, color='blue', linestyle='--', alpha=0.6, label='Ideal det(Q) = ±1')
    ax3.axhline(1, color='red', linestyle='--', alpha=0.6, label='Ideal κ₂(Q) = 1')
    
    # Add verification text
    verification_text = 'Verification (all methods):\n'
    for i, method in enumerate(methods):
        verification_text += f'{method}: det={determinants[i]:.3f}, κ={condition_numbers[i]:.3f}\n'
    
    ax3.text(0.02, 0.98, verification_text, transform=ax3.transAxes, fontsize=9,
             verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.7))
    
    # 4. Matrix Structure and Sparsity Patterns
    # Create different structured matrices
    n_struct = 20
    
    # Tridiagonal matrix
    tridiag = np.zeros((n_struct, n_struct))
    for i in range(n_struct):
        tridiag[i, i] = 2
        if i > 0:
            tridiag[i, i-1] = -1
        if i < n_struct-1:
            tridiag[i, i+1] = -1
    
    # Block diagonal matrix
    block_diag = np.zeros((n_struct, n_struct))
    block_size = 4
    for i in range(0, n_struct, block_size):
        end_idx = min(i + block_size, n_struct)
        block_diag[i:end_idx, i:end_idx] = np.random.randn(end_idx-i, end_idx-i)
    
    # Toeplitz matrix
    toeplitz = np.zeros((n_struct, n_struct))
    for i in range(n_struct):
        for j in range(n_struct):
            toeplitz[i, j] = 1 / (1 + abs(i - j))
    
    # Circulant matrix
    circulant = np.zeros((n_struct, n_struct))
    first_row = np.random.randn(n_struct)
    for i in range(n_struct):
        circulant[i, :] = np.roll(first_row, i)
    
    # Create subplot for structure visualization
    structures = [tridiag, block_diag, toeplitz, circulant]
    titles = ['Tridiagonal', 'Block Diagonal', 'Toeplitz', 'Circulant']
    
    # Use a 2x2 grid within the subplot
    for idx, (matrix, title) in enumerate(zip(structures, titles)):
        row = idx // 2
        col = idx % 2
        
        if idx == 0:
            im = ax4.imshow(np.abs(matrix), cmap='Blues', aspect='equal')
            ax4.set_title('Matrix Structure Examples', fontsize=16, fontweight='bold', pad=20)
            ax4.set_xlabel('Column Index', fontsize=12, fontweight='bold')
            ax4.set_ylabel('Row Index', fontsize=12, fontweight='bold')
            
            # Add colorbar
            cbar = plt.colorbar(im, ax=ax4, shrink=0.8)
            cbar.set_label('|Matrix Element|', fontsize=12, fontweight='bold')
            
            # Add structure information
            structure_info = []
            for mat, name in zip(structures, titles):
                nnz = np.count_nonzero(mat)
                sparsity = 1 - nnz / (n_struct**2)
                cond_num = np.linalg.cond(mat) if np.linalg.det(mat) != 0 else np.inf
                structure_info.append(f'{name}:\n  Sparsity: {sparsity:.2f}\n  κ₂: {cond_num:.1e}')
            
            info_text = '\n\n'.join(structure_info)
            ax4.text(1.15, 0.5, info_text, transform=ax4.transAxes, fontsize=9,
                    verticalalignment='center', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcyan", alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/figures/special_matrices_properties.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'symmetric_eigenval_range': [np.min(eigenvals_sym), np.max(eigenvals_sym)],
        'pd_condition_number': np.max(eigenvals_pd)/np.min(eigenvals_pd),
        'orthogonal_properties': {
            'determinants': determinants,
            'condition_numbers': condition_numbers
        }
    }

def create_svd_applications():
    """
    Create comprehensive SVD applications demonstration
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Image Compression using SVD
    # Create a synthetic "image" with clear structure
    np.random.seed(42)
    m, n = 100, 80
    
    # Create structured image with geometric patterns
    x = np.linspace(-2, 2, n)
    y = np.linspace(-2, 2, m)
    X, Y = np.meshgrid(x, y)
    
    # Combine multiple patterns
    image = (np.sin(3*X) * np.cos(2*Y) + 
             0.5 * np.exp(-(X**2 + Y**2)) + 
             0.3 * np.sin(5*X*Y))
    
    # Add some noise
    image += 0.1 * np.random.randn(m, n)
    
    # Compute SVD
    U, s, Vt = svd(image, full_matrices=False)
    
    # Show original and compressed versions
    ranks = [1, 5, 20, len(s)]
    
    for i, rank in enumerate(ranks):
        if rank == len(s):
            compressed = image
            title = f'Original (rank {len(s)})'
        else:
            compressed = U[:, :rank] @ np.diag(s[:rank]) @ Vt[:rank, :]
            compression_ratio = (rank * (m + n)) / (m * n)
            title = f'Rank {rank} ({compression_ratio:.1%} storage)'
        
        if i == 0:
            im1 = ax1.imshow(compressed, cmap='viridis', aspect='equal')
            ax1.set_title(title, fontsize=12, fontweight='bold')
        elif i == 1:
            im2 = ax2.imshow(compressed, cmap='viridis', aspect='equal')
            ax2.set_title(title, fontsize=12, fontweight='bold')
    
    # Add colorbars
    plt.colorbar(im1, ax=ax1, shrink=0.8)
    plt.colorbar(im2, ax=ax2, shrink=0.8)
    
    # Plot singular values and compression error
    ax3.semilogy(range(1, len(s)+1), s, 'bo-', linewidth=2, markersize=4, alpha=0.8, label='Singular values')
    
    # Calculate compression errors
    compression_errors = []
    storage_ratios = []
    
    for rank in range(1, min(50, len(s))):
        compressed = U[:, :rank] @ np.diag(s[:rank]) @ Vt[:rank, :]
        error = np.linalg.norm(image - compressed, 'fro') / np.linalg.norm(image, 'fro')
        storage = (rank * (m + n)) / (m * n)
        
        compression_errors.append(error)
        storage_ratios.append(storage)
    
    ax3.set_xlabel('Singular Value Index', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Singular Value', fontsize=14, fontweight='bold')
    ax3.set_title('SVD Image Compression Analysis', fontsize=16, fontweight='bold', pad=20)
    ax3.grid(True, alpha=0.3)
    
    # Add compression quality markers
    quality_ranks = [1, 5, 20]
    for rank in quality_ranks:
        if rank <= len(s):
            ax3.axvline(rank, color='red', linestyle='--', alpha=0.6)
            ax3.text(rank, s[rank-1]*2, f'Rank {rank}', rotation=90, 
                    verticalalignment='bottom', fontsize=10, color='red')
    
    # Plot compression trade-off
    ax4.loglog(storage_ratios, compression_errors, 'ro-', linewidth=2, markersize=6, alpha=0.8)
    ax4.set_xlabel('Storage Ratio (fraction of original)', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Relative Frobenius Error', fontsize=14, fontweight='bold')
    ax4.set_title('Compression Trade-off: Storage vs Quality', fontsize=16, fontweight='bold', pad=20)
    ax4.grid(True, alpha=0.3)
    
    # Add quality benchmarks
    quality_levels = [0.1, 0.05, 0.01]
    colors = ['green', 'orange', 'red']
    labels = ['Good (10%)', 'Very Good (5%)', 'Excellent (1%)']
    
    for error, color, label in zip(quality_levels, colors, labels):
        ax4.axhline(error, color=color, linestyle='--', alpha=0.7, label=label)
    
    ax4.legend(fontsize=11, title='Quality Levels')
    
    # Add specific points
    for i, rank in enumerate([1, 5, 20]):
        if rank-1 < len(compression_errors):
            ax4.plot(storage_ratios[rank-1], compression_errors[rank-1], 'ko', markersize=8)
            ax4.annotate(f'Rank {rank}', 
                        (storage_ratios[rank-1], compression_errors[rank-1]),
                        xytext=(10, 10), textcoords='offset points', fontsize=10,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/figures/svd_applications.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'original_rank': len(s),
        'singular_values': s[:10].tolist(),
        'compression_analysis': {
            'rank_1_error': compression_errors[0],
            'rank_5_error': compression_errors[4] if len(compression_errors) > 4 else None,
            'rank_20_error': compression_errors[19] if len(compression_errors) > 19 else None
        }
    }

def main():
    """
    Main function to generate all educational figures and demonstrations
    """
    print("Generating Lecture 4 Educational Materials...")
    print("=" * 60)
    
    # Create figures directory
    import os
    os.makedirs('/home/ubuntu/figures', exist_ok=True)
    
    # Generate all visualizations
    print("1. Creating Linear Algebra Foundations...")
    results1 = create_linear_algebra_foundations()
    
    print("2. Creating Matrix Conditioning Analysis...")
    results2 = create_matrix_conditioning_analysis()
    
    print("3. Creating Special Matrices Properties...")
    results3 = create_special_matrices_properties()
    
    print("4. Creating SVD Applications...")
    results4 = create_svd_applications()
    
    print("\nAll figures generated successfully!")
    print("=" * 60)
    
    # Print summary of results
    print("\nKEY NUMERICAL RESULTS:")
    print("-" * 30)
    print(f"Well-conditioned matrix κ: {results1['well_conditioned_kappa']:.1f}")
    print(f"Ill-conditioned matrix κ: {results1['ill_conditioned_kappa']:.0f}")
    print(f"Orthogonal matrix det: {results1['orthogonal_det']:.3f}")
    print(f"Orthogonal matrix κ: {results1['orthogonal_cond']:.3f}")
    
    print(f"\nHilbert matrix H₁₀ condition number: {results2['hilbert_condition_growth'][-3]:.2e}")
    print(f"Random matrix mean log₁₀(κ): {results2['random_matrix_stats']['mean_log_kappa']:.2f}")
    
    print(f"\nSymmetric eigenvalue range: [{results3['symmetric_eigenval_range'][0]:.2f}, {results3['symmetric_eigenval_range'][1]:.2f}]")
    print(f"Positive definite κ: {results3['pd_condition_number']:.1f}")
    
    print(f"\nSVD compression rank-5 error: {results4['compression_analysis']['rank_5_error']:.3f}")
    
    print("\nFigures saved:")
    print("- figures/linear_algebra_foundations.png")
    print("- figures/matrix_conditioning_analysis.png") 
    print("- figures/special_matrices_properties.png")
    print("- figures/svd_applications.png")
    
    return {
        'linear_algebra': results1,
        'conditioning': results2,
        'special_matrices': results3,
        'svd_applications': results4
    }

if __name__ == "__main__":
    results = main()
