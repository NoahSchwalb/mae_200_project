import initial_conditions

## Max velocity flight
class v_max_flight():
	def __init__(self):
		fuel = 0.5*V_fuel_max # []
		W_add = 0
		alt = 28000 # [ft]
		v_max = 0.801*mach
		range = 175.8 # [miles]

## Max endurance flight
class E_max_flight():
	def __init__(self):
		fuel = V_fuel_max
		W_add = 30000 # [lb]
		alt = 15000 # [ft]
		t_alt = 465.23 #[R] # table
		rho_alt = 0.0014962 #[slugs/ft^3] # table
		mu = 2.27*10**-8*((t_alt**1.5)/(t_alt+198.6)) # [lb*s/ft^2] # sutherland's law
		gamma = 1.6
		R = 1716 #[forget unit]
		mach = (gamma*R*t_alt)**0.5
		E_max = 0.9283 # [hr]
		v_inf = 0.4127*mach