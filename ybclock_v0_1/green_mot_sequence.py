from labscript import start, stop, add_time_marker, AnalogOut, DigitalOut
from labscriptlib.ybclock_v0_1.connection_table import define_connection_table

def green_mot(time=t0):
	pass

if __name__ == '__main__':

	define_connection_table()
	
	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()

	t = 0

	mot_duration = green_mot_sequence(t)

	t += mot_duration

	# Stop the experiment shot with stop()
	stop(t)
