import georinex as gr

nav = gr.load("C:/Users/louis/OneDrive - The Hong Kong Polytechnic University/URIS/URIS Data/calgary_20240712/UCAL_NAV_20240712(with Galileo).rnx")

# Extract the coordinates
x_coords = nav['X'].values
y_coords = nav['Y'].values
z_coords = nav['Z'].values

# Extract the time and satellite values
times = nav['time'].values
satellites = nav['sv'].values

# Iterate over the time and satellite dimensions to print the coordinates
for i, time in enumerate(times):
    print(f"\nSatellite coordinates at {time}:")
    for j, sat in enumerate(satellites):
        x = x_coords[i, j]
        y = y_coords[i, j]
        z = z_coords[i, j]
        if not (x is None or y is None or z is None):
            print(f"  {sat}: X={x:.3f} km, Y={y:.3f} km, Z={z:.3f} km")