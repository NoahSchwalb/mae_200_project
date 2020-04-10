from aircraft import Aircraft
from flight import Flight, State
import initial_conditions as initial
import math as m
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

class mae_200_project():
    def __init__(self):
        #
        # DON'T FORGET TO FIX ALL THE LIST/NUMPY ARRAY ISSUES
        # NOAH WAS BEING STUPID AND CONVERTED THE NUMPY ARRAYS TO LISTS
        # DON'T LET HIM BE STUPID
        #


        # Part 1
        aircraft = Aircraft()
        gamma = aircraft.state.gamma
        R = aircraft.state.R

        fuel 	 = 	0.5*initial.V_fuel_max 						 	   # [lbf] 			 # [SOW]
        W_add 	 = 	0 									 		   # [lb] 			 # [SOW]
        t_alt 	 = 	418.97 									 		   # [R] 			 # [Table]
        rho_alt  = 	0.00095801 										   # [slugs/ft^3] 	 # [Table]
        mu 	     = 	2.27*10**-8*((t_alt**1.5)/(t_alt+198.6)) # [lb-s/ft^2] 	 # [FS]
        mach	 = 	(gamma*R*t_alt)**0.5 			   # [] 			 # [FS]
        E	     = 	''									 		   # [s] 			 # [SOW]
        v 	     = 	0.801 								   # [ft/s] 			 # [SOW]
        rnge     =  175.8*5280

        V_max_flight = Flight(fuel,W_add,t_alt,rho_alt,v,rnge,E)

        fuel 	 = 	1*initial.V_fuel_max 						 	   # [lbf] 			 # [SOW]
        W_add 	 = 	30000 									 		   # [lb] 			 # [SOW]
        t_alt 	 = 	465.23 									 		   # [R] 			 # [Table]
        rho_alt  = 	0.0014962 										   # [slugs/ft^3] 	 # [Table]
        mu 	     = 	2.27*10**-8*((t_alt**1.5)/(t_alt+198.6)) # [lb-s/ft^2] 	 # [FS]
        mach	 = 	(gamma*R*t_alt)**0.5 			   # [] 			 # [FS]
        E	     = 	0.9283*3600 									 		   # [s] 			 # [SOW]
        v 	     = 	0.4127 								   # [ft/s] 			 # [SOW]
        rnge     =  ''

        E_max_flight = Flight(fuel,W_add,t_alt,rho_alt,v,rnge,E)

        # Find c_t using E_max_flight
        C_L = aircraft.CL(rho_alt,E_max_flight.v,E_max_flight.W_i)
        e = aircraft.oswaldEfficiency(initial.AR_front)
        C_D_i = aircraft.CDi(C_L,e,initial.AR_front)
        C_D_o = C_D_i #max endurance condition
        C_D = aircraft.CD(C_D_i,C_D_o)
        c_t = aircraft.ct(E_max_flight.E,C_L,C_D,E_max_flight.W_i,E_max_flight.W_f)

        # Find C_D_o using V_max_flight
        C_L = aircraft.CL(V_max_flight.rho_alt,V_max_flight.v,V_max_flight.W_i)
        C_D_i = aircraft.CDi(C_L,e,initial.AR_front)
        C_D_o = aircraft.CDo(V_max_flight.rho_alt,initial.S,c_t,C_L,C_D_i,V_max_flight.W_i,V_max_flight.W_f,V_max_flight.rnge)
        C_D = aircraft.CD(C_D_i,C_D_o)

        T_a_28k = aircraft.thrustAvailable(V_max_flight.W_i,C_L,C_D)
        T_a_sl = aircraft.thrustAvailable2Alt(T_a_28k,V_max_flight.rho_alt,aircraft.state.rho_sea)
        #print('T_a_28k: ' + str(T_a_28k))
        #print('T_a_sl: ' + str(T_a_sl))

        v_sl = np.linspace(0.1,1.0,10000)
        v_sl.tolist()
        length = len(v_sl)

        W_add = initial.W_max-initial.V_fuel_max*initial.sigma_fuel-initial.W_f #additional weight needed to reach max possible weight
        sl_flight = Flight(fuel,W_add,aircraft.state.t_sea,aircraft.state.rho_sea,v_sl,'','')
        C_L_sl = aircraft.CL_vector(aircraft.state.rho_sea,sl_flight.v,sl_flight.W_i,length)
        C_D_i_sl = aircraft.CDi_vector(C_L_sl,e,initial.AR_front,length)
        C_D_sl = aircraft.CD_vector(C_D_i_sl,C_D_o,length)
        E_sl = aircraft.endurance_vector(c_t,C_L_sl,C_D_sl,sl_flight.W_i,sl_flight.W_f,length)
        E_max_sl = 0
        for i,value in enumerate(E_sl):
            if value > E_max_sl:
                E_max_sl = value
                E_v_max_sl = sl_flight.v[i]
        
        R_max_sl = 0
        R_sl = aircraft.rnge_vector(sl_flight.rho_alt,initial.S,c_t,C_L_sl,C_D_sl,sl_flight.W_i,sl_flight.W_f,length)
        for i,value in enumerate(R_sl):
            if value > R_max_sl:
                R_max_sl = value
                R_v_max_sl = sl_flight.v[i]


        print('The maximum endurance at sea level is ' + str(E_max_sl) + ' hr and the speed required to achieve that endurance is ' + str(E_v_max_sl) + ' ft/s.\n')
        print('The maximum range at sea level is ' + str(R_max_sl/5280) + ' mi and the speed required to achieve that endurance is ' + str(R_v_max_sl) + ' ft/s.\n')


        # Plot looks about right
        plt.figure(1)
        plt.plot(sl_flight.v,E_sl/3600,label='Endurance')
        plt.plot(E_v_max_sl,E_max_sl/3600,'r*',label='Maximum endurance')
        plt.xlabel('Velcoity [ft/s]')
        plt.ylabel('Endurance [hr]')
        plt.title('Endurance vs Velocity at Sea Level')
        plt.legend()
        plt.savefig('max_E_sl.png')

        plt.figure(2)
        plt.plot(sl_flight.v,R_sl/5280,label='Range')
        plt.plot(R_v_max_sl,R_max_sl/5280,'r*',label='Maximum range')
        plt.xlabel('Velcoity [ft/s]')
        plt.ylabel('Range [mi]')
        plt.title('Range vs Velocity at Sea Level')
        plt.legend()
        plt.savefig('max_R_sl.png')
        


        # Part 2
        v = np.linspace(50,1000,100)
        #rho = np.linspace(0.0000035642,0.002377,100)

        length = len(v)
        #rnge = aircraft.rnge_vector(rho,initial.S,c_t,C_L,C_D,W_i,W_f,length)

        absolute_ceiling_rho = 0.0005680
        P_r = aircraft.powerRequired_vector(absolute_ceiling_rho,v,initial.S,C_D_o,length)

        P_r_min = 10000000000000000000000
        for i,value in enumerate(P_r):
            if value < P_r_min:
                P_r_min = value
                P_r_v_min = sl_flight.v[i]
        #print(P_r_max)
        #print(P_r_v_max)
        P_r_rho_min = absolute_ceiling_rho
        rnge_max_global = aircraft.maxRange(P_r_v_min,P_r_rho_min,C_D_o,c_t,sl_flight.W_i,sl_flight.W_f)
        print(rnge_max_global/5280)
        print(P_r_v_min)
        #fig = plt.figure()
        #ax = fig.gca(projection='3d')

        # Make data.
        #X = rho
        #Y = v
        #Z = rnge
        #X, Y = np.meshgrid(X, Y)
        #R = 4/initial.S/c_t*np.sqrt(initial.W_max)*(np.sqrt(initial.W_max)-np.sqrt(initial.W_max-initial.V_fuel_max*initial.sigma_fuel))
        #Z = R/np.sqrt(Y)/X/(C_D_o+(2*initial.W_max/(Y*X**2*initial.S))**2/np.pi/e/initial.AR_front)

        # Plot the surface.
        #surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
        #                    linewidth=0, antialiased=False)

        # Customize the z axis.
        #ax.set_zlim(-1.01, 1.01)
        #ax.zaxis.set_major_locator(LinearLocator(10))
        #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # Add a color bar which maps values to colors.
        #fig.colorbar(surf, shrink=0.5, aspect=5)

        #plt.show()

        
        #print(rnge)






    

if __name__ == "__main__":
    mae_200_project()