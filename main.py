from aircraft import Aircraft
from flight import Flight, State
import initial_conditions as initial
import math as m
import numpy as np
import matplotlib.pyplot as plt

def mae_200_project():
    aircraft = Aircraft()
    gamma = aircraft.state.gamma
    R = aircraft.state.R

    fuel 	 = 	1*initial.V_fuel_max 						 	   # [lbf] 			 # [SOW]
    W_add 	 = 	30000 									 		   # [lb] 			 # [SOW]
    t_alt 	 = 	465.23 									 		   # [R] 			 # [Table]
    rho_alt  = 	0.0014962 										   # [slugs/ft^3] 	 # [Table]
    mu 	     = 	2.27*10**-8*((t_alt**1.5)/(t_alt+198.6)) # [lb-s/ft^2] 	 # [FS]
    mach	 = 	(gamma*R*t_alt)**0.5 			   # [] 			 # [FS]
    E	 = 	0.9283*3600 									 		   # [s] 			 # [SOW]
    v 	     = 	0.4127*mach 								   # [] 			 # [SOW]
    rnge     =  ''

    
    E_max_flight = Flight(fuel,W_add,t_alt,rho_alt,v,rnge,E)
    C_L = aircraft.CL(rho_alt,v,E_max_flight.W_i)
    e = aircraft.oswaldEfficiency(initial.AR_front)
    C_D_i = aircraft.CDi(C_L,e,initial.AR_front)
    C_D_o = C_D_i #max endurance condition
    C_D = aircraft.CD(C_D_i,C_D_o)
    c_t = aircraft.ct(E_max_flight.E,C_L,C_D,E_max_flight.W_i,E_max_flight.W_f)
    rnge = aircraft.rnge(rho_alt,initial.S,c_t,C_L,C_D,E_max_flight.W_i,E_max_flight.W_f) #range for the max endurance flight data
    
    v_sl = np.linspace(0,1.0,500)
    v_sl.tolist()
    length = len(v_sl)
    W_add = initial.W_max-initial.V_fuel_max*initial.sigma_fuel-initial.W_f #additional weight needed to reach max possible weight
    E_sl_flight = Flight(fuel,W_add,aircraft.state.t_sea,aircraft.state.rho_sea,v_sl,'','')
    C_L_sl = aircraft.CL_vector(aircraft.state.rho_sea,E_sl_flight.v,E_sl_flight.W_i,length)
    C_D_i_sl = aircraft.CDi_vector(C_L_sl,e,initial.AR_front,length)
    C_D_o_sl = C_D_i_sl
    C_D_sl = aircraft.CD_vector(C_D_i_sl,C_D_o_sl,length)
    E_sl = aircraft.endurance_vector(c_t,C_L_sl,C_D_sl,E_sl_flight.W_i,E_sl_flight.W_f,length)
    for i,value in enumerate(E_sl):
        if value == 'nan':
            E_sl[i] = 0
    print(E_sl)
    plt.plot(v_sl,E_sl/3600)
    plt.show()
    #print(C_L_sl[300])
    #print(C_D_sl[300])
    #print(v_sl[300])
    #print(E_sl_flight.W_i)
    #print(E_sl_flight.W_f)
    #print(E_sl[300]/3600)

    

if __name__ == "__main__":
    mae_200_project()