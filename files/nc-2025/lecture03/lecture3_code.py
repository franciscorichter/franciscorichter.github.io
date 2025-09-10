"""
NUMERICAL COMPUTING - LECTURE 3: COMPLETE CODE PACKAGE
Root-Finding Methods and Nonlinear Equations
Università della Svizzera Italiana
Author: Francisco Richter Mendoza
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Configuration for high-quality figures
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'figure.dpi': 150,
    'savefig.dpi': 200
})

def setup_directories():
    import os
    os.makedirs('figures', exist_ok=True)
    print("Created figures directory")

# ================================================
# ROOT-FINDING ALGORITHMS
# ================================================

def bisection_method(f, a, b, tol=1e-10, max_iter=100):
    """
    Bisection method for root finding
    
    Mathematical foundation:
    If f is continuous on [a,b] and f(a)f(b) < 0, then by IVT,
    there exists c ∈ (a,b) such that f(c) = 0
    
    Convergence: |x_n - x*| ≤ (b-a)/2^n
    """
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    
    iterations = []
    errors = []
    
    for i in range(max_iter):
        c = (a + b) / 2
        iterations.append(c)
        
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c, iterations, errors
        
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
            
        errors.append((b - a) / 2)
    
    return c, iterations, errors

def newton_method(f, df, x0, tol=1e-10, max_iter=100):
    """
    Newton's method for root finding
    
    Mathematical foundation:
    x_{k+1} = x_k - f(x_k)/f'(x_k)
    
    Convergence: Quadratic if f'(x*) ≠ 0
    lim |x_{k+1} - x*|/|x_k - x*|² = |f''(x*)|/(2|f'(x*)|)
    """
    iterations = [x0]
    errors = []
    
    x = x0
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        
        if abs(dfx) < 1e-15:
            raise ValueError("Derivative too small, method may fail")
        
        x_new = x - fx / dfx
        iterations.append(x_new)
        
        if abs(x_new - x) < tol:
            return x_new, iterations, errors
        
        errors.append(abs(x_new - x))
        x = x_new
    
    return x, iterations, errors

def secant_method(f, x0, x1, tol=1e-10, max_iter=100):
    """
    Secant method for root finding
    
    Mathematical foundation:
    x_{k+1} = x_k - f(x_k) * (x_k - x_{k-1})/(f(x_k) - f(x_{k-1}))
    
    Convergence: Superlinear with order φ = (1+√5)/2 ≈ 1.618
    """
    iterations = [x0, x1]
    errors = []
    
    for i in range(max_iter):
        fx0, fx1 = f(x0), f(x1)
        
        if abs(fx1 - fx0) < 1e-15:
            raise ValueError("Function values too close, method may fail")
        
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        iterations.append(x2)
        
        if abs(x2 - x1) < tol:
            return x2, iterations, errors
        
        errors.append(abs(x2 - x1))
        x0, x1 = x1, x2
    
    return x1, iterations, errors

def fixed_point_iteration(g, x0, tol=1e-10, max_iter=100):
    """
    Fixed-point iteration: x_{k+1} = g(x_k)
    
    Convergence condition: |g'(x*)| < 1 for linear convergence
    If g'(x*) = 0, then quadratic convergence
    """
    iterations = [x0]
    errors = []
    
    x = x0
    for i in range(max_iter):
        x_new = g(x)
        iterations.append(x_new)
        
        if abs(x_new - x) < tol:
            return x_new, iterations, errors
        
        errors.append(abs(x_new - x))
        x = x_new
    
    return x, iterations, errors

# ================================================
# VISUALIZATION FUNCTIONS
# ================================================

def create_method_comparison():
    """Generate comprehensive comparison of root-finding methods"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Test function: f(x) = x³ - 2x - 5
    def f(x):
        return x**3 - 2*x - 5
    
    def df(x):
        return 3*x**2 - 2
    
    # 1. Bisection method visualization
    x = np.linspace(1.5, 3, 1000)
    y = f(x)
    
    ax1.plot(x, y, 'b-', linewidth=2, label='f(x) = x³ - 2x - 5')
    ax1.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax1.grid(True, alpha=0.3)
    
    # Show bisection steps
    a, b = 2.0, 3.0
    for i in range(4):
        c = (a + b) / 2
        fc = f(c)
        ax1.plot([c, c], [0, fc], 'r--', alpha=0.7)
        ax1.plot(c, fc, 'ro', markersize=6)
        ax1.text(c, fc + 0.5, f'x_{i}', ha='center', fontsize=10)
        
        if f(a) * fc < 0:
            b = c
        else:
            a = c
    
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.set_title('Bisection Method Steps')
    ax1.legend()
    
    # 2. Newton's method visualization
    ax2.plot(x, y, 'b-', linewidth=2, label='f(x) = x³ - 2x - 5')
    ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax2.grid(True, alpha=0.3)
    
    # Show Newton steps
    x_newton = 3.0
    for i in range(3):
        fx = f(x_newton)
        dfx = df(x_newton)
        
        # Tangent line
        x_tan = np.linspace(x_newton - 0.5, x_newton + 0.5, 100)
        y_tan = fx + dfx * (x_tan - x_newton)
        ax2.plot(x_tan, y_tan, 'g--', alpha=0.7, linewidth=1)
        
        # Current point and next point
        ax2.plot(x_newton, fx, 'ro', markersize=8)
        x_next = x_newton - fx / dfx
        ax2.plot([x_next, x_next], [0, f(x_next)], 'r:', alpha=0.7)
        ax2.text(x_newton, fx + 1, f'x_{i}', ha='center', fontsize=10)
        
        x_newton = x_next
    
    ax2.set_xlabel('x')
    ax2.set_ylabel('f(x)')
    ax2.set_title("Newton's Method Steps")
    ax2.legend()
    
    # 3. Convergence rate comparison
    methods = ['Bisection', 'Secant', 'Newton']
    iterations = [20, 6, 4]  # Typical iterations to reach 1e-10 accuracy
    colors = ['red', 'orange', 'green']
    
    bars = ax3.bar(methods, iterations, color=colors, alpha=0.7)
    ax3.set_ylabel('Iterations to Convergence')
    ax3.set_title('Convergence Speed Comparison')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Add convergence order annotations
    orders = ['Linear (p=1)', 'Superlinear (p≈1.618)', 'Quadratic (p=2)']
    for bar, order in zip(bars, orders):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                order, ha='center', va='bottom', fontsize=9)
    
    # 4. Fixed-point iteration visualization
    def g(x):
        return np.cbrt(2*x + 5)  # x = ∛(2x + 5) from x³ - 2x - 5 = 0
    
    x_range = np.linspace(1.5, 3, 1000)
    ax4.plot(x_range, x_range, 'k--', alpha=0.5, label='y = x')
    ax4.plot(x_range, g(x_range), 'b-', linewidth=2, label='g(x) = ∛(2x + 5)')
    ax4.grid(True, alpha=0.3)
    
    # Cobweb plot
    x_fp = 2.5
    for i in range(5):
        gx = g(x_fp)
        ax4.plot([x_fp, x_fp], [x_fp, gx], 'r-', alpha=0.7)
        ax4.plot([x_fp, gx], [gx, gx], 'r-', alpha=0.7)
        ax4.plot(x_fp, gx, 'ro', markersize=4)
        x_fp = gx
    
    ax4.set_xlabel('x')
    ax4.set_ylabel('g(x)')
    ax4.set_title('Fixed-Point Iteration (Cobweb Plot)')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('figures/root_finding_methods.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("Generated: figures/root_finding_methods.png")

def create_convergence_analysis():
    """Generate detailed convergence analysis visualization"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Test function: f(x) = x² - 2 (finding √2)
    def f(x):
        return x**2 - 2
    
    def df(x):
        return 2*x
    
    true_root = np.sqrt(2)
    
    # 1. Error vs iteration for different methods
    x0_bisection_a, x0_bisection_b = 1.0, 2.0
    _, bisection_its, _ = bisection_method(f, x0_bisection_a, x0_bisection_b, tol=1e-12)
    bisection_errors = [abs(x - true_root) for x in bisection_its]
    
    x0_newton = 2.0
    _, newton_its, _ = newton_method(f, df, x0_newton, tol=1e-12)
    newton_errors = [abs(x - true_root) for x in newton_its]
    
    x0_secant, x1_secant = 1.0, 2.0
    _, secant_its, _ = secant_method(f, x0_secant, x1_secant, tol=1e-12)
    secant_errors = [abs(x - true_root) for x in secant_its]
    
    ax1.semilogy(range(len(bisection_errors)), bisection_errors, 'r-o', 
                 label='Bisection', markersize=4)
    ax1.semilogy(range(len(newton_errors)), newton_errors, 'g-s', 
                 label='Newton', markersize=4)
    ax1.semilogy(range(len(secant_errors)), secant_errors, 'b-^', 
                 label='Secant', markersize=4)
    
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Absolute Error')
    ax1.set_title('Convergence Rate Comparison')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Convergence order verification
    # For Newton's method, plot |e_{k+1}| vs |e_k|²
    if len(newton_errors) > 2:
        newton_e_k = newton_errors[:-1]
        newton_e_k1 = newton_errors[1:]
        newton_e_k_squared = [e**2 for e in newton_e_k[:-1]]
        newton_e_k1_trimmed = newton_e_k1[:-1]
        
        ax2.loglog(newton_e_k_squared, newton_e_k1_trimmed, 'go-', 
                   label='Newton: |e_{k+1}| vs |e_k|²', markersize=6)
        
        # Theoretical slope = 1 for quadratic convergence
        if len(newton_e_k_squared) > 1:
            x_theory = np.array(newton_e_k_squared)
            y_theory = x_theory * (newton_e_k1_trimmed[0] / newton_e_k_squared[0])
            ax2.loglog(x_theory, y_theory, 'k--', alpha=0.7, label='Slope = 1')
    
    ax2.set_xlabel('|e_k|²')
    ax2.set_ylabel('|e_{k+1}|')
    ax2.set_title('Quadratic Convergence Verification')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Basin of attraction for Newton's method
    def complex_newton_basin():
        # For f(z) = z³ - 1, roots are 1, ω, ω² where ω = e^(2πi/3)
        roots = [1, np.exp(2j*np.pi/3), np.exp(4j*np.pi/3)]
        
        x = np.linspace(-2, 2, 400)
        y = np.linspace(-2, 2, 400)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j*Y
        
        basin = np.zeros_like(Z, dtype=int)
        
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]):
                z = Z[i, j]
                for _ in range(50):  # Max iterations
                    if abs(z**3 - 1) < 1e-6:
                        break
                    dz = 3*z**2
                    if abs(dz) > 1e-10:
                        z = z - (z**3 - 1) / dz
                
                # Determine which root it converged to
                distances = [abs(z - root) for root in roots]
                basin[i, j] = np.argmin(distances)
        
        return X, Y, basin
    
    X, Y, basin = complex_newton_basin()
    colors = ['red', 'green', 'blue']
    ax3.contourf(X, Y, basin, levels=[-0.5, 0.5, 1.5, 2.5], colors=colors, alpha=0.7)
    ax3.set_xlabel('Real')
    ax3.set_ylabel('Imaginary')
    ax3.set_title('Newton Basins: f(z) = z³ - 1')
    ax3.grid(True, alpha=0.3)
    ax3.set_aspect('equal')
    
    # 4. Multiple root behavior
    # f(x) = (x-1)²(x-2) has double root at x=1, simple root at x=2
    def f_multiple(x):
        return (x - 1)**2 * (x - 2)
    
    def df_multiple(x):
        return 2*(x - 1)*(x - 2) + (x - 1)**2
    
    x_mult = np.linspace(0, 3, 1000)
    y_mult = f_multiple(x_mult)
    
    ax4.plot(x_mult, y_mult, 'b-', linewidth=2, label='f(x) = (x-1)²(x-2)')
    ax4.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax4.axvline(x=1, color='r', linestyle=':', alpha=0.7, label='Double root at x=1')
    ax4.axvline(x=2, color='g', linestyle=':', alpha=0.7, label='Simple root at x=2')
    
    # Show Newton convergence to double root (slow)
    x_newton_mult = 0.5
    for i in range(5):
        fx = f_multiple(x_newton_mult)
        dfx = df_multiple(x_newton_mult)
        if abs(dfx) > 1e-10:
            ax4.plot(x_newton_mult, fx, 'ro', markersize=6)
            x_newton_mult = x_newton_mult - fx / dfx
    
    ax4.set_xlabel('x')
    ax4.set_ylabel('f(x)')
    ax4.set_title('Multiple Root Convergence')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figures/convergence_analysis.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("Generated: figures/convergence_analysis.png")

def create_practical_considerations():
    """Generate visualization of practical implementation issues"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Sensitivity to initial guess
    def f_sensitive(x):
        return x**3 - 2*x - 5
    
    def df_sensitive(x):
        return 3*x**2 - 2
    
    x = np.linspace(0, 4, 1000)
    y = f_sensitive(x)
    
    ax1.plot(x, y, 'b-', linewidth=2, label='f(x) = x³ - 2x - 5')
    ax1.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax1.grid(True, alpha=0.3)
    
    # Show different starting points
    initial_guesses = [0.5, 1.5, 2.5, 3.5]
    colors = ['red', 'green', 'orange', 'purple']
    
    for i, (x0, color) in enumerate(zip(initial_guesses, colors)):
        try:
            root, iterations, _ = newton_method(f_sensitive, df_sensitive, x0, max_iter=20)
            ax1.plot(x0, f_sensitive(x0), 'o', color=color, markersize=8, 
                    label=f'x₀={x0} → x*={root:.3f}')
        except:
            ax1.plot(x0, f_sensitive(x0), 'x', color=color, markersize=8, 
                    label=f'x₀={x0} → Diverged')
    
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.set_title('Sensitivity to Initial Guess')
    ax1.legend()
    
    # 2. Derivative issues
    def f_derivative_issue(x):
        return np.tanh(10*x)  # Very flat near x=0
    
    def df_derivative_issue(x):
        return 10 * (1 - np.tanh(10*x)**2)
    
    x_deriv = np.linspace(-1, 1, 1000)
    y_deriv = f_derivative_issue(x_deriv)
    dy_deriv = df_derivative_issue(x_deriv)
    
    ax2.plot(x_deriv, y_deriv, 'b-', linewidth=2, label='f(x) = tanh(10x)')
    ax2_twin = ax2.twinx()
    ax2_twin.plot(x_deriv, dy_deriv, 'r--', linewidth=2, label="f'(x)")
    
    ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax2.set_xlabel('x')
    ax2.set_ylabel('f(x)', color='b')
    ax2_twin.set_ylabel("f'(x)", color='r')
    ax2.set_title('Small Derivative Issues')
    ax2.grid(True, alpha=0.3)
    
    # Show problematic region
    ax2.axvspan(-0.2, 0.2, alpha=0.2, color='yellow', label='Problematic region')
    ax2.legend(loc='upper left')
    ax2_twin.legend(loc='upper right')
    
    # 3. Oscillatory behavior
    def f_oscillatory(x):
        return x * np.sin(1/x) if x != 0 else 0
    
    def df_oscillatory(x):
        if x != 0:
            return np.sin(1/x) - np.cos(1/x)/x
        else:
            return 0
    
    x_osc = np.linspace(-0.5, 0.5, 2000)
    x_osc = x_osc[x_osc != 0]  # Remove x=0
    y_osc = [f_oscillatory(xi) for xi in x_osc]
    
    ax3.plot(x_osc, y_osc, 'b-', linewidth=1, label='f(x) = x sin(1/x)')
    ax3.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax3.grid(True, alpha=0.3)
    
    # Show Newton iterations that might oscillate
    x_newton_osc = 0.1
    newton_points_x = [x_newton_osc]
    newton_points_y = [f_oscillatory(x_newton_osc)]
    
    for i in range(10):
        fx = f_oscillatory(x_newton_osc)
        dfx = df_oscillatory(x_newton_osc)
        if abs(dfx) > 1e-6 and abs(x_newton_osc) > 1e-6:
            x_newton_osc = x_newton_osc - fx / dfx
            if abs(x_newton_osc) < 0.5:
                newton_points_x.append(x_newton_osc)
                newton_points_y.append(f_oscillatory(x_newton_osc))
        else:
            break
    
    ax3.plot(newton_points_x, newton_points_y, 'ro-', markersize=4, alpha=0.7)
    ax3.set_xlabel('x')
    ax3.set_ylabel('f(x)')
    ax3.set_title('Oscillatory Function Challenges')
    ax3.legend()
    
    # 4. Condition number effects
    def condition_analysis():
        # For f(x) = x^n - a, condition number is |x*|/|f'(x*)|
        powers = np.arange(2, 10)
        a = 2
        condition_numbers = []
        
        for n in powers:
            root = a**(1/n)  # True root
            derivative = n * root**(n-1)
            condition = abs(root) / abs(derivative)
            condition_numbers.append(condition)
        
        return powers, condition_numbers
    
    powers, cond_nums = condition_analysis()
    
    ax4.semilogy(powers, cond_nums, 'bo-', linewidth=2, markersize=6)
    ax4.set_xlabel('Power n in f(x) = xⁿ - 2')
    ax4.set_ylabel('Condition Number')
    ax4.set_title('Root Condition Number vs Function Power')
    ax4.grid(True, alpha=0.3)
    
    # Add annotations
    for i, (p, c) in enumerate(zip(powers, cond_nums)):
        if i % 2 == 0:  # Annotate every other point
            ax4.annotate(f'n={p}\nκ={c:.2f}', (p, c), 
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=9, ha='left')
    
    plt.tight_layout()
    plt.savefig('figures/practical_considerations.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("Generated: figures/practical_considerations.png")

def create_advanced_methods():
    """Generate visualization of advanced root-finding techniques"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Hybrid methods (Brent's method simulation)
    def f_hybrid(x):
        return x**3 - 2*x - 5
    
    x = np.linspace(1.5, 3, 1000)
    y = f_hybrid(x)
    
    ax1.plot(x, y, 'b-', linewidth=2, label='f(x) = x³ - 2x - 5')
    ax1.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax1.grid(True, alpha=0.3)
    
    # Simulate hybrid approach: start with bisection, switch to faster method
    a, b = 2.0, 3.0
    bisection_steps = []
    
    # Bisection phase
    for i in range(3):
        c = (a + b) / 2
        bisection_steps.append(c)
        ax1.plot(c, f_hybrid(c), 'ro', markersize=6, alpha=0.7)
        if f_hybrid(a) * f_hybrid(c) < 0:
            b = c
        else:
            a = c
    
    # Switch to Newton-like method
    x_newton = bisection_steps[-1]
    newton_steps = [x_newton]
    for i in range(2):
        fx = f_hybrid(x_newton)
        dfx = 3*x_newton**2 - 2
        x_newton = x_newton - fx / dfx
        newton_steps.append(x_newton)
        ax1.plot(x_newton, f_hybrid(x_newton), 'gs', markersize=6, alpha=0.7)
    
    ax1.plot([], [], 'ro', label='Bisection phase', markersize=6)
    ax1.plot([], [], 'gs', label='Newton phase', markersize=6)
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.set_title('Hybrid Method Strategy')
    ax1.legend()
    
    # 2. Deflation for multiple roots
    def polynomial_with_known_roots(x):
        # p(x) = (x-1)(x-2)(x-3) = x³ - 6x² + 11x - 6
        return x**3 - 6*x**2 + 11*x - 6
    
    x_poly = np.linspace(0, 4, 1000)
    y_poly = polynomial_with_known_roots(x_poly)
    
    ax2.plot(x_poly, y_poly, 'b-', linewidth=2, label='p(x) = (x-1)(x-2)(x-3)')
    ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    
    # Mark the three roots
    roots = [1, 2, 3]
    for root in roots:
        ax2.plot(root, 0, 'ro', markersize=8)
        ax2.annotate(f'x = {root}', (root, 0), xytext=(0, 20), 
                    textcoords='offset points', ha='center')
    
    # Show deflated polynomials
    def deflated_poly1(x):  # After removing (x-1)
        return x**2 - 5*x + 6
    
    def deflated_poly2(x):  # After removing (x-1) and (x-2)
        return x - 3
    
    ax2.plot(x_poly, deflated_poly1(x_poly), 'g--', alpha=0.7, 
             label='After deflating x=1')
    ax2.plot(x_poly, deflated_poly2(x_poly), 'r:', alpha=0.7, 
             label='After deflating x=1,2')
    
    ax2.set_xlabel('x')
    ax2.set_ylabel('p(x)')
    ax2.set_title('Polynomial Deflation')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Convergence acceleration (Aitken's Δ² method)
    def slow_converging_sequence():
        # Generate a slowly converging sequence
        n = np.arange(1, 20)
        x_n = 1 + 1/n  # Converges to 1
        
        # Apply Aitken acceleration
        x_accelerated = []
        for i in range(len(x_n) - 2):
            x0, x1, x2 = x_n[i], x_n[i+1], x_n[i+2]
            if (x2 - 2*x1 + x0) != 0:
                x_acc = x0 - (x1 - x0)**2 / (x2 - 2*x1 + x0)
                x_accelerated.append(x_acc)
        
        return n, x_n, x_accelerated
    
    n, x_orig, x_acc = slow_converging_sequence()
    
    ax3.plot(n, x_orig, 'bo-', label='Original sequence', markersize=4)
    ax3.plot(n[:-2], x_acc, 'rs-', label="Aitken's acceleration", markersize=4)
    ax3.axhline(y=1, color='k', linestyle='--', alpha=0.5, label='True limit')
    
    ax3.set_xlabel('Iteration n')
    ax3.set_ylabel('x_n')
    ax3.set_title("Aitken's Δ² Acceleration")
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Stability regions for different methods
    def stability_analysis():
        # For f(x) = x² - a, analyze stability of different methods
        # as a function of the multiplier in the iteration
        
        alphas = np.linspace(0.1, 2, 100)
        stability_newton = []
        stability_fixed = []
        
        for alpha in alphas:
            # Newton: x_{k+1} = x_k - f(x_k)/f'(x_k)
            # For f(x) = x² - a, this gives x_{k+1} = (x_k + a/x_k)/2
            # Stability analysis around x* = √a
            
            # Fixed point: x_{k+1} = x_k - α(x_k² - a)
            # Derivative at fixed point x* = √a is 1 - 2α√a
            # Stable if |1 - 2α√a| < 1
            
            a = 1  # For simplicity
            sqrt_a = 1
            
            # Newton is always stable for simple roots
            stability_newton.append(1)  # Always stable
            
            # Fixed point stability
            derivative = abs(1 - 2*alpha*sqrt_a)
            stability_fixed.append(1 if derivative < 1 else 0)
        
        return alphas, stability_newton, stability_fixed
    
    alphas, stab_newton, stab_fixed = stability_analysis()
    
    ax4.fill_between(alphas, 0, stab_fixed, alpha=0.3, color='blue', 
                     label='Fixed-point stable region')
    ax4.axhline(y=1, color='green', linewidth=3, label='Newton (always stable)')
    ax4.axvline(x=1, color='red', linestyle='--', alpha=0.7, 
                label='Optimal α = 1')
    
    ax4.set_xlabel('Parameter α')
    ax4.set_ylabel('Stability')
    ax4.set_title('Stability Regions: x_{k+1} = x_k - α(x_k² - 1)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(-0.1, 1.5)
    
    plt.tight_layout()
    plt.savefig('figures/advanced_methods.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("Generated: figures/advanced_methods.png")

# ================================================
# EDUCATIONAL DEMONSTRATIONS
# ================================================

def demonstrate_key_concepts():
    """Demonstrate key concepts with numerical examples"""
    
    print("=" * 60)
    print("LECTURE 3: ROOT-FINDING METHODS DEMONSTRATIONS")
    print("=" * 60)
    
    # Test function: f(x) = x³ - 2x - 5
    def f(x):
        return x**3 - 2*x - 5
    
    def df(x):
        return 3*x**2 - 2
    
    print(f"\nTest function: f(x) = x³ - 2x - 5")
    print(f"Looking for root in [2, 3]")
    
    # Bisection method
    print(f"\n1. BISECTION METHOD:")
    root_bis, its_bis, _ = bisection_method(f, 2.0, 3.0, tol=1e-10)
    print(f"   Root found: {root_bis:.10f}")
    print(f"   Iterations: {len(its_bis)}")
    print(f"   Final error: {abs(f(root_bis)):.2e}")
    
    # Newton's method
    print(f"\n2. NEWTON'S METHOD:")
    root_newton, its_newton, _ = newton_method(f, df, 2.5, tol=1e-10)
    print(f"   Root found: {root_newton:.10f}")
    print(f"   Iterations: {len(its_newton)}")
    print(f"   Final error: {abs(f(root_newton)):.2e}")
    
    # Secant method
    print(f"\n3. SECANT METHOD:")
    root_secant, its_secant, _ = secant_method(f, 2.0, 3.0, tol=1e-10)
    print(f"   Root found: {root_secant:.10f}")
    print(f"   Iterations: {len(its_secant)}")
    print(f"   Final error: {abs(f(root_secant)):.2e}")
    
    # Convergence rate analysis
    print(f"\n4. CONVERGENCE ANALYSIS:")
    print(f"   Bisection: Linear convergence, {len(its_bis)} iterations")
    print(f"   Newton: Quadratic convergence, {len(its_newton)} iterations")
    print(f"   Secant: Superlinear convergence, {len(its_secant)} iterations")
    
    # Fixed-point iteration
    print(f"\n5. FIXED-POINT ITERATION:")
    def g(x):
        return np.cbrt(2*x + 5)  # From x³ - 2x - 5 = 0
    
    root_fp, its_fp, _ = fixed_point_iteration(g, 2.5, tol=1e-10)
    print(f"   Root found: {root_fp:.10f}")
    print(f"   Iterations: {len(its_fp)}")
    print(f"   Final error: {abs(f(root_fp)):.2e}")

def generate_all_lecture3_materials():
    """Generate all materials for Lecture 3"""
    
    print("GENERATING LECTURE 3 MATERIALS")
    print("=" * 40)
    
    setup_directories()
    
    print("\nGenerating figures...")
    create_method_comparison()
    create_convergence_analysis()
    create_practical_considerations()
    create_advanced_methods()
    
    print("\nRunning demonstrations...")
    demonstrate_key_concepts()
    
    print("\n" + "=" * 40)
    print("LECTURE 3 MATERIALS COMPLETE!")
    print("Generated 4 comprehensive figures")

if __name__ == "__main__":
    generate_all_lecture3_materials()
