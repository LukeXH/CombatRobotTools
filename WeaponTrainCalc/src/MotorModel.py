#
# Lucas Xu-Hill
# March 15, 2023

import numpy as np


class MotorModel:
    def __init__(self, a:float, b:float) -> None:
        # Torque curve torque = a - b* speed
        #   a = torque curve constant a
        #   b = torque curve constant b
        self.a = a
        self.b = b

    def velocity(self, t:np.matrix, I:np.matrix) -> np.matrix:
        # Calculate velocity of the motor as a function of time
        # and inertia
        #   t = time, sec
        #   I = inertial load on the motor (kg-m^2)
        # Outputs
        #   motor velocity in rad/s
        return self.a/self.b * (1 - np.exp(-self.b * np.divide(t,I)))
    
    def torque(self, t:np.matrix, I:np.matrix) -> np.matrix:
        # N-m
        return self.a - self.b * self.velocity(t,I)
    
    def power(self, t:np.matrix, I:np.matrix) -> np.matrix:
        # Watts (N-m/s)
        v = self.velocity(t,I)
        return np.multiply(v, self.a - self.b*v)
    
    def energy(self, t:np.matrix, I:np.matrix) -> np.matrix:
        # kg * (m/s)^2
        return 0.5 * np.multiply(I, np.multiply(self.velocity(t,I), self.velocity(t,I)) )

    def inertia(self, t:np.matrix, I:np.matrix) -> np.matrix:
        # kg * m/s
        return np.multiply(I, self.velocity(t,I) )

    def power(self, t:np.matrix, I:np.matrix) -> np.matrix:
        # Watts
        x = np.divide(t,I)
        return self.a**2 / self.b * np.multiply(np.exp(-2.0*self.b*x), (np.exp(self.b*x) - 1))