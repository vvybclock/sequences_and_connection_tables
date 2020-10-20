from labscript import start, stop, AnalogOut, DigitalOut
from labscriptlib.ybclock_v0_1.connection_table import define_connection_table
from labscriptlib.ybclock_v0_1.subsequences import *

blue_mot_duration 






if __name__ == '__main__':

	define_connection_table()
	
	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()

	t = 0.1

	blue_mot_duration = blue_mot(t)

	trigger_the_cameras(t, duration=blue_mot_duration,frame_period_ms=148)

	t += blue_mot_duration

	t += load_green_mot(t, ramp_time = 40e-3)
	
	green_mot_duration = 5
	trigger_the_cameras(t, duration=green_mot_duration,frame_period_ms=148)

	t += green_mot_duration
	# Stop the experiment shot with stop()
	stop(t)

print("Compiled loading_sequence!")