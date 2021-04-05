'''
	extracts photon arrival times from the single shot .lst file. 

	This is done manually. So if you want tips on how to extract data manually
	from the HDF file look here.

	Saves the results as attributes to the '/data/photon_arrivals' group
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
	
	#extract the .lst binarys
	with h5py.File(path,'a') as hdf:
		arrival_lst_binary = np.array(hdf['/data/photon_arrivals/all_arrivals'])
		arrival_lst_bytestr = arrival_lst_binary.tobytes()

	#process the .lst binary
	(_,newline)                	= photon_counter.determine_newline_type(arrival_lst_bytestr)
	(header, data)             	= photon_counter.split_file_into_header_and_data(entire_file=arrival_lst_bytestr, newline=newline)
	header                     	= photon_counter.decode_header(header,verbose=False)
	(channels, quantized_times)	= photon_counter.decode_data(data, verbose=False)
	arrival_times              	= photon_counter.convert_to_absolute_time(t0=0, channels=channels,quantized_times=quantized_times, start_trigger_period=1e-3, quantized_time_unit=2e-9)
	
	# print(quantized_times)
	#save the processed variables to the hdf files
	run = Run(path)
	processed_arrivals = {}

	for i in range(4):
		run.save_result(
			name   	=f'processed_arrivals_ch_{i}',
			value  	=np.array(arrival_times[i]),
			# group	='/data/photon_arrivals/'
			)

	print("processed_arrivals saved in hdf.")
	

	

	