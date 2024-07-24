import pandas as pd

# Function to import positioning file from Excel
def import_excel(file_path):
    try:
        data = pd.read_excel(file_path)
        return data
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", str(e))

# Function that returns the master satellite for each epoch
def get_master_sat(data):
    master_sat = {
        'Epoch': [],
        'Satellite ID': []
    }
    for epoch_count in data['Epoch'].max():
        if epoch_count == 0:
            continue
        # If we define the master satellite as the satellite with the highest elevation angle
        max_ele = data.loc[data['Epoch'] == epoch_count]['Elevation'].max()
        master_sat['Epoch'].append(epoch_count)
        master_sat['Satellite ID'].append(data.loc[(data['Epoch'] == epoch_count) & (data['Elevation'] == max_ele)]['Satllite ID'].values[0])
        # If we define the master satellite as the satellite with the highest SNR
        # max_snr = data.loc[data['Epoch'] == epoch_count]['SNR (dbHz)'].max()
        # master_sat['Epoch'].append(epoch_count)
        # master_sat['Satellite ID'].append(data.loc[(data['Epoch'] == epoch_count) & (data['SNR (dbHz)'] == max_snr)]['Satllite ID'].values[0])
    return master_sat

# Function for double difference calculation
def double_difference(sat2ref, sat2rover, master2ref, master2rover):
    SD_sat = sat2ref - sat2rover # Single difference for satellite
    SD_master = master2ref - master2rover # Single difference for master satellite
    DD = SD_sat - SD_master # Double difference
    return DD

# Function for pseudorange retrievals
def get_pseudorange(data_rover, data_ref):
    # Retrieve the master satellites for each epoch
    master_sat = get_master_sat(data_rover)
    for rows in len(data_rover):
        # Initialize the data structure
        pseudoranges={
            'epoch' : [],
            'satID' : [],
            'sat2ref': [],
            'sat2rover': [],
            'master2ref': [],
            'master2rover': []
        }

        epoch = data_rover['Epoch'][rows-1]
        TOW = data_rover['TOW'][rows-1]
        satID = data_rover['Satellite ID'][rows-1]
        master_satID = master_sat[(master_sat['Epoch']==epoch)]['Satellite ID']

        # Locate the lines in data_ref with the same TOW and satID
        ref_row = data_ref[(data_ref['TOW'] == TOW) & (data_ref['Satellite ID'] == satID)]
        if satID == master_satID: # If it is a master satellite
            sat2ref = master2ref = ref_row['Pseudorange']
            sat2rover = master2rover = data_rover['Pseuodrange'][rows-1]
        else:
            sat2ref = ref_row['Pseudorange']
            sat2rover = data_rover['Pseudorange'][rows-1]
            master2ref = data_ref[(data_ref['TOW'] == TOW) & (data_ref['Satellite ID'] == master_satID)]['Pseudorange']
            master2rover = data_rover[(data_rover['Epoch'] == epoch) & (data_rover['Satellite ID'] == master_satID)]['Pseudorange']
        
        # Append to pseudoranges
        pseudoranges['epoch'].append(epoch)
        pseudoranges['satID'].append(satID)
        pseudoranges['sat2ref'].append(sat2ref)
        pseudoranges['sat2rover'].append(sat2rover)
        pseudoranges['master2ref'].append(master2ref)
        pseudoranges['master2rover'].append(master2rover)
        
    return pseudoranges

def calc_pseudorange_error(pseudoranges, ranges):
    pseudorange_error ={
        'Epoch' : [],
        'Satellite ID' : [],
        'Pseudorange Error' : []
    }
    for rows in len(pseudoranges):
        pseudorange_DD = double_difference(
            pseudoranges['sat2ref'],
            pseudoranges['sat2rover'],
            pseudoranges['master2ref'],
            pseudoranges['master2rover']
        )
        range_DD = double_difference(
            ranges['sat2ref'],
            ranges['sat2rover'],
            ranges['master2ref'],
            ranges['master2rover']
        )
        pseudorange_error['Epoch'].append(pseudoranges['Epoch'][rows-1])
        pseudorange_error['Satellite ID'].append(pseudoranges['Epoch'][rows-1])
        pseudorange_error['Pseudorange Error'].append(range_DD-pseudorange_DD)
    return pseudorange_error

if __name__ == '__main__':
    # Import data
    data = import_excel('data.xlsx')
    # Get master satellite
    master_sat = master_sat(data)
    # Calculate double difference
    DD = double_difference(data['Sat2Ref'], data['Sat2Rover'], data['Master2Ref'], data['Master2Rover'])
    print(DD)
