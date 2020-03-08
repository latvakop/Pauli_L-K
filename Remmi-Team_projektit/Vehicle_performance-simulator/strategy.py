# Made by: Pauli Latva-Kokko
# Strategy that uses acceleration points on the track and accelerates from a point on the track to a certain end speed.

import configparser


class Strategy:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./constants.ini')
        first_lap_accels = config.get('STRATEGY', 'FIRST_LAP_ACCELS')
        normal_accels = config.get('STRATEGY', 'NORMAL_ACCELS')
        last_lap_accels = config.get('STRATEGY', 'LAST_LAP_ACCELS')

        self.total_laps = config.getint('EVENT', 'TOTAL_LAPS')
        self.first_lap_accels = self.parse_config(
            first_lap_accels)  # All the acceleration points and end speeds in first lap as tuple
        self.normal_accels = self.parse_config(normal_accels)  # Normal acceleration points and end speeds as tuple
        self.last_lap_accels = self.parse_config(last_lap_accels)  # Acceleration points and end speeds for the last lap
        self.stop_acceleration = False
        self.last_point = -1

    def parse_config(self, accels):
        accels = accels.split(';')
        for i in range(len(accels)):
            parts = accels[i].split(',')
            accels[i] = (float(parts[0]), float(parts[1]))
        return accels

    def accelerate(self, accels, current_speed, Tyre_3, Engine, track_position):
        """
        Takes the strategy acceleration points and end speeds as tuple and decides where to accelerate
        or not based on that.
        """

        for i in range(len(accels) - 1, -1, -1):
            # Point is the position on the track where the acceleration starts
            point = accels[i][0]
            end_speed = accels[i][1]
            if track_position > point:
                if point > self.last_point:
                    self.stop_acceleration = False
                    self.last_point = point

                # Accelerate
                if current_speed < end_speed / 3.6 and not self.stop_acceleration:
                    power_added = Engine.getPower(Tyre_3, current_speed)
                    return power_added

                if current_speed > end_speed / 3.6 and not self.stop_acceleration:
                    power_added = 0
                    self.stop_acceleration = True
                    return power_added

                if self.stop_acceleration:
                    power_added = 0
                    self.last_point = point
                    return power_added
                power_added = 0
                return power_added
        power_added = 0
        return power_added

    def get_strategy(self, current_speed, Tyre_3, Engine, lap_counter,
                     track_position):
        """
        Returns the power added depending on the strategy. Strategy is inputted to constants.py
        file.
        Parameters.
        -----------
        current_speed : float
            Current speed of the vehicle
        Tyre_3 : Tyre
            The backwheel of the vehicle
        Engine: Engine
            The engine
        lap_counter : int
            The number of the current lap
        track_position: float
            The position of the car in the track in meters.
        Returns.
        --------
        Power_added: float
            The power added by the engine
        """
        if lap_counter == 0:
            power_added = self.accelerate(self.first_lap_accels, current_speed, Tyre_3, Engine, track_position)
            return power_added
        if lap_counter == self.total_laps - 1:
            power_added = self.accelerate(self.last_lap_accels, current_speed, Tyre_3, Engine, track_position)
            return power_added
        if lap_counter > 0 and lap_counter < self.total_laps - 1:
            power_added = self.accelerate(self.normal_accels, current_speed, Tyre_3, Engine, track_position)
            return power_added
