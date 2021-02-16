from labscript import start, stop, AnalogOut, DigitalOut
from labscriptlib.ybclock.connection_table import define_connection_table
from labscriptlib.ybclock.subsequences import *


if __name__ == '__main__':

	define_connection_table()
	
	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()

	set_default_values()

	ms = 1e-3
	kHz = 1e3
	t = 0.1*ms

	t += load_from_oven_to_optical_lattice(t)

	# Stop the experiment shot with stop()

	set_default_values(t)
	stop(t+1)

print("Compiled loading_sequence!")
