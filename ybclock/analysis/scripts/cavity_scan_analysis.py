'''

	Loops through the parameters saved by ExperimentalCavity() class and
	performs analysis by passing the 3 parameters needed to an analysis function.

'''
from lyse import *
from pylab import *

#Add in libraries for working with HDF files
import labscript_utils.h5_lock
import h5py

#Add class
from labscriptlib.ybclock.subsequences import ExperimentalCavity

#analysis libs
import numpy as np
import matplotlib.pyplot as plt
import labscriptlib.ybclock.analysis.functions.fit_functions as fit_functions
from labscriptlib.ybclock.analysis.functions.empty_cavity_helper import empty_cavity_analysis
from labscriptlib.ybclock.analysis.functions.atoms_in_cavity_helper import atom_cavity_analysis
import pickle


if __name__ == '__main__':
	#get data
	run = Run(path)


	#extract cavity_scan_parameters metadata
	try:
		exp_cavity = ExperimentalCavity()
		cavity_scan_parameters = exp_cavity.get_parameters(path)
		print(f'Discovered {len(cavity_scan_parameters)} types of scans: {cavity_scan_parameters.keys()}')
	except:
		print("Error: Could not extract cavity_scan_parameters.")


	#extract photon data
	try:
		photon_arrival_times = run.get_result_array(group='extract_photon_arrival_times',name='processed_arrivals_ch_1')
	except:
		print("Error: Could not extract photon_arrival_times.")


	#check to see if we need to run any sort of cavity analysis
	for each_key in cavity_scan_parameters.keys():
		if each_key == 'empty_cavity':
		#we prioritize empty cavity scans
			empty_cavity_analysis(
				data=photon_arrival_times,
				scan_parameters=cavity_scan_parameters[each_key],
				path=path
			)

	for each_key in cavity_scan_parameters.keys():
		#we analyse all other cavity scan not empty
		if each_key == 'atoms_in_cavity':
			atom_cavity_analysis(
				data=photon_arrival_times,
				scan_parameters=cavity_scan_parameters[each_key],
				path=path
			)