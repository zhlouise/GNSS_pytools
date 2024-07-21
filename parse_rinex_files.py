import georinex as gr
import numpy as np
from datetime import datetime, timedelta

def parse_rinex_files(obs_file, nav_file):
    # Read observation file
    obs = gr.load(obs_file)
    
    # Read navigation file
    nav = gr.load(nav_file)
    
    # Get list of satellites
    satellites = obs.sv.values
    
    results = []
    
    for sat in satellites:
        # Extract pseudorange (C1C)
        if 'C1C' in obs:
            pseudorange = obs['C1C'].sel(sv=sat).dropna(dim='time')
        else:
            print(f"C1C not found for satellite {sat}")
            continue
        
        # Extract carrier-to-noise ratio (S1C)
        if 'S1C' in obs:
            cnr = obs['S1C'].sel(sv=sat).dropna(dim='time')
        else:
            print(f"S1C not found for satellite {sat}")
            continue
        
        # Calculate elevation angle
        times = pseudorange.time.values
        elevations = []
        
        for time in times:
            # Get satellite position
            sat_pos = gr.sat_position(nav, time, sat)
            if sat_pos is None:
                continue
            
            # Get receiver position (assuming it's constant)
            rcv_pos = obs.position
            
            # Calculate elevation angle
            sat_vec = sat_pos - rcv_pos
            sat_range = np.linalg.norm(sat_vec)
            elev = np.arcsin(sat_vec[2] / sat_range)
            elevations.append(np.degrees(elev))
        
        # Combine results
        for pr, cn, el, t in zip(pseudorange.values, cnr.values, elevations, times):
            results.append({
                'satellite': sat,
                'time': t,
                'pseudorange': pr,
                'cnr': cn,
                'elevation': el
            })
    
    return results

# # Example usage
# obs_file = 'path/to/your/observation.rnx'
# nav_file = 'path/to/your/navigation.rnx'

# parsed_data = parse_rinex_files(obs_file, nav_file)

# # Print results
# for data in parsed_data:
#     print(f"Satellite: {data['satellite']}")
#     print(f"Time: {data['time']}")
#     print(f"Pseudorange: {data['pseudorange']:.2f} meters")
#     print(f"Carrier-to-Noise Ratio: {data['cnr']:.2f} dB-Hz")
#     print(f"Elevation Angle: {data['elevation']:.2f} degrees")
#     print("---")
