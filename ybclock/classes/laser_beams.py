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

	def turnoff(self, t):
		'''
			Turns off beam if and only if on.
		'''
		if is_on:
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
			self.is_on = False
	
	def turnon(self, t):
		'''
			Turns on beam if and only if off.
		'''
		self.is_on = True

	def constant(self, t):
		self.turnon(t)
		self.__intensity_channel.constant(args)
		pass

	def ramp(self, t):
		self.turnon(t)
		pass
	pass

class LaserBeam():
	"""This is a template that holds functions for controlling the laser beam properties of a *single beampath*: intensity, and frequency."""

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

	mot = None
	beampaths = []
	def __init__(self):
		''' Defines the `LaserBeam`s, and `LaserIntensity` and `LaserFrequency` controls.

		Beampaths: (mot)
		'''
		print("Constructing blue laser...")

		print("\tblue.mot...")
		#define the beampaths
		try:
			mot = LaserBeam(
					intensity_control	= LaserIntensity(
					                 		intensity_channel	= blue_mot_power,
					                 		shutter_channel  	= blue_mot_shutter
					                 	)
				)
			self.beampaths.append('mot')
		except Exception as e:
			print(f"Error creating mot beampath: {e}")
			pass

		print("\tDone!")

	def __str__(self):
		string = f'Blue Laser has the beampaths {self.beampaths}'

		return string
	pass
	pass
if __name__ == '__main__':
	pass