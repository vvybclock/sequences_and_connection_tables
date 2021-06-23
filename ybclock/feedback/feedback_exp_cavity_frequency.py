'''

	Changes the HP8648 Frequency so that the ExperimentalCavity frequency shows
	up at the appropriate location.

	This will use a simple PID loop.

'''

#make sure the .ini config file has the correct address for the Runmanager!!!
import runmanager.remote as remote
from lyse import *
import os

MHz = 1e6

#variables for repacking the globals file
userProfile      	= "C:\\Users\\YbMinutes"
globals_file     	= os.path.join(userProfile,"labscript-suite\\userlib\\labscriptlib\\ybclock\\globals.h5")
hdf5repack_file  	= os.path.join(userProfile,r"labscript-suite\userlib\labscriptlib\ybclock\feedback\h5repack.exe")
temp_globals_file	= os.path.join(userProfile,r"labscript-suite\userlib\labscriptlib\ybclock\temp_globals.h5")

try:
	#read cavity frequency
	print("Reading Cavity Frequency...")
	run = Run(path)
	actual_cavity_frequency = run.get_result('empty_cavity_helper','exp_cavity_frequency')


	print("Performing Feedback & Getting Globals...")
	#get PID variables
	retrieved_globals = remote.get_globals()

	G         	= retrieved_globals['cavity_frequency_G']
	I         	= retrieved_globals['cavity_frequency_I']
	P         	= retrieved_globals['cavity_frequency_P']
	integrator	= retrieved_globals['cavity_frequency_integrator']

	#read desired setpoint
	setpoint	= retrieved_globals['exp_cavity_set_frequency']

	#perform PID
	error = actual_cavity_frequency - setpoint

	output = -G*(P*error)

	#set cavity frequency 
	temp_bridging_frequency = retrieved_globals['bridging_frequency_759']
	temp_bridging_frequency -= output

	if temp_bridging_frequency < 420 or temp_bridging_frequency > 450:
		print("Warning: Feedback seems out of lock... Near boundarys [420,450]")
	else:
		retrieved_globals['bridging_frequency_759'] = temp_bridging_frequency

		#update the global variables
		print("Setting Global Variables...")
		remote.set_globals(retrieved_globals)

	#engage the next shot.
	print("Engaging Next Shot...", end='')
	remote.engage()
	print("Done!")

	#repack the globals
	print("Repacking Globals...",end="")
	os.rename(globals_file, temp_globals_file)
	os.system(f'{hdf5repack_file} {temp_globals_file} {globals_file}')
	os.remove(temp_globals_file)
	print("Done!")


	print("Succesfully Performed Feedback.")
except Exception as e:
	print(f"Failed Feedback: {e}")
	#engage the next shot.
	print("Engaging Next Shot...", end='')
	remote.engage()
	print("Done!")

	pass

