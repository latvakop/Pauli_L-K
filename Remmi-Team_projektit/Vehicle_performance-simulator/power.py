# Made by: Remmi-team
# Refactoring to python: Pauli Latva-Kokko

# Object for calculating the engine power.
import math
import numpy as np


class Power:
    """
    Object for calculating the engine power.
    """

    def __init__(self, torqueInput, effiencyInput, driveRatioInput):
        """
        Initializes the power/engine object.
        Parameters
        ----------
        torqueInput: float
            Torque of the engine
        effiencyInput: float
            Efficiency of the engine
        driveRatioInput: float
            Drive ratio of the engine
        """
        self.engine_efficiency_data = np.loadtxt('../engine_efficiency.csv', delimiter=';', skiprows=1)
        self.efficiency_data = self.engine_efficiency_data[:, 1]
        self.engine_rpm_data = self.engine_efficiency_data[:, 0]
        self.torque = torqueInput
        self.effiency = effiencyInput
        self.driveRatio = driveRatioInput
        self.rpm = 0

    def getPower(self, tyreObject, vehicleSpeedInput):
        """
        Calculates the current engine power.
        Parameters
        ----------
        tyreObject: Tyre
            The backwheel of the vehicle.
        vehicleSpeedInput: float
            current speed of the vehicle.

        Returns
        -------
        power: float
            current power of the engine.
        """

        # Calculates rpm from vehicle speed and outputs power.
        if vehicleSpeedInput < 2:  # CLUTCH SLIPS, ENGINE RPM IS IN STEADY STATE
            self.rpm = 2000
        else:  # CLUTCH DOES NOT SLIP, ENGINE RPM DEPENDS ON VEHICLE SPEED
            self.rpm = vehicleSpeedInput / (tyreObject.diam * math.pi) * (1 / self.driveRatio) * 60
            # engineRpm = vehicleSpeedInput/(0.48*math.pi)*(1/self.driveRatio)*60
        power = self.rpm * self.torque / 9.5488

        # Calculating the engine efficiency based on the current rpm, using pre-measured csv-data.
        for i in range(self.engine_rpm_data.size - 2):
            if self.engine_rpm_data[i] < self.rpm and self.engine_rpm_data[i + 1] > self.rpm:
                distance = self.engine_rpm_data[i + 1] - self.engine_rpm_data[i]
                slope = self.engine_efficiency_data[i + 1] / distance
                self.efficiency = slope * (self.rpm - self.engine_rpm_data[i]) + self.engine_efficiency_data[i]

        return power

