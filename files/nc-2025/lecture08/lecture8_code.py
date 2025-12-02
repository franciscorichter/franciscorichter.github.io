import numpy as np
import matplotlib.pyplot as plt
import time
import os

def load_image(path):
    """Loads an image and converts it to grayscale."""
    if not os.path.exists(path):
        print(f"Error: Image not found at {path}")
        # Create a synthetic image if file missing
        x = np.linspace(-3, 3, 400)
        y = np.linspace(-3, 3, 400)
        X, Y = np.meshgrid(x, y)
        img = np.exp(-(X**2 + Y**2)) * np.cos(X*5 + Y*5)
        img = (img - img.min()) / (img.max() - img.min()) * 255
        return img.astype(np.uint8)

    img = plt.imread(path)
    if img.ndim == 3:
        # RGB to Grayscale
        img = np.dot(img[...,:3], [0.299, 0.587, 0.114])
    
    # Normalize to 0-255
    if img.max() <= 1.0:
        img = (img * 255).astype(np.uint8)
        
    return img

def analyze_svd(img):
    """Performs SVD analysis on the image."""
    print("Computing SVD...")
    U, S, Vt = np.linalg.svd(img, full_matrices=False)
    
    # 1. Plot Singular Values
    plt.figure(figsize=(8, 5))
    plt.semilogy(S, '.-', markersize=2)
    plt.title("Singular Values (Log Scale)")
    plt.xlabel("Index")
    plt.ylabel("Singular Value")
    plt.grid(True)
    plt.savefig("singular_values.png")
    print("Saved singular_values.png")
    
    # 2. Compression Levels
    ranks = [5, 20, 50, 100]
    fig, axes = plt.subplots(1, len(ranks) + 1, figsize=(15, 4))
    
    # Original
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title(f"Original\nRank {min(img.shape)}")
    axes[0].axis('off')
    
    for i, r in enumerate(ranks):
        img_approx = U[:, :r] @ np.diag(S[:r]) @ Vt[:r, :]
        axes[i+1].imshow(img_approx, cmap='gray')
        axes[i+1].set_title(f"Rank {r}")
        axes[i+1].axis('off')
        
    plt.tight_layout()
    plt.savefig("compression_levels.png")
    print("Saved compression_levels.png")

    # 3. Error Analysis
    print("Analyzing Error...")
    errors = []
    k_values = range(1, 151, 5)
    norm_A = np.linalg.norm(img, 'fro')
    
    for k in k_values:
        # Reconstruct
        img_k = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
        error = np.linalg.norm(img - img_k, 'fro') / norm_A
        errors.append(error)
        
    plt.figure(figsize=(8, 5))
    plt.plot(k_values, errors, 'r-')
    plt.title("Relative Reconstruction Error vs. Rank")
    plt.xlabel("Rank k")
    plt.ylabel("Relative Frobenius Error")
    plt.grid(True)
    plt.savefig("reconstruction_error.png")
    print("Saved reconstruction_error.png")

    # 4. Compression Ratio
    print("Calculating Compression Ratios...")
    m, n = img.shape
    original_size = m * n
    ratios = []
    
    for k in k_values:
        # Size of U_k (m*k) + Sigma_k (k) + V_k^T (k*n)
        compressed_size = k * (m + n + 1)
        ratios.append(original_size / compressed_size)
        
    plt.figure(figsize=(8, 5))
    plt.plot(k_values, ratios, 'g-')
    plt.axhline(y=1, color='k', linestyle='--')
    plt.title("Compression Ratio (Original / Compressed)")
    plt.xlabel("Rank k")
    plt.ylabel("Ratio")
    plt.grid(True)
    plt.savefig("compression_ratio.png")
    print("Saved compression_ratio.png")

def benchmark_performance(img):
    """Benchmarks SVD computation time vs resolution."""
    print("Benchmarking Performance...")
    resolutions = [100, 200, 400, 600, 800, 1000, 1200]
    times = []
    
    from skimage.transform import resize
    
    for N in resolutions:
        # Resize image
        img_resized = resize(img, (N, N), anti_aliasing=True)
        
        start_time = time.time()
        np.linalg.svd(img_resized, full_matrices=False)
        end_time = time.time()
        
        times.append(end_time - start_time)
        print(f"Size {N}x{N}: {times[-1]:.4f}s")
        
    plt.figure(figsize=(8, 5))
    plt.loglog(resolutions, times, 'bo-')
    
    # Fit line to estimate complexity slope
    coeffs = np.polyfit(np.log(resolutions), np.log(times), 1)
    slope = coeffs[0]
    
    plt.title(f"SVD Computation Time vs. Size (Slope $\\approx$ {slope:.2f})")
    plt.xlabel("Image Size N (NxN)")
    plt.ylabel("Time (seconds)")
    plt.grid(True, which="both", ls="-")
    plt.savefig("performance_benchmark.png")
    print("Saved performance_benchmark.png")

if __name__ == "__main__":
    # Path to image
    img_path = "../images/clown.png"
    
    # Load
    img = load_image(img_path)
    
    # Analyze
    analyze_svd(img)
    
    # Benchmark
    # Note: Requires scikit-image for resizing. If not present, this might fail.
    try:
        import skimage
        benchmark_performance(img)
    except ImportError:
        print("scikit-image not installed. Skipping benchmark resizing.")
