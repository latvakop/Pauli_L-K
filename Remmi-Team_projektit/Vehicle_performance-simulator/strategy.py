# Made by: Teemu Lehtonen from Remmi-Team
# Refactoring to python: Jesper Granat

class Strategy:

    StrategyState = 0
    accelerationCounter = 0
    EventParameter = 21
    
    def __init__(self, StrategyNumber,
                       FirstAccelerationStop, OtherAccelerationStart,
                       OtherAccelerationStop, LastAccelerationStart,
                       LastAccelerationStop):
        """
        Constructor for creating a strategy with the wanted speed parameters.
        Parameters
        ----------
        StrategyNumber: int
            The number of the strategy, there is only one strategy now but maybe more will be added later
        FirstAccelerationStop: float
            The speed in which the first acceleration is stopped(km/h)
        OtherAccelerationStart: float
            The speed in which all the other accelerations that are not the first or last will be started(km/h)
        OtherAccelerationStop: float
            The speed where all the other accelerations that are not the first or last one will be stopped(km/h)
        LastAccelerationStart
            Starting speed of the last acceleration(km/h)
        LastAccelerationStop:
            Ending speed of the last acceleration(km/h)
        """
        self.StrategyNumber = StrategyNumber
        self.FirstAccelerationStop = FirstAccelerationStop/3.6
        self.OtherAccelerationStart = OtherAccelerationStart/3.6
        self.OtherAccelerationStop = OtherAccelerationStop/3.6
        self.LastAccelerationStart = LastAccelerationStart/3.6
        self.LastAccelerationStop = LastAccelerationStop/3.6
            
        
    def getStrategy(self, CurrentSpeed, Tyre_3, Engine, lapCounter,
                    TOTAL_LAPS, TrackPosition, TRACK_LENGTH):
        if self.StrategyNumber == 1:
            # First acceleration
            if self.accelerationCounter == 0:
                if CurrentSpeed < self.FirstAccelerationStop: # Start acceleration
                    powerAdded = Engine.getPower(Tyre_3,CurrentSpeed)
                elif CurrentSpeed > self.FirstAccelerationStop: #End acceleration
                    powerAdded = 0
                    self.accelerationCounter = self.accelerationCounter + 1

            # Other accelerations
            elif lapCounter < TOTAL_LAPS - 1:
                if CurrentSpeed < self.OtherAccelerationStart and self.StrategyState == 0: # Start acceleration
                    self.StrategyState = 1
                    powerAdded = Engine.getPower(Tyre_3,CurrentSpeed)
                elif CurrentSpeed < self.OtherAccelerationStop and self.StrategyState == 1:
                    powerAdded = Engine.getPower(Tyre_3,CurrentSpeed)
                elif CurrentSpeed > self.OtherAccelerationStop and self.StrategyState == 1: #End acceleration
                    self.StrategyState = 0
                    powerAdded = 0
                    self.accelerationCounter = self.accelerationCounter + 1
                else:
                    powerAdded = 0

            # Last acceleration
            elif lapCounter == TOTAL_LAPS - 1:
                if TrackPosition > TRACK_LENGTH/2:
                    self.StrategyState = 0
                    powerAdded = 0
                    self.accelerationCounter = self.accelerationCounter + 1
                elif CurrentSpeed < self.LastAccelerationStart and self.StrategyState == 0: # Start acceleration
                    self.StrategyState = 1
                    powerAdded = Engine.getPower(Tyre_3,CurrentSpeed)
                elif CurrentSpeed < self.LastAccelerationStop and self.StrategyState == 1:
                    powerAdded = Engine.getPower(Tyre_3,CurrentSpeed)
                elif CurrentSpeed > self.LastAccelerationStop and self.StrategyState == 1:#  End acceleration
                    self.StrategyState = 0
                    powerAdded = 0
                    self.accelerationCounter = self.accelerationCounter + 1
                else:
                    powerAdded = 0
            else:
                powerAdded = 0
        return powerAdded
