from labscript import start, stop, AnalogOut, DigitalOut
from labscriptlib.ybclock.connection_table import define_connection_table
from labscriptlib.ybclock.subsequences import *


if __name__ == '__main__':

	define_connection_table()
	
	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()
	# set_default_values(t=1e-6)

	ms = 1e-3
	kHz = 1e3
	t = 0.1*ms


	#load the atoms
	t += blue_mot(t,                           	duration= 3000*ms, take_picture=True)
	t += transfer_blue_mot_to_green_mot(t,     	duration= 40*ms, 	samplerate=1*kHz)
	t += cool_atoms_in_green_mot(t,            	duration= 180*ms,	samplerate=1*kHz)
	# t += position_atoms_to_optical_lattice(t,	duration= 40*ms, 	samplerate=1*kHz)

	#take a picture of the atoms
	add_time_marker(t+20*ms, "Take Pictures", verbose=True)
	wide_angle_cam.expose(t + 20*ms,	name='green_mot', frametype='signal', trigger_duration=20*ms)
	isometric_cam.expose(t + 20*ms, 	name='green_mot', frametype='signal', trigger_duration=20*ms)

	t += hold_atoms(t,	duration= 40*ms)

	# Stop the experiment shot with stop()
	stop(t+1)

print("Compiled loading_sequence!")
