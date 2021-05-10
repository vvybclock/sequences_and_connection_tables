'''
	Holds the classes for laser light control.

	#Laser Classes

	`Laser()` is just meant to group together `LaserBeam`s as part of the
	datatypes it remembers. `LaserBeam()` is just meant to group together
	frequency and intensity controller classes: `LaserIntensity()` and
	`LaserFrequency()`.
	
	##Desired Example Definitions

	```python

	#define the lasers
	green 	= GreenLaser()
	yellow	= YellowLaser()
	trap  	= TrapLaser()
	```

	##Desired Example Usage
	```python
	green.probe.frequency.constant(t,'10 Mhz')
	green.probe.turnoff(t)

	#automatically checks to see if laser is off, if so turn on.
	green.probe.intensity.constant(t,'1 mW')
	green.probe.turnoff(t)
	```
'''
class LaserFrequency():
	__frequency_channel = None
	pass
class LaserIntensity():
	'''
		
		This is a controller for dealing with the annoying details of turning a
		laser on and off.

		Auto turnoff, turnon features assume sequential usage of the light power
		commands. If you do them out of order, they will not behave correctly. In
		this case, you need to manually set is_on = True/False, or set the overload
		arg to true.

		#To Do

			[ ] turnoff function
			[ ] turnon function
			[ ] constant
			[ ] ramp

	'''
	__intensity_channel = None
	__shutter_channel  	= None
	__turnoff_voltage  	= None
	__shutter_closetime	= None

	is_on = False

	def __init__(self, intensity_channel=None, shutter_channel=None, turnoff_voltage=None,shutter_closetime=None):
		self.__intensity_channel	= intensity_channel
		self.__shutter_channel  	= shutter_channel
		self.__turnoff_voltage  	= turnoff_voltage
		self.__shutter_closetime	= shutter_closetime

	def turnoff(self, t,overload=False):
		'''
			Turns off beam if and only if on unless `overload == True` then always turn off.

			#To Do
				[ ]	Set up AOM/EOM turn on/off
				[ ]	Set up Shutter turn on/off
				[ ]	Set up RF Switch turn on/off

		'''
		if is_on or overload:
			#turn off aom/eom
			if self.__turnoff_voltage is None:
				self.__intensity_channel.constant(t,value=0)
			else:
				self.__intensity_channel.constant(t,value=self.__turnoff_voltage)
			
			#close shutter iff we have a shutter
			if self.__shutter_channel is not None:
				if self.__shutter_closetime is None:
					self.__shutter_channel.disable(t-global_shutter_closetime)
				else:
					self.__shutter_channel.disable(t-self.__shutter_closetime)

			#turn on  aom/eom
			'''
			if self.__shutter_closetime is None:
					self.__intensity_channel.constant(t+global_shutter_closetime,value=turnon_value)
				else:
					self.__intensity_channel.constant(t+self.__shutter_closetime,value=turnon_value)
			'''
			print("Not turning on AOM after shutter close!")


			#change on/off status
			if not overload:
				self.is_on = False
	
	def turnon(self, t, overload=False):
		'''
			Turns on beam if and only if off.

			## Sequence Turn On Details

			We turn off the beam with the fast control (AOM/EOM) before opening. This
			ensures that the light profile across the atoms is 1) always uniform and 2)
			well controlled in the time domain.

		'''
		if (not is_on) or overload:
			#turn off beam
			#open shutter if we have a shutter
			#turn on beam
			pass
			if not overload:
				self.is_on = True

	def constant(self, t, *args, **kwargs):
		self.turnon(t)
		self.__intensity_channel.constant(t, *args, **kwargs)
		pass

	def ramp(self, t):
		self.turnon(t)
		self.__intensity_channel.constant(t, *args, **kwargs)
		pass
	pass

class LaserBeam():
	""" 

	This is a template that holds functions for controlling the laser beam
	properties of a *single beampath*: intensity, and frequency. This class
	mostly just holds together, semantically, the two controllers for the
	intensity and frequency of our laserbeam.

	"""

	intensity	= None
	frequency	= None

	def __init__(self, intensity_control=None, frequency_control=None):
		'''
			Accepts arguments of the type `LaserIntensity`, and `LaserFrequency`.

			Each of the objects of these types define all the control methods for
			`self.intensity` and `self.frequency`.
			
			I want to particular about how my classes distinguish between the channel
			and the custom functions defined in the `LaserIntensity` and
			`LaserFrequency` classes.
		'''
		#save the controller
		self.intensity = intensity_control
		self.frequency = frequency_control
		pass


class Laser():
	'''
		This keeps track of the various laser beampaths that a single laser can be the source of. This is good for grouping our beampaths symantically.
		This is all it can do functionally.

		The really laser managment must be done in the LaserBeam class.

		E.g:

		```python
		green      	= Laser()
		green.probe	= LaserBeam()
		green.pump 	= LaserBeam() 
		```
	'''
	pass

class BlueLaser(Laser):

	#beampath names go here
	mot = None

	def __init__(self):
		''' 

		Defines the `LaserBeam`s, and `LaserIntensity` and `LaserFrequency`
		controls.

		Beampaths: (mot)
		'''

		#define the beampaths
		try:
			mot = LaserBeam(
					intensity_control	= LaserIntensity(
					                 		intensity_channel	= blue_mot_power,
					                 		shutter_channel  	= blue_mot_shutter
					                 	)
				)
		except Exception as e:
			print(f"Error creating mot beampath: {e}")
			pass


if __name__ == '__main__':
	pass