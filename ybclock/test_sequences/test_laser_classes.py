'''
	Example usage for classes. This is also a development tool for myself.
'''

from labscript import start, stop
from labscriptlib.ybclock.connection_table import define_connection_table
from labscriptlib.ybclock.classes import *

def define_classes():
	print(f"Constructing green...")
	green = Laser()
	print(f"Constructing green.probe...")
	green.probe = LaserBeam()
	print(f"Constructing green.pump...")
	green.pump = LaserBeam()

	blue = BlueLaser()

	print(blue)
	pass


if __name__ == '__main__':
	define_connection_table()
	define_classes()

	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start(); t = 0;


	blue.mot.turnon(t)

	t = 1

	blue.mot.turnoff(t)

	t = 2 

	blue.mot.constant(t, value=)

	stop(1)
