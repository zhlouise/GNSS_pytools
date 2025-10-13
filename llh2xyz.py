from math import sin, cos, sqrt, radians
from typing import Tuple
import argparse

#!/usr/bin/env python3
# llh2xyz.py
# Convert geodetic latitude, longitude, height (LLH) to ECEF (XYZ) using WGS84.



# WGS84 ellipsoid constants
WGS84_A = 6378137.0                 # Semi-major axis (meters)
WGS84_F = 1 / 298.257223563         # Flattening
WGS84_E2 = WGS84_F * (2.0 - WGS84_F)  # First eccentricity squared


def llh_to_ecef(lat: float, lon: float, h: float = 0.0, degrees: bool = True) -> Tuple[float, float, float]:
    """
    Convert geodetic latitude, longitude, height (LLH) to ECEF (XYZ).

    Args:
        lat: Geodetic latitude (degrees if degrees=True, else radians).
        lon: Geodetic longitude (degrees if degrees=True, else radians).
        h: Ellipsoidal height above WGS84 ellipsoid (meters).
        degrees: Interpret lat/lon as degrees if True, else radians.

    Returns:
        (x, y, z): ECEF coordinates in meters.
    """
    if degrees:
        lat_rad = radians(lat)
        lon_rad = radians(lon)
    else:
        lat_rad = lat
        lon_rad = lon

    s = sin(lat_rad)
    c = cos(lat_rad)
    cl = cos(lon_rad)
    sl = sin(lon_rad)

    # Prime vertical radius of curvature
    N = WGS84_A / sqrt(1.0 - WGS84_E2 * s * s)

    x = (N + h) * c * cl
    y = (N + h) * c * sl
    z = (N * (1.0 - WGS84_E2) + h) * s
    return x, y, z


def _main() -> None:
    parser = argparse.ArgumentParser(description="Convert LLH (WGS84) to ECEF (XYZ).")
    parser.add_argument("--lat", type=float, required=True, help="Latitude in degrees by default.")
    parser.add_argument("--lon", type=float, required=True, help="Longitude in degrees by default.")
    parser.add_argument("--h", type=float, default=0.0, help="Ellipsoidal height in meters (default: 0).")
    parser.add_argument("--radians", action="store_true", help="If set, lat/lon are provided in radians.")
    parser.add_argument("--precision", type=int, default=6, help="Decimal precision for output.")
    args = parser.parse_args()

    x, y, z = llh_to_ecef(args.lat, args.lon, args.h, degrees=not args.radians)
    fmt = f"{{:.{args.precision}f}}"
    print(f"{fmt.format(x)} {fmt.format(y)} {fmt.format(z)}")


if __name__ == "__main__":
    _main()