from labscriptlib.ybclock.analysis.functions import fit_functions
import numpy as np
import matplotlib.pyplot as plt
from labscriptlib.ybclock.analysis.functions.metadata import extract_sequence_repetition_numbers, extract_date,extract_sequence_name

def empty_cavity_analysis(data, scan_parameters,path):
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
		try:
			best_param = fit_functions.fit_rabi_splitting_transmission_MLE(
				data=photon_arrivals_in_frequency_MHz, 
				bnds={"fatom_range":(5,5), "fcavity_range":(0,50), "Neta_range":(0,0)}
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
		                                    		
		#plot data
		# plt.hist(
		#	photons_in_scan_time-start_time,
		#	bins=np.arange(0,end_time-start_time, 200e-6),
		#	align='mid'
		#  )

		# #decorate plot
		# plt.title(f"({date}) #{sequence_number}_r{repetition_number}\n{sequence_name}")
		# plt.ylabel("Photon Counts, (200us Bin)")
		# plt.xlabel("Time (s)")

		plt.hist(
			photon_arrivals_in_frequency_MHz,
			bins=np.arange(0,50, 0.1),
			align='mid'
		 )
		

		#decorate plot
		plt.title(f"({date}) #{sequence_number}_r{repetition_number}\n{sequence_name}")
		plt.ylabel("Photon Counts, (50 kHz Bin)")
		plt.xlabel("frequency (MHz)")
		
		#plot fit
		try:
			x = np.arange(0,50, 0.1)
			y = fit_functions.rabi_splitting_transmission(
					f = x,
					fatom = best_param["fatom"],
					fcavity = best_param["fcavity"],
					Neta = best_param["Neta"],
					gamma = best_param["gamma"],
					kappa = best_param["kappa"]
				)
			plt.plot(x,200*y) # I need to scale automatically the amplitude of the signal. I need to implement also the dark counts
		except:
			print("Failed plotting fit!")