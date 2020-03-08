# Made by: Pauli Latva-Kokko
# Graphical ui uses this file because I wanted to keep the optimization algorithm separate from the ui.

import math

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import configparser


from tyre import Tyre
from bearing import Bearing
from aerodynamic import Aerodynamic_object
from power import Power
from plotter import Plotter
from strategy_optimization import Strategy_optimazation
from strategy import Strategy



def CalculateHeight(track_position, heights):
    """
    Calculates the height

    Parameters
    ----------
    track_position: float
        The position on the track in meters

    heights: iterable (list, np.ndarray)
        The track height data

    Returns
    -------
    height: float
        The current height on the track
    """
    position_lower = math.floor(track_position) - 1
    last_position = len(heights) - 1
    if (position_lower >= last_position):
        m = (heights[0] - heights[position_lower]) / 1
        height = heights[position_lower] + m * (
                    track_position - position_lower)
    else:
        m = (heights[position_lower + 1] - heights[position_lower]) / 1
        height = heights[position_lower] + m * (
                    track_position - position_lower - 1)
    return height


def calculate_result(init_speed, end_speed, initial_acceleration=None,
                     final_acceleration=None, plotting_on=True, file_name='../track_data_nokia.csv'):
    """
    Calculate the result based on physics and SEM competition rules

    Parameters
    ----------
    init_speed: float
        The initial speed before the acceleration

    end_speed: float
        The final speed after the acceleration

    Returns
    -------
    result: float
        Total consumption of the fuel.
    """
    # Normal variables
    lap_counter = 0
    time = 0
    sample = 0
    track_position = 1
    previous_position = 0
    current_speed = 0
    total_loss = 0
    power_added = 0
    fuel_used = 0
    fuel_used_total = 0
    current_potentialEnergy = 0
    distance = 1
    radius = 0
    centripetal_force = 0
    change_in_potential_energy = 0
    previous_power_added = 0

    # csv parsing
    config = configparser.ConfigParser()
    config.read('./constants.ini')

    track_data = np.loadtxt('../Lontoo2020_ready.csv', delimiter=';',
                            skiprows=1)
    sample_count_per_lap = len(track_data)
    heights = track_data[:, 1]
    track_positions = track_data[:, 0]
    track_data_radius = track_data[:, 2]
    # TODO: take this from the heights list
    current_height = 0
    last_position = len(heights)

    # Constant initializing
    VEHICLE_MASS = config.getint('VEHICLE', 'VEHICLE_MASS')
    TOTAL_LAPS = config.getint('EVENT', 'TOTAL_LAPS')
    END_TIME = config.getint('SIMULATION', 'END_TIME')
    GRAVITATION_CONSTANT = config.getfloat('SIMULATION',
                                           'GRAVITATION_CONSTANT')
    SAMPLE_TIME = config.getfloat('SIMULATION', 'SAMPLE_TIME')
    ENERGY_DENSITY_J = config.getfloat('FUEL', 'ENERGY_DENSITY_J') * 10 ** 6
    FUEL_DENSITY = config.getfloat('FUEL', 'FUEL_DENSITY')
    F_R = config.getint('VEHICLE', 'F_R')
    ENGINE_STARTUP = config.getfloat('FUEL', 'ENGINE_STARTUP')

    # List initializing
    height_data = []
    time_data = []
    speed_data = []
    speed_data_kmh = []
    distance_data = []
    centripetal_force_data = []
    fuel_used_data = []

    # Based on constants
    previous_potential_energy = VEHICLE_MASS * GRAVITATION_CONSTANT * heights[0]
    current_kinetic_energy = 0.5 * VEHICLE_MASS * current_speed ** 2

    # Object initialization
    tyre = Tyre(config.getfloat('VEHICLE', 'ROLLING_RESISTANCE_COEF'),
                config.getfloat('VEHICLE', 'TYRE_DIAMETER'))
    bearings = ['Angular'] * 4 + ['Groove'] * 2
    bearings = [Bearing(i) for i in bearings]
    aerodynamic = Aerodynamic_object(config.getfloat('VEHICLE', 'DRAG_COEF'),
                                     config.getfloat('VEHICLE', 'FRONT_AREA'),
                                     config.getfloat('VEHICLE', 'RHO'))
    engine = Power(config.getfloat('VEHICLE', 'ENGINE_TORGUE'),
                   config.getfloat('VEHICLE', 'ENGINE_EFFICIENCY'),
                   config.getint('VEHICLE', 'REAR_SPROCKET')/
                   config.getint('VEHICLE', 'FRONT_SPROCKET'))

    optimal_strategy = Strategy_optimazation(init_speed, end_speed,
                                             initial_acceleration,
                                             final_acceleration,
                                             TOTAL_LAPS)
    london_strategy = Strategy()

    while time < END_TIME and lap_counter < TOTAL_LAPS:

        current_speed = math.sqrt(
            current_kinetic_energy / (0.5 * VEHICLE_MASS))
        current_height = CalculateHeight(track_position, heights)
        height_data.append(current_height)

        current_potentialEnergy = VEHICLE_MASS * GRAVITATION_CONSTANT * current_height
        change_in_potential_energy = current_potentialEnergy - previous_potential_energy
        previous_potential_energy = current_potentialEnergy

        # Calculating energy loss of bearings,tyres and aerodynamics.
        bearing_loss = 0
        for i in range(6):
            bearing_loss += bearings[i].calculate_loss(current_speed, 150, 150)

        tyre_loss = 0
        for i in range(3):
            tyre_loss += tyre.calculate_loss(current_speed, F_R)

        aerodynamic_loss = aerodynamic.calculate_loss(current_speed)
        total_loss = aerodynamic_loss + tyre_loss + bearing_loss

        # Power added depends on the current strategy
        # power_added = strategy.getStrategy(current_speed, tyre, engine,lap_counter,
        # TOTAL_LAPS, track_position, last_position)

        #power_added = optimal_strategy.get_strategy(current_speed, tyre,
        #                                            engine, lap_counter)

        power_added = london_strategy.get_strategy(current_speed, tyre, engine, lap_counter, track_position)

        # Fuel usage depends on engine power and efficiency and energy density of the fuel.
        fuel_used = ((power_added * SAMPLE_TIME) / engine.effiency) / \
                    (
                                ENERGY_DENSITY_J * FUEL_DENSITY) * 1000  # Conversion to ml included
        # If engine is started up it consumes extra fuel.
        if previous_power_added == 0 and power_added > 0:
            fuel_used += ENGINE_STARTUP
        fuel_used_total = fuel_used_total + fuel_used


        # Current kinetic energy calculated based on lost energy, potential energy and power added by the engine.
        current_kinetic_energy = max(
            current_kinetic_energy - total_loss * SAMPLE_TIME - \
            change_in_potential_energy + power_added * SAMPLE_TIME, 0)

        # Calculate distance based on speed and time
        distance = distance + current_speed * SAMPLE_TIME
        distance_data.append(distance)

        track_position = distance % last_position

        # calculating time
        time = (sample + 1) * SAMPLE_TIME

        # Calculate the centripetal force in the corners
        radius = track_data_radius[math.floor(track_position)]
        if radius > 0:
            centripetal_force = (VEHICLE_MASS * current_speed ** 2) / radius
        else:
            centripetal_force = 0

        # Lap counter
        if track_position - previous_position < 0:
            lap_counter += 1
            # print(lap_counter)
        previous_position = track_position
        previous_power_added = power_added

        # Add values to lists to plot them later
        speed_data.append(current_speed)
        speed_data_kmh.append(current_speed * 3.6)
        centripetal_force_data.append(centripetal_force)
        time_data.append(time)
        fuel_used_data.append(fuel_used)

        sample += 1
    # Print the end result of the race.
    # print("Fuel used:", fuel_used_total, "km/l:", distance / fuel_used_total, "Init speed:", init_speed, "End speed:",
    #     end_speed)
    # Plotting some data



    plot = Plotter(time_data, "Time(s)")
    plot.new_plot(speed_data_kmh, "Speed(km/h)", "Speed graph")
    #plot.new_plot(speed_data, "Speed(m/s)", "Speed graph")
    #plot.new_plot(fuel_used_data, "Fuel used(ml)", "Fuel consumption graph")
    plot.new_plot(centripetal_force_data, "Centripetal force(N)",
                  "Centripetal force graph")
    plot2 = Plotter(distance_data, "Distance(m)")
    plot2.new_plot(speed_data_kmh, "Speed(km/h)", "Distance graph")
    plot2.new_plot(height_data, "Height(m)", "Height graph")

    if plotting_on == True:
        plt.show()
        return

    return distance / fuel_used_total, init_speed, end_speed, lap_counter

if __name__ == '__main__':
    res = calculate_result(9.921, 29.657, 25.274, 29.819, True)