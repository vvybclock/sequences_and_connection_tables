''' This metanalysis will plot and analyse the fit quality ofer the time. It
will be used to monitor how fitting Rabi splitting works over the time and/or
as a function of experimental parameters

 # To Do 
 	[] make atoms_in_cavity_helper.py write the chi^2 value (and/or LogLikelihood) of fit in lyse parameters
 	[] read lyse parameters here
 	[] plot chi^2 over the time
 	[] statistics (hist plot, for example) of chi^2 results
 	[] statistics versus some interesting parameter, like photons detected for example

'''

from lyse import *
import pickle
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
	#exposes all the variables available in the lyse window
	dataframe = data()


	runtimes = list(dataframe['run time'])
	paths = list(dataframe['filepath'])
	frequencies = list(dataframe['empty_cavity_helper','exp_cavity_frequency'])
	#this is what we call the run number. we'll use it to change the color, so we can tell when we changed the sequence.
	sequence_index = list(dataframe['sequence_index'])


	#make some colors.
	cerulean = (4/256,146/256,194/256)
	crimson = (185/256, 14/256, 10/256)
	colors = [cerulean if seq%2 == 0 else crimson for seq in sequence_index]


	#s - size
	plt.scatter(runtimes, frequencies, s=1, c = colors)

	plt.title("Empty Cavity Frequency")
	plt.ylabel("Frequency (MHz)")
	plt.xlabel("Time")