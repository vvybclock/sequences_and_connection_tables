'''
	Holds sequences regarding loading atoms into our traps.
'''

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

def load_green_mot(t0,ramp_time):

	t = t0

	blue_power.ramp(t, 
		duration  	= ramp_time, 
		initial   	= 0.24, 
		final     	= 50e-3, 
		samplerate	= 1e3
	)

	x_bias_field.ramp(t, 
		duration  	= ramp_time,
		initial   	= -0.608,
		final     	= 1.3,
		samplerate	= 1e3
	)

	z_bias_field.ramp(t, 
		duration  	= ramp_time,
		initial   	= 2.110,
		final     	= 0,
		samplerate	= 1e3
	)


	t += ramp_time

	blue_mot_aom_and_shutter.disable(t + 74e-3)
	green_frequency_fpga_trigger.enable(t)

	return ramp_time

print("Imported 'loading_subsequences'")