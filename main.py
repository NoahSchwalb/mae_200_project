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

        # Calculate service and absolute ceiling, and max R/C at sea level
        length = 5000
        v = np.linspace(50,1000,length)
        rho = np.linspace(0.001,0.002377,length)
        #rho = np.linspace(0.001,0.002,length)
        
        L_D = np.zeros((length,length))
        T_a = np.zeros((length,length))
        T_r = np.zeros((length,length))
        P_r = np.zeros((length,length))
        P_a = np.zeros((length,length))
        R_C = np.zeros((length,length))
        R_C_max = np.zeros(length)

        R_C_service_ceiling = np.zeros((length,length))
        rho_service_ceiling = np.zeros((length,length))
        v_service_ceiling = np.zeros((length,length))
        max_range = np.zeros(length)
        range_test = np.zeros((length,length))
        endurance = np.zeros((length,length))

        R_C_absolute_ceiling = np.zeros((length,length))
        rho_absolute_ceiling = np.zeros((length,length))
        v_absolute_ceiling = np.zeros((length,length))

        tolerance = 1e-2
        for i,rho_val in enumerate(rho):
            for j,v_val in enumerate(v):
                T_a[i][j] = aircraft.thrustAvailable2Alt(T_a_sl,aircraft.state.rho_sea,rho_val)
                C_L = aircraft.CL(rho_val,v_val,sl_flight.W_i)
                C_D_i = aircraft.CDi(C_L,e,initial.AR_front)
                L_D[i][j] = C_L/(C_D_i+C_D_o)
                T_r[i][j] = sl_flight.W_i/L_D[i][j]
                P_r[i][j] = T_r[i][j]*v_val
                P_a[i][j] = T_a[i][j]*v_val
                R_C[i][j] = 60*(P_a[i][j]-P_r[i][j])/sl_flight.W_i
                if R_C[i][j] >= 0:
                    endurance[i][j] = L_D[i][j]*np.log(sl_flight.W_i/sl_flight.W_f)/c_t
                    range_test[i][j] = aircraft.rnge(rho[i],initial.S,c_t,C_L,C_D_o+C_D_i,sl_flight.W_i,sl_flight.W_f)
            temp = 0
            for k,val in enumerate(P_r[i]):
                if R_C[i][k] > temp:
                    temp = R_C[i][k]
            R_C_max[i] = temp

            for h,val in enumerate(R_C[i]):
                if val <= 100+tolerance and val >= 100-tolerance:
                    #print('R/C is about 100')
                    #print('R_C: ' + str(val))
                    #print('rho: ' + str(rho[i]))
                    #print('v: ' + str(v[h]))
                    #print(str(aircraft.rho2Alt(rho[i])) + '\n')
                    R_C_service_ceiling[i][h] = val
                    rho_service_ceiling[i][h] = rho[i]
                    v_service_ceiling[i][h] = v[h]
                elif val <= tolerance and val >= -tolerance:
                    #print('R/C is about 0')
                    #print('R_C: ' + str(val))
                    #print('rho: ' + str(rho[i]))
                    #print('v: ' + str(v[h]))
                    #print(str(aircraft.rho2Alt(rho[i])) + '\n')
                    R_C_absolute_ceiling[i][h] = val
                    rho_absolute_ceiling[i][h] = rho[i]
                    v_absolute_ceiling[i][h] = v[h]
         
        temp1 = 1
        temp3 = 1
        temp2 = 0
        temp4 = 0
        for i,i_val in enumerate(v_absolute_ceiling):
            for j,j_val in enumerate(v_absolute_ceiling):
                if rho_absolute_ceiling[i][j] > 0:
                    #print('Rho (absolute): ' + str(rho_absolute_ceiling[i][j]))
                    #print('V (absolute): ' + str(v_absolute_ceiling[i][j]))
                    #print('\n')
                    if rho_absolute_ceiling[i][j] < temp1:
                        temp1 = rho_absolute_ceiling[i][j]
                        temp2 = v_absolute_ceiling[i][j]
                if rho_service_ceiling[i][j] > 0:
                    #print('Rho (service): ' + str(rho_service_ceiling[i][j]))
                    #print('V (absolute): ' + str(v_service_ceiling[i][j]))
                    #print('\n')
                    if rho_service_ceiling[i][j] < temp3:
                        temp3 = rho_service_ceiling[i][j]
                        temp4 = v_service_ceiling[i][j]

        absolute_ceiling = temp1
        v_absolute = temp2
        service_ceiling = temp3
        v_service = temp4


        max_range = 0
        max_range_v = 0
        max_range_rho = 0
        
        for i,i_val in enumerate(range_test):
            for j,j_val in enumerate(range_test[i]):
                if j_val > max_range:
                    max_range = j_val
                    max_range_v = v[i]
                    max_range_rho = rho[j]

        #print('Velocity for minimum T_r: ' + str(v[np.argmin(T_r[length-1])]))
        #print('Velocity for maximum R_C: ' + str(v[np.argmax(R_C[length-1])]))
        #print('Velocity for maximum L/D: ' + str(v[np.argmax(L_D[length-1])]))
        #print('Velocity for minimum P_r: ' + str(v[np.argmin(P_r[length-1])]))
        #print('Velocity for maximum range: ' + str(v[np.argmax(range_test[length-1])]))
        #print('Velocity for maxmum endurance: ' + str(v[np.argmax(endurance[length-1])]))

        
        fig1 = plt.figure()
        plt.plot(v,range_test[length-1]/5280)
        plt.plot(v[np.argmax(range_test[length-1])],max(range_test[length-1]/5280),'r*',label='Maximum Range')
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('Range [mi]')
        plt.title('Range vs Velocity at Sea Level')
        plt.legend()
        fig1.savefig('rnge_v_sl')
        fig2 = plt.figure()
        plt.plot(v,P_r[length-1],label='Power Required')
        plt.plot(v,P_a[length-1],label='Power Available')
        plt.plot(v[np.argmax(range_test[length-1])],P_r[length-1][np.argmax(range_test[length-1])],'r*',label='Point of Maximum Range')
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('Power [W]')
        plt.title('Power Required vs Power Available at Sea Level')
        plt.legend()
        fig2.savefig('Pr_Pa_sl')
        fig3 = plt.figure()
        plt.plot(v,T_r[length-1],label='Thrust Required')
        plt.plot(v,T_a[length-1],label='Thrust Available')
        plt.plot(v[np.argmax(endurance[length-1])],T_r[length-1][np.argmax(endurance[length-1])],'r*',label='Maximum Endurance and L/D')
        #plt.plot(v,T_v[length-1])
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('Thrust [lb]')
        plt.title('Thrust Required vs Thrust Available at Sea Level')
        plt.legend()
        fig3.savefig('Tr_Ta_sl')
        fig4 = plt.figure()
        plt.plot(v,L_D[length-1])
        plt.plot(v[np.argmax(L_D[length-1])],max(L_D[length-1]),'r*',label='Maximum L/D')
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('L/D [-]')
        plt.title('L/D vs Velocity at Sea Level')
        plt.legend()
        fig4.savefig('L_over_D_sl')
        fig5 = plt.figure()
        plt.plot(v,endurance[length-1]/3600)
        plt.plot(v[np.argmax(endurance[length-1])],max(endurance[length-1]/3600),'r*',label='Maximum Endurance')
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('Endurance [hr]')
        plt.title('Endurance vs Velocity at Sea Level')
        plt.legend()
        fig5.savefig('endurance_v_sl')
        #fig6 = plt.figure()
        #plt.plot(v,ratio[length-1])
        #plt.ylim(0,10)
        #plt.xlabel('Velocity [ft/s]')
        #plt.ylabel('C_D_i/C_D_o [-]')
        #plt.title('Ratio of Induced Drag to Parasitic Drag vs Velocity at Sea Level')
        #plt.show()
        

        # Part 1
        print('\n')
        print('The maximum endurance at sea level is ' + str(E_max_sl/3600) + ' hr and the speed required to achieve that endurance is ' + str(E_v_max_sl) + ' ft/s.\n')
        print('The maximum range at sea level is ' + str(R_max_sl/5280) + ' mi and the speed required to achieve that range is ' + str(R_v_max_sl) + ' ft/s.\n')

        # Part 2
        print('\n')
        print('Global Max Range Data')
        print('Range: ' + str(max_range/5280))
        print('V: ' + str(max_range_v))
        print('Rho: ' + str(max_range_rho))
        index = np.argwhere(rho==max_range_rho)
        print('Alt: ' + str(aircraft.rho2Alt(rho[int(index)])))

        # Part 3


        # Part 4
        print('\n')
        print('Absolute Ceiling: ' + str(aircraft.rho2Alt(absolute_ceiling)) + ' ft at ' + str(v_absolute) + ' ft/s')
        print('Service Ceiling: ' + str(aircraft.rho2Alt(service_ceiling)) + ' ft at ' + str(v_service) + ' ft/s')

        # Part 5
        print('\n')
        print('Max rate of climb at sea level: ' + str(R_C_max[length-1]))
   
        """
        # Graphs at sea level and 23,000 ft
        length = 100
        rho = np.array([0.0011435,0.002377])
        v = np.linspace(50,1000,length)
        T_a = np.zeros((2,length))
        L_D = np.zeros((2,length))
        T_r = np.zeros((2,length))
        P_r = np.zeros((2,length))
        P_a = np.zeros((2,length))
        R_C = np.zeros((2,length))
        endurance = np.zeros((2,length))
        rnge = np.zeros((2,length))

        for i,rho_val in enumerate(rho):
            for j,v_val in enumerate(v):
                T_a[i][j] = aircraft.thrustAvailable2Alt(T_a_sl,aircraft.state.rho_sea,rho_val)
                C_L = aircraft.CL(rho_val,v_val,sl_flight.W_i)
                C_D_i = aircraft.CDi(C_L,e,initial.AR_front)
                L_D[i][j] = C_L/(C_D_i+C_D_o)
                T_r[i][j] = sl_flight.W_i/L_D[i][j]
                P_r[i][j] = T_r[i][j]*v_val
                # P_r[i][j] = np.sqrt(2*(sl_flight.W_i)**3*(C_D_o+C_D_i)**2/(rho_val*initial.S*C_L**3))
                P_a[i][j] = T_a[i][j]*v_val
                R_C[i][j] = 60*(P_a[i][j]-P_r[i][j])/sl_flight.W_i
                if R_C[i][j] >= 0:
                    endurance[i][j] = L_D[i][j]*np.log(sl_flight.W_i/sl_flight.W_f)/c_t
                    rnge[i][j] = aircraft.rnge(rho_val,initial.S,c_t,C_L,C_D_o+C_D_i,sl_flight.W_i,sl_flight.W_f)

        # 23,000 ft graphs
        fig6 = plt.figure()
        plt.plot(v,P_r[0],label='Power Required')
        plt.plot(v,P_a[0],label='Power Available')
        plt.plot(v[np.argmax(rnge[0])],P_r[0][np.argmax(rnge[0])],'r*',label='Point of Maximum Range')
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('Power [W]')
        plt.title('Power Required vs Power Available at 23,000 ft')
        plt.legend()
        fig6.savefig('Pr_Pa_23k')
        fig7 = plt.figure()
        plt.plot(v,T_r[0],label='Thrust Required')
        plt.plot(v,T_a[0],label='Thrust Available')
        plt.plot(v[np.argmax(endurance[0])],T_r[0][np.argmax(endurance[0])],'r*',label='Point of Maximum Endurance and L/D')
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('Thrust [lb]')
        plt.title('Thrust Required vs Thrust Available at 23,000 ft')
        plt.legend()
        fig7.savefig('Tr_Ta_23k')
        fig8 = plt.figure()
        plt.plot(v,R_C[0],label='Rate of Climb')
        plt.plot(v[np.argmax(R_C[0])],max(R_C[0]),'r*',label='Maximum Rate of Climb')
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('Rate of Climb [ft/min]')
        plt.title('Rate of Climb vs Velocity at 23,000 ft')
        plt.legend()
        fig8.savefig('R_C_23k')

        # Sea level graphs
        fig9 = plt.figure()
        plt.plot(v,P_r[1],label='Power Required')
        plt.plot(v,P_a[1],label='Power Available')
        plt.plot(v[np.argmax(rnge[1])],P_r[1][np.argmax(rnge[1])],'r*',label='Point of Maximum Range')
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('Power [W]')
        plt.title('Power Required vs Power Available at Sea Level')
        plt.legend()
        fig9.savefig('Pr_Pa_sl')
        fig10 = plt.figure()
        plt.plot(v,T_r[1],label='Thrust Required')
        plt.plot(v,T_a[1],label='Thrust Available')
        plt.plot(v[np.argmax(endurance[1])],T_r[1][np.argmax(endurance[1])],'r*',label='Point of Maximum Endurance and L/D')
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('Thrust [lb]')
        plt.title('Thrust Required vs Thrust Available at Sea Level')
        plt.legend()
        fig10.savefig('Tr_Ta_sl')
        fig11 = plt.figure()
        plt.plot(v,R_C[1],label='Rate of Climb')
        plt.plot(v[np.argmax(R_C[1])],max(R_C[1]),'r*',label='Maximum Rate of Climb')
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('Rate of Climb [ft/min]')
        plt.title('Rate of Climb vs Velocity at 23,000 ft')
        plt.legend()
        fig11.savefig('R_C_sl')

        plt.show()
        """

        # Modification/Optimization

        # started doing this, realized it was going to be a lot of work so stopped
        """
        S_front = 1.2*initial.S_front
        AR = initial.b_front**2/S_front
        W_f = initial.W_f + 0.2*initial.S*initial.sigma_wing
        C_D_o = 1.06*C_D_o

        aircraft = Aircraft()
        gamma = aircraft.state.gamma
        R = aircraft.state.R

        fuel 	 = 	0.5*initial.V_fuel_max 						 	   # [lbf] 			 # [SOW]
        W_add 	 = 	0.2*initial.S*initial.sigma_wing 									 		   # [lb] 			 # [SOW]
        t_alt 	 = 	418.97 									 		   # [R] 			 # [Table]
        rho_alt  = 	0.00095801 										   # [slugs/ft^3] 	 # [Table]
        mu 	     = 	2.27*10**-8*((t_alt**1.5)/(t_alt+198.6)) # [lb-s/ft^2] 	 # [FS]
        mach	 = 	(gamma*R*t_alt)**0.5 			   # [] 			 # [FS]
        E	     = 	''									 		   # [s] 			 # [SOW]
        v 	     = 	0.801 								   # [ft/s] 			 # [SOW]
        rnge     =  175.8*5280

        V_max_flight = Flight(fuel,W_add,t_alt,rho_alt,v,rnge,E)

        C_L = aircraft.CL(V_max_flight.rho_alt,V_max_flight.v,V_max_flight.W_i)
        C_D_i = aircraft.CDi(C_L,e,)

        T_a_28k = aircraft.thrustAvailable(V_max_flight.W_i,C_L,C_D)
        """

        # conditions that change for the modification
        c_t = 0.5*c_t
        V_fuel_max = 0.75*initial.V_fuel_max

        fuel 	 = 	1*V_fuel_max 						 	   # [lbf] 			 # [SOW]
        W_add = initial.W_max-V_fuel_max*initial.sigma_fuel-initial.W_f #additional weight needed to reach max possible weight
        modified_flight = Flight(fuel,W_add,aircraft.state.t_sea,aircraft.state.rho_sea,0,'','')

        # Main loop, need to edit the one up aboce to only have 1 main loop as well
        length = 5000
        v = np.linspace(50,1000,length)
        rho = np.linspace(0.001,0.002377,length)
        
        L_D = np.zeros((length,length))
        T_a = np.zeros((length,length))
        T_r = np.zeros((length,length))
        P_r = np.zeros((length,length))
        P_a = np.zeros((length,length))
        R_C = np.zeros((length,length))
        R_C_max = np.zeros(length)

        R_C_service_ceiling = np.zeros((length,length))
        rho_service_ceiling = np.zeros((length,length))
        v_service_ceiling = np.zeros((length,length))
        R_C_absolute_ceiling = np.zeros((length,length))
        rho_absolute_ceiling = np.zeros((length,length))
        v_absolute_ceiling = np.zeros((length,length))

        max_range = np.zeros(length)
        range_test = np.zeros((length,length))
        endurance = np.zeros((length,length))

        max_range = 0
        max_range_v = 0
        max_range_rho = 0
        temp1 = 1
        temp3 = 1
        temp2 = 0
        temp4 = 0

        tolerance = 1e-2
        for i,rho_val in enumerate(rho):
            temp = 0
            for j,v_val in enumerate(v):
                T_a[i][j] = aircraft.thrustAvailable2Alt(T_a_sl,aircraft.state.rho_sea,rho_val)
                C_L = aircraft.CL(rho_val,v_val,modified_flight.W_i)
                C_D_i = aircraft.CDi(C_L,e,initial.AR_front)
                L_D[i][j] = C_L/(C_D_i+C_D_o)
                T_r[i][j] = modified_flight.W_i/L_D[i][j]
                P_r[i][j] = T_r[i][j]*v_val
                P_a[i][j] = T_a[i][j]*v_val
                R_C[i][j] = 60*(P_a[i][j]-P_r[i][j])/modified_flight.W_i
                if R_C[i][j] >= 0:
                    endurance[i][j] = L_D[i][j]*np.log(modified_flight.W_i/modified_flight.W_f)/c_t
                    range_test[i][j] = aircraft.rnge(rho_val,initial.S,c_t,C_L,C_D_o+C_D_i,modified_flight.W_i,modified_flight.W_f)
                if R_C[i][j] > temp:
                    temp = R_C[i][j]
                R_C_max[i] = temp
                if R_C[i][j] <= 100+tolerance and R_C[i][j] >= 100-tolerance:
                    R_C_service_ceiling[i][j] = R_C[i][j]
                    rho_service_ceiling[i][j] = rho_val
                    v_service_ceiling[i][j] = v_val
                elif R_C[i][j] <= tolerance and R_C[i][j] >= -tolerance:
                    R_C_absolute_ceiling[i][j] = R_C[i][j]
                    rho_absolute_ceiling[i][j] = rho_val
                    v_absolute_ceiling[i][j] = v_val
                if rho_absolute_ceiling[i][j] < temp1 and rho_absolute_ceiling[i][j] > 0:
                    temp1 = rho_absolute_ceiling[i][j]
                    temp2 = v_absolute_ceiling[i][j]
                if rho_service_ceiling[i][j] < temp3 and rho_service_ceiling[i][j] > 0:
                    temp3 = rho_service_ceiling[i][j]
                    temp4 = v_service_ceiling[i][j]
                if range_test[i][j] > max_range:
                    max_range = range_test[i][j]
                    max_range_v = v_val
                    max_range_rho = rho_val

        absolute_ceiling = temp1
        v_absolute = temp2
        service_ceiling = temp3
        v_service = temp4

        fig1 = plt.figure()
        plt.plot(v,range_test[length-1]/5280)
        plt.plot(v[np.argmax(range_test[length-1])],max(range_test[length-1]/5280),'r*',label='Maximum Range')
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('Range [mi]')
        plt.title('Range vs Velocity at Sea Level')
        plt.legend()
        fig1.savefig('rnge_v_sl')
        fig2 = plt.figure()
        plt.plot(v,P_r[length-1],label='Power Required')
        plt.plot(v,P_a[length-1],label='Power Available')
        plt.plot(v[np.argmax(range_test[length-1])],P_r[length-1][np.argmax(range_test[length-1])],'r*',label='Point of Maximum Range')
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('Power [W]')
        plt.title('Power Required vs Power Available at Sea Level')
        plt.legend()
        fig2.savefig('Pr_Pa_sl')
        fig3 = plt.figure()
        plt.plot(v,T_r[length-1],label='Thrust Required')
        plt.plot(v,T_a[length-1],label='Thrust Available')
        plt.plot(v[np.argmax(endurance[length-1])],T_r[length-1][np.argmax(endurance[length-1])],'r*',label='Maximum Endurance and L/D')
        #plt.plot(v,T_v[length-1])
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('Thrust [lb]')
        plt.title('Thrust Required vs Thrust Available at Sea Level')
        plt.legend()
        fig3.savefig('Tr_Ta_sl')
        fig4 = plt.figure()
        plt.plot(v,L_D[length-1])
        plt.plot(v[np.argmax(L_D[length-1])],max(L_D[length-1]),'r*',label='Maximum L/D')
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('L/D [-]')
        plt.title('L/D vs Velocity at Sea Level')
        plt.legend()
        fig4.savefig('L_over_D_sl')
        fig5 = plt.figure()
        plt.plot(v,endurance[length-1]/3600)
        plt.plot(v[np.argmax(endurance[length-1])],max(endurance[length-1]/3600),'r*',label='Maximum Endurance')
        plt.xlabel('Velocity [ft/s]')
        plt.ylabel('Endurance [hr]')
        plt.title('Endurance vs Velocity at Sea Level')
        plt.legend()
        fig5.savefig('endurance_v_sl')
        #fig6 = plt.figure()
        #plt.plot(v,ratio[length-1])
        #plt.ylim(0,10)
        #plt.xlabel('Velocity [ft/s]')
        #plt.ylabel('C_D_i/C_D_o [-]')
        #plt.title('Ratio of Induced Drag to Parasitic Drag vs Velocity at Sea Level')
        #plt.show()
        

        # Part 1
        print('\n')
        print('The maximum endurance at sea level is ' + str(max(endurance[length-1]/3600)) + ' hr and the speed required to achieve that endurance is ' + str(v[np.argmax(endurance[length-1])]) + ' ft/s.\n')
        print('The maximum range at sea level is ' + str(max(range_test[length-1]/5280)) + ' mi and the speed required to achieve that range is ' + str(v[np.argmax(range_test[length-1])]) + ' ft/s.\n')

        # Part 2
        print('\n')
        print('Global Max Range Data')
        print('Range: ' + str(max_range/5280))
        print('V: ' + str(max_range_v))
        print('Rho: ' + str(max_range_rho))
        index = np.argwhere(rho==max_range_rho)
        print('Alt: ' + str(aircraft.rho2Alt(rho[int(index)])))

        # Part 3


        # Part 4
        print('\n')
        print('Absolute Ceiling: ' + str(aircraft.rho2Alt(absolute_ceiling)) + ' ft at ' + str(v_absolute) + ' ft/s')
        print('Service Ceiling: ' + str(aircraft.rho2Alt(service_ceiling)) + ' ft at ' + str(v_service) + ' ft/s')

        # Part 5
        print('\n')
        print('Max rate of climb at sea level: ' + str(R_C_max[length-1]))








if __name__ == "__main__":
    mae_200_project()