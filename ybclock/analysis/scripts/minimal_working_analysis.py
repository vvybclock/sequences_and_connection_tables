'''Minimal working lyse script.

You can use this as a starting point for making new lyse scripts.
'''
from lyse import *
#Add in libraries for working with HDF files
import labscript_utils.h5_lock
import h5py
#analysis libs
import numpy as np



if __name__ == '__main__':
	#path is defined in 'from lyse import *'
	all_lyse_data = data(path)

	with h5py.File(path,'a') as hdf:
		#pull data from hdf
		file_array = np.array(hdf['/data/photon_arrivals/all_arrivals'])		