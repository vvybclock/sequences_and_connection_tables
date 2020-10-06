from labscript import start, stop, add_time_marker, AnalogOut, DigitalOut
from labscriptlib.ybclock_v0_1.connection_table import define_connection_table

blue_mot_duration = 30	

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


def trigger_the_cameras(t0, duration, frame_period_ms):

	trigger_voltage = 8;

	t = t0

	while t < t0 + duration:
		wide_range_camera_trigger.constant(t, value=trigger_voltage)
		one_to_one_camera_trigger.constant(t, value=trigger_voltage)
		t += 0.001*frame_period_ms/2
		wide_range_camera_trigger.constant(t, value=0)
		one_to_one_camera_trigger.constant(t, value=0)
		t += 0.001*frame_period_ms/2
		

	return duration


if __name__ == '__main__':

	define_connection_table()
	
	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()

	t = 0.1

	blue_mot_duration = blue_mot(t)

	trigger_the_cameras(t, duration=blue_mot_duration,frame_period_ms=148)

	t += blue_mot_duration

	# Stop the experiment shot with stop()
	stop(t)