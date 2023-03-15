#
# Lucas Xu-Hill
# March 15, 2023

from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import MotorModel

class WeaponSysModel:
    def __init__(self) -> None:
        self.motorM : MotorModel.MotorModel = None

        # Motor parameters
        self.kv = 0.0
        self.kt = 0.0
        self.figs = []

    def initMotorModel(self,
                  kv_rpm,
                  i_stall,
                  v_stall,
                  v_op):
        """Initialize model """
        self.kv = 2.0*np.pi/60.0 * kv_rpm
        self.kt = 1/self.kv
        i_nom_stall = v_op/v_stall * i_stall
        a = self.kt * i_nom_stall
        b = a/(self.kv * v_op)
        self.motorM = MotorModel.MotorModel(a,b)

    def displayGraphs(self, t_target, weapon_moi, gear_ratio):
        """ Create the graph of energy for 
                t_target = sec, time target for spinup
                weapon_moi = kg * m^2
                gear_ratio = size of gears out:in ( > 1 more torque, < 1 more speed)
        """
        t_arr = np.linspace(0.0, t_target + 2.0, 30)
        w_m_order = np.log10(weapon_moi)
        I_arr = np.logspace(np.floor(w_m_order) - 1.0, np.ceil(w_m_order) + 1.0, 30)
        g_arr = np.linspace(gear_ratio/10.0, gear_ratio*10.0, 30)
        
        # For the energy graph, fixed gear ratio
        I_g_arr = I_arr / gear_ratio**2.0
        I_g_mat, t_mat = np.meshgrid(I_g_arr, t_arr)
        velo_mat_for_tI = self.motorM.energy(t_mat, I_g_mat)

        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        self.figs.append(fig)
        # Plot the surface.
        surf = ax.plot_surface(I_g_mat, t_mat, velo_mat_for_tI, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False)
        
        plt.show()

    def closeGraphs(self):
        # print('Closing all graphs inside')
        while self.figs:
            plt.close(self.figs.pop())