from labscript import start, stop, add_time_marker, AnalogOut, DigitalOut
from labscriptlib.ybclock_v0_1.connection_table import define_connection_table

def loading_sequence(time=t0):
	t = t0

	#turn on the blue mot
	mot_coil_current.constant(t, value=9.1)
	blue_power.constant(t, value=0.24)
	x_bias_field.constant(t, value=-0.608)
	y_bias_field.constant(t, value=1.374)
	z_bias_field.constant(t, value=2.2)
	green_power.constant(t, value=0.3) #why?
	
	#do something else???

	pass

if __name__ == '__main__':

	define_connection_table()
	
	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()

	t = 0

	mot_duration = loading_sequence(t)

	t += mot_duration

	# Stop the experiment shot with stop()
	stop(t)
s