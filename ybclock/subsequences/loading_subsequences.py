'''
	Holds sequences regarding loading atoms into our traps.

	#An Outline of How MOT Trapping Works

	Let's start from what we know a MOT should do. It should cool and it should
	trap. From the fact that it should cool, and we presume it cools via simple
	Doppler cooling, we can surmise that all MOT beams must be red detuned.

	From the fact it should trap, we can surmise that we need to create a
	position dependent force. I leave it as an exercise to the reader, to show
	that a position dependent energy of the excited state can give this position
	dependent force.

	One of the easiest ways we perform this position dependent force is via a
	magnetic field gradient and the magnetic properties of angular momentum
	excited states. The magnetic field gradient pushes the atoms into resonance
	at certain positions causing them to get forced into the center of the trap.

	#A summary of MOT characteristics

	By analysis of the above properties, we can determine, that the trap size is
	a function of magnetic field gradient and detuning, and the cooling is a
	function of the detuning.

	We can also surmise that the MOT trapping position depends on the
	`bias_field`. 

'''

from labscript import add_time_marker

def blue_mot(t,duration):
	'''
	# Blue MOT Loading Sequence

	It's very simple simple turn on all the lights and magnetic fields, and let 
	the atoms trap.

	The Blue MOT is assisted by Green Molasses (Doppler Cooling).
	'''
	#turn on the blue mot
	add_time_marker(t, "Turn On Blue MOT", verbose=True)

	#set voltage limit on mot
	mot_coil_voltage.constant(t,value=8.5)

	#set magnetic fields
	mot_coil_current.constant(t, value=9.1)
	x_bias_field.constant(t, value=-0.608)
	y_bias_field.constant(t, value=1.374)
	z_bias_field.constant(t, value=2.2)

	#set light power
	blue_mot_aom_and_shutter.enable(t)
	blue_mot_power.constant(t, value=0.28)
	
	green_mot_power_switch.enable(t)
	green_mot_shutter.enable(t)
	green_mot_power.constant(t, value=0.3) #why?
	#the green light serves as extra doppler cooling.

	return duration

def transfer_blue_mot_to_green_mot(t,duration, samplerate):

	'''Ramp down blue light while moving atoms to green MOT position.'''

	#ramp down blue
	blue_mot_power.ramp(t, duration, initial=0.28, final=0.05, samplerate=samplerate)

	#move magnetic field zero
	x_bias_field.ramp(t, duration, initial=-0.608,	final=5.29,  	samplerate=samplerate)
	y_bias_field.ramp(t, duration, initial=1.374, 	final=0.32,  	samplerate=samplerate)
	z_bias_field.ramp(t, duration, initial=2.2,   	final=-0.795,	samplerate=samplerate)

	#start ramping up green frequency to set up green mot.
	green_frequency_fpga_trigger.enable(t)

def cool_atoms_in_green_mot(t,duration):

	#turn off the blue light.
	blue_mot_aom_and_shutter.disable(t)
	
	pass

def position_atoms_to_optical_lattice(t, duration):

	pass

def load_green_mot(t,ramp_time):
	'''
	# Blue MOT to Green MOT Transfer Sequence

	Currently not working.
	'''

	blue_mot_power.ramp(t, 
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

print("Imported 'loading_subsequences'")