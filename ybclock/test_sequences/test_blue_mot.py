from labscript import start, stop, AnalogOut, DigitalOut
from labscriptlib.ybclock.connection_table import define_connection_table
from labscriptlib.ybclock.subsequences import *


if __name__ == '__main__':

	define_connection_table()
	
	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()
	# set_default_values(t=1e-6)

	ms = 1e-3
	kHz = 1e3
	t = 0.0001


	#load the atoms
	t += blue_mot(t,	duration= 100*ms)	
	
	#take a picture of the atoms but first...
	#turn off the green light
	green_mot_shutter.disable(t)
	add_time_marker(t+20*ms, "Take Pictures", verbose=True)
	wide_angle_cam.expose(t + 20*ms,	name='pic', trigger_duration=20*ms)
	isometric_cam.expose(t + 20*ms, 	name='pic', trigger_duration=20*ms)


	# Stop the experiment shot with stop()
	stop(t+1)

print("Compiled test_blue_mot!")
