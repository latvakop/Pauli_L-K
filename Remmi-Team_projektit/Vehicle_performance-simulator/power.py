# Made by: Remmi-team
# Refactoring to python: Pauli Latva-Kokko

import math

# Object for calculating the engine power.
class Power:

    def __init__(self, torque_input, efficiency_input, drive_ratio_input):
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
        self.torque = torque_input
        self.efficiency = efficiency_input
        self.drive_ratio = drive_ratio_input
        
        
    def getPower(self,tyre_object,vehicle_speed_input):
        """
        Calculates the current engine power.
        Parameters
        ----------
        tyre_object: Tyre
            The backwheel of the vehicle.
        vehicle_speed_input: float
            current speed of the vehicle.

        Returns
        -------
        power: float
            current power of the engine.
        """
        # Calculates rpm from vehicle speed and outputs power.        
        if vehicle_speed_input < 2: # CLUTCH SLIPS, ENGINE RPM IS IN STEADY STATE
            engine_rpm = 2000
        else:   # CLUTCH DOES NOT SLIP, ENGINE RPM DEPENDS ON VEHICLE SPEED
            engine_rpm = vehicle_speed_input / (tyre_object.diam*math.pi)*(1/self.drive_ratio)*60
            #engineRpm = vehicle_speed_input/(0.48*math.pi)*(1/self.drive_ratio)*60
        power = engine_rpm*self.torque/9.5488
        return power
   

