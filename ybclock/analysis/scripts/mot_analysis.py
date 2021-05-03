'''
	Plots Images of the MOT for debugging.
'''
from lyse import *
#Add in libraries for working with HDF files
import labscript_utils.h5_lock
import h5py
#analysis libs
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

	#get data
	run = Run(path)

	#extract green mot images
	try:
		bg       	= run.get_image('isometric_cam','green_mot','bg')
		green_mot	= run.get_image('isometric_cam','green_mot','loaded')

		plt.imshow(abs(green_mot - bg))
	except:
		pass
	pass