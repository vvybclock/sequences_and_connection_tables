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
from labscriptlib.ybclock.analysis.functions.metadata import extract_sequence_repetition_numbers, extract_date,extract_sequence_name
import labscriptlib.ybclock.analysis.functions.fit_functions as fit_functions
from labscriptlib.ybclock.analysis.functions.empty_cavity_helper import empty_cavity_analysis

run = Run(path)

#extract metadata
(sequence_number, repetition_number)	= extract_sequence_repetition_numbers(path)
date                                	= extract_date(path)
sequence_name                       	= extract_sequence_name(path)

#extract cavity_scan_parameters metadata
exp_cavity = ExperimentalCavity()
cavity_scan_parameters = exp_cavity.get_parameters(path)

print(f"Cavity Scan Parameters:\n\n\n{cavity_scan_parameters}\n\n\n\n")

#extract globals
# data_globals = run.get_globals()

#extract data
photon_arrival_times = run.get_result(group='extract_photon_arrival_times',name='processed_arrivals_ch_1')

#check to see if we need to run empty cavity analysis
for each_key in cavity_scan_parameters.keys():
	if each_key == 'empty_cavity':
		empty_cavity_analysis(
			data=photon_arrival_times,
			scan_parameters=cavity_scan_parameters[each_key]
		)































#plot data
plt.hist(
	photon_arrival_times,
	bins=np.arange(0,30e-3, 200e-6),
	align='mid'
 )

#decorate plot
plt.title(f"({date}) #{sequence_number}_r{repetition_number}\n{sequence_name}")
plt.ylabel("Photon Counts, (200us Bin)")
plt.xlabel("Time (s)")


#*********************
#	Fit Cavity Scans with MLE
#*********************

# for each_key in cavity_scan_parameters.keys():
#	switch each_key:
#		'empty_cavity':
#			empty_cavity_scan_analysis()
#		'atomic_lifetime':
#			atomic_lifetime_analysis()

# #perform fit
# (best_guess, cov_best_guess) = fit_functions.fit_single_cavity_peak(
#	data=photon_arrival_times,
#	start=0,
#	end=30e-3,
#	bin_interval=200e-6,
# )

# #perform fit with Rabi splitting MLE


# #plot fit
# x = np.arange(0,30e-3,20e-6)
# y = fit_functions.lorentzian(x=x,x0=best_guess[0], a=best_guess[1], gamma=best_guess[2], offset=best_guess[3])
# plt.plot(x,y)
