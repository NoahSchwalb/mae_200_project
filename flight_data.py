import initial_conditions as initial
from aircraft import Aircraft

## Max velocity flight
class v_max_flight(Aircraft):
	def __init__(self):
		self.fuel 	 = 	0.5*initial.V_fuel_max 					 		   # [lbf] 			 # [SOW]
		self.W_add 	 = 	0 										 		   # [lbf] 			 # [SOW]
		self.alt 	 = 	28000 									 		   # [ft] 			 # [SOW]
		self.t_alt 	 = 	418.97 									 		   # [R] 			 # [Table]
		self.rho_alt = 	0.00095801 								 		   # [slugs/ft^3] 	 # [Table]
		self.mu 	 = 	2.27*10**-8*((self.t_alt**1.5)/(self.t_alt+198.6)) # [lb-s/ft^2] 	 # [FS]
		self.gamma 	 = 	1.6 									 		   # [] 			 # []
		self.R		 = 	1716 									 		   # [ft-lbf/slug-R] # [FS]
		self.mach 	 = 	(self.gamma*self.R*self.t_alt)**0.5 			   # [ft/s] 		 # [FS]
		self.v_max 	 = 	0.801*self.mach  							 	   # [ft/s] 		 # [SOW]
		self.range 	 = 	175.8 									 		   # [mi] 			 # [SOW]

## Max endurance flight
class E_max_flight(Aircraft):
	def __init__(self):
		self.fuel 	 = 	initial.V_fuel_max 						 		   # [lbf] 			 # [SOW]
		self.W_add 	 = 	30000 									 		   # [lb] 			 # [SOW]
		self.alt 	 = 	15000 									 		   # [ft] 			 # [SOW]
		self.t_alt 	 = 	465.23 									 		   # [R] 			 # [Table]
		self.rho_alt = 	0.0014962 										   # [slugs/ft^3] 	 # [Table]
		self.mu 	 = 	2.27*10**-8*((self.t_alt**1.5)/(self.t_alt+198.6)) # [lb-s/ft^2] 	 # [FS]
		self.gamma 	 = 	1.6 									 		   # [] 			 # []
		self.R 		 = 	1716 									 		   # [ft-lbf/slug-R] # [FS]
		self.mach	 = 	(self.gamma*self.R*self.t_alt)**0.5 			   # [] 			 # [FS]
		self.E_max	 = 	0.9283 									 		   # [hr] 			 # [SOW]
		self.v_inf 	 = 	0.4127*self.mach 								   # [] 			 # [SOW]