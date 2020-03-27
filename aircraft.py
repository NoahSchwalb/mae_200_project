import initial_conditions as initial
import flight_data as data
import math as m

class Aircraft():
    def __init__(self):
        # Module to create an aircraft
        # v_max: creates object of v_max_flight with conditions from the max velocity flight
        # E_max: creates object of E_max_flight with conditions from the max endurance flight
        self.v_max = data.v_max_flight()
        self.E_max = data.E_max_flight()
    
    def C_L(self,rho):
        # Calculate the C_L at any given rho
        C_L = (2*(self.v_max.v_max/m.log(initial.W_i/initial.W_f))*m.sqrt(2/rho/initial.S)*(initial.W_i**0.5-initial.W_f**0.5))**2
        return C_L

    def oswaldEfficiency(self,AR):
        # Calculate the oswald efficiency factor for any given aspect ratio
        oswald = 4.61*(1-0.045*AR**0.68)*(m.cos(initial.omega)**0.15)-3.1
        return oswald

    def C_D_i(self,C_L,e,AR):
        # Calculate the C_D at any given coefficient of lift, oswald efficiency factor, and aspect ratio
        C_D_i = C_L**2/(m.pi*e*AR)
        return C_D_i