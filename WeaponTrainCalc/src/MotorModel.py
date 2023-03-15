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
        # m/s
        return self.a/self.b * (1 - np.exp(-self.b * np.divide(t,I)))
    
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