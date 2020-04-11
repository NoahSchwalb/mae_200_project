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

        """
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
        """


        # Part 2
        length = 100
        v = np.linspace(50,1000,length)
        #rho = np.linspace(0.00001,0.002377,length)
        rho = np.linspace(0.0010620000000000002,0.001085909090909091,length)
        
        P_r = np.zeros((length,length))
        P_r_min = np.zeros(length)
        P_r_min_v = np.zeros(length)
        P_a = np.zeros((length,length))
        R_C = np.zeros((length,length))
        R_C_max = np.zeros(length)

        for i,rho_val in enumerate(rho):
            T_a = aircraft.thrustAvailable2Alt(T_a_sl,aircraft.state.rho_sea,rho_val)
            for j,v_val in enumerate(v):
                C_L = aircraft.CL(rho_val,v_val,sl_flight.W_i)
                C_D_i = aircraft.CDi(C_L,e,initial.AR_front)
                P_r[i][j] = np.sqrt(2*(sl_flight.W_i)**3*(C_D_o+C_D_i)**2/(rho_val*initial.S*C_L**3))
                P_a[i][j] = T_a*v_val
                R_C[i][j] = 60*(P_a[i][j]-P_r[i][j])/sl_flight.W_i
            temp1 = 1e20
            temp3 = 0
            for k,val in enumerate(P_r[i]):
                if val < temp1:
                    temp1 = val
                    temp2 = v[k]
                if R_C[i][k] > temp3:
                    temp3 = R_C[i][k]
            P_r_min[i] = temp1
            P_r_min_v[i] = temp2
            R_C_max[i] = temp3
        
        #print(P_r_min)
        #print(P_r_min_v)
        print(R_C_max)
        print(R_C_max[82])
        print(rho[81])
        print(rho[82]) #service ceiling density
        print(aircraft.rho2Alt(rho[82])) #service ceiling altitude

        #X,Y = np.meshgrid(v,rho)
        #Z = P_r
        #fig = plt.figure()
        #ax = fig.gca(projection='3d')
        #surf = ax.plot_surface(X,Y,Z)
        #plt.show()

        
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