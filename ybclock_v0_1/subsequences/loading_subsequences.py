from labscript import add_time_marker

def blue_mot(t0):
	t = t0

	#turn on the blue mot
	add_time_marker(t, "Turn On Blue MOT", verbose=True)


	#set voltage limit on mot
	mot_voltage_setting_do_not_use.constant(t,value=8.5)

	#set magnetic fields
	mot_coil_current.constant(t, value=9.1)
	x_bias_field.constant(t, value=-0.608)
	y_bias_field.constant(t, value=1.374)
	z_bias_field.constant(t, value=2.2)
	

	#set light power
	blue_mot_aom_and_shutter.enable(t)
	green_mot_aom.enable(t)
	green_mot_shutter.enable(t)
	blue_power.constant(t, value=0.24)
	green_power.constant(t, value=0.3) #why?

	#do something else???
	return blue_mot_duration


print("Imported 'loading_subsequences'...")