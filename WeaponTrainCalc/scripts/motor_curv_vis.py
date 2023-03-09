#
# Lucas Xu-Hill
# March 8, 2023

from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

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

    # Now plot things
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    t_arr = np.linspace(0.0, 5.0, 30)
    I_arr = np.logspace(-5, -3, 30)
    t_mat, I_mat = np.meshgrid(t_arr, I_arr)
    velo_mat = motorModelVelocity(t_mat, I_mat, a, b)

    # Plot the surface.
    surf = ax.plot_surface(I_mat, t_mat, velo_mat, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
    
    plt.show()