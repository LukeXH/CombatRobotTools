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
        # Initialize Motor Model
        self.kv = 2.0*np.pi/60.0 * kv_rpm
        self.kt = 1/self.kv
        i_nom_stall = v_op/v_stall * i_stall
        a = self.kt * i_nom_stall
        b = a/(self.kv * v_op)
        self.motorM = MotorModel.MotorModel(a,b)

    def velocity(self, t:np.matrix, I:np.matrix, g:np.matrix) -> np.matrix:
        """
        Calculate velocity of the weapon as a function of time
        and inertia
          t = time, sec
          I = inertial load on the motor (kg-m^2)
          g = gear ratio out:in ( > 1 more torque, < 1 more speed)
        Outputs
          weapon velocity in rad/sec
        """
        # First calculate the reflected inertia, interia experienced
        # by the motor through whatever gearbox is there
        I_ref = np.divide(I, np.multiply(g,g))
        return np.multiply(np.divide(1.0, g),self.motorM.velocity(t,I_ref))

    def energy(self, t:np.matrix, I:np.matrix, g:np.matrix) -> np.matrix:
        """
        Calculate energy of the weapon as a function of time
        and inertia
          t = time, sec
          I = inertial load on the motor (kg-m^2)
          g = gear ratio out:in ( > 1 more torque, < 1 more speed)
        Outputs
          weapon energy in Joules (kg-m^2/sec^2)
        """
        # First calculate the reflected inertia, interia experienced
        # by the motor through whatever gearbox is there
        I_ref = np.divide(I, np.multiply(g,g))
        v_wep = np.multiply(np.divide(1.0, g),self.motorM.velocity(t,I_ref))
        return 0.5 * np.multiply(I, np.multiply(v_wep, v_wep))

    def displayGraphs(self, t_target, weapon_moi, gear_ratio) -> float:
        """ Create the graph of energy for 
                t_target = sec, time target for spinup
                weapon_moi = kg * m^2
                gear_ratio = size of gears out:in ( > 1 more torque, < 1 more speed)
        """
        t_arr = np.linspace(0.0, t_target + 2.0, 30)
        w_m_order = np.log10(weapon_moi)
        I_arr = np.logspace(np.floor(w_m_order) - 1.0, w_m_order+np.log10(2), 30)
        g_r_order = np.log10(gear_ratio)
        g_arr = np.logspace(g_r_order - np.log10(4), g_r_order + np.log10(4), 30)
        
        # For the energy graph, fixed gear ratio
        I_mat1, t_mat = np.meshgrid(I_arr, t_arr)
        velo_mat_for_tI = self.velocity(t_mat, I_mat1, gear_ratio)
        velo_line_for_t = self.velocity(t_arr, weapon_moi, gear_ratio)
        velo_line_for_I = self.velocity(t_target, I_arr, gear_ratio)
        energy_mat_for_tI = self.energy(t_mat, I_mat1, gear_ratio)
        energy_line_for_t = self.energy(t_arr, weapon_moi, gear_ratio)
        energy_line_for_I = self.energy(t_target, I_arr, gear_ratio)

        # Energy graph for fixed time
        I_mat2, g_mat = np.meshgrid(I_arr, g_arr)
        energy_mat_gI = self.energy(t_target, I_mat2, g_mat)
        energy_line_gI_for_g = self.energy(t_target, weapon_moi, g_arr)
        energy_line_gI_for_I = self.energy(t_target, I_arr, gear_ratio)

        # Energy graph for fixed MoI
        g_mat3, t_mat3 = np.meshgrid(g_arr, t_arr)
        energy_mat_gt = self.energy(t_mat3, weapon_moi, g_mat3)
        energy_line_gt_for_g = self.energy(t_target, weapon_moi, g_arr)
        energy_line_gt_for_t = self.energy(t_arr, weapon_moi, gear_ratio)

        # Plot the surface for the energy graph
        fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
        self.figs.append(fig1)
        surf = ax1.plot_surface(I_mat1, t_mat, energy_mat_for_tI, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False, zorder=1)
        # surf = ax1.plot_surface(I_mat, t_mat, energy_mat_for_tI, cmap=cm.coolwarm, antialiased=False, zorder=1)
        ax1.plot( weapon_moi*np.ones(t_arr.size), t_arr, energy_line_for_t, 'k', linewidth=4, zorder=3) # No clue why zorder has to be 3...
        ax1.plot( I_arr, t_target*np.ones(I_arr.size), energy_line_for_I, 'k', linewidth=4, zorder=3) # No clue why zorder has to be 3...
        ax1.set_xlabel("MoI (kg-m^2)")
        ax1.set_ylabel("Time (sec)")
        ax1.set_zlabel("Energy (J)")
        ax1.set_title("Energy Graph for fixed gear ratio (out:in): " + str(gear_ratio))

        # Plot the surface for the velocity graph
        fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})
        self.figs.append(fig2)
        surf = ax2.plot_surface(I_mat1, t_mat, velo_mat_for_tI, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False)
        ax2.plot(weapon_moi*np.ones(t_arr.size), t_arr, velo_line_for_t, 'k', linewidth=4, zorder=3) # No clue why zorder has to be 3...
        ax2.plot( I_arr, t_target*np.ones(I_arr.size), velo_line_for_I, 'k', linewidth=4, zorder=3) # No clue why zorder has to be 3...
        ax2.set_xlabel("MoI (kg-m^2)")
        ax2.set_ylabel("Time (sec)")
        ax2.set_zlabel("Velocity (rad/sec)")
        ax2.set_title("Velocity Graph for fixed gear ratio (out:in): " + str(gear_ratio))
        
        # Plot the surface for the energy graph for fixed time
        fig3, ax3 = plt.subplots(subplot_kw={"projection": "3d"})
        self.figs.append(fig3)
        surf = ax3.plot_surface(I_mat2, g_mat, energy_mat_gI, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False)
        ax3.plot(weapon_moi*np.ones(g_arr.size), g_arr, energy_line_gI_for_g, 'k', linewidth=4, zorder=3) # No clue why zorder has to be 3...
        ax3.plot(I_arr, gear_ratio*np.ones(I_arr.size), energy_line_gI_for_I, 'k', linewidth=4, zorder=3) # No clue why zorder has to be 3...
        ax3.set_xlabel("MoI (kg-m^2)")
        ax3.set_ylabel("gear ratio (out:in)")
        ax3.set_zlabel("Energy (J)")
        ax3.set_title("Energy Graph for fixed time: " + str(t_target))

        # Plot the surface for the energy graph for fixed MoI
        fig4, ax4 = plt.subplots(subplot_kw={"projection": "3d"})
        self.figs.append(fig4)
        surf = ax4.plot_surface(g_mat3, t_mat3, energy_mat_gt, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False)
        ax4.plot(g_arr, t_target*np.ones(g_arr.size), energy_line_gt_for_g, 'k', linewidth=4, zorder=3) # No clue why zorder has to be 3...
        ax4.plot(gear_ratio*np.ones(t_arr.size), t_arr, energy_line_gt_for_t, 'k', linewidth=4, zorder=3) # No clue why zorder has to be 3...
        ax4.set_xlabel("gear ratio (out:in)")
        ax4.set_ylabel("Time (sec)")
        ax4.set_zlabel("Energy (J)")
        ax4.set_title("Energy Graph for MoI: " + str(weapon_moi))

        plt.show()

        return (self.energy(t_target, weapon_moi, gear_ratio), self.velocity(t_target, weapon_moi, gear_ratio))

    def closeGraphs(self):
        # print('Closing all graphs inside')
        while self.figs:
            plt.close(self.figs.pop())