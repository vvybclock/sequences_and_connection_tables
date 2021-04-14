from labscriptlib.ybclock.analysis.functions import fit_functions
import numpy as np
import matplotlib.pyplot as plt
from labscriptlib.ybclock.analysis.functions.metadata import extract_sequence_repetition_numbers, extract_date,extract_sequence_name
from lyse import Run

def empty_cavity_analysis(data, scan_parameters, path):
	'''

	Here we take the photons arrival time (`data`), check which one has arrived within an
	empty cavity scan, and, for each scan, we convert the arrival time into
	photon's frequency. We finally fit each scan and plot a graph overlapping all the cavity scans.

	If the number of photons detected is huge (set a limit here... maybe 1000), we bin the data and fit the resulting histogram with a normal minimization of residuals' variance-

	'''

	for params in scan_parameters:
		# params is a dictionary whose properties are defined in exp_cavity.py
		start_time	= params['t']
		end_time  	= start_time + params['duration']
		final_f   	= params['final_f']
		initial_f 	= params['initial_f']

		#Select photons in the scan range
		photons_in_scan_time = data[(data > start_time) & (data < end_time)]
                        
		#Extract photon's frequency based on arrival time
		#since we have calibrated frequency vs voltage, and performed the scan across frequency
		#there is a true linear relationship between a arrival time and frequency :)
		photon_arrivals_in_frequency_MHz = (photons_in_scan_time - start_time)*(final_f-initial_f)/(end_time-start_time)

		#Fit the Data using the MLE method.
		best_param = fit_functions.fit_rabi_splitting_transmission_MLE(
			data=photon_arrivals_in_frequency_MHz, 
			bnds={"fatom_range":(0,50), "fcavity_range":(0,50), "Neta_range":(0,.001)}, 
			path=path
		)
		try:
			best_param = fit_functions.fit_rabi_splitting_transmission_MLE(
				data=photon_arrivals_in_frequency_MHz, 
				bnds={"fatom_range":(0,50), "fcavity_range":(0,50), "Neta_range":(0,0.001)}, #  Each lower bound must be strictly less than each upper bound. Use fatom_range = fcavity_range, to avoid any possible error.
				path=path
			)
			print(best_param)
		except:
			print("MLE Photon Arrival Time Fit Failed.")


		#Plot
		#Plot
		#Plot

		#extract metadata
		(sequence_number, repetition_number)	= extract_sequence_repetition_numbers(path)
		date                                	= extract_date(path)
		sequence_name                       	= extract_sequence_name(path)
		
		run=Run(path)
		data_globals = run.get_globals()

		#plot data
		histogram_resolution = .2;

		n = plt.hist(
			photon_arrivals_in_frequency_MHz,
			bins=np.arange(data_globals["empty_cavity_frequency_sweep_initial"],data_globals["empty_cavity_frequency_sweep_range"], histogram_resolution),
			align='mid'
		 )
		
		#decorate plot
		plt.title(f"({date}) #{sequence_number}_r{repetition_number}\n{sequence_name}")
		plt.ylabel("Photon Counts, (50 kHz Bin)")
		plt.xlabel("frequency (MHz)")
		
		#plot fit
		x = np.arange(data_globals["empty_cavity_frequency_sweep_initial"],data_globals["empty_cavity_frequency_sweep_range"], histogram_resolution/3)
		y = fit_functions.rabi_splitting_transmission(
				f = x,
				fatom = best_param["fatom"],
				fcavity = best_param["fcavity"],
				Neta = best_param["Neta"],
				gamma = best_param["gamma"],
				kappa = best_param["kappa"]
			)
		plt.plot(x,max(n[0])*y)
		try:
			x = np.arange(data_globals["empty_cavity_frequency_sweep_initial"],data_globals["empty_cavity_frequency_sweep_range"], histogram_resolution/3)
			y = fit_functions.rabi_splitting_transmission(
					f = x,
					fatom = best_param["fatom"],
					fcavity = best_param["fcavity"],
					Neta = best_param["Neta"],
					gamma = best_param["gamma"],
					kappa = best_param["kappa"]
				)
			plt.plot(x,max(n[0])*y) # I need to scale automatically the amplitude of the signal. Multiply by the max histogram value.
		except:
			print("Failed plotting empty_cavity fit!")