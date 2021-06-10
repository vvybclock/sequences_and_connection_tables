from math import pi
import numpy as np
#Desired Usage.
# rf = RabiDrive()
# clock = RabiDrive()

# rf.rabi_pulse(rabi_area,phase,duration,amplitude_correction)

# clock.rabi_pulse(...)

class Spinor:
	'''

		This class keeps track of the *net* unitary applied to the atoms at the start of the experiment after preparation.

		The easiest way to keep track of the dark time is to use the
		interaction picture: \\(\\vec{\\psi'}  = \\hat{T} \\vec {\\psi} \\) 
		where \\(\\hat{T} = \\exp{\\frac{i}{\\hbar} \\hat{H_0} t} \\) and
		\\(\\hat{H_0} = \\frac{\\hbar}{2} \\omega_0 (\\hat{\\sigma_z} + 1) \\) is the hamiltonian for the atoms in free space.

		The rotating frame Hamiltonian is \\(\\hat{V}' = \\hat{T} \\hat{V} \\hat{T}^\\dagger\\). 
		Evidently, this outlines our transformation for Hermitian operators.


	'''

	unitary     	= None #our net unitary operator
	t_last      	= None #time since last applied unitary 
	w_larmor    	= None #atomic precession frequency
	pauli_vector	= [
	            	np.matrix(
	            		[
	            			[0,	1],
	            			[1,	0]
	            		] #sx
	            	),
	            	np.matrix(
	            		[
	            			[0, 	-1j],
	            			[1j,	0]
	            		] #sy
	            	),
	            	np.matrix(
	            		[
	            			[1,	0],
	            			[0,	1]
	            		] #sz
	            	)
	]

	def __init__(self):
		pass

	def prepare_atom_unitary(self, t):
		'''
			Set the spin unitary to the identity matrix and record the spin preperation time for keeping track of phase evolution.
		'''
		self.unitary = np.identity(2, dtype=complex)
		#save the preparation time.
		self.t_last = t

	# def T(self, t):
	#	'''
	#		Returns the unitary that transforms from the lab frame to the
	#		rotating frame at the larmor frequency \\(\\omega_0\\).
	#	'''
	#	w = self.w_larmor
	#	T = np.matrix(
	#		[
	#			[np.exp(1j*w*t),	0],
	#			[0,             	1],
	#		]
	#	)

	#	return T

	def U_V(self, Omega):
		'''
			Calculates the unitary interaction in the rotating frame of the
			magnetic field (where the Hamiltonian is time independent). Assumes `Omega` is a list of at most 3 real elements.
			See [the formula]
			(https://en.wikipedia.org/wiki/Pauli_matrices#Exponential_of_a_Pauli_vector)
			for the exponential of a pauli matrix.

		'''
		if len(Omega) > 3:
			raise Exception("Omega should be a list of at most 3 numbers.")

		identity = np.identity(2,dtype=complex)
		norm = np.linalg.norm(Omega)
		unit_vector = Omega/norm
		
		return identity*np.cos(norm) + 1j*np.dot(unit_vector, self.pauli_vector)*np.sin(norm)



	# def to_rotating_frame(self, t, M):
	#	Mp = M
	#	return Mp
	# def to_lab_frame():
	#	return M
	# pass
class RfRabiDrive:
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

	def rabi_pulse(self,t,rabi_area,phase,duration,samplerate,amplitude_correction=0):
		'''
			rabi_area           	- the rotated angle of the spin state in radians.
			phase               	- the phase of the Rabi Drive relative to the Local Oscillator (LO) or Oscillation Phase of the atoms.
			duration            	- how long should the pulse be applied for.
			amplitude_correction	- fractional correction one should apply to the amplitude to accomodate for digitization errors.
		'''

		sine_area_correction = 2
		angfreq = 2*pi*self.larmor_frequency

		self.rabi_channel.sine(
			t         	= t,
			duration  	= duration,
			amplitude 	= (1 + amplitude_correction)* rabi_area/duration * sine_area_correction,
			angfreq   	= angfreq,
			phase     	= phase + angfreq*t,
			dc_offset 	= 0,
			samplerate	= samplerate
		)


		pass
