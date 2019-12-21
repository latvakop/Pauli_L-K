# Made by: Remmi-team
# Refactoring to python: Pauli Latva-Kokko

from constants import GRAVITATION_CONSTANT

class Tyre:
    """
    Tyre model

    Parameters
    ----------
    rolling_resistance: float
        The rolling resistance of the tyre

    diam: float
        The diameter of the tyre

    Returns
    -------

    """
    def __init__(self, rolling_resistance_coeff, diam):
        """
        Initializing the tyre.
        Parameters
        ----------
        rolling_resistance_coeff: float
            The rolling resistance of the tire
        diam: float
            The diameter of the tyre in meters.
        """
        self.C_rr = rolling_resistance_coeff

        # TODO: use this to calculate F_r in the future
        self.diam = diam

    def calculate_loss(self, vehicle_speed, F_r):
        """
        Calculates the energy lost by the tyre's friction.
        Parameters
        ----------
        vehicle_speed: float
            Current speed of the vehicle
        F_r: float
            Radient force
        Returns
        -------
        F_roll: float
            The energy lost by the rolling friction.
        """
        if vehicle_speed <= 0:
            F_roll = 0;
        else:
            F_roll = GRAVITATION_CONSTANT * F_r * self.C_rr;
        return F_roll
