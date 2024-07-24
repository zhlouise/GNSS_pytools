import georinex as gr
import numpy as np
from datetime import datetime

def get_pseudoranges(rinex_file):
    # Read the RINEX file
    obs = gr.load(rinex_file)
    
    # Get the list of available measurement types
    meas_types = obs.data_vars
    
    # Look for pseudorange measurements (usually C1C, C1P, or C1)
    pr_types = [m for m in meas_types if m.startswith('C')]
    
    if not pr_types:
        print("No pseudorange measurements found in the file.")
        return None
    
    # Use the first available pseudorange type
    pr_type = pr_types[0]
    
    # Extract pseudorange data
    pseudoranges = obs[pr_type].values
    
    # Get timestamps
    timestamps = obs.time.values
    
    # Get satellite PRNs
    satellites = obs[pr_type].sv.values
    
    return timestamps, satellites, pseudoranges

def main():
    rinex_file = 'path/to/your/rinex_file.rnx'  # Replace with your RINEX file path
    
    result = get_pseudoranges(rinex_file)
    
    if result:
        timestamps, satellites, pseudoranges = result
        
        print(f"Pseudorange measurements from {rinex_file}:")
        for i, time in enumerate(timestamps):
            print(f"\nTimestamp: {time}")
            for j, sat in enumerate(satellites):
                if not np.isnan(pseudoranges[i, j]):
                    print(f"  Satellite {sat}: {pseudoranges[i, j]:.3f} meters")

if __name__ == "__main__":
    main()