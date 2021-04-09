'''
	Loads atoms from the Oven Up to the Optical Lattice, 
	applies the large bias field, and measures the "Vacuum" Rabi Splitting.
'''
from labscript import start, stop, AnalogOut, DigitalOut,add_time_marker
from labscriptlib.ybclock.connection_table import define_connection_table
from labscriptlib.ybclock.subsequences import *


if __name__ == '__main__':

	define_connection_table()
	exp_cavity = ExperimentalCavity()

	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()

	set_default_values()

	ms = 1e-3
	kHz = 1e3
	t = 0.1*ms

	t += load_from_oven_to_optical_lattice(t)

	#ramp magnetic fields
	add_time_marker(t, "Ramp Bias Fields.")
	ramp_duration = 2*ms
	z_bias_field.ramp(t, duration=ramp_duration, initial=-0.8,final=7.35,samplerate=1*kHz)
	y_bias_field.ramp(t, duration=ramp_duration, initial=0.32,final=-1.86,samplerate=1*kHz)
	x_bias_field.ramp(t, duration=ramp_duration, initial=5.29,final=-0.02,samplerate=1*kHz)

	t += 200*ms

	t += exp_cavity.scan(t, label='atoms_in_cavity')

	set_default_values(t)
	# Stop the experiment shot with stop()
	stop(t+1)

print("Compiled loading_sequence!")
