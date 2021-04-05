from lyse import *
import numpy as np
import matplotlib.pyplot as plt
from labscriptlib.ybclock.analysis.functions.metadata import extract_sequence_repetition_numbers, extract_date,extract_sequence_name
import labscriptlib.ybclock.analysis.functions.fit_functions as fit_functions

run = Run(path)

# load globals (gives an empty variable {} if there are no globals)
data_globals = run.get_globals()


#extract metadata
(sequence_number, repetition_number)	= extract_sequence_repetition_numbers(path)
date                                	= extract_date(path)
sequence_name                       	= extract_sequence_name(path)

#extract data
photon_arrival_times = run.get_result(group='extract_photon_arrival_times',name='processed_arrivals_ch_1')

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
#	Fit Cavity Scan
#*********************

# I need to identify Empty cavity scans

#perform fit
(best_guess, cov_best_guess) = fit_functions.fit_single_cavity_peak(
	data=photon_arrival_times,
	start=0,
	end=30e-3,
	bin_interval=200e-6,
)

<<<<<<< HEAD
=======
#perform fit with Rabi splitting MLE

>>>>>>> fc8658fcb41cb2ef75082167e3a9455718f2578e

#plot fit
x = np.arange(0,30e-3,20e-6)
y = fit_functions.lorentzian(x=x,x0=best_guess[0], a=best_guess[1], gamma=best_guess[2], offset=best_guess[3])
plt.plot(x,y)


#*********************
#	Fit Rabi Scan
#*********************

# I need to identify Rabi scans
