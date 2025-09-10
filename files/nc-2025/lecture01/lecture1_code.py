"""
NUMERICAL COMPUTING - LECTURE 1: COMPLETE CODE PACKAGE
Università della Svizzera Italiana (USI)
Author: Francisco Richter Mendoza

This file contains all Python code for Lecture 1:
- Figure generation for slides and notes
- Educational demonstrations
- Practical examples
- Exercises and solutions

Topics covered:
- Well-posed vs ill-posed problems
- Error analysis and propagation
- Condition numbers and stability
- Floating point arithmetic
- Catastrophic cancellation
- Machine epsilon discovery
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.linalg import hilbert
import numpy.linalg as la
import warnings
warnings.filterwarnings('ignore')

# ================================================
# CONFIGURATION FOR HIGH-QUALITY FIGURES
# ================================================

# Set style for slide-optimized figures
plt.rcParams.update({
    'font.size': 14,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 18,
    'lines.linewidth': 2.5,
    'axes.linewidth': 1.5,
    'grid.linewidth': 1.0,
    'figure.dpi': 150
})

def setup_directories():
    """Create necessary directories for output"""
    import os
    os.makedirs('figures', exist_ok=True)
    print("Created figures directory")

# ================================================
# FIGURE 1: WELL-POSED VS ILL-POSED PROBLEMS
# ================================================

def create_well_posed_comparison():
    """Generate comparison of well-posed vs ill-posed linear systems"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Well-posed: Linear system visualization
    x = np.linspace(-1.5, 1.5, 100)
    y1 = 2*x + 1      # Line 1: 2x - y = -1
    y2 = -0.5*x + 0.5 # Line 2: -0.5x - y = -0.5
    
    ax1.plot(x, y1, 'b-', linewidth=3, label='2x - y = -1')
    ax1.plot(x, y2, 'r-', linewidth=3, label='-0.5x - y = -0.5')
    ax1.plot(0, 1, 'go', markersize=12, label='Solution (0,1)', zorder=5)
    
    # Add perturbation visualization
    ax1.plot(x, y1 + 0.1, 'b--', linewidth=2, alpha=0.7, label='Perturbed system')
    ax1.plot(x, y2 + 0.1, 'r--', linewidth=2, alpha=0.7)
    ax1.plot(0.067, 1.133, 'yo', markersize=10, label='Perturbed solution', zorder=5)
    
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1, 3)
    ax1.grid(True, alpha=0.4)
    ax1.legend(loc='upper right', fontsize=11)
    ax1.set_title('WELL-POSED PROBLEM\nκ(A) = 6.85 (Well-conditioned)', fontweight='bold', pad=20)
    ax1.set_xlabel('x', fontweight='bold')
    ax1.set_ylabel('y', fontweight='bold')
    
    # Add annotation
    ax1.annotate('Small perturbation\n→ Small change in solution', 
                xy=(0.067, 1.133), xytext=(0.8, 2.2),
                arrowprops=dict(arrowstyle='->', color='orange', lw=2),
                fontsize=12, ha='center', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow'))
    
    # Ill-posed: Nearly parallel lines
    y3 = x + 1        # Line 1: x - y = -1
    y4 = x + 1.01     # Line 2: x - y = -1.01 (tiny perturbation)
    
    ax2.plot(x, y3, 'b-', linewidth=3, label='x - y = -1')
    ax2.plot(x, y4, 'r-', linewidth=3, label='x - y = -1.01')
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1, 3)
    ax2.grid(True, alpha=0.4)
    ax2.legend(loc='upper left', fontsize=11)
    ax2.set_title('ILL-POSED PROBLEM\nκ(A) = 40,002 (Ill-conditioned)', fontweight='bold', pad=20)
    ax2.set_xlabel('x', fontweight='bold')
    ax2.set_ylabel('y', fontweight='bold')
    
    # Add annotation for ill-posed
    ax2.annotate('Tiny perturbation (0.01)\n→ No unique intersection!', 
                xy=(0, 1), xytext=(-1, 2.5),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=12, ha='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('figures/well_posed_comparison.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print("Generated: figures/well_posed_comparison.png")

# ================================================
# FIGURE 2: ERROR PROPAGATION ANALYSIS
# ================================================

def create_error_propagation():
    """Generate error propagation analysis for numerical differentiation"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    h_values = np.logspace(-16, 0, 100)
    true_derivative = np.cos(1.0)  # d/dx sin(x) at x=1
    
    # Forward difference approximation
    numerical_derivative = (np.sin(1.0 + h_values) - np.sin(1.0)) / h_values
    error = np.abs(numerical_derivative - true_derivative)
    
    # Theoretical error components
    truncation_error = h_values/2  # O(h) truncation error
    roundoff_error = 2.22e-16/h_values  # Machine epsilon / h
    total_error = truncation_error + roundoff_error
    
    ax.loglog(h_values, error, 'b-', linewidth=3, label='Actual Error', zorder=3)
    ax.loglog(h_values, truncation_error, 'r--', linewidth=2.5, 
              label='Truncation Error O(h)', alpha=0.8)
    ax.loglog(h_values, roundoff_error, 'g--', linewidth=2.5, 
              label='Roundoff Error O(ε/h)', alpha=0.8)
    ax.loglog(h_values, total_error, 'k:', linewidth=2, 
              label='Total Error (sum)', alpha=0.7)
    
    # Find and mark optimal h
    optimal_idx = np.argmin(total_error)
    optimal_h = h_values[optimal_idx]
    optimal_error = total_error[optimal_idx]
    
    ax.plot(optimal_h, optimal_error, 'ro', markersize=12, zorder=5)
    ax.annotate(f'Optimal h ≈ {optimal_h:.2e}\nMinimal Error ≈ {optimal_error:.2e}', 
                xy=(optimal_h, optimal_error), xytext=(1e-8, 1e-4),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=12, ha='center',
                bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue'))
    
    ax.set_xlabel('Step Size h', fontweight='bold')
    ax.set_ylabel('Error Magnitude', fontweight='bold')
    ax.set_title('ERROR PROPAGATION IN NUMERICAL DIFFERENTIATION\n' + 
                 'f\'(x) ≈ [f(x+h) - f(x)]/h for f(x) = sin(x) at x = 1', 
                 fontweight='bold', pad=20)
    ax.legend(loc='upper right', fontsize=12)
    ax.grid(True, alpha=0.4)
    
    # Add regions
    ax.axvspan(1e-16, 1e-10, alpha=0.2, color='red', label='Roundoff Dominated')
    ax.axvspan(1e-4, 1, alpha=0.2, color='blue', label='Truncation Dominated')
    
    plt.tight_layout()
    plt.savefig('figures/error_propagation.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Generated: figures/error_propagation.png")

# ================================================
# FIGURE 3: CONDITION NUMBER DEMONSTRATION
# ================================================

def create_condition_number_demo():
    """Generate condition number demonstration with Hilbert matrices and geometric interpretation"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Hilbert matrices condition numbers
    n_values = range(2, 13)
    cond_numbers = [la.cond(hilbert(n)) for n in n_values]
    
    ax1.semilogy(n_values, cond_numbers, 'ro-', linewidth=3, markersize=8)
    ax1.set_xlabel('Matrix Size n', fontweight='bold')
    ax1.set_ylabel('Condition Number κ(Hₙ)', fontweight='bold')
    ax1.set_title('HILBERT MATRIX CONDITIONING\nH[i,j] = 1/(i+j-1)', 
                  fontweight='bold', pad=20)
    ax1.grid(True, alpha=0.4)
    
    # Add annotations for specific values
    for i, (n, cond_val) in enumerate(zip(n_values, cond_numbers)):
        if n in [3, 5, 8, 10]:
            ax1.annotate(f'κ(H_{n}) = {cond_val:.1e}', 
                        xy=(n, cond_val), xytext=(n+0.5, cond_val*2),
                        arrowprops=dict(arrowstyle='->', color='blue'),
                        fontsize=10, ha='left')
    
    # Geometric interpretation of conditioning
    theta = np.linspace(0, 2*np.pi, 100)
    
    # Well-conditioned (circle)
    x1 = np.cos(theta)
    y1 = np.sin(theta)
    ax2.plot(x1, y1, 'b-', linewidth=3, label='κ ≈ 1 (Circle)')
    
    # Moderately conditioned (ellipse)
    x2 = 3 * np.cos(theta)
    y2 = 1 * np.sin(theta)
    ax2.plot(x2, y2, 'g-', linewidth=3, label='κ ≈ 3 (Ellipse)')
    
    # Ill-conditioned (very flat ellipse)
    x3 = 5 * np.cos(theta)
    y3 = 0.1 * np.sin(theta)
    ax2.plot(x3, y3, 'r-', linewidth=3, label='κ ≈ 50 (Flat)')
    
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.4)
    ax2.set_title('GEOMETRIC INTERPRETATION\nLevel curves of quadratic forms', 
                  fontweight='bold', pad=20)
    ax2.set_xlabel('x₁', fontweight='bold')
    ax2.set_ylabel('x₂', fontweight='bold')
    ax2.legend(fontsize=12)
    
    # Add explanation
    ax2.text(0, -6, 'Higher condition number\n→ More elongated ellipse\n→ Greater sensitivity', 
             ha='center', va='center', fontsize=12,
             bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow'))
    
    plt.tight_layout()
    plt.savefig('figures/condition_number_demo.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Generated: figures/condition_number_demo.png")

# ================================================
# FIGURE 4: FLOATING POINT ARITHMETIC
# ================================================

def create_floating_point_demo():
    """Generate floating point arithmetic demonstration"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Machine epsilon demonstration
    powers = np.arange(1, 60)
    eps_values = 2.0**(-powers)
    test_results = [1.0 + eps > 1.0 for eps in eps_values]
    
    # Find machine epsilon
    machine_eps_idx = np.where(np.array(test_results) == False)[0][0]
    machine_eps = eps_values[machine_eps_idx]
    
    ax1.semilogy(powers, eps_values, 'bo-', markersize=6, linewidth=2)
    ax1.axhline(y=machine_eps, color='r', linestyle='--', linewidth=3, 
                label=f'Machine ε ≈ {machine_eps:.2e}')
    ax1.axvline(x=powers[machine_eps_idx], color='r', linestyle='--', linewidth=2, alpha=0.7)
    
    # Color code the regions
    working_region = powers < machine_eps_idx
    ax1.scatter(powers[working_region], eps_values[working_region], 
               c='green', s=50, alpha=0.7, label='1 + ε > 1 (True)')
    ax1.scatter(powers[~working_region], eps_values[~working_region], 
               c='red', s=50, alpha=0.7, label='1 + ε = 1 (False)')
    
    ax1.set_xlabel('Power p (ε = 2⁻ᵖ)', fontweight='bold')
    ax1.set_ylabel('Epsilon Value', fontweight='bold')
    ax1.set_title('MACHINE EPSILON DISCOVERY\nSmallest ε such that 1 + ε > 1', 
                  fontweight='bold', pad=20)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.4)
    
    # Catastrophic cancellation
    x = np.linspace(1e-10, 1e-6, 1000)
    
    # Stable computation
    stable = 0.5 - x**2/24 + x**4/720  # Taylor series
    
    # Unstable computation (simulated with noise)
    unstable = np.where(x < 1e-8, 
                       np.random.normal(0.5, 0.1, len(x)),  # Random noise for very small x
                       0.5 - x**2/24)  # Correct for larger x
    
    ax2.semilogx(x, stable, 'g-', linewidth=3, label='Stable: Taylor Series')
    ax2.semilogx(x, unstable, 'r-', linewidth=3, alpha=0.8, label='Unstable: Direct Computation')
    ax2.axhline(y=0.5, color='b', linestyle=':', linewidth=2, label='True Value = 0.5')
    
    ax2.set_xlabel('x', fontweight='bold')
    ax2.set_ylabel('(1 - cos(x))/x²', fontweight='bold')
    ax2.set_title('CATASTROPHIC CANCELLATION\n(1 - cos(x))/x² for small x', 
                  fontweight='bold', pad=20)
    ax2.legend(fontsize=12)
    ax2.grid(True, alpha=0.4)
    ax2.set_ylim(0, 1)
    
    # Add annotation
    ax2.annotate('Cancellation region\nDirect computation fails!', 
                xy=(1e-9, 0.3), xytext=(1e-8, 0.8),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=12, ha='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('figures/floating_point_issues.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Generated: figures/floating_point_issues.png")

# ================================================
# EDUCATIONAL DEMONSTRATIONS
# ================================================

def demonstrate_well_posed_problems():
    """Educational demonstration of well-posed vs ill-posed problems"""
    
    print("=" * 60)
    print("WELL-POSED vs ILL-POSED PROBLEMS DEMONSTRATION")
    print("=" * 60)
    
    # Well-posed example: Well-conditioned linear system
    print("\n1. WELL-POSED PROBLEM:")
    print("   System: Ax = b with A well-conditioned")
    
    A_good = np.array([[2, 1], [1, 1]])
    b = np.array([3, 2])
    x_exact = np.linalg.solve(A_good, b)
    cond_good = la.cond(A_good)
    
    print(f"   A = {A_good}")
    print(f"   b = {b}")
    print(f"   Solution: x = {x_exact}")
    print(f"   Condition number: κ(A) = {cond_good:.2f}")
    
    # Small perturbation in b
    b_pert = b + 0.01 * np.array([1, 1])
    x_pert = np.linalg.solve(A_good, b_pert)
    rel_error = np.linalg.norm(x_pert - x_exact) / np.linalg.norm(x_exact)
    
    print(f"   Perturbed b: {b_pert}")
    print(f"   Perturbed solution: {x_pert}")
    print(f"   Relative error: {rel_error:.6f}")
    
    # Ill-posed example: Ill-conditioned system
    print("\n2. ILL-POSED PROBLEM:")
    print("   System: Ax = b with A ill-conditioned")
    
    A_bad = np.array([[1, 1], [1, 1.0001]])  # Nearly singular
    b_bad = np.array([2, 2.0001])
    x_bad = np.linalg.solve(A_bad, b_bad)
    cond_bad = la.cond(A_bad)
    
    print(f"   A = {A_bad}")
    print(f"   b = {b_bad}")
    print(f"   Solution: x = {x_bad}")
    print(f"   Condition number: κ(A) = {cond_bad:.0f}")
    
    # Small perturbation
    b_bad_pert = b_bad + 0.01 * np.array([1, 1])
    x_bad_pert = np.linalg.solve(A_bad, b_bad_pert)
    rel_error_bad = np.linalg.norm(x_bad_pert - x_bad) / np.linalg.norm(x_bad)
    
    print(f"   Perturbed b: {b_bad_pert}")
    print(f"   Perturbed solution: {x_bad_pert}")
    print(f"   Relative error: {rel_error_bad:.6f}")
    
    print(f"\n   Error amplification factor: {rel_error_bad/rel_error:.1f}x")

def demonstrate_floating_point():
    """Educational demonstration of floating point arithmetic"""
    
    print("\n" + "=" * 60)
    print("FLOATING POINT ARITHMETIC DEMONSTRATION")
    print("=" * 60)
    
    # Machine epsilon
    print("\n1. MACHINE EPSILON:")
    eps = np.finfo(float).eps
    print(f"   Machine epsilon: {eps}")
    print(f"   1 + ε/2 == 1: {1 + eps/2 == 1}")
    print(f"   1 + ε == 1: {1 + eps == 1}")
    
    # Catastrophic cancellation
    print("\n2. CATASTROPHIC CANCELLATION:")
    x = 1e-8
    
    # Bad way: direct computation
    bad_result = (1 - np.cos(x)) / x**2
    
    # Good way: using Taylor series
    good_result = 0.5 - x**2/24 + x**4/720
    
    # True value (high precision)
    true_result = 0.5
    
    print(f"   Computing (1 - cos(x))/x² for x = {x}")
    print(f"   Direct computation: {bad_result}")
    print(f"   Taylor series: {good_result}")
    print(f"   True value: {true_result}")
    print(f"   Relative error (direct): {abs(bad_result - true_result)/true_result:.2e}")
    print(f"   Relative error (Taylor): {abs(good_result - true_result)/true_result:.2e}")

def demonstrate_condition_numbers():
    """Educational demonstration of condition numbers"""
    
    print("\n" + "=" * 60)
    print("CONDITION NUMBER DEMONSTRATION")
    print("=" * 60)
    
    print("\n1. HILBERT MATRICES (notorious for ill-conditioning):")
    
    for n in [3, 5, 8, 10]:
        H = hilbert(n)
        cond_H = la.cond(H)
        print(f"   H_{n}: κ(H) = {cond_H:.2e}")
        
        if n == 5:
            print(f"   H_5 = ")
            for i in range(n):
                row_str = "   ["
                for j in range(n):
                    row_str += f"{H[i,j]:.4f} "
                row_str += "]"
                print(row_str)

def find_optimal_step_size():
    """Find optimal step size for numerical differentiation"""
    
    print("\n" + "=" * 60)
    print("OPTIMAL STEP SIZE FOR NUMERICAL DIFFERENTIATION")
    print("=" * 60)
    
    # Function: f(x) = sin(x), f'(x) = cos(x)
    x = 1.0
    true_derivative = np.cos(x)
    
    h_values = np.logspace(-16, 0, 1000)
    errors = []
    
    for h in h_values:
        approx_derivative = (np.sin(x + h) - np.sin(x)) / h
        error = abs(approx_derivative - true_derivative)
        errors.append(error)
    
    errors = np.array(errors)
    optimal_idx = np.argmin(errors)
    optimal_h = h_values[optimal_idx]
    optimal_error = errors[optimal_idx]
    
    print(f"   Function: f(x) = sin(x) at x = {x}")
    print(f"   True derivative: f'({x}) = {true_derivative:.10f}")
    print(f"   Optimal step size: h* = {optimal_h:.2e}")
    print(f"   Minimal error: {optimal_error:.2e}")
    print(f"   Theoretical optimal: h* ≈ √(2ε) = {np.sqrt(2 * np.finfo(float).eps):.2e}")

# ================================================
# EXERCISE SOLUTIONS
# ================================================

def exercise_hilbert_condition():
    """Exercise: Compute condition number of 5x5 Hilbert matrix"""
    
    print("\n" + "=" * 60)
    print("EXERCISE: HILBERT MATRIX CONDITION NUMBER")
    print("=" * 60)
    
    H5 = hilbert(5)
    cond_H5 = la.cond(H5)
    
    print("5x5 Hilbert Matrix:")
    for i in range(5):
        row_str = "["
        for j in range(5):
            row_str += f"{H5[i,j]:.6f} "
        row_str += "]"
        print(row_str)
    
    print(f"\nCondition number: κ(H_5) = {cond_H5:.2e}")
    print(f"This is considered ill-conditioned because κ >> 1")
    print(f"Small perturbations in input can cause large changes in output")

def exercise_catastrophic_cancellation():
    """Exercise: Implement stable and unstable versions"""
    
    print("\n" + "=" * 60)
    print("EXERCISE: CATASTROPHIC CANCELLATION")
    print("=" * 60)
    
    x = 1e-10
    
    # Unstable version
    unstable = (1 - np.cos(x)) / x**2
    
    # Stable version using Taylor series
    stable = 0.5 - x**2/24 + x**4/720 - x**6/40320
    
    # True value
    true_value = 0.5
    
    print(f"Computing (1 - cos(x))/x² for x = {x}")
    print(f"Unstable result: {unstable}")
    print(f"Stable result: {stable}")
    print(f"True value: {true_value}")
    print(f"Unstable error: {abs(unstable - true_value):.2e}")
    print(f"Stable error: {abs(stable - true_value):.2e}")

# ================================================
# MAIN EXECUTION FUNCTION
# ================================================

def generate_all_lecture1_materials():
    """Generate all materials for Lecture 1"""
    
    print("GENERATING ALL LECTURE 1 MATERIALS")
    print("=" * 60)
    
    # Setup
    setup_directories()
    
    # Generate all figures
    print("\n1. GENERATING FIGURES:")
    create_well_posed_comparison()
    create_error_propagation()
    create_condition_number_demo()
    create_floating_point_demo()
    
    # Run demonstrations
    print("\n2. RUNNING EDUCATIONAL DEMONSTRATIONS:")
    demonstrate_well_posed_problems()
    demonstrate_floating_point()
    demonstrate_condition_numbers()
    find_optimal_step_size()
    
    # Run exercises
    print("\n3. RUNNING EXERCISE SOLUTIONS:")
    exercise_hilbert_condition()
    exercise_catastrophic_cancellation()
    
    print("\n" + "=" * 60)
    print("LECTURE 1 MATERIALS GENERATION COMPLETE!")
    print("=" * 60)
    print("\nGenerated files:")
    print("- figures/well_posed_comparison.png")
    print("- figures/error_propagation.png")
    print("- figures/condition_number_demo.png")
    print("- figures/floating_point_issues.png")
    print("\nAll demonstrations and exercises completed successfully!")

if __name__ == "__main__":
    generate_all_lecture1_materials()
