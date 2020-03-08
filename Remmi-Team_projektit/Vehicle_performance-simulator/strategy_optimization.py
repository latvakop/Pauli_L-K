# Made by: Pauli Latva-Kokko

# Strategy class for running the optimization algorithm.
class Strategy_optimazation:
    """
    Strategy class for running the optimization algorithm.
    """
    def __init__(self, init_speed, end_speed, initial_acceleration, final_acceleration, number_of_laps=None):
        """
        Initializes the strategy object.
        Parameters
        ----------
        init_speed: float
            The speed of starting the acceleration(km/h)
        end_speed: float
            The speed of ending the acceleration(km/h)
        """
        self.init_speed = init_speed/3.6
        self.end_speed = end_speed/3.6
        self.init_acceleration_speed = initial_acceleration/3.6
        self.final_acceleration_speed = final_acceleration/3.6
        self.total_laps = number_of_laps
        self.strategy_state = 0

    def get_strategy(self, current_speed, tyre_3, engine, lap_counter=None):
        """
        Function that returns the current power based on the strategy object, engine object, tyre object and current
        speed.
        Parameters
        ----------
        current_speed: float
            The current speed of the vehicle
        tyre_3: Tyre
            The backwheel of the vehicle.
        engine: Power
            The engine of the vehicle
        Returns
        -------
        power: float
            The current power of the engine
        """
        init_speed = self.init_speed
        end_speed = self.end_speed
        if lap_counter is not None and lap_counter == 0:
            init_speed = self.init_speed
            end_speed = self.init_acceleration_speed
        if lap_counter is not None and lap_counter == self.total_laps:
            end_speed = self.final_acceleration_speed

        if current_speed < init_speed and self.strategy_state == 0:
            power_added = engine.getPower(tyre_3, current_speed)
            self.strategy_state = 1
        elif current_speed < end_speed and self.strategy_state == 1:
            power_added = engine.getPower(tyre_3, current_speed)
        elif current_speed > end_speed and self.strategy_state == 1:
            power_added = 0
            self.strategy_state = 0
        else:
            power_added = 0

        return power_added