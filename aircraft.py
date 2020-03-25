import initial_conditions as initial
import flight_data as data
import math as m

class Aircraft():
    def __init__(self):
        self.v_max = data.v_max_flight()
        self.E_max = data.E_max_flight()
    
    def C_L(self,rho):
        C_L = (2*(self.v_max.v_max/m.log(initial.W_i/initial.W_f))*m.sqrt(2/rho/initial.S)*(initial.W_i**0.5-initial.W_f**0.5))**2
        return C_L
