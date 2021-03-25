'''
	Holds functions for performing cavity scans and saving data.
'''
import labscript_utils.h5_lock
import h5py


class ExperimentalCavity:
	'''
	Records parameters and saves them once the program quits.
	'''
	cavity_scan_parameters = {}
	met

	def __init__(self):
		''' Try to create the metadata group. '''
		with h5py.File(compiler.hdf5_filename, 'a') as hdf5_file:
			hdf5_file.require_group('metadata')

	def __del__(self):
		with h5py.File(compiler.hdf5_filename, 'a') as hdf5_file:

			pass

	def scan(t, label):
		'''

		t    	- scan light across the cavity at time t.
		label	- name of the cavity scan you are performing.

		The label will be used for analysis and grouping parameters together. The
		label should be identical if you are using it for the same purpose.

		'''
		#make room in the dictionary if this label is used for the first time.
		cavity_scan_parameters.setdefault(label, [])

		#calculate the parameters from globals
		duration  	= empty_cavity_sweep_duration*ms
		initial_f 	= empty_cavity_frequency_sweep_initial
		final_f   	= empty_cavity_frequency_sweep_initial+empty_cavity_frequency_sweep_range
		samplerate	= empty_cavity_samples/(empty_cavity_sweep_duration*ms)

		#record the parameters in a dictionary inside a list that holds dictionarys.
		cavity_scan_parameters[label].append({
			"t"         	: t,
			"duration"  	: duration,
			"initial_f" 	: initial_f,
			"final_f"   	: final_f,
			"samplerate"	: samplerate
		})

		#tell labscript to perform the scan with the given parameters.


t += probe_sideband_frequency.ramp(
	t, 
	duration=empty_cavity_sweep_duration*ms,
	initial=empty_cavity_frequency_sweep_initial,
	final= empty_cavity_frequency_sweep_initial+empty_cavity_frequency_sweep_range,
	samplerate=empty_cavity_samples/(empty_cavity_sweep_duration*ms), units="MHz"
	)