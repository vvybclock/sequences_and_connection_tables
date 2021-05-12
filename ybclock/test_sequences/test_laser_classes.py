'''
	Example usage for classes. This is also a development tool for myself.
'''

from labscript import start, stop,add_time_marker
from labscriptlib.ybclock.connection_table import define_connection_table
from labscriptlib.ybclock.classes import *




if __name__ == '__main__':
	define_connection_table()
	define_classes()


	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start(); t = 0;

	t += 1
	add_time_marker(t, label='Turn On')
	blue.mot.intensity.turnon(t, value=3)

	t += 1

	add_time_marker(t, label='Turn Off')
	blue.mot.intensity.turnoff(t, warmup_value=1)

	t += 1 

	add_time_marker(t, label='Ramp')	
	blue.mot.intensity.ramp(t=t, duration=0.5, initial=1,final=2,samplerate=1e3)

	stop(t+1)
