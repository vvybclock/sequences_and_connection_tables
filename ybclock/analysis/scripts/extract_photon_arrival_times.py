'''Minimal working lyse script.

You can use this as a starting point for making new lyse scripts.  See the
`lyse` docs bulit in labscriptlib.ybclock.html for details on the lyse
functions.

'''
from lyse import *

#Add in libraries for working with HDF files
import labscript_utils.h5_lock
import h5py

#analysis libs
import numpy as np
import labscriptlib.ybclock.analysis.functions.photon_counter as photon_counter


if __name__ == '__main__':
	#load data from the last run
	path #path is defined in `from lyse ...`
	with h5py.File(path,'a') as hdf:
		print(hdf['/data/photon_arrivals'])

		#create folder for photon counts
		# grp = hdf.create_group("/data/photon_arrivals")
		# file_array = np.fromfile(p7888.p7888_data_file,dtype='<i4')
		# lst_file = grp.create_dataset("all_arrivals",data=file_array)
		# lst_file.attrs.create("Description", data=
		#	'Contains the very large photon arrival file. This file contains the data of arrival times from multiple shots. Not just the one shot we care about here.'
		# )

	#extract the .lst binary

	#process the .lst binary

	#save the processed variables to the hdf file