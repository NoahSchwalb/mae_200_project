import initial_conditions as initial
from flight import Flight, State
import math as m
import numpy as np

class Aircraft():
    """
	Module to define an aircraft

	Units: English

	Example:
		aircraft = Aircraft()

	"""
    def __init__(self):
        self.state = State()

    def CL(self,rho,v,W_i):
        # Calculate the C_L at any given rho
        #C_L = (2*(v/m.log(initial.W_i/initial.W_f))*m.sqrt(2/rho/initial.S)*(initial.W_i**0.5-initial.W_f**0.5))**2
        C_L = 2*W_i/(rho*v**2*initial.S)
        return C_L

    def CL_vector(self,rho,v,W_i,length):
        # Calculate the C_L at any given rho
        C_L = np.zeros(length)
        C_L.tolist()
        for i in range(0,length):
            C_L[i] = 2*W_i/(rho*v[i]**2*initial.S)
        return C_L

    def oswaldEfficiency(self,AR):
        # Calculate the oswald efficiency factor for any given aspect ratio
        oswald = 4.61*(1-0.045*(AR**0.68))*(m.cos(m.radians(initial.omega))**0.15)-3.1
        return oswald

    def CDo(self,rho,S,c_t,C_L,C_D_i,W_i,W_f,rnge):
        # Calculate the C_D_o
        C_D_o = 2*m.sqrt(2/(rho*S))/c_t*C_L**0.5/rnge*(W_i**0.5-W_f**0.5)-C_D_i
        return C_D_o

    def CDi(self,C_L,e,AR):
        # Calculate the C_D_i at any given coefficient of lift, oswald efficiency factor, and aspect ratio
        C_D_i = C_L**2/(m.pi*e*AR)
        return C_D_i

    def CDi_vector(self,C_L,e,AR,length):
        # Calculate the C_D_i at any given coefficient of lift, oswald efficiency factor, and aspect ratio
        C_D_i = np.zeros(length)
        C_D_i.tolist()
        for i in range(0,length):
            C_D_i[i] = C_L[i]**2/(m.pi*e*AR)
        return C_D_i

    def CD(self,C_D_i,C_D_o):
        # Calculate the total C_D at any given C_D_i and C_D_o
        C_D = C_D_i+C_D_o
        return C_D

    def CD_vector(self,C_D_i,C_D_o,length):
        # Calculate the total C_D at any given C_D_i and C_D_o
        C_D = np.zeros(length)
        C_D.tolist()
        for i in range(0,length):
            C_D[i] = C_D_i[i]+C_D_o
        return C_D

    def ct(self,E,C_L,C_D,W_i,W_f):
        c_t = (1/E)*(C_L/C_D)*m.log(W_i/W_f)
        return c_t

    def endurance(self,c_t,C_L,C_D,W_i,W_f):
        E = 1/c_t*C_L/C_D*m.log(W_i/W_f)
        return E

    def endurance_vector(self,c_t,C_L,C_D,W_i,W_f,length):
        E = np.zeros(length)
        E.tolist()
        for i in range(0,length):
            E[i] = 1/c_t*C_L[i]/C_D[i]*m.log(W_i/W_f)
        return E

    def rnge(self,rho,S,c_t,C_L,C_D,W_i,W_f):
        rnge = 2*m.sqrt(2/rho/S)/c_t*m.sqrt(C_L)/C_D*(m.sqrt(W_i)-m.sqrt(W_f))
        return rnge

    def rnge_vector(self,rho,S,c_t,C_L,C_D,W_i,W_f,length):
        rnge = np.zeros(length)
        rnge.tolist()
        for i in range(0,length):
            rnge[i] = 2*m.sqrt(2/rho/S)/c_t*m.sqrt(C_L[i])/C_D[i]*(m.sqrt(W_i)-m.sqrt(W_f))
        return rnge

    #def enduranceSeaLevel(self,E,rho,v):
    #    v_sl = self.state.vAlt2Sea(rho,v)
    #    C_L = self.CL(rho,v)
    #    C_L_sl = self.CL(self.state.rho_sea,v_sl)
    #    c_t = self.ct(rho,v)
    #    c_t_sl = self.ct(self.state.rho_sea,v_sl)
    #    E_sl = E*(C_L/C_L_sl)*(c_t/c_t_sl)
    #    return E_sl

    #def range(self,rho,ct,C_L,C_D,W_i,W_f):
    #    range = 1
    #    return range
