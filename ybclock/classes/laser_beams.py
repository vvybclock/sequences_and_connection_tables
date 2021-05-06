'''
	Holds the classes for laser light control.

	##Desired Example Definitions

	```python

	#define the lasers
	green 	= Laser()
	yellow	= Laser()
	trap  	= Laser()

	#define the beampaths for the green laser
	green.probe	= LaserBeam()
	green.pump 	= LaserBeam()

	#define the methods for each LaserBeam.
	green.probe.turnoff = 
	```

	##Desired Example Usage
'''
class LaserFrequency():
	pass
class LaserIntensity():
	self.is_on = False

	def turnoff():
		self.is_on = False
		
	pass

class LaserBeam():
	"""This is a template that holds functions for controlling the laser beam properties of a *single beampath*: intensity, and frequency."""

	self.intensity = None
	self.frequency = None
	def __init__(self):
		pass

class Laser():
	'''
		This keeps track of the various laser beampaths that a single laser can be the source of. This is good for grouping our beampaths symantically.
	'''
	pass