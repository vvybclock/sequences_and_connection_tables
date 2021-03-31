from labscriptlib.ybclock.analysis.functions import fit_functions

def empty_cavity_analysis(data, scan_parameters):
	'''

	Here we take the photons arrival time (`data`), check which one has arrived within an
	empty cavity scan, and, for each scan, we convert the arrival time into
	photon's frequency. We finally fit each scan.

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
		best_param = fit_functions.fit_rabi_splitting_transmission_MLE(data=photon_arrivals_in_frequency_MHz)
		print(best_param)
		
