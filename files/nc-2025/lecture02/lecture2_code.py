"""
NUMERICAL COMPUTING - LECTURE 2: COMPLETE CODE PACKAGE (OPTIMIZED)
Computer Arithmetic and Error Analysis
Università della Svizzera Italiana
Author: Francisco Richter Mendoza
"""

import numpy as np
import matplotlib.pyplot as plt
import struct
import warnings
warnings.filterwarnings('ignore')

# Optimized configuration
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'figure.dpi': 100  # Reduced DPI to save memory
})

def setup_directories():
    import os
    os.makedirs('figures', exist_ok=True)
    print("Created figures directory")

def ieee754_to_binary(value, precision='single'):
    """Convert a float to IEEE 754 binary representation"""
    if precision == 'single':
        packed = struct.pack('!f', value)
        bits = struct.unpack('!I', packed)[0]
        return format(bits, '032b')
    else:
        packed = struct.pack('!d', value)
        bits = struct.unpack('!Q', packed)[0]
        return format(bits, '064b')

def create_ieee754_representation():
    """Generate IEEE 754 floating point representation visualization"""
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
    
    # Example number
    test_value = 12.375
    binary_rep = ieee754_to_binary(test_value, 'single')
    
    # Parse binary
    sign_bit = binary_rep[0]
    exponent_bits = binary_rep[1:9]
    mantissa_bits = binary_rep[9:]
    
    # Create visual representation
    ax1.set_xlim(0, 32)
    ax1.set_ylim(-0.5, 1.5)
    
    # Draw bit boxes with colors
    colors = ['red', 'blue', 'green']
    bit_ranges = [(0, 1), (1, 9), (9, 32)]
    
    for i, (start, end) in enumerate(bit_ranges):
        for j in range(start, end):
            ax1.add_patch(plt.Rectangle((j, 0), 1, 1, facecolor=colors[i], alpha=0.3, edgecolor='black'))
            ax1.text(j + 0.5, 0.5, binary_rep[j], ha='center', va='center', fontweight='bold')
    
    # Labels
    ax1.text(0.5, 1.2, 'Sign', ha='center', fontweight='bold', color=colors[0])
    ax1.text(5, 1.2, 'Exponent', ha='center', fontweight='bold', color=colors[1])
    ax1.text(20.5, 1.2, 'Mantissa', ha='center', fontweight='bold', color=colors[2])
    
    ax1.set_title(f'IEEE 754 Single Precision: {test_value}', fontweight='bold')
    ax1.set_xlabel('Bit Position')
    ax1.set_yticks([])
    ax1.grid(True, alpha=0.3)
    
    # Machine epsilon demonstration
    powers = np.arange(20, 55, 2)  # Reduced range
    eps_values = [2.0**(-p) for p in powers]
    machine_eps = np.finfo(float).eps
    
    ax2.semilogy(powers, eps_values, 'b-', linewidth=2, label='2^(-p)')
    ax2.axhline(y=machine_eps, color='r', linestyle='--', linewidth=2, 
                label=f'Machine ε = {machine_eps:.2e}')
    
    ax2.set_xlabel('Power p')
    ax2.set_ylabel('Epsilon Value')
    ax2.set_title('Machine Epsilon Discovery')
    ax2.legend()
    ax2.grid(True, alpha=0.4)
    
    plt.tight_layout()
    plt.savefig('figures/ieee754_representation.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("Generated: figures/ieee754_representation.png")

def create_roundoff_error_analysis():
    """Generate roundoff error accumulation analysis"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # 1. Error accumulation in summation
    n_values = np.logspace(1, 3, 20)  # Reduced range
    machine_eps = np.finfo(float).eps
    
    theoretical_bound = n_values * machine_eps
    
    ax1.loglog(n_values, theoretical_bound, 'r-', linewidth=2, label='Theoretical Bound')
    ax1.set_xlabel('Number of Terms n')
    ax1.set_ylabel('Error Bound')
    ax1.set_title('Error Accumulation in Summation')
    ax1.legend()
    ax1.grid(True, alpha=0.4)
    
    # 2. Kahan summation comparison
    test_size = 1000
    numbers = np.random.uniform(-1, 1, test_size)
    
    # Different methods
    naive_sum = sum(numbers)
    
    # Kahan sum
    def kahan_sum(arr):
        s = c = 0.0
        for x in arr:
            y = x - c
            t = s + y
            c = (t - s) - y
            s = t
        return s
    
    kahan_result = kahan_sum(numbers)
    reference = np.sum(numbers.astype(np.longdouble))
    
    methods = ['Naive', 'Kahan']
    errors = [abs(naive_sum - float(reference)), abs(kahan_result - float(reference))]
    
    ax2.bar(methods, errors, color=['red', 'green'], alpha=0.7)
    ax2.set_ylabel('Absolute Error')
    ax2.set_title('Summation Algorithm Comparison')
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.4)
    
    # 3. Condition number effect
    condition_numbers = np.logspace(0, 10, 30)
    input_error = 1e-15
    amplified_errors = condition_numbers * input_error
    
    ax3.loglog(condition_numbers, amplified_errors, 'purple', linewidth=2)
    ax3.axhline(y=machine_eps, color='orange', linestyle='--', linewidth=2)
    ax3.set_xlabel('Condition Number')
    ax3.set_ylabel('Output Error')
    ax3.set_title('Error Amplification')
    ax3.grid(True, alpha=0.4)
    
    # 4. Polynomial evaluation
    x = 1.1
    degrees = np.arange(2, 15)
    horner_errors = []
    
    for degree in degrees:
        # Simple polynomial (x-1)^degree
        true_val = (x - 1)**degree
        
        # Horner evaluation simulation
        horner_result = true_val * (1 + degree * machine_eps)  # Simplified error model
        error = abs(horner_result - true_val) / abs(true_val)
        horner_errors.append(error)
    
    ax4.semilogy(degrees, horner_errors, 'g-', linewidth=2, marker='o')
    ax4.axhline(y=machine_eps, color='orange', linestyle='--', linewidth=2)
    ax4.set_xlabel('Polynomial Degree')
    ax4.set_ylabel('Relative Error')
    ax4.set_title('Polynomial Evaluation Error')
    ax4.grid(True, alpha=0.4)
    
    plt.tight_layout()
    plt.savefig('figures/roundoff_error_analysis.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("Generated: figures/roundoff_error_analysis.png")

def create_catastrophic_cancellation():
    """Generate catastrophic cancellation demonstration"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # 1. (1 + x) - 1 for small x
    x_values = np.logspace(-15, -2, 30)
    
    unstable_results = [(1.0 + x) - 1.0 for x in x_values]
    unstable_errors = [abs(result - x) / x for result, x in zip(unstable_results, x_values)]
    
    ax1.loglog(x_values, unstable_errors, 'r-', linewidth=2, label='(1+x)-1')
    ax1.axhline(y=np.finfo(float).eps, color='orange', linestyle='--', linewidth=2, label='Machine ε')
    ax1.set_xlabel('x')
    ax1.set_ylabel('Relative Error')
    ax1.set_title('Catastrophic Cancellation: (1+x)-1')
    ax1.legend()
    ax1.grid(True, alpha=0.4)
    
    # 2. Quadratic formula
    b_values = np.logspace(2, 8, 20)
    a, c = 1, 1
    
    unstable_errors = []
    stable_errors = []
    
    for b in b_values:
        discriminant = b*b - 4*a*c
        
        # Unstable: standard formula
        root_unstable = (-b + np.sqrt(discriminant)) / (2*a)
        
        # Stable: alternative formula
        root_stable = (-2*c) / (b + np.sqrt(discriminant))
        
        # True value (high precision)
        true_root = float((-b + np.sqrt(b*b - 4*a*c, dtype=np.longdouble)) / (2*a))
        
        unstable_error = abs(root_unstable - true_root) / abs(true_root)
        stable_error = abs(root_stable - true_root) / abs(true_root)
        
        unstable_errors.append(unstable_error)
        stable_errors.append(stable_error)
    
    ax2.loglog(b_values, unstable_errors, 'r-', linewidth=2, label='Standard Formula')
    ax2.loglog(b_values, stable_errors, 'g-', linewidth=2, label='Stable Formula')
    ax2.set_xlabel('Coefficient b')
    ax2.set_ylabel('Relative Error')
    ax2.set_title('Quadratic Formula Cancellation')
    ax2.legend()
    ax2.grid(True, alpha=0.4)
    
    # 3. sqrt(1+x) - 1
    x_vals = np.logspace(-15, -2, 30)
    
    unstable_sqrt = [np.sqrt(1 + x) - 1 for x in x_vals]
    stable_sqrt = [x / (np.sqrt(1 + x) + 1) for x in x_vals]
    
    # True values (Taylor series approximation)
    true_sqrt = x_vals/2 - x_vals**2/8
    
    unstable_sqrt_errors = [abs(u - t) / t for u, t in zip(unstable_sqrt, true_sqrt)]
    stable_sqrt_errors = [abs(s - t) / t for s, t in zip(stable_sqrt, true_sqrt)]
    
    ax3.loglog(x_vals, unstable_sqrt_errors, 'r-', linewidth=2, label='√(1+x) - 1')
    ax3.loglog(x_vals, stable_sqrt_errors, 'g-', linewidth=2, label='x/(√(1+x) + 1)')
    ax3.set_xlabel('x')
    ax3.set_ylabel('Relative Error')
    ax3.set_title('Function Evaluation Cancellation')
    ax3.legend()
    ax3.grid(True, alpha=0.4)
    
    # 4. Precision loss visualization
    x = 1e-8
    steps = ['x', '1+x', '(1+x)-1', 'Error']
    values = [x, 1+x, (1+x)-1, abs((1+x)-1-x)]
    
    colors = ['blue', 'orange', 'red', 'purple']
    bars = ax4.bar(range(len(steps)), [abs(v) if v != 0 else 1e-20 for v in values], 
                   color=colors, alpha=0.7)
    
    ax4.set_yscale('log')
    ax4.set_xticks(range(len(steps)))
    ax4.set_xticklabels(steps)
    ax4.set_ylabel('Magnitude')
    ax4.set_title(f'Precision Loss: x = {x:.0e}')
    ax4.grid(True, alpha=0.4)
    
    plt.tight_layout()
    plt.savefig('figures/catastrophic_cancellation.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("Generated: figures/catastrophic_cancellation.png")

def create_stability_analysis():
    """Generate numerical stability analysis visualization"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # 1. Forward vs Backward Error
    condition_numbers = np.logspace(0, 8, 30)
    backward_error = 1e-15
    forward_errors = condition_numbers * backward_error
    
    ax1.loglog(condition_numbers, forward_errors, 'b-', linewidth=2, label='Forward Error')
    ax1.axhline(y=backward_error, color='green', linestyle='--', linewidth=2, label='Backward Error')
    ax1.set_xlabel('Condition Number')
    ax1.set_ylabel('Error Magnitude')
    ax1.set_title('Forward vs Backward Error')
    ax1.legend()
    ax1.grid(True, alpha=0.4)
    
    # 2. Algorithm stability comparison
    algorithms = ['Gaussian\n(no pivot)', 'Gaussian\n(pivot)', 'QR', 'SVD']
    stability_factors = [1e8, 1e2, 1e1, 1e0]
    colors = ['red', 'orange', 'lightgreen', 'darkgreen']
    
    bars = ax2.bar(algorithms, stability_factors, color=colors, alpha=0.7)
    ax2.set_yscale('log')
    ax2.set_ylabel('Error Growth Factor')
    ax2.set_title('Algorithm Stability Comparison')
    ax2.grid(True, alpha=0.4)
    
    # 3. Iterative refinement
    iterations = np.arange(0, 8)
    kappa_values = [1e2, 1e6, 1e10]
    
    for kappa in kappa_values:
        errors = [1e-2 * (0.9**it) * max(1, kappa * np.finfo(float).eps / 1e-2) for it in iterations]
        ax3.semilogy(iterations, errors, 'o-', linewidth=2, label=f'κ = {kappa:.0e}')
    
    ax3.set_xlabel('Iteration')
    ax3.set_ylabel('Relative Error')
    ax3.set_title('Iterative Refinement')
    ax3.legend()
    ax3.grid(True, alpha=0.4)
    
    # 4. Rounding error in polynomial evaluation
    degrees = np.arange(2, 12)
    horner_errors = [degree * np.finfo(float).eps for degree in degrees]
    naive_errors = [degree**2 * np.finfo(float).eps for degree in degrees]
    
    ax4.semilogy(degrees, horner_errors, 'g-', linewidth=2, marker='o', label="Horner's Method")
    ax4.semilogy(degrees, naive_errors, 'r-', linewidth=2, marker='s', label='Naive Evaluation')
    ax4.set_xlabel('Polynomial Degree')
    ax4.set_ylabel('Relative Error')
    ax4.set_title('Polynomial Evaluation Stability')
    ax4.legend()
    ax4.grid(True, alpha=0.4)
    
    plt.tight_layout()
    plt.savefig('figures/stability_analysis.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("Generated: figures/stability_analysis.png")

def demonstrate_key_concepts():
    """Demonstrate key concepts with numerical examples"""
    
    print("=" * 60)
    print("LECTURE 2: KEY CONCEPT DEMONSTRATIONS")
    print("=" * 60)
    
    # Machine epsilon
    eps = np.finfo(float).eps
    print(f"\nMachine epsilon: {eps:.2e}")
    print(f"1 + ε/2 == 1: {1.0 + eps/2 == 1.0}")
    print(f"1 + ε == 1: {1.0 + eps == 1.0}")
    
    # Catastrophic cancellation
    x = 1e-15
    unstable = (1 + x) - 1
    print(f"\nCatastrophic cancellation example:")
    print(f"x = {x}")
    print(f"(1 + x) - 1 = {unstable}")
    print(f"Relative error: {abs(unstable - x) / x:.2e}")
    
    # Quadratic formula
    a, b, c = 1, 1e8, 1
    discriminant = b*b - 4*a*c
    root1_unstable = (-b + np.sqrt(discriminant)) / (2*a)
    root1_stable = (-2*c) / (b + np.sqrt(discriminant))
    
    print(f"\nQuadratic formula comparison:")
    print(f"Unstable root: {root1_unstable}")
    print(f"Stable root: {root1_stable}")
    print(f"Relative difference: {abs(root1_unstable - root1_stable) / abs(root1_stable):.2e}")

def generate_all_lecture2_materials():
    """Generate all materials for Lecture 2"""
    
    print("GENERATING LECTURE 2 MATERIALS")
    print("=" * 40)
    
    setup_directories()
    
    print("\nGenerating figures...")
    create_ieee754_representation()
    create_roundoff_error_analysis()
    create_catastrophic_cancellation()
    create_stability_analysis()
    
    print("\nRunning demonstrations...")
    demonstrate_key_concepts()
    
    print("\n" + "=" * 40)
    print("LECTURE 2 MATERIALS COMPLETE!")
    print("Generated 4 high-quality figures")

if __name__ == "__main__":
    generate_all_lecture2_materials()
