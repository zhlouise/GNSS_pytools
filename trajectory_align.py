import numpy as np
from scipy.spatial import KDTree
from scipy.interpolate import CubicSpline

import matplotlib.pyplot as plt

def generate_2d_trajectory(n_points=100):
    # Generate a smooth random 2D trajectory using a random cubic spline
    t_vals = np.linspace(0, 1, n_points)
    # Random control points for x and y
    control_t = np.linspace(0, 1, 6)
    control_x = np.random.uniform(-5, 5, size=6)
    control_y = np.random.uniform(-5, 5, size=6)
    spline_x = CubicSpline(control_t, control_x)
    spline_y = CubicSpline(control_t, control_y)
    x = spline_x(t_vals)
    y = spline_y(t_vals)
    traj = np.column_stack((x, y))
    # Generate random rotation angle and translation
    theta = np.random.uniform(0, 2 * np.pi)
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    t = np.random.uniform(-2, 2, size=2)
    # Apply rotation and translation (no noise)
    traj_transformed = traj @ R.T + t
    return traj, traj_transformed

def align_least_squares(A, B):
    # A, B: Nx2 arrays
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    A_centered = A - centroid_A
    B_centered = B - centroid_B
    # Solve for rotation
    H = A_centered.T @ B_centered
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T
    if np.linalg.det(R) < 0:
        Vt[1,:] *= -1
        R = Vt.T @ U.T
    t = centroid_B - centroid_A @ R
    A_aligned = A @ R + t
    return A_aligned, R, t

def align_svd(A, B):
    # Procrustes analysis via SVD
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    A_centered = A - centroid_A
    B_centered = B - centroid_B
    M = B_centered.T @ A_centered
    U, _, Vt = np.linalg.svd(M)
    R = U @ Vt
    t = centroid_B - centroid_A @ R
    A_aligned = A @ R + t
    return A_aligned, R, t

def align_icp(A, B, max_iter=20, tol=1e-6):
    # Iterative Closest Point
    A_aligned = A.copy()
    prev_error = None
    for i in range(max_iter):
        tree = KDTree(B)
        distances, indices = tree.query(A_aligned)
        B_matched = B[indices]
        # Align using least squares
        A_aligned_new, R, t = align_least_squares(A_aligned, B_matched)
        error = np.mean(distances)
        if prev_error is not None and abs(prev_error - error) < tol:
            break
        prev_error = error
        A_aligned = A_aligned_new
    return A_aligned, R, t

# Generate trajectories
A, B = generate_2d_trajectory()

# Align using different methods
A_ls, R_ls, t_ls = align_least_squares(A, B)
A_svd, R_svd, t_svd = align_svd(A, B)
A_icp, R_icp, t_icp = align_icp(A, B)

# Plot results
plt.figure(figsize=(10, 8))
plt.plot(A[:,0], A[:,1], 'k--', label='Original Trajectory')
plt.plot(B[:,0], B[:,1], 'r--', label='Transformed Trajectory')
plt.plot(A_ls[:,0], A_ls[:,1], 'b-', label='Least Squares Aligned')
plt.plot(A_svd[:,0], A_svd[:,1], 'g-', label='SVD Aligned')
plt.plot(A_icp[:,0], A_icp[:,1], 'm-', label='ICP Aligned')
plt.legend()
plt.axis('equal')
plt.title('2D Trajectory Alignment')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()