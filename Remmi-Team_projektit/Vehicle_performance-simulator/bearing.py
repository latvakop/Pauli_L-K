# Made by: Remmi-Team
# Refactoring to python: Jesper Granat

import math
from constants import BEARING_DISTANCE, TYRE_DIAMETER


class Bearing:
    """
    Bearing class for calculating the energy loss of the bearings in the car.
    """
    BearingInnerDia = 20  # Bore diameter of bearing [mm]
    BearingOuterDia = 42  # Outer diameter of bearing [mm]
    BearingMeanDia = 31
    OilOperatingVisc = 15  # Actual  operating viscosity of the oil [mm**2/s]

    def __init__(self, bearing_type):
        """
        Constructor for creating certain type of bearings.
        Parameters
        ----------
        bearing_type: str
            The type of the bearing, Angular or Groove
        """
        self.BearingType = bearing_type
        if self.BearingType == "Angular":
            self.K_z = 4.4
            self.R_1 = 3.5e-7
            self.R_2 = 3.64
            self.R_3 = 0.41 * 2.3e-12  # If ceramic balls, multiply by 0,41
            self.S_1 = 1.05e-2
            self.S_2 = 1.55
            self.S_3 = 0.41 * 2.3e-12  # If ceramic balls, multiply by 0,41
            self.C_0 = 1460
        elif self.BearingType == "Groove":
            self.K_z = 3.1
            self.R_1 = 4.3e-7
            self.R_2 = 1.7
            self.S_1 = 4.75e-3
            self.S_2 = 3.6
            self.C_0 = 1460
        else:
            raise NotImplementedError()

    def calculate_loss(self, VehicleSpeed, F_a, F_r):
        # TODO: check that the angle is calculated correctly
        """
        Calculates the energy lost int the bearings

        Parameters
        ----------
        VehicleSpeed: float
            The current speed of the vehicle

        F_a: float
            Force that is to the direction of the acceleration

        F_r: float
            Radial force

        Returns
        -------
        result: float
            The energy loss of the bearing
        """
        WheelRpm = VehicleSpeed / (3.6 * math.pi * 0.48)

        MomentOnHub = TYRE_DIAMETER / 2 * F_a  # Moment force acting on bearings.
        F_rb = MomentOnHub / BEARING_DISTANCE  # Force on bearing caused by the moment.
        F_r = F_r + F_rb  # Resultant force

        phi_ish = 1 / (1 + 1.84 * 10e-9 * (WheelRpm * self.BearingMeanDia) ** 1.28 * self.OilOperatingVisc * 0.64)
        phi_rs = 1 / math.exp((6 * 10 ** -8) * self.OilOperatingVisc * WheelRpm * (
                    self.BearingInnerDia + self.BearingOuterDia) * math.sqrt(
            self.K_z / (2 * (self.BearingOuterDia - self.BearingInnerDia))))
        if self.BearingType == "Angular":
            F_g = self.R_3 * self.BearingMeanDia ** 4 * WheelRpm ** 2
            G_rr = self.R_1 * self.BearingMeanDia ** 1.85 * (F_r + F_g + self.R_2 * F_a) ** 0.54
        elif self.BearingType == "Groove":
            if F_a == 0:
                G_rr = self.R_1 * self.BearingMeanDia ** 1.96 * F_r ** 0.54
            else:
                alpha_F = 24.6 * (F_a / self.C_0) ** 0.24
                G_rr = self.R_1 * self.BearingMeanDia ** 1.96 * (
                            F_r + self.R_2 / math.sin(math.radians(alpha_F)) * F_a) ** 0.54

        M_rr = phi_ish * phi_rs * G_rr * (WheelRpm * self.OilOperatingVisc) ** 0.6
        if self.BearingType == "Angular":
            F_g = self.S_3 * self.BearingMeanDia ** 4 * WheelRpm ** 2
            G_sl = self.S_1 * self.BearingMeanDia ** 0.26 * ((F_r + F_g) ** (4 / 3) + self.S_2 * F_a ** (4 / 3))
        elif self.BearingType == "Groove":
            if F_a == 0:
                G_sl = self.S_1 * self.BearingMeanDia ** -0.26 * F_r ** (5 / 3)
            else:
                alpha_F = 24.6 * (F_a / self.C_0) ** 0.24
                G_sl = self.S_1 * self.BearingMeanDia ** -0.145 * (
                            F_r ** 5 + (self.S_2 * self.BearingMeanDia ** 1.5) / math.sin(
                        math.radians(alpha_F)) * F_a ** 4) ** (1 / 3)
        phi_bl = 1 / math.exp(2.6 * 10 ** -8 * (WheelRpm * self.OilOperatingVisc) ** 1.4 * self.BearingMeanDia)
        myy_sl = phi_bl * 0.12 + (1 - phi_bl) * 0.04
        M_sl = G_sl * myy_sl

        Loss = (M_rr + M_sl) / 1000  # Frictional moment [Nm]
        Loss = Loss * WheelRpm
        return Loss
