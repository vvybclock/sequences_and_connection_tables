'''
	Defines python classes that group together sequence primitives for simplifying lab control/scripting.
'''
import builtins
from labscriptlib.ybclock.classes import *

def define_classes(name_space=globals()):
	''' Defines the objects for controlling our lasers '''

	#this the only way I found to actually define variables for use outside the module.
	builtins.blue 	= BlueLaser()
	builtins.green	= GreenLaser()
	builtins.red  	= RedLaser()