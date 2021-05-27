'''
	Holds sequences regarding loading atoms into our traps.

	All functions return their duration.

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

def blue_mot(t,duration,add_marker=True,take_picture=False):
	'''
	# Blue MOT Loading Sequence

	It's very simple simple turn on all the lights and magnetic fields, and let 
	the atoms trap.

	The Blue MOT is assisted by Green Molasses (Doppler Cooling).
	'''

	#turn on the blue mot
	if add_marker: add_time_marker(t, "Turn On Blue MOT", verbose=True)
	#turn off extra light sources that can interrupt loading
	cooling_pi_power_switch.disable(t)
	cooling_pi_shutter.disable(t)

	#set voltage limit on mot
	mot_coil_voltage.constant(t,value=8.5)

	#set magnetic fields
	mot_coil_current.constant(t, value=9.1)
	x_bias_field.constant(t, value=-0.608)
	y_bias_field.constant(t, value=1.374)
	z_bias_field.constant(t, value=2.2)

	#set light power
	blue.mot.intensity.constant(t, value=0.3)
	green.mot.intensity.constant(t, value=0.28) #why?
	#the green light serves as extra doppler cooling.


	if take_picture:
		ms = 1e-3
		trigger_duration = 20*ms
		
		#take background picture
		wide_angle_cam.expose(t,
			name            	='blue_mot', 
			frametype       	='bg',
			trigger_duration	=trigger_duration
		)

		# take picture with atoms
		wide_angle_cam.expose(t+duration-trigger_duration,
			name            	='blue_mot',
			frametype       	='atoms',
			trigger_duration	=trigger_duration
		)

	return duration

def transfer_blue_mot_to_green_mot(t,duration, samplerate,add_marker=True):

	'''Ramp down blue light while moving atoms to green MOT position.'''
	if add_marker: add_time_marker(t, "Transfer Blue MOT", verbose=True)
	#ramp down blue
	blue.mot.intensity.ramp(t, duration, initial=0.28, final=0.05, samplerate=samplerate)
	#turn off the blue light at end of ramp
	blue.mot.intensity.turnoff(t+duration, warmup_value=0.28)
	
	#move magnetic field zero
	x_bias_field.ramp(t, duration, initial=-0.608,	final=1.3,  	samplerate=samplerate)
	y_bias_field.ramp(t, duration, initial=1.374, 	final=-0.15,	samplerate=samplerate)
	z_bias_field.ramp(t, duration, initial=2.2,   	final=0,    	samplerate=samplerate)

	return duration

def cool_atoms_in_green_mot(t,duration,samplerate, add_marker=True):
	ms=1e-3
	if add_marker: add_time_marker(t, "Hold Green MOT", verbose=True)
	#start ramping up green frequency to set up green mot.
	green_frequency_fpga_trigger.enable(t)

	#ramp down green power so we don't blind the camera.
	green.mot.intensity.ramp(t+duration-60*ms, duration=60*ms, initial=0.3, final=0.135, samplerate=samplerate)

	return duration

def position_atoms_to_optical_lattice(t, duration,samplerate, add_marker=True):
	#move the MOT center again
	if add_marker: add_time_marker(t, "Move to Opt. Latt.", verbose=True)
	x_bias_field.ramp(t, duration, initial=1.3,  	final=5.29,  	samplerate=samplerate)
	y_bias_field.ramp(t, duration, initial=-0.15,	final=0.32,  	samplerate=samplerate)
	z_bias_field.ramp(t, duration, initial=0,    	final=-0.795,	samplerate=samplerate)

	return duration

def optimize_position_atoms_to_optical_lattice(t, duration,samplerate, add_marker=True):
	pass

def hold_atoms(t, duration,add_marker=True):
	if add_marker: add_time_marker(t, "Hold Green MOT", verbose=True)
	return duration

def load_from_oven_to_optical_lattice(t, add_marker=True, take_picture=True):
	'''  This is meta-subsequence. It holds all the calls for loading from the
	oven up until loading into the optical lattice.'''
	ms = 1e-3
	kHz = 1e3

	t0 = t
	#load the atoms
	t += blue_mot(t,                      	duration= blue_mot_duration,	take_picture=take_picture, add_marker=add_marker)
	t += transfer_blue_mot_to_green_mot(t,	duration= 40*ms,            	samplerate=1*kHz, add_marker=add_marker)
	t += cool_atoms_in_green_mot(t,       	duration= 180*ms,           	samplerate=1*kHz, add_marker=add_marker)

	#record timestamps for when we shift frequencies of the green using the PTS
	tPTS = t; #577ms in Excel Sequences
	add_time_marker(tPTS, "PTS: Trigger 1st")
	tPTS += 100*ms; 
	add_time_marker(tPTS, "PTS: 1st to 2nd")
	tPTS += 180*ms;
	add_time_marker(tPTS, "PTS: 2nd to 3rd")
	tPTS += 40*ms;
	add_time_marker(tPTS, "PTS: 3rd to 4th")

	t += position_atoms_to_optical_lattice(t,	duration= 40*ms,	samplerate=1*kHz, add_marker=add_marker)

	#take a picture of the atoms
	add_time_marker(t+20*ms, "Take Picture of Green MOT", verbose=True)
	if take_picture:
		isometric_cam.expose(t + 20*ms,	name='green_mot', frametype='almost_loaded', trigger_duration=20*ms)

	t += hold_atoms(t,	duration= 40*ms)

	return t-t0

print("Imported 'loading_subsequences'")