import initial_conditions as initial
import math as m

class Flight():
	"""
	Module to define the flight segment of an aircraft mission

	Units: English

	Example:
		import initial_conditions as initial

		fuel = 1*initial.V_fuel_max
		W_add = 0
		t_alt = 400
		rho_alt = 0.0001234
		velocity = 0.5
		rnge = 1000
		flight = Flight(fuel,W_add,t_alt,rho_alt,velocity,rnge)

	Inputs:
	 1. fuel  - weight of fuel as function of max fuel
	 2. W_add - additional weight added to the aircraft
	 3. t 	  - temperature at the altitude for the flight
	 4. rho   - density at the altitude for the flight
	 5. v 	  - velocity as a function of mach number
	 6. rnge  - range of the aircraft for the flight
	 
	"""
  
	def __init__(self,fuel,W_add,t_alt,rho_alt,v,rnge,E):
		state = State()
		self.fuel 	 = 	fuel					 		   				   # [lbf] 			 # [SOW]
		self.W_add 	 = 	W_add 											   # [lbf] 			 # [SOW]
		self.W_f 	 =  initial.W_f+W_add 								   # [lbf] 			 # [SOW]
		self.W_i 	 =  self.W_f+self.fuel*initial.sigma_fuel			   # [lbf]			 # [SOW]
		self.t_alt 	 = 	t_alt									 		   # [R] 			 # [Table]
		self.rho_alt = 	rho_alt 								 		   # [slugs/ft^3] 	 # [Table]
		self.mu 	 = 	2.27*10**-8*((self.t_alt**1.5)/(self.t_alt+198.6)) # [lb-s/ft^2] 	 # [FS]
		self.mach 	 = 	(state.gamma*state.R*self.t_alt)**0.5 			   # [ft/s] 		 # [FS]
		if str(v) != '':
			self.v 	 	 = 	v*self.mach  							 	   	   # [ft/s] 		 # [SOW]
		else:
			self.v 	 =  v
		self.rnge 	 =  rnge										   	   # [ft] 			 # [SOW]
		self.E 		 =  E										 	 	   # [hr]			 # [SOW]

class State():
	def __init__(self):
		self.gamma 	 = 	1.4 									 		   # [-] 			 # [-]
		self.R		 = 	1716 									 		   # [ft-lbf/slug-R] # [FS]
		self.rho_sea = 	0.002377										   # [slugs/ft^3]	 # [FS]
		self.t_sea 	 = 	518.67											   # [R] 			 # [FS]
		self.mu_sea  = 	2.27*10**-8*((self.t_sea**1.5)/(self.t_sea+198.6)) # [lb-s/ft^2] 	 # [FS]

	def vAlt2Sea(self,rho,v):
		sea = v*m.sqrt(rho/self.rho_sea)
		return sea

	def vSea2Alt(self,rho,v):
		alt = v*m.sqrt(self.rho_sea/rho)
		return alt



# Old code
# May work, no use in current state
"""
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
"""