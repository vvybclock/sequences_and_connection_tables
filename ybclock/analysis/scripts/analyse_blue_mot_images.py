'''Pulls blue_mot images from sequences and draws the atom cloud.
'''
from lyse import *
#Add in libraries for working with HDF files
import labscript_utils.h5_lock
import h5py
#analysis libs
import numpy as np



if __name__ == '__main__':
	#load data from the last run
	run = Run(path) #path is defined in `from lyse ...`

	try:
		#get the blue_mot images
		pass
	except:
		print("Missing or no images. Skipping blue_mot_analysis.")
		return