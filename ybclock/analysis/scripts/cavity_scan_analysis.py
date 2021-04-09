####################################################
####################################################
#
#
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
import pickle

run = Run(path)



try:
	#extract cavity_scan_parameters metadata
	exp_cavity = ExperimentalCavity()
	cavity_scan_parameters = exp_cavity.get_parameters(path)
except:
	print("Error: Could not extract cavity_scan_parameters.")

try:
	#extract data
	photon_arrival_times = run.get_result_array(group='extract_photon_arrival_times',name='processed_arrivals_ch_1')
except:
	print("Error: Could not extract photon_arrival_times.")

	#check to see if we need to run empty cavity analysis
for each_key in cavity_scan_parameters.keys():
	try:
		if each_key == 'empty_cavity':
			empty_cavity_analysis(
				data=photon_arrival_times,
				scan_parameters=cavity_scan_parameters[each_key],
				path=path
			)
		if each_key == 'atom_cavity':
			atom_cavity_analysis(
				data=photon_arrival_times,
				scan_parameters=cavity_scan_parameters[each_key],
				path=path
			)
	except:
		print(f"Error: Could not analyse '{each_key}' scans.")