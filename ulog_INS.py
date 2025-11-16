import numpy as np
from pyulog import ULog
import matplotlib.pyplot as plt

def load_ulog_data(ulog_file):
    """Load GNSS and INS data from ulog file"""
    ulog = ULog(ulog_file)
    
    # Extract GNSS position data
    gnss_data = ulog.get_dataset('vehicle_gps_position')
    # Extract GNSS position data
    gnss_data = ulog.get_dataset('vehicle_gps_position')
    gnss_time = gnss_data.data['timestamp'] * 1e-6  # Convert to seconds
    gnss_lat = gnss_data.data['latitude_deg']  # Already in degrees
    gnss_lon = gnss_data.data['longitude_deg']  # Already in degrees
    gnss_alt = gnss_data.data['altitude_msl_m']  # Already in meters
    ins_data = ulog.get_dataset('vehicle_local_position')
    ins_time = ins_data.data['timestamp'] * 1e-6
    ins_x = ins_data.data['x']
    ins_y = ins_data.data['y']
    ins_z = ins_data.data['z']
    
    # Extract velocity for dead reckoning
    ins_vx = ins_data.data['vx']
    ins_vy = ins_data.data['vy']
    ins_vz = ins_data.data['vz']
    
    return {
        'gnss': {'time': gnss_time, 'lat': gnss_lat, 'lon': gnss_lon, 'alt': gnss_alt},
        'ins': {'time': ins_time, 'x': ins_x, 'y': ins_y, 'z': ins_z, 
                'vx': ins_vx, 'vy': ins_vy, 'vz': ins_vz}
    }

def dead_reckoning(ins_data):
    """Calculate dead reckoning position from velocity integration"""
    time = ins_data['time']
    vx = ins_data['vx']
    vy = ins_data['vy']
    vz = ins_data['vz']
    
    # Initialize position
    dr_x = np.zeros_like(vx)
    dr_y = np.zeros_like(vy)
    dr_z = np.zeros_like(vz)
    
    # Integrate velocity
    for i in range(1, len(time)):
        dt = time[i] - time[i-1]
        dr_x[i] = dr_x[i-1] + vx[i] * dt
        dr_y[i] = dr_y[i-1] + vy[i] * dt
        dr_z[i] = dr_z[i-1] + vz[i] * dt
    
    return dr_x, dr_y, dr_z

def latlon_to_local(lat, lon, lat0, lon0):
    """Convert lat/lon to local coordinates"""
    R = 6371000  # Earth radius in meters
    x = R * np.radians(lon - lon0) * np.cos(np.radians(lat0))
    y = R * np.radians(lat - lat0)
    return x, y

def plot_trajectories(data, dr_x, dr_y, dr_z):
    """Plot 3D trajectories comparison"""
    # Convert GNSS to local coordinates
    lat0 = data['gnss']['lat'][0]
    lon0 = data['gnss']['lon'][0]
    gnss_x, gnss_y = latlon_to_local(data['gnss']['lat'], data['gnss']['lon'], lat0, lon0)
    gnss_z = data['gnss']['alt'] - data['gnss']['alt'][0]
    
    # Convert INS from PX4 NED -> ENU for comparison:
    # PX4: ins_x = North, ins_y = East, ins_z = Down
    ins_n = np.asarray(data['ins']['x'])
    ins_e = np.asarray(data['ins']['y'])
    ins_z_up = -np.asarray(data['ins']['z'])  # make "up" positive
    # Dead-reckoning from INS (dr_x/dr_y are in INS frame: North,East)
    dr_e = dr_y
    dr_n = dr_x
    dr_z_up = -dr_z
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot using ENU ordering (east,north,up) so GNSS and INS align
    ax.plot(ins_e, ins_n, ins_z_up, label='INS/GNSS Coupled (Ground Truth)', linewidth=2)
    ax.plot(gnss_x, gnss_y, gnss_z, label='GNSS Only', linewidth=2, alpha=0.7)
    ax.plot(dr_e, dr_n, dr_z_up, label='Dead Reckoning (INS Only)', linewidth=2, alpha=0.7, linestyle='--')
     
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Flight Trajectory Comparison')
    ax.legend()
    plt.tight_layout()
    
def plot_positioning_errors(data, dr_x, dr_y, dr_z):
    """Plot positioning errors over time"""
    # Convert GNSS to local coordinates and interpolate to INS time
    lat0 = data['gnss']['lat'][0]
    lon0 = data['gnss']['lon'][0]
    gnss_x, gnss_y = latlon_to_local(data['gnss']['lat'], data['gnss']['lon'], lat0, lon0)
    gnss_z = data['gnss']['alt'] - data['gnss']['alt'][0]
    
    # Interpolate GNSS to INS timestamps
    gnss_x_interp = np.interp(data['ins']['time'], data['gnss']['time'], gnss_x)
    gnss_y_interp = np.interp(data['ins']['time'], data['gnss']['time'], gnss_y)
    gnss_z_interp = np.interp(data['ins']['time'], data['gnss']['time'], gnss_z)
    
    # Convert INS from NED -> ENU for error computation
    ins_e = np.asarray(data['ins']['y'])
    ins_n = np.asarray(data['ins']['x'])
    ins_z_up = -np.asarray(data['ins']['z'])
    # Interpolated INS (if needed) already on INS time so compare directly
    gnss_error = np.sqrt((gnss_x_interp - ins_e)**2 + 
                         (gnss_y_interp - ins_n)**2 + 
                         (gnss_z_interp - ins_z_up)**2)
    
    # Dead-reckoning transformed to ENU (dr_x/dr_y are North,East)
    dr_e = dr_y
    dr_n = dr_x
    dr_z_up = -dr_z
    dr_error = np.sqrt((dr_e - ins_e)**2 + (dr_n - ins_n)**2 + (dr_z_up - ins_z_up)**2)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data['ins']['time'], gnss_error, label='GNSS Only Error', linewidth=2)
    ax.plot(data['ins']['time'], dr_error, label='Dead Reckoning Error', linewidth=2)
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Position Error (m)')
    ax.set_title('Positioning Error vs Time')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

if __name__ == '__main__':
    # Load ulog file
    ulog_file = 'C:/Users/louis/Dropbox/FYP/Data/taihungtun_20251012/pixhawk_log_dynamic1.ulg'  # Replace with your file path
    
    data = load_ulog_data(ulog_file)
    
    # Calculate dead reckoning
    dr_x, dr_y, dr_z = dead_reckoning(data['ins'])
    
    # Generate plots
    plot_trajectories(data, dr_x, dr_y, dr_z)
    plot_positioning_errors(data, dr_x, dr_y, dr_z)
    
    plt.show()