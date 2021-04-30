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
from labscriptlib.ybclock.analysis.functions.atom_cavity_helper import atom_cavity_analysis
from labscriptlib.ybclock.analysis.functions.empty_cavity_helper import empty_cavity_analysis

'''
## Minimally complete analysis code

In this analysis code we have all the ingredients to extract the needed information from the detected photons.

The code will first search for empty cavity scans and eventually analyse them. After that it will search for and analyse the atom cavity scans.
We first analyse the empty cavity scan because in some cases we may want to use some empty_cavity fit parameters as fixed parameters in the atom_cavity fit. For example, in a sequence where we know a priori that there are no atoms in the m=-1/2 sub-state of the Yb171 GS, we can fix the empty_cavity frequency parameter in the fit.

'''


run = Run(path)

#extract cavity_scan_parameters metadata
exp_cavity = ExperimentalCavity()
cavity_scan_parameters = exp_cavity.get_parameters(path)

# print(f"Cavity Scan Parameters:\n\n\n{cavity_scan_parameters}\n\n\n\n")

#extract globals
# data_globals = run.get_globals()

#extract data
photon_arrival_times = run.get_result_array(group='extract_photon_arrival_times',name='processed_arrivals_ch_1')

#check to see if we need to run empty cavity analysis
for each_key in cavity_scan_parameters.keys():
	if each_key == 'empty_cavity':
		atom_cavity_analysis(
			data=photon_arrival_times,
			scan_parameters=cavity_scan_parameters[each_key],
			path=path
		)