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
		arrival_lst_binary = np.array(hdf['/data/photon_arrivals/all_arrivals'])
		arrival_lst_bytestr = arrival_lst_binary.tobytes()
		
		(_,newline)                	= photon_counter.determine_newline_type(arrival_lst_bytestr)
		(header, data)             	= photon_counter.split_file_into_header_and_data(entire_file=arrival_lst_bytestr, newline=newline)
		header                     	= photon_counter.decode_header(header,verbose=False)
		(channels, quantized_times)	= photon_counter.decode_data(data, verbose=False)
		
	print(channels)
	print(quantized_times)
	#extract the .lst binary

	#process the .lst binary

	#save the processed variables to the hdf file