from labscript import start, stop, AnalogOut, DigitalOut
from labscriptlib.ybclock.connection_table import define_connection_table
from labscriptlib.ybclock.subsequences import *


if __name__ == '__main__':

	define_connection_table()
	
	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()
	set_default_values(t=1e-6)

	ms = 1e-3
	t = 0.1


	#load the atoms
	t += blue_mot(t,                         	duration= 100*ms)
	t += transfer_blue_mot_to_green_mot(t,   	duration= 40*ms,	samplerate=)
	t += position_atoms_to_optical_lattice(t,	duration= ,     	samplerate=)

	t += load_green_mot(t, ramp_time = 40e-3)	
	green_mot_duration = 0
	t += green_mot_duration


	#take pictures while we load the MOTs.
	frame_period_s = 148*1e-3
	t0 = 0.1
	tloop = t0
	i =0
	while tloop < t0 + blue_mot_duration + green_mot_duration:
		i+=1
		wide_angle_cam.expose(t=tloop,	name='wide_angle_frame',	frametype=f'{i}',	trigger_duration=frame_period_s/2)
		isometric_cam.expose(t=tloop, 	name='isometric_frame', 	frametype=f'{i}',	trigger_duration=frame_period_s/2)
		tloop += frame_period_s


	# Stop the experiment shot with stop()
	stop(t+1)

print("Compiled loading_sequence!")
