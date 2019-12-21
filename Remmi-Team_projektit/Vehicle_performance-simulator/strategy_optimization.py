# Made by: Pauli Latva-Kokko

# Strategy class for running the optimization algorithm.
class Strategy_optimazation:
    def __init__(self, init_speed, end_speed):
        """
        Initializes the strategy object.
        Parameters
        ----------
        init_speed: float
            The speed of starting the acceleration(km/h)
        end_speed: float
            The speed of ending the acceleration(km/h)
        """
        self.init_speed_ = init_speed/3.6
        self.end_speed_ = end_speed/3.6
        self.strategy_state = 0

    def get_strategy(self, current_speed, tyre_3, engine):
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
        if current_speed < self.init_speed_ and self.strategy_state == 0:
            power_added = engine.getPower(tyre_3, current_speed)
            self.strategy_state = 1
        elif current_speed < self.end_speed_ and self.strategy_state == 1:
            power_added = engine.getPower(tyre_3, current_speed)
        elif current_speed > self.end_speed_ and self.strategy_state == 1:
            power_added = 0
            self.strategy_state = 0
        else:
            power_added = 0
        return power_added