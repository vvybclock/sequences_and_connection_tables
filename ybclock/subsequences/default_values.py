
def set_default_values(t):

	#set up mot fields
	mot_coil_voltage.constant(t,value=8.5)
	mot_coil_current.constant(t, value=9.1)

	#set up bias fields
	x_bias_field.constant(t, value=-0.608)
	y_bias_field.constant(t, value=1.374)
	z_bias_field.constant(t, value=2.2)

	#set up red laser
	red_cavity_power.constant(t, 1.375)
	red_cavity_power_switch.enable(t)
	
	#set up blue laser
	blue_mot_shutter.enable(t)
	blue_mot_power.constant(t, value=0.28)

	#set up green laser
	#mot
	green_mot_shutter.enable(t)
	green_mot_power_switch.enable(t)
	green_mot_power.constant(t, value=0.3)

	#frequency
	green_frequency_fpga_trigger.disable(t)

	#cooling
	cooling_pi_power_switch.enable(t)
	cooling_pi_shutter.disable(t)