from labscript import start, stop

from labscriptlib.ybclock_v0_1.connection_functions import define_hardware_cards
from labscriptlib.ybclock_v0_1.connection_functions import define_channels

def define_connection_table():

	define_hardware_cards()
	
	define_channels()

	#the labscript compiler spits out time markers defined in the main sequence.
	#this is to add text that should have been included in the main labscript
	#compiler.
	print("Time Markers:")



if __name__ == '__main__':

	define_connection_table()
	
	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()

	# Stop the experiment shot with stop()
	stop(1.0)
