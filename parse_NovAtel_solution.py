def parse_NovAtel_solution(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # # Extracting previous information
    # project = lines[1].split(':')[1].strip()
    # program = lines[2].split(':')[1].strip()
    # profile = lines[3].split(':')[1].strip()
    # source = lines[4].split(':')[1].strip()
    # process_info = lines[5].split(':')[1].strip()
    # datum = lines[7].split(':')[1].strip()
    # master1 = lines[8].split(':')[1].strip()
    # remote = lines[8].split(':')[1].strip()
    # geoid = lines[9].split(':')[1].strip()

    # Parsing X-ECEF, Y-ECEF, Z-ECEF, Latitude, Longitude, and H-MSL values
    data = {
        'X-ECEF': [],
        'Y-ECEF': [],
        'Z-ECEF': [],
        'Latitude': [],
        'Longitude': [],
        'H-MSL': []
    }
    for line in lines[16:]:
        values = line.split()
        data['X-ECEF'].append(float(values[0]))
        data['Y-ECEF'].append(float(values[1]))
        data['Z-ECEF'].append(float(values[2]))
        data['Latitude'].append(float(values[3]))
        data['Longitude'].append(float(values[4]))
        data['H-MSL'].append(float(values[5]))

    return data

def calculate_means(data):
    means = {}
    for key in data:
        if data[key]:  # Check if the list is not empty
            mean_value = sum(data[key]) / len(data[key])
            means[key] = mean_value
        else:
            means[key] = None  # Handle empty lists
    return means


file_path = 'C:/Users/louis/OneDrive - The Hong Kong Polytechnic University/URIS/URIS Data/calgary_20240712/GT_solutions.txt'
data = parse_NovAtel_solution(file_path)
means = calculate_means(data)
for key, mean in means.items():
    print(f"Mean of {key}: {mean}")
