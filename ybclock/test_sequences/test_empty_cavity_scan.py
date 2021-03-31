from labscript import start, stop, AnalogOut, DigitalOut
from labscriptlib.ybclock.connection_table import define_connection_table
from labscriptlib.ybclock.subsequences import *
from labscript_utils.unitconversions import *


if __name__ == '__main__':
	define_connection_table()

	exp_cavity = ExperimentalCavity()
	
	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()

	set_default_values()

	ms = 1e-3
	us = 1e-6
	kHz = 1e3
	t = 1*ms


	#calibration
	for i in range(5):
		t += exp_cavity.scan(t,label=f'empty_cavity')
	
	t += 1

	for i in range(5):
		t += exp_cavity.scan(t,label=f'empty_cavity')
	


	set_default_values(t+1*ms)
	stop(t+10*ms)

print("Compiled test_empty_cavity_scan!")