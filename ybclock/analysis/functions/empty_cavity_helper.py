from labscriptlib.ybclock.analysis.functions import fit_functions
import numpy as np
import matplotlib.pyplot as plt
from labscriptlib.ybclock.analysis.functions.metadata import extract_sequence_repetition_numbers, extract_date,extract_sequence_name
from lyse import Run
import pickle

def empty_cavity_analysis(data, scan_parameters,path):
	'''

	Here we take the photons arrival time (`data`), check which one has arrived within an
	empty cavity scan, and, for each scan, we convert the arrival time into
	photon's frequency. We finally fit each scan.

	This script saves cavity frequency parameters, as well as some vestigial parameters that
	come from the free parameters in the fitting function.

	The save parameters are stored in "results/empty_cavity_helper/fitted_exp_cavity_frequency_parameters"

	We do not perform MLE analysis if we detect enough photons in the scan. "Enough photons" means that MLE and least_square provide the same uncertainty on the atom number estimation, see [MLE_vs_leastSquare](https://paper.dropbox.com/doc/Fit-and-measurement-quality--BJneIwnJqNOnEEYUYTkog5qxAg-szpYsBrXGK81Qq4BF6jEF) for details.

	'''

	results_to_save = []

	for a_scan in scan_parameters:
		# a_scan is a dictionary whose properties are defined in exp_cavity.py
		start_time	= a_scan['t']
		end_time  	= start_time + a_scan['duration']
		final_f   	= a_scan['final_f']
		initial_f 	= a_scan['initial_f']

		#Select photons in the scan range
		photons_in_scan_time = data[(data > start_time) & (data < end_time)]
                        
		#Extract photon's frequency based on arrival time
		#since we have calibrated frequency vs voltage, and performed the scan across frequency
		#there is a true linear relationship between arrival time and frequency :)
		photon_arrivals_in_frequency_MHz = (photons_in_scan_time - start_time)*(final_f-initial_f)/(end_time-start_time)

		# Decide if we should use MLE fit or not.
		if len(photon_arrivals_in_frequency_MHz) > 250:
			#Fit the Data using the least_square method.
			try:
				best_param = fit_functions.fit_rabi_splitting_transmission(
					data=photon_arrivals_in_frequency_MHz, 
					bnds={"fatom_range":(0,50), "fcavity_range":(0,50), "Neta_range":(0,0.001)},
					#Each lower bound must be strictly less than each upper bound. Use fatom_range == fcavity_range to avoid any possible error.
					path=path
				)
				print(best_param)
			except:
				print("Least_square Photon Arrival Time Fit Failed.")
		else:
			#Fit the Data using the MLE method.
			try:
				best_param = fit_functions.fit_rabi_splitting_transmission_MLE(
					data=photon_arrivals_in_frequency_MHz, 
					bnds={"fatom_range":(0,50), "fcavity_range":(0,50), "Neta_range":(0,0.001)},
					#Each lower bound must be strictly less than each upper bound. Use fatom_range == fcavity_range to avoid any possible error.
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
		                                    		
		#plot histogram                     	
		freq_bin_width_MHz = 0.1
		n = plt.hist(
			photon_arrivals_in_frequency_MHz,
			bins=np.arange(0,50, freq_bin_width_MHz),
			align='mid'
		 )
		
		#decorate plot
		plt.title(f"({date}) #{sequence_number}_r{repetition_number}\n{sequence_name}")
		plt.ylabel(f"Photon Counts, ({freq_bin_width_MHz*1000:.3g} kHz Bin)")
		plt.xlabel("Frequency (MHz)")
		
		#plot fit
		try:
			x = np.arange(0,50, freq_bin_width_MHz)
			y = fit_functions.rabi_splitting_transmission(
					f = x,
					fatom = best_param["fatom"],
					fcavity = best_param["fcavity"],
					Neta = best_param["Neta"],
					gamma = best_param["gamma"],
					kappa = best_param["kappa"]
				)
			plt.plot(x,max(n[0])*y) # I need to scale automatically the amplitude of the signal. Just multiply by the size of largest histogram.
		except:
			print("Failed plotting fit!")

		try:
			#store all the results in a dictionary
			parameters = best_param
			#add all the scan_parameters to the dictionary
			parameters.update(a_scan)
			results_to_save.append(parameters)
		except:
			pass

	#save fit parameters into hdf file.
	run = Run(path)

	#save some documentation with the parameters
	docstring = '''

	Fit results are saved to a list. Each element represents an
	empty_cavity_scan. Each element is a dictionary that holds all the
	parameters describing the fit results. Pull the keys to see the fit values.

	To extract the data use python3.8, pickle and numpy, and lyse.

	void_pickled_dict_list = run.get_result_array(group='_scan_analysis_name_.py',
	name='')
	pickled_dict_list = void_pickled_dict.tobytes()
	fit_parameter_list = pickle.loads(pickled_dict_list)

	'''

	#save all parameters
	pickled_dict_list = pickle.dumps(results_to_save)
	run.save_result_array(
		name='fitted_exp_cavity_frequency_parameters',
		data=np.void(pickled_dict_list)
	)
	
	#save some documentation
	run.save_result(
		name='documentation_fitted_exp_cavity_frequency_parameters',
		value=docstring,
		group='empty_cavity_helper/fitted_exp_cavity_frequency_parameters'
	)

	#save averaged sample of the cavity frequency.
	try:
		average_frequency = 0
		number_of_scans = 0
		for each_scan in results_to_save:
			average_frequency += each_scan['fcavity']
			number_of_scans += 1

		average_frequency = average_frequency / number_of_scans
		run.save_result(
			name='exp_cavity_frequency',
			value=average_frequency
		)
	except:
		pass