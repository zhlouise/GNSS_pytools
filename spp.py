import numpy as np

class GNSSPositioning:
    def __init__(self, satellites, observations, initial_position=None):
        self.satellites = satellites
        self.observations = observations
        self.position = initial_position if initial_position is not None else np.zeros(3)
        self.clock_bias = 0.0  # Initialize clock bias

    def compute_position(self):
        num_satellites = self.satellites.shape[0]
        
        # Construct the design matrix and the observation vector
        A = np.zeros((num_satellites, 5))  # 5 columns for x, y, z, range, and clock bias
        L = np.zeros(num_satellites)  # Observation vector
        
        for i in range(num_satellites):
            sat_pos = self.satellites[i]
            range_estimate = np.linalg.norm(self.position - sat_pos) + self.clock_bias  # Include clock bias
            A[i, :3] = (self.position - sat_pos) / np.linalg.norm(self.position - sat_pos)  # Normalized direction
            A[i, 3] = -1  # For the range equation
            A[i, 4] = 1  # For the clock bias
            L[i] = self.observations[i] - range_estimate  # Pseudorange residual
        
        # Solve the least squares problem
        delta = np.linalg.pinv(A.T @ A) @ (A.T @ L)
        
        # Update the position estimate
        self.position += delta[:3]
        self.clock_bias += delta[3]  # Update clock bias
        
        # Iterate until convergence or a maximum number of iterations
        for _ in range(10):  # Example: 10 iterations
            for i in range(num_satellites):
                sat_pos = self.satellites[i]
                range_estimate = np.linalg.norm(self.position - sat_pos) + self.clock_bias  # Include clock bias
                A[i, :3] = (self.position - sat_pos) / np.linalg.norm(self.position - sat_pos)  # Normalized direction
                A[i, 3] = -1  # For the range equation
                A[i, 4] = 1  # For the clock bias
                L[i] = self.observations[i] - range_estimate  # Pseudorange residual
            
            delta = np.linalg.pinv(A.T @ A) @ (A.T @ L)
            self.position += delta[:3]
            self.clock_bias += delta[3]  # Update clock bias
        
        return self.position, self.clock_bias  # Return both position and clock bias

if __name__ == "__main__":
    # Example satellite positions (x, y, z) in meters
    satellites = np.array([[12456300, -18234500, 14567200],
                            [-21345200, -8765400, 11234800],
                            [15678900, 17890300, -9876500],
                            [-8976500, 22345100, 10234600],
                            [19876400, 5432100, -16789300]])
            
    # Example pseudorange observations in meters
    observations = np.array([21342567.3, 22876432.1, 20654321.8, 23456789.5, 21987654.2])
    
    # Input your initial position estimate (x, y, z) in meters
    initial_position = np.array([1348634.100716, -4703246.042294, 4078049.850961])
            
    # Create an instance of the GNSSPositioning class
    gnss = GNSSPositioning(satellites, observations, initial_position)
            
    # Compute the position
    estimated_position, clock_bias = gnss.compute_position()
            
    # Print the estimated position and clock bias
    print("Estimated Position (x, y, z):", estimated_position)
    print("Estimated Clock Bias:", clock_bias)