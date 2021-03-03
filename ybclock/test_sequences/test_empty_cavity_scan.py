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
	us = 1e-6
	kHz = 1e3
	t = 1*ms

	add_time_marker(t,"Cavity Scan Prep")
	#set sideband frequency before turning on power
	probe_sideband_frequency.constant(t, value=5)
	#turn on light power
	probe_sideband_power_switch.enable(t)
	probe_sideband_power.constant(t, value=1.8)

	probe_power_switch.disable(t)
	photon_counter_shutter.enable(t)	#open photon counter shutter
	probe_shutter.enable(t); t += 5*ms
	probe_power_switch.enable(t)

	tloop = t

	
	#sweep probe sideband frequency
	sweep_duration = 30*ms
	frequency_sweep_range = 60e3*kHz
	frequency_resolution = 50*kHz
	samples = frequency_sweep_range/frequency_resolution

	t += probe_sideband_frequency.ramp(
		t, 
		duration=30*ms,
		initial=5,
		final=-2.5,
		samplerate=(samples/sweep_duration)
	)

	while tloop < t:
		p7888_start_trigger.enable(tloop)
		p7888_start_trigger.disable(tloop + 500*us)
		tloop += 1*ms

	#turn off all the light
	#turn on light power
	probe_sideband_power_switch.disable(t)
	probe_sideband_power.constant(t, value=0)

	probe_power_switch.disable(t)
	photon_counter_shutter.disable(t)	#open photon counter shutter
	probe_shutter.disable(t); t += 5*ms
	probe_power_switch.enable(t)

	

	set_default_values(t+1*ms)
	stop(t+2*ms)

print("Compiled loading_sequence!")
