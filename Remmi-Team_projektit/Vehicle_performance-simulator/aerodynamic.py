# Made by: Remmi-Team
# Refactoring to python: Pauli Latva-Kokko

# Class for calculating the cars aerodynamics
class Aerodynamic_object:

    def __init__(self, drag_coef, front_area, rho):
        """
        Initializing the aerodynamic object.
        Parameters
        ----------
        drag_coef: float
            The drag coefficient
        front_area: float
            The area of the front of the car.
        rho: float
            Density of the air
        """
        self.drag_coef = drag_coef
        self.front_area = front_area
        self.rho = rho
    
    def calculate_loss(self, vehicle_speed):
        """
        Parameters
        ----------
        vehicle_speed: float
            The speed of the vehicle
        Returns
        -------
        F_drag: float
            The drag force
        """
        F_drag = 0.5*self.drag_coef*self.front_area*self.rho*vehicle_speed**2
        F_drag = F_drag *vehicle_speed
        return F_drag