import initial_conditions as initial

## Max velocity flight
class v_max_flight():
	def __init__(self):
		fuel 	= 	0.5*initial.V_fuel_max 					 # [lbf] 			# [SOW]
		W_add 	= 	0 										 # [lbf] 			# [SOW]
		alt 	= 	28000 									 # [ft] 			# [SOW]
		t_alt 	= 	418.97 									 # [R] 				# [Table]
		rho_alt = 	0.00095801 								 # [slugs/ft^3] 	# [Table]
		mu 		= 	2.27*10**-8*((t_alt**1.5)/(t_alt+198.6)) # [lb-s/ft^2] 		# [FS]
		gamma 	= 	1.6 									 # [] 				# []
		R		= 	1716 									 # [ft-lbf/slug-R]  # [FS]
		mach 	= 	(gamma*R*t_alt)**0.5 					 # [ft/s] 			# [FS]
		v_max 	= 	0.801*mach  							 # [ft/s] 			# [SOW]
		range 	= 	175.8 									 # [mi] 			# [SOW]

## Max endurance flight
class E_max_flight():
	def __init__(self):
		fuel 	= 	initial.V_fuel_max 						 # [lbf] 			# [SOW]
		W_add 	= 	30000 									 # [lb] 			# [SOW]
		alt 	= 	15000 									 # [ft] 			# [SOW]
		t_alt 	= 	465.23 									 # [R] 				# [Table]
		rho_alt = 	0.0014962 								 # [slugs/ft^3] 	# [Table]
		mu 		= 	2.27*10**-8*((t_alt**1.5)/(t_alt+198.6)) # [lb-s/ft^2] 		# [FS]
		gamma 	= 	1.6 									 # [] 				# []
		R 		= 	1716 									 # [ft-lbf/slug-R] 	# [FS]
		mach	= 	(gamma*R*t_alt)**0.5 					 # [] 				# [FS]
		E_max	= 	0.9283 									 # [hr] 			# [SOW]
		v_inf 	= 	0.4127*mach 							 # [] 				# [SOW]