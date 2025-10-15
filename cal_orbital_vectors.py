import numpy as np

a = 11000
e = 0.001
i = 22
ohm = 113
omega = 45
E = 263
mu = 398600

# calculate theta
theta = np.arccos((np.cos(np.radians(E)) - e) / (1 - e * np.cos(np.radians(E))))
theta = np.degrees(theta)
print(f"theta is {theta}")

# calculate r
r = a * (1 - e**2) / (1 + e * np.cos(np.radians(theta)))
print(f"r is {r}")

# calculate p
p = a * (1 - e**2) 
print(f"p is {p}")

# calculate rp vector
rp = np.array([r * np.cos(np.radians(theta)), r * np.sin(np.radians(theta)), 0])
print(f"rp vector is {rp}")

# calculate vp vector
vp = np.array([-np.sqrt(mu/p) * np.sin(np.radians(theta)), np.sqrt(mu/p) * (e + np.cos(np.radians(theta))), 0])
print(f"vp vector is {vp}")

# calculate rotation matrix A
A = np.array([[np.cos(np.radians(ohm)) * np.cos(np.radians(omega)) - np.sin(np.radians(ohm)) * np.sin(np.radians(omega)) * np.cos(np.radians(i)), 
                -np.cos(np.radians(ohm)) * np.sin(np.radians(omega)) - np.sin(np.radians(ohm)) * np.cos(np.radians(omega)) * np.cos(np.radians(i)), 
                np.sin(np.radians(ohm)) * np.sin(np.radians(i))],
               [np.sin(np.radians(ohm)) * np.cos(np.radians(omega)) + np.cos(np.radians(ohm)) * np.sin(np.radians(omega)) * np.cos(np.radians(i)), 
                -np.sin(np.radians(ohm)) * np.sin(np.radians(omega)) + np.cos(np.radians(ohm)) * np.cos(np.radians(omega)) * np.cos(np.radians(i)), 
                -np.cos(np.radians(ohm)) * np.sin(np.radians(i))],
               [np.sin(np.radians(omega)) * np.sin(np.radians(i)), 
                np.cos(np.radians(omega)) * np.sin(np.radians(i)), 
                np.cos(np.radians(i))]])
print(f"A rotation matrix is:\n{A}")

# calculate ri
ri = A @ rp
print(f"ri vector is {ri}")

# calculate vi
vi = A @ vp
print(f"vi vector is {vi}")
