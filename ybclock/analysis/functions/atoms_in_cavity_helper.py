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

	We do not perform MLE analysis if we detect enough photons in the scan. "Enough photons" means that MLE and least_square provide the same uncertainty on the atom number estimation, see [MLE_vs_leastSquare](https://paper.dropbox.com/doc/Fit-and-measurement-quality--BJneIwnJqNOnEEYUYTkog5qxAg-szpYsBrXGK81Qq4BF6jEF) for details.


	The save parameters are stored in "results/empty_cavity_helper/fitted_exp_cavity_frequency_parameters"

	'''

	results_to_save = []
	#get empty cavity scan parameters from hdf file.
	run = Run(path)
	#Fit the Data using both least_square method or MLE method.
	try:
		# Check if there is an empty cavity fit and extract empty cavity frequency
		empty_cavity_frequency_from_fit = run.get_result("empty_cavity_helper", "exp_cavity_frequency")
		# When we have atoms in the spin down state, the effective empty cavity
		# frequency is "pushed" up by ~400kHz per 1000 N_downeta, hence the
		# asymmetric bounds 
		cavity_range = (empty_cavity_frequency_from_fit - 1, empty_cavity_frequency_from_fit + 1);
	except Exception as e:
		cavity_range = (0,50);
		print(f"No empty cavity scan result found. {e}")

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

		histogram_resolution = .2;
		if len(photon_arrivals_in_frequency_MHz) > 200:
			#Fit the Data using the least_square method.
			# Remember to add fatom_guess in globals!
			try:
				best_param = fit_functions.fit_rabi_splitting_transmission(
					data = photon_arrivals_in_frequency_MHz,
					bnds={"fatom_range":(0,50), "fcavity_range":cavity_range, "Neta_range":(0,10000)},
					bin_interval=histogram_resolution,
					path = path
					)
				print("Rabi Splitting Fit Params:")
				for key, value in best_param.items():
					if key not in "jacobian":
						print(f"{key}: {value}")
			except Exception as e:
				print("least square Photon Arrival Time Fit Failed. Because: ", e)
		else:
			try:
				best_param = fit_functions.fit_rabi_splitting_transmission_MLE(
					data=photon_arrivals_in_frequency_MHz, 
					bnds={"fatom_range":(0,50), "fcavity_range":cavity_range, "Neta_range":(0,20000)},
					path=path
				)
				print("Rabi Splitting Fit Params:")
				for key, value in best_param.items():
					if key not in 'covariance':
						print(f"{key}: {value}")

			except Exception as e:
				print(f"MLE Photon Arrival Time Fit Failed. {e}")

		#Plot


		#extract metadata
		(sequence_number, repetition_number)	= extract_sequence_repetition_numbers(path)
		date                                	= extract_date(path)
		sequence_name                       	= extract_sequence_name(path)
		                                    		
		run=Run(path)
		data_globals = run.get_globals()

		#plot histogram	
		#plot data
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
		try:
			x = np.arange(data_globals["empty_cavity_frequency_sweep_initial"],data_globals["empty_cavity_frequency_sweep_range"], histogram_resolution)
			y = fit_functions.rabi_splitting_transmission(
			                         		f = x,
			                         		fatom = best_param["fatom"],
			                         		fcavity = best_param["fcavity"],
			                         		Neta = best_param["Neta"],
			                         		gamma = best_param["gamma"],
			                         		kappa = best_param["kappa"]
			                         	)
			try:
				plt.plot(x,best_param["amplitude"]*y)
			except Exception as e:
				plt.plot(x,sum(n[0])*histogram_resolution*y)
				print("amplitude fit parameter not found:", e)
		except Exception as e:
			print(f"Failed plotting fit! {e}")

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

#save chi square for each fit
	try:
		chi_2_list=[]
		for each_scan in results_to_save:
			chi_2_list.append(best_param["chi_square"])

		run.save_result(
				name='cavity_scan_fit_chi2',
				value=chi_2_list
				)
	except Exception as e:
		print("Failed Saving Fit Results in Lyse. Error:", e)
#save chi square for each fit
	try:
		Neta_list=[]
		for each_scan in results_to_save:
			Neta_list.append(best_param["Neta"])

		run.save_result(
				name='Neta_fit',
				value=Neta_list
				)
	except Exception as e:
		print("Failed Saving Fit Results in Lyse. Error:", e)