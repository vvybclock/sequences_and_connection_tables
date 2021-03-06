'''
	This is a simple file that shows you the minimal elements you need 
	to write your own experimental sequence.
'''
from labscript import start, stop
from labscriptlib.ybclock.connection_table import define_connection_table

if __name__ == '__main__':

	define_connection_table()
	
	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()
	stop(1)