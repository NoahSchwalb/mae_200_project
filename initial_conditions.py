## Initial conditions
#
#
# aircraft constants
W_eng 		= 	7000 	# [lb]
b_front     = 	169.8 	# [ft]
S_front 	= 	3800 	# [ft^2]
omega 		= 	35 		# [degrees]
W_f_old 	= 	282500 	# [lbf]
W_max_old 	= 	585000 	# [lbf]
sigma_fuel 	=  	6.84 	# [lb/gal]
V_fuel_max 	= 	35546	# [gal]
b_back		= 	65 		# [ft]
sigma_wing 	= 	12 		# [lb/ft^2]
n_new_eng 	=   2       # [-]
W_avi 		= 	0		# [lbf]
W_cell 		= 	6000 	# [lbf]
W_lab  		= 	3000 	# [lbf]

# aircraft variables
AR_front = b_front**2/S_front
AR_back = AR_front
S_back = b_back**2/AR_back
S = S_back + S_front

# aircraft weight after modifcations
W_f = W_f_old + S_back*sigma_wing + 2*W_eng + W_avi + W_cell + W_lab
W_max = W_max_old + n_new_eng*100000
