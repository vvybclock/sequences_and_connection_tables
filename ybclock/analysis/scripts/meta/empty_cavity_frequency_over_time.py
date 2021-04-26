from lyse import *
import pickle
import numpy as np
import matplotlib.pyplot as plt


#exposes all the variables available in the lyse window
dataframe = data()

runtimes = list(dataframe['run time'])
paths = list(dataframe['filepath'])

fitted_cavity_frequency = []
cavity_scan_runtime = []

for path in paths:
	#pull pickled fit parameters from file
	with h5py.File(path, 'r') as hdf5_file:
		try:
			grp = hdf5_file['/results/empty_cavity_helper']
		except:
			print("Failed to open results group.")

		try:
			void_pickled_dict = np.array(grp["fitted_exp_cavity_frequency_parameters"])
		except:
			print("Failed to pull pickled dict.")

		try:
			#de-pickle them
			pickled_dict_list = void_pickled_dict.tobytes()
		except:
			print("Failed to convert to bytestream")

		try:
			fit_parameter_list = pickle.loads(pickled_dict_list)
		except:
			print("Failed to de-pickle")

	#pull fitted cavity frequencies
	i = paths.index(path)
	for each_scan in fit_parameter_list:
		cavity_scan_runtime.append(runtimes[i])
		fitted_cavity_frequency.append(each_scan["fcavity"])

plt.scatter(cavity_scan_runtime, fitted_cavity_frequency)
plt.title("Empty Cavity Frequency")
plt.ylabel("Frequency (MHz)")
plt.xlabel("Time")