def parse_NovAtel_solution(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extracting previous information
    project = lines[1].split(':')[1].strip()
    program = lines[2].split(':')[1].strip()
    profile = lines[3].split(':')[1].strip()
    source = lines[4].split(':')[1].strip()
    process_info = lines[5].split(':')[1].strip()
    datum = lines[6].split(':')[1].strip()
    master1 = lines[7].split(':')[1].strip()
    remote = lines[8].split(':')[1].strip()
    geoid = lines[9].split(':')[1].strip()

    # Parsing X-ECEF, Y-ECEF, Z-ECEF, Latitude, Longitude, and H-MSL values
    data = []
    for line in lines[15:]:
        values = line.split()
        x_ecef = float(values[0])
        y_ecef = float(values[1])
        z_ecef = float(values[2])
        latitude = float(values[3])
        longitude = float(values[4])
        h_msl = float(values[5])
        data.append((x_ecef, y_ecef, z_ecef, latitude, longitude, h_msl))

    return project, program, profile, data

# Usage example
file_path = '/d:/GNSS_pytools/parse_NovAtel_solution.py'
project, program, profile, data = parse_solution_file(file_path)
print(f"Project: {project}")
print(f"Program: {program}")
print(f"Profile: {profile}")
print(f"Data: {data}")