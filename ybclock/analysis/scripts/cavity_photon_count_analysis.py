'''
	Analyses the photons received through the cavity for other reasons beyond cavity scans.
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
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def integrate_pump_photons(data, scan_parameters, path):

	run = Run(path)
	iteration = 0
	for photon_count_read in scan_parameters:
		start_time	= photon_count_read['t']
		end_time  	= start_time + photon_count_read['duration']
		photons_in_scan_time = data[(data > start_time) & (data < end_time)]

		print(start_time)
		print(photons_in_scan_time)
		run.save_result(
			name 	= f'pump_photons_{iteration}',
			value	= sum(photons_in_scan_time > 0),
		)
		print(f'Pump Photons : Iter {iteration} : {sum(photons_in_scan_time > 0)}')
		iteration += 1



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
	try:
		for each_key in cavity_scan_parameters.keys():
			if each_key == 'pump_photons':
			#we prioritize empty cavity scans
				try:
					integrate_pump_photons(
						data=photon_arrival_times,
						scan_parameters=cavity_scan_parameters[each_key],
						path=path
					)
				except Exception as e:
					print(f"Cavity Scan Type {each_key} Error: {e}")
	except Exception as e:
		print(f"Error: {e}")
