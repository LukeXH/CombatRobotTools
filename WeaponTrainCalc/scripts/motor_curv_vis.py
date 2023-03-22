#
# Lucas Xu-Hill
# March 8, 2023

from matplotlib import cm
import matplotlib.pyplot as plt
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
        return self.a/self.b * (1 - np.exp(-b * np.divide(t,I)))
    
    def energy(self, t:np.matrix, I:np.matrix) -> np.matrix:
        # kg * (m/s)^2
        return 0.5 * np.multiply(I, np.multiply(self.velocity(t,I), self.velocity(t,I)) )

    def inertia(self, t:np.matrix, I:np.matrix) -> np.matrix:
        # kg * m/s
        return np.multiply(I, self.velocity(t,I) )

    def power(self, t:np.matrix, I:np.matrix) -> np.matrix:
        x = np.divide(t,I)
        return self.a**2 / self.b * np.multiply(np.exp(-2.0*self.b*x), (np.exp(self.b*x) - 1))

def motorModelVelocity(t:np.matrix, I:np.matrix, a:float, b:float) -> np.matrix:
    # Function that produces a time curve of the motor velocity in rad/sec
    # given the following parameters:
    #   t = time in n x m array/matrix
    #   I = MoI in kg-m^2 in n x m array/matrix
    #   a = torque curve constant a
    #   b = torque curve constant b
    return a/b * (1 - np.exp(-b * np.divide(t,I)))

if __name__ == "__main__":
    # User defined weapon parameters
    moi_wep = 5.6e-4 # kg-m^2

    # User defined motor parameters
    #   Tmotor AS2814 900KV
    kv_rpm = 900 # Motor KV in RPM, posted on sheet
    i_stall = 37 # stall current @ max power
    w_max = 553 # Max power
    v_op = 11.1 # operational voltage

    # Derived motor parameters
    kv = 2.0*np.pi/60.0 * kv_rpm # rad/sec * 1/V
    kt = 1/kv
    v_nom = w_max / i_stall
    i_nom_stall = v_op/v_nom * i_stall

    # Motor torque curve parameters
    # torque = a - b * speed (rad/sec)
    a = kt * i_nom_stall
    b = a/(kv*v_op)

    motor_model = MotorModel(a,b)

    # Now plot things
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    t_arr = np.linspace(0.0, 5.0, 30)
    I_arr = np.logspace(-5, -3, 30)
    I_mat, t_mat = np.meshgrid(I_arr, t_arr)
    velo_mat = motor_model.energy(t_mat, I_mat)

    # Plot the surface.
    surf = ax.plot_surface(I_mat, t_mat, velo_mat, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
    
    plt.show()