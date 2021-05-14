''' This metanalysis will plot and analyse the initially loaded Neta versus the time. It
will be used to monitor how fitting Rabi splitting works over the time and/or
as a function of experimental parameters

 # To Do 
 	[x] make atoms_in_cavity_helper.py write the Neta 1 value per scan number of fit in lyse parameters
 	[] read lyse parameters here
 	[] drop Neta based on bad chi^2 
 	[] multiple scan number and different color for different scan number in the sequence
 	[] statistics (hist plot, for example) of Neta results

'''

from lyse import *
import pickle
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
	try:
		#exposes all the variables available in the lyse window
		dataframe = data()


		runtimes = list(dataframe['run time'])
		paths = list(dataframe['filepath'])
		fit_quality = list(dataframe['empty_cavity_helper','cavity_scan_fit_chi2'])
		Neta_1 = list(dataframe['atoms_in_cavity_helper','Neta_1'])
		#this is what we call the run number. we'll use it to change the color, so we can tell when we changed the sequence.
		sequence_index = list(dataframe['sequence_index'])


		#make some colors.
		cerulean = (4/256,146/256,194/256)
		crimson = (185/256, 14/256, 10/256)
		colors = [cerulean if seq%2 == 0 else crimson for seq in sequence_index]

		#Calculate and print Good Fit Ratio
		good_chi_for_fit = [0.4,10]

		is_good_fit = []
		for set_of_fits in fit_quality:
			is_good_set_fit = []
			for fit in set_of_fits:
				is_good_set_fit.append(
						(fit > good_chi_for_fit[0]) and (fit < good_chi_for_fit[1])
					)
			is_good_fit.append(is_good_set_fit)


		# select good runs
		# Neta_sel = []
		# runtimes_sel = []
		# for i in range(len(is_good_fit)):
		# 	for j in range(len(is_good_fit[i])):
		# 		if is_good_fit[i][j]:
		# 			Neta_sel.append(Neta_list[i][j])
		# 			runtimes_sel.append(runtimes[i])

		blue = (0,0,1)
		#s - size
		plt.scatter(runtimes_sel, Neta_sel, s=20, c = blue)

		plt.title("Fitted Neta" )
		plt.ylabel("Neta")
		plt.xlabel("Time")


	except Exception as e:
		print(f"Rabi Splitting: {e}")