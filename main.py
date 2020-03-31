from aircraft import Aircraft
from flight import Flight, State
import initial_conditions as initial

def mae_200_project():
    state = State()
    gamma = state.gamma
    R = state.R

    fuel 	 = 	1*initial.V_fuel_max 						 	   # [lbf] 			 # [SOW]
    W_add 	 = 	30000 									 		   # [lb] 			 # [SOW]
    t_alt 	 = 	465.23 									 		   # [R] 			 # [Table]
    rho_alt  = 	0.0014962 										   # [slugs/ft^3] 	 # [Table]
    mu 	     = 	2.27*10**-8*((t_alt**1.5)/(t_alt+198.6)) # [lb-s/ft^2] 	 # [FS]
    mach	 = 	(gamma*R*t_alt)**0.5 			   # [] 			 # [FS]
    E_max	 = 	0.9283 									 		   # [hr] 			 # [SOW]
    v 	     = 	0.4127*mach 								   # [] 			 # [SOW]
    rnge     =  'N/A'

    E_max_flight = Flight(fuel,W_add,t_alt,rho_alt,v,E_max,rnge)

    

if __name__ == "__main__":
    mae_200_project()