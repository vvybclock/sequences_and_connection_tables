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

class LaserFrequency(AnalogQuantity):
	'''

		You actually don't need a special class for LaserFrequency. It's just of
		type AnalogQuantity, so just pass the frequency channel to
		`LaserBeam(frequency_control)`.
	
	'''
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

			[x] turnoff function
			[x] turnon function
			[x] constant
			[x] ramp

	'''
	__intensity_channel = None
	__shutter_channel  	= None
	__turnoff_voltage  	= None
	__shutter_closetime	= None
	__rf_switch_channel	= None

	is_on = False

	def __init__(self, intensity_channel=None, shutter_channel=None, turnoff_voltage=None,shutter_closetime=None,rf_switch_channel=None):
		self.__intensity_channel	= intensity_channel
		self.__turnoff_voltage  	= turnoff_voltage
		self.__shutter_channel  	= shutter_channel
		self.__shutter_closetime	= shutter_closetime
		self.__rf_switch_channel	= rf_switch_channel

	def turnoff(self, t, warmup_value, overload=False):
		'''
			Turns off beam if and only if on unless `overload == True` then always turn off.
			`warmup_value` is what value you want for the aom while the shutter is closed.

			#To Do
				[x]	Set up AOM/EOM turn on/off
				[x]	Set up Shutter turn on/off
				[x]	Set up RF Switch turn on/off

		'''

		#determine shutter close time
		if self.__shutter_closetime is None:
			shutter_closetime =	global_shutter_closetime
		else:
			shutter_closetime = self.__shutter_closetime
		#determine aom/eom turnoff voltage
		if self.__turnoff_voltage is None:
			turnoff_voltage = 0
		else:
			turnoff_voltage = self.__turnoff_voltage





		if self.is_on or overload:
			#turn off aom/eom
			if self.__rf_switch_channel is None:
				self.__intensity_channel.constant(t,value=turnoff_voltage)
			else:
				self.__rf_switch_channel.disable(t)
			
			#close shutter iff we have a shutter
			if self.__shutter_channel is not None:
				self.__shutter_channel.disable(t - shutter_closetime)

			#turn on  aom/eom
			if self.__rf_switch_channel is None:
				self.__intensity_channel.constant(t + shutter_closetime,value=warmup_value)
			else:
				self.__rf_switch_channel.enable(t + shutter_closetime)

			#change on/off status
			if not overload:
				self.is_on = False
	
	def turnon(self, t, *args, overload=False, **kwargs):
		'''
			Turns on beam if and only if off. `*args`, `**kwargs` get passed to the turn on value for the laser.

			## Sequence Turn On Details

			We turn off the beam with the fast control (AOM/EOM) before opening. This
			ensures that the light profile across the atoms is 1) always uniform and 2)
			well controlled in the time domain.

			#To Do
				[x]	Set up AOM/EOM turn on/off
				[x]	Set up Shutter turn on/off
				[x]	Set up RF Switch turn on/off
		'''

		#determine shutter close time
		if self.__shutter_closetime is None:
			shutter_closetime =	global_shutter_closetime
		else:
			shutter_closetime = self.__shutter_closetime
		#determine aom/eom turnoff voltage
		if self.__turnoff_voltage is None:
			turnoff_voltage = 0
		else:
			turnoff_voltage = self.__turnoff_voltage




		if (not self.is_on) or overload:
			#turn off beam
			if self.__rf_switch_channel is not None:
				#just turn off the rf switch
				self.__rf_switch_channel.disable(t - shutter_closetime)
			else:
				#turn off the aom/eom
				self.__intensity_channel.constant(t,value=turnoff_voltage)

			#open shutter if we have a shutter
			if self.__shutter_channel is not None:
				self.__shutter_channel.enable(t - shutter_closetime)

			#turn on beam
			if self.__rf_switch_channel is not None:
				#just turn on the rf switch
				self.__rf_switch_channel.enable(t)
			else:
				#turn on the aom/eom if we've been told a value.
				if args or kwargs:
					self.__intensity_channel.constant(t, *args, **kwargs)
			if not overload:
				self.is_on = True

	def constant(self, t, *args, **kwargs):
		#save args, and kwargs as they get modified after self.turnon(t) call for some reason
		_args = args
		_kwargs = kwargs
		self.turnon(t)
		self.__intensity_channel.constant(t, *_args, **_kwargs)

	def ramp(self, t, *args, **kwargs):
		#save args, and kwargs as they get modified after self.turnon(t) call for some reason
		_args = args
		_kwargs = kwargs
		self.turnon(t)
		self.__intensity_channel.ramp(t, *_args, **_kwargs)


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
			self.mot = LaserBeam(
					intensity_control	= LaserIntensity(
					                 		intensity_channel	= blue_mot_power,
					                 		shutter_channel  	= blue_mot_shutter
					                 	),
					frequency_control	= None
				)
		except Exception as e:
			print(f"Error creating mot beampath: {e}")
			pass

class GreenLaser(Laser):

	#beampath names go here
	probe	= None
	pump 	= None
	mot  	= None
	cooling = None

	#define the beampaths
	try:
		self.mot = LaserBeam(
				intensity_control = LaserIntensity(
						intensity_channel = green_mot_power,
						rf_switch_channel = green_mot_power_switch,
						shutter_channel = green_mot_shutter
					),
				frequency_control = None,
			)

		self.probe = LaserBeam(
				intensity_control = None,
				frequency_control = None,
			)

		self.pump = LaserBeam(
				intensity_control = None,
				frequency_control = None,
			)

		self.cooling = LaserBeam(
				intensity_control = None,
				frequency_control = None,
			)
	except Exception as e:
		pass
	pass

if __name__ == '__main__':
	pass