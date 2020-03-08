# Made by: Remmi-Team
# Refactoring to Python: Pauli Latva-Kokko and Jesper Granat

# Simulation parameters
SAMPLE_TIME = 0.01
END_TIME = 3000
GRAVITATION_CONSTANT = 9.81
BEST_INIT_SPEED = 12.9696
BEST_END_SPEED = 35.688

# FUEL PARAMETERS
ENERGY_DENSITY_MJ = 44.888 # MJ/kg 
ENERGY_DENSITY_J = 43.5*10**6
FUEL_DENSITY = 0.6871 # kg/l

# Vehicle parameters
VEHICLE_MASS = 81 # Mass of the vehicle with driver
F_R = (VEHICLE_MASS*9.81)/3 # Radial force acting on each wheel. 50/50 weight distribution is assumed
DRAG_COEF = 0.11 # Used for calculating the drag of the vehicle.
FRONT_AREA = 0.35 # Frontal area of the vehicle. Used for calculating the drag of the vehicle.
RHO = 1.2
ENGINE_TORGUE = 3.15
ENGINE_EFFICIENCY = 0.30
FRONT_SPROCKET = 141
REAR_SPROCKET = 18
DRIVE_RATIO = REAR_SPROCKET / FRONT_SPROCKET
ROLLING_RESISTANCE_COEF = 0.001
TYRE_DIAMETER = 0.48
BEARING_DISTANCE = 0.025 # Meters, Distance between the bearings on front wheel hub. Used for bearing force calculation.

# Strategy parameters


# Event parameters
TOTAL_LAPS = 11