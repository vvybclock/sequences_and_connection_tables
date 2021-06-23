'''
	Plot's the Empty Cavity Frequency over Time.

	Currently it changes plot point color depending on the parity of the sequence
	number. This helps keep track of changes to the sequence. This feature is
	kind of useless seeing as with feedback the sequence will change every shot.

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
		frequencies = list(dataframe['empty_cavity_helper','fcavity_1'])
		#this is what we call the run number. we'll use it to change the color, so we can tell when we changed the sequence.
		sequence_index = list(dataframe['sequence_index'])


		#make some colors.
		cerulean = (4/256,146/256,194/256)
		crimson = (185/256, 14/256, 10/256)
		colors = [cerulean if seq%2 == 0 else crimson for seq in sequence_index]


		#s - size
		plt.scatter(runtimes, frequencies, s=20, c = colors)

		plt.title("Empty Cavity Frequency")
		plt.ylabel("Frequency (MHz)")
		plt.xlabel("Time")

	except Exception as e:
		print(e)