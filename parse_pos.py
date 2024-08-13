def parse_pos_file(file_path):
    latitudes = []
    longitudes = []
    heights = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if line.startswith('%') or line.startswith('#'):
                continue

            data = line.split()
            if len(data) >= 4:
                latitude = float(data[2])
                longitude = float(data[3])
                height = float(data[4])

                latitudes.append(latitude)
                longitudes.append(longitude)
                heights.append(height)

    if len(latitudes) == 0 or len(longitudes) == 0 or len(heights) == 0:
        return None

    mean_latitude = sum(latitudes) / len(latitudes)
    mean_longitude = sum(longitudes) / len(longitudes)
    mean_height = sum(heights) / len(heights)

    return mean_latitude, mean_longitude, mean_height

file_path = 'C:/Users/louis/OneDrive/Desktop/GT_location2_20240812.pos'
result = parse_pos_file(file_path)
if result is not None:
    mean_latitude, mean_longitude, mean_height = result
    print(f"Mean LLA position: Latitude={mean_latitude}, Longitude={mean_longitude}, Height={mean_height}")
else:
    print("No valid data found in the file.")