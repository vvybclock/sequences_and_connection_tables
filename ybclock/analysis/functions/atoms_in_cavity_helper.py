from labscriptlib.ybclock.analysis.functions import fit_functions
import numpy as np
import matplotlib.pyplot as plt
from labscriptlib.ybclock.analysis.functions.metadata import extract_sequence_repetition_numbers, extract_date,extract_sequence_name
from lyse import Run
import pickle

def atom_cavity_analysis(data, scan_parameters,path):
	'''

	This script calculates and saves "vacuum" rabi splitting parameters, as well
	as some vestigial parameters that come from the free parameters in the
	fitting function.

	Here we take the photons arrival time (`data`), check which one has arrived within an
	empty cavity scan, and, for each scan, we convert the arrival time into
	photon's frequency. We finally fit each scan.

	The save parameters are stored in "results/empty_cavity_helper/fitted_exp_cavity_frequency_parameters"

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
		#there is a true linear relationship between a arrival time and frequency :)
		photon_arrivals_in_frequency_MHz = (photons_in_scan_time - start_time)*(final_f-initial_f)/(end_time-start_time)

		#Fit the Data using the MLE method.
		try:
			best_param = fit_functions.fit_rabi_splitting_transmission_MLE(
				data=photon_arrivals_in_frequency_MHz, 
				bnds={"fatom_range":(20,25), "fcavity_range":(20,30), "Neta_range":(0,3000)}
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
		plt.hist(
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
			plt.plot(x,200*y) # I need to scale automatically the amplitude of the signal. Just multiply by the size of largest histogram.
		except:
			print("Failed plotting fit!")

		#store all the results in a dictionary
		parameters = best_param
		#add all the scan_parameters to the dictionary
		parameters.update(a_scan)
		results_to_save.append(parameters)

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

	pickled_dict_list = pickle.dumps(results_to_save)
	run.save_result_array(
		name='fitted_exp_cavity_frequency_parameters',
		data=np.void(pickled_dict_list)
	)
	run.save_result(
		name='documentation_fitted_exp_cavity_frequency_parameters',
		value=docstring,
		group='empty_cavity_helper/fitted_exp_cavity_frequency_parameters'
	)
			