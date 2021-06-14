'''
	Loads atoms from the Oven Up to the Optical Lattice, 
	applies the large bias field, and measures the "Vacuum" Rabi Splitting.
'''
from math import pi

from labscript import start, stop, AnalogOut, DigitalOut,add_time_marker
from labscriptlib.ybclock.connection_table import define_connection_table
from labscriptlib.ybclock.subsequences import *
from labscriptlib.ybclock.classes import define_classes

def wait(duration):
	return duration

if __name__ == '__main__':

	ms = 1e-3
	kHz = 1e3

	define_connection_table()
	define_classes()
	HP8648Cfor759.constant(bridging_frequency_759)

	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()

	set_default_values()

	t = 10.1*ms


	#load atoms
	t += load_from_oven_to_optical_lattice(t,add_marker = False)

	#ramp magnetic fields (for setting atoms on resonance with cavity)
	add_time_marker(t, "Ramp Bias Fields.")
	ramp_duration = 2*ms
	z_bias_field.ramp(t, duration=ramp_duration, initial=-0.795,final=spin_b_field_z,samplerate=10*kHz)
	y_bias_field.ramp(t, duration=ramp_duration, initial=0.28,final=-1.86,samplerate=10*kHz)
	x_bias_field.ramp(t, duration=ramp_duration, initial=5.105,final=-0.02,samplerate=10*kHz)
	t += ramp_duration
	
	#ramp down mot
	t+= mot_coil_current.ramp(t,
		duration=20*ms,
		initial=9.1,
		final=9.1*(8/8.5),
		samplerate= 10*kHz
	)

	t+= mot_coil_current.ramp(t,
		duration=40*ms,
		initial=9.1*(8/8.5),
		final=9.1*(8/8.5)*0.8,
		samplerate=10*kHz
		)

	t+= mot_coil_current.ramp(t,
		duration=50*ms,
		initial=9.1*(8/8.5)*0.8,
		final=9.1*(8/8.5)*0.8/4,
		samplerate=10*kHz
	)

	t+= mot_coil_current.ramp(t,
		duration=35*ms,
		initial=9.1*(8/8.5)*0.8/4,
		final=0,
		samplerate=10*kHz
	)


	#wait
	t += 200*ms + 140*ms

	#read atom number.
	t += exp_cavity.scan(t, label='atoms_in_cavity')

	t+=5*ms
	#pump atoms
	pump_duration = 20*ms
	green.pump.intensity.constant(t, value=spin_polarization_power)
	exp_cavity.count_photons(t=t,duration=pump_duration,label='pump_photons')
	t+= pump_duration
	green.pump.turnoff(t,warmup_value=0)

	RF.atom_unitary.prepare_atom_unitary(t)

	t+= 20*ms

	#read atom number.
	t += exp_cavity.scan(t, label='atoms_in_cavity')
	

	#perform rabi pulse then cavity scan
	t += RF.resonant_rabi_pulse(
		t        	= t,
		rabi_area	= pi,
		phase    	= 0,
		duration 	= 2.29*ms,
		samplerate  = 100*kHz
		)

	t+= 20*ms

	t += exp_cavity.scan(t, label='atoms_in_cavity')

	#perform an empty cavity scan
	blue.mot.intensity.constant(t, value=0.28)
	t += 20*ms
	blue.mot.intensity.turnoff(t,warmup_value=0.28)
	t += exp_cavity.scan(t, label='empty_cavity')

	t += mot_coil_current.ramp(t,
		duration=10*ms,
		initial=0,
		final=9.1,
		samplerate=10*kHz
		)
	set_default_values(t)
	# Stop the experiment shot with stop()
	stop(t+0.1)

print("Compiled loading_sequence!")
