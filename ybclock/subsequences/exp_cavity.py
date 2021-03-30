'''
	Holds functions for performing cavity scans and saving data.
'''
from labscript import compiler, add_time_marker
import labscript_utils.h5_lock
import h5py
import pickle
import numpy as np

class ExperimentalCavity:
	'''
	Records parameters and saves them once the program quits.
	'''
	scan_parameters = {}

	def __init__(self):
		''' Try to create the metadata group if it doesn't exist. 
		Clear the scan_parameters dict, as it seems to stay full after each shot compilation.'''

		self.scan_parameters = {}
		with h5py.File(compiler.hdf5_filename, 'a') as hdf5_file:
			hdf5_file.require_group('metadata')
			hdf5_file.require_group('/metadata/exp_cavity')

	def save_parameters(self):
		''' Pickle Parameters then Save to HDF'''
		with h5py.File(compiler.hdf5_filename, 'a') as hdf5_file:
			pickled_dict = pickle.dumps(self.scan_parameters)
			grp = hdf5_file['/metadata/exp_cavity']
			grp.attrs["scan_parameters"] = np.void(pickled_dict)


	def get_parameters(self):
		''' Load from HDF file then Unpickle '''
		with h5py.File(compiler.hdf5_filename, 'a') as hdf5_file:
			grp = hdf5_file['/metadata/exp_cavity']
			void_pickled_dict = grp.attrs["scan_parameters"]
			pickled_dict = void_pickled_dict.tobytes()
			self.scan_parameters = pickle.loads(pickled_dict)

	def scan(self,t, label, verbose=False):
		'''

		t    	- scan light across the cavity at time t.
		label	- name of the cavity scan you are performing.
		verbose - adds time markers and the beginning of  each scan.

		The label will be used for analysis and grouping parameters together. The
		label should be identical if you are using it for the same purpose. This
		makes it easier for the analysis code to partition the shots.

		'''
		ms = 1e-3
		us = 1e-6
		t0 = t

		#make room in the dictionary if this label is used for the first time.
		self.scan_parameters.setdefault(label, [])

		#calculate the parameters from globals
		duration  	= empty_cavity_sweep_duration*ms
		initial_f 	= empty_cavity_frequency_sweep_initial
		final_f   	= empty_cavity_frequency_sweep_initial+empty_cavity_frequency_sweep_range
		samplerate	= empty_cavity_samples/(empty_cavity_sweep_duration*ms)

		#record the parameters in a dictionary inside a list that holds dictionarys.
		self.scan_parameters[label].append({
			"t"         	: t,
			"duration"  	: duration,
			"initial_f" 	: initial_f,
			"final_f"   	: final_f,
			"samplerate"	: samplerate
		})

		#initial laser light management
		if verbose: add_time_marker(t,f"Cavity Scan Prep: {label}")
		#set sideband frequency before turning on power
		probe_sideband_frequency.constant(t, value=initial_f, units='MHz')
		#turn on light power
		probe_sideband_power_switch.enable(t)
		probe_sideband_power.constant(t, value=empty_cavity_scan_power)

		probe_power_switch.disable(t)
		photon_counter_shutter.enable(t)	#open photon counter shutter
		probe_shutter.enable(t); t += 5*ms
		probe_power_switch.enable(t)

		tloop = t
		#tell labscript to perform the scan with the given parameters.
		t += probe_sideband_frequency.ramp(
			t, 
			duration=duration,
			initial=initial_f,
			final=final_f,
			samplerate=samplerate, units="MHz"
		)

		#run the photon counter
		while tloop < t:
			p7888_start_trigger.enable(tloop)
			p7888_start_trigger.disable(tloop + 500*us)
			tloop += 1*ms

		#turn off lights
		probe_sideband_power_switch.disable(t)
		probe_sideband_power.constant(t, value=0)

		probe_power_switch.disable(t)
		photon_counter_shutter.disable(t)	#open photon counter shutter
		probe_shutter.disable(t); t += 5*ms
		probe_power_switch.enable(t)

		self.save_parameters()

		return t-t0