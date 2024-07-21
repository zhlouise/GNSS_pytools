# AI written code, not how it actually works

import math

def calculate_pseudorange_error(rover_obs, reference_obs, rover_coords, reference_coords):
    # Calculate the Euclidean distance between the rover and reference station
    distance = math.sqrt((rover_coords[0] - reference_coords[0])**2 + (rover_coords[1] - reference_coords[1])**2 + (rover_coords[2] - reference_coords[2])**2)
    
    # Calculate the pseudorange error
    pseudorange_error = []
    for i in range(len(rover_obs)):
        error = rover_obs[i] - reference_obs[i] - distance
        pseudorange_error.append(error)
    
    return pseudorange_error

# Example usage
rover_obs = [10.5, 12.3, 9.8, 11.2]
reference_obs = [9.7, 11.8, 9.2, 10.9]
rover_coords = [0, 0, 0]
reference_coords = [1, 1, 1]

error = calculate_pseudorange_error(rover_obs, reference_obs, rover_coords, reference_coords)
print(error)