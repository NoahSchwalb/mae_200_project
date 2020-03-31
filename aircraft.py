import initial_conditions as initial
import flight
import math as m
import numpy as np

class Aircraft():
    """
	Module to define an aircraft

	Units: English

	Example:
		aircraft = Aircraft()

	 
	"""
    def C_L(self,rho,velocity):
        # Calculate the C_L at any given rho
        C_L = (2*(velocity/m.log(initial.W_i/initial.W_f))*m.sqrt(2/rho/initial.S)*(initial.W_i**0.5-initial.W_f**0.5))**2
        return C_L

    def oswaldEfficiency(self,AR):
        # Calculate the oswald efficiency factor for any given aspect ratio
        oswald = 4.61*(1-0.045*AR**0.68)*(m.cos(initial.omega)**0.15)-3.1
        return oswald

    def C_D_i(self,C_L,e,AR):
        # Calculate the C_D_i at any given coefficient of lift, oswald efficiency factor, and aspect ratio
        C_D_i = C_L**2/(m.pi*e*AR)
        return C_D_i

    def C_D(self,C_D_i,C_D_o):
        # Calculate the total C_D at any given C_D_i and C_D_o
        C_D = C_D_i+C_D_o
        return C_D

    #def range(self,rho,ct,C_L,C_D,W_i,W_f):
    #    range = 1
    #    return range