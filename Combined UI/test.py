import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the spreadsheet into a pandas DataFrame
file_path = '/Users/rishayjain/Desktop/torus_calc/torus_final_calcs2.csv'  # Replace with the actual path
df = pd.read_csv(file_path)

# Identify unique result names
result_names = df['Results_Name'].unique()

print(result_names)

# Create a dictionary to store data for each result name
result_data = {}

dicts = {}

for result_name in result_names:
    dicts[result_name] = []


# print(df.values)
# Iterate over result names
for index in df.values:
    # Filter the DataFrame based on the current result name
    # result_df = df[df['Results_Name'] == result_name]
    
    name = index[0]
    val = index[1]

    dicts[name].append(val)



# Specify the alpha value for which you want to plot the trajectory
target_alpha = 10.0  # Replace with the desired alpha value

# Filter the DataFrame based on the target alpha
# filtered_df = df[df['Alpha'] == target_alpha]

# Extract relevant columns
time_points = dicts['Results_Time']
alpha_values = dicts['Alpha']
velocity_values = dicts['FC_Vinf_']
cl_values = dicts['CL']
cd_values = dicts['CDtot']

# Convert alpha to radians
alpha_rad = np.radians(target_alpha)

# Constants
rho = 1.225  # Air density at sea level in kg/m^3 (adjust as needed)
S_ref = np.pi * ((14 / 2) ** 2 - (10 / 2) ** 2)  # Reference area of the torus in m^2
mass = 1.0  # Mass of the torus in kg (adjust as needed)
g = 9.81  # Acceleration due to gravity in m/s^2

# Time parameters
dt = 0.1  # Time step in seconds
total_time = 100.0  # Total simulation time in seconds

# Initial conditions
v0 = 50.0  # Initial velocity in m/s
theta0 = 45.0  # Initial launch angle in degrees

# Convert initial conditions to radians
theta0_rad = np.radians(theta0)

# Function to calculate aerodynamic forces
def calculate_forces(v, alpha, cl, cd):
    # Calculate aerodynamic forces
    rho = 1.225  # Air density at sea level in kg/m^3 (adjust as needed)
    S_ref = np.pi * ((14 / 2) ** 2 - (10 / 2) ** 2)  # Reference area of the torus in m^2
    mass = 1.0  # Mass of the torus in kg (adjust as needed)
    g = 9.81  # Acceleration due to gravity in m/s^2
    
    v = float(v)
    cd = float(cd)
    cl = float(cl)
    D = 0.5 * rho * float(v) ** 2 * float(S_ref) * float(cd)
    L = 0.5 * rho * v ** 2 * S_ref * float(cl)

    # Resolve forces into components
    Fx = -D * np.cos(alpha) - L * np.sin(alpha)
    Fy = -D * np.sin(alpha) + L * np.cos(alpha)

    return Fx, Fy

# Function to simulate projectile motion
def simulate_projectile_motion():
    # Initialize arrays to store results
    x_points, y_points = [], []
    vx_points, vy_points = [], []

    # Initial conditions
    x, y, vx, vy = 0.0, 0.0, float(velocity_values[0]) * float(np.cos(alpha_rad)), float(velocity_values[0]) * float(np.sin(alpha_rad))

    for i in range(91):
        # Calculate aerodynamic forces using values at each time step
        Fx, Fy = calculate_forces(velocity_values[i], alpha_rad, cl_values[i], cd_values[i])

        # Calculate accelerations
        ax = Fx / mass
        ay = Fy / mass - g  # Include gravity

        # Update velocities and positions using Euler's method
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt

        # Store results
        x_points.append(x)
        y_points.append(y)
        vx_points.append(vx)
        vy_points.append(vy)

    return x_points, y_points

# Run simulation
x_pos, y_pos = simulate_projectile_motion()

# Plot the trajectory
plt.figure(figsize=(10, 6))
plt.plot(x_pos, y_pos)
plt.title(f"Projectile Motion of Torus at Alpha = {target_alpha} degrees")
plt.xlabel("Horizontal Distance (m)")
plt.ylabel("Vertical Distance (m)")
plt.grid(True)
plt.show()
