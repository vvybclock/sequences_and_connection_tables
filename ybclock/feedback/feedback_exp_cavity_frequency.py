'''

	Changes the HP8648 Frequency so that the ExperimentalCavity frequency shows
	up at the appropriate location.

	This will use a simple PID loop.

'''

#make sure the .ini config file has the correct address for the Runmanager!!!
import runmanager.remote as remote
from lyse import *


MHz = 1e6

#read cavity frequency
run = Run(path)
actual_cavity_frequency = run.get_result('empty_cavity_helper','exp_cavity_frequency')


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
retrieved_globals['bridging_frequency_759'] -= output

#update the global variables
remote.set_globals(retrieved_globals)




#engage the next shot.
remote.engage()