'''
	Defines python classes that group together sequence primitives for simplifying lab control/scripting.
'''
from labscriptlib.ybclock.classes import *

def define_classes():
	''' Defines the objects for controlling our lasers '''
	global blue, green, red

	blue 	= BlueLaser()
	green	= GreenLaser()
	red  	= RedLaser()