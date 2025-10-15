import math

r = [-3370, 3625, 4576]
v = [-6.66, -2.39, -3.01]
mu = 398600

# r and v magnitudes
r_norm = math.sqrt(sum(x * x for x in r))
v_norm = math.sqrt(sum(x * x for x in v))
print(f"r_norm is {r_norm} and v_norm is {v_norm}")

# calculate h and h_norm
h = [
    r[1] * v[2] - r[2] * v[1],
    r[2] * v[0] - r[0] * v[2],
    r[0] * v[1] - r[1] * v[0],
]
print(f"h is: {h}")
h_norm = math.sqrt(sum(c * c for c in h))
print(f"h_norm is {h_norm}")

# calculate a
a = 1/(2/r_norm-(v_norm**2)/mu)
print(f"a is {a}")

# calculate e and e_norm
vxh = [
    v[1] * h[2] - v[2] * h[1],
    v[2] * h[0] - v[0] * h[2],
    v[0] * h[1] - v[1] * h[0],
]
e = [vxh[i] / mu - r[i] / r_norm for i in range(3)]
print(f"e is: {e}")
e_norm = math.sqrt(sum(c * c for c in e))
print(f"e_norm is {e_norm}")

# calculate i
ratio = h[2] / h_norm
ratio = max(-1.0, min(1.0, ratio))
i = math.acos(ratio) * (180 / math.pi)  
print(f"i is {i}")

# calculate N and N_norm
iz = [0, 0, 1]  # unit vector in the z-direction
N = [
    iz[1] * h[2] - iz[2] * h[1],
    iz[2] * h[0] - iz[0] * h[2],
    iz[0] * h[1] - iz[1] * h[0],
]
N_norm = math.sqrt(sum(c * c for c in N))
print(f"N is: {N}")
print(f"N_norm is {N_norm}")

# calculate ohm
if N[1] >= 0:
    ohm = math.acos(N[0] / N_norm) * (180 / math.pi)
else:
    ohm = 360 - math.acos(N[0] / N_norm) * (180 / math.pi)
print(f"ohm is {ohm}")

# calculate omega
if e[2] >= 0:
    omega = math.acos(sum(N[i] * e[i] for i in range(3)) / (N_norm * e_norm)) * (180 / math.pi)
else:
    omega = 360 - math.acos(sum(N[i] * e[i] for i in range(3)) / (N_norm * e_norm)) * (180 / math.pi)
print(f"omega is {omega}")

# calculate r dot v
r_dot_v = sum(r[i] * v[i] for i in range(3))
print(f"r dot v is {r_dot_v}")

# calculate theta
if r_dot_v >= 0:
    theta = math.acos(sum(e[i] * r[i] for i in range(3)) / (e_norm * r_norm)) * (180 / math.pi)
else:
    theta = 360 - math.acos(sum(e[i] * r[i] for i in range(3)) / (e_norm * r_norm)) * (180 / math.pi)
print(f"theta is {theta}")

# calculate E
E = 2 * math.atan(math.sqrt((1 - e_norm) / (1 + e_norm)) * math.tan(math.radians(theta) / 2))
E = math.degrees(E)  # Convert E to degrees
print(f"E is {E}")