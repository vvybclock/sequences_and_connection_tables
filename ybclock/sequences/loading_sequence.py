'''
	Loads atoms from the Oven Up to the Optical Lattice, 
	applies the large bias field, and measures the "Vacuum" Rabi Splitting.
'''
from labscript import start, stop, AnalogOut, DigitalOut,add_time_marker
from labscriptlib.ybclock.connection_table import define_connection_table
from labscriptlib.ybclock.subsequences import *
from labscriptlib.ybclock.classes import define_classes

if __name__ == '__main__':

	ms = 1e-3
	kHz = 1e3

	define_connection_table()
	define_classes()
	exp_cavity = ExperimentalCavity()
	HP8648Cfor759.constant(bridging_frequency_759)

	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()

	set_default_values()

	t = 10.1*ms


	#load atoms
	t += load_from_oven_to_optical_lattice(t)

	#ramp magnetic fields (for setting atoms on resonance with cavity)
	add_time_marker(t, "Ramp Bias Fields.")
	ramp_duration = 2*ms
	z_bias_field.ramp(t, duration=ramp_duration, initial=-0.795,final=7.35,samplerate=1*kHz)
	y_bias_field.ramp(t, duration=ramp_duration, initial=0.28,final=-1.86,samplerate=1*kHz)
	x_bias_field.ramp(t, duration=ramp_duration, initial=5.105,final=-0.02,samplerate=1*kHz)

	#wait
	t += 200*ms

	#read atom number.
	t += exp_cavity.scan(t, label='atoms_in_cavity')
	

	#perform an empty cavity scan
	blue.mot.intensity.constant(t, value=0.28)
	t += 20*ms
	t += exp_cavity.scan(t, label='empty_cavity')

	set_default_values(t)
	# Stop the experiment shot with stop()
	stop(t+1)

print("Compiled loading_sequence!")
