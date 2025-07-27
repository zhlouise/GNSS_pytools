from pyulog import ULog
from pyubx2 import UBXReader

# Load ULog
ulog = ULog('C:/Users/louis/OneDrive/Desktop/log_0_2025-7-27-18-14-38.ulg')

# Extract gps_dump topic
gps_dump = ulog.get_dataset('gps_dump').data

with open('gps_raw.bin', 'wb') as f:
    for key in gps_dump:
        f.write(gps_dump[key].tobytes())


with open('gps_raw.bin', 'rb') as stream:
    ubr = UBXReader(stream)
    for (raw, parsed) in ubr:
        if parsed is not None:
            # Print only raw measurement messages
            if parsed.identity in ('RXM-RAWX', 'RXM-SFRBX'):
                print(parsed)