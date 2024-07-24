
import pandas as pd

def parse_pos_stat(file_path):
    data = {
        'Epoch': [], 
        'Week': [], # GPS week number
        'TOW': [], # Time of week
        'Satllite ID': [],
        'Frequency': [], # (1:L1,2:L2,3:L5,...)
        'Azimuth': [],
        'Elevation': [],
        'Pseudorange Residual': [],
        'Carrier-phase Residual': [],
        'Valid Data Flag' : [], # (0: invalid, 1: valid)
        'SNR (dbHz)': [], # Signal to noise ratio
        'Ambiguity Flag': [], # (0:no data,1:float,2:fixed,3:hold)
        'Cycle-slip Flag' : [], # (bit1:slip,bit2:parity unknown)
        'Carrier-lock Count': [],
        'Data Outage Count': [],
        'Cycle-slip Count': [],
        'Data Reject Count': []
    }
    
    with open(file_path, 'r') as file:
        epoch_counter = 0
        for line in file:
            if line.startswith('$'):
                parts = line.strip().split(',')
                record_type = parts[0][1:]  # Remove '$' and get the record type
                if record_type == 'POS':
                    # Record the epoch count
                    epoch_counter += 1
                if record_type == 'SAT':
                    data['Epoch'].append(epoch_counter)
                    data['Week'].append(parts[1])
                    data['TOW'].append(parts[2])
                    data['Satllite ID'].append(parts[3])
                    data['Frequency'].append(parts[4])
                    data['Azimuth'].append(parts[5])
                    data['Elevation'].append(parts[6])
                    data['Pseudorange Residual'].append(parts[7])
                    data['Carrier-phase Residual'].append(parts[8])
                    data['Valid Data Flag'].append(parts[9])
                    data['SNR (dbHz)'].append(parts[10])
                    data['Ambiguity Flag'].append(parts[11])
                    data['Cycle-slip Flag'].append(parts[12])
                    data['Carrier-lock Count'].append(parts[13])
                    data['Data Outage Count'].append(parts[14])
                    data['Cycle-slip Count'].append(parts[15])
                    data['Data Reject Count'].append(parts[16]) 
    return data

file_path = 'C:/Users/louis/OneDrive/Desktop/GP7-4_20240712_obs.pos.stat'
parsed_data = parse_pos_stat(file_path)
df = pd.DataFrame(parsed_data)

# Export to Excel
excel_path = 'C:/Users/louis/OneDrive/Desktop/parsedGP7-4_20240712.xlsx'
df.to_excel(excel_path, index=False, engine='openpyxl')

print(f"Data exported to {excel_path}")