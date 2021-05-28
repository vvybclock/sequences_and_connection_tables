
#Desired Usage.
rf = RabiDrive()
clock = RabiDrive()

rf.rabi_pulse(rabi_area,phase,duration,amplitude_correction)

clock.rabi_pulse(...)

def RfRabiDrive():
	'''

	'''

	rabi_channel	= None
	larmor_frequency = None

	def __init__(self, rabi_channel, larmor_frequency):
		'''
			rabi_channel - Specify the analog channel for controlling the Rabi Field.
			larmor_frequency - Specify the precession frequency in Hertz.
		'''
		self.rabi_channel    	= rabi_channel
		self.larmor_frequency	= larmor_frequency

	def rabi_pulse(self,t,rabi_area,phase,duration,amplitude_correction):
		'''
			rabi_area           	- the rotated angle of the spin state in radians.
			phase               	- the phase of the Rabi Drive relative to the Local Oscillator (LO) or Oscillation Phase of the atoms.
			duration            	- how long should the pulse be applied for.
			amplitude_correction	- fractional correction one should apply to the amplitude to accomodate for digitization errors.
		'''

		


		pass
