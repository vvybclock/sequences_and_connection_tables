from math import pi
import numpy as np
import scipy as sp
#Desired Usage.
# rf = RabiDrive()
# clock = RabiDrive()

# rf.rabi_pulse(rabi_area,phase,duration,amplitude_correction)

# clock.rabi_pulse(...)

class Spinor:
	'''

		This class keeps track of the *net* unitary applied to the atoms at the start of the experiment after preparation.

		The easiest way to keep track of the dark time is to use the just
		apply a unitary corresponding to free evolution during the dark
		time. During the rabi pulse, we transform to the RF rotating frame
		and then apply the stationary effective Hamiltonian. 


		interaction picture: \\(\\vec{\\psi'}  = \\hat{T} \\vec {\\psi} \\) 
		where \\(\\hat{T} = \\exp{\\frac{i}{\\hbar} \\omega_{RF}\\hat{\\sigma_z} (t - t')} \\) and
		\\(\\hat{H_0} = \\frac{\\hbar}{2} \\omega_L (\\hat{\\sigma_z}) \\) is the hamiltonian for the atoms in free space.

		The rotating frame interaction Hamiltonian is \\(\\hat{V}' = \\hat{T} \\hat{V} \\hat{T}^\\dagger\\). 
		Evidently, this outlines our transformation for Hermitian operators.


	'''

	unitary     	= None #our net unitary operator
	t_last      	= None #time since last applied unitary 
	f_larmor    	= None #atomic precession frequency
	pauli_vector	= (
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
	            			[0,	-1]
	            		] #sz
	            	)
	)

	def __init__(self, f_larmor):
		self.f_larmor = f_larmor

	def prepare_atom_unitary(self, t):
		'''
			Set the spin unitary to the identity matrix and record the spin preperation time for keeping track of phase evolution.
		'''
		self.unitary = np.identity(2, dtype=complex)
		#save the preparation time.
		self.t_last = t

	def rabi_pulse(self, t, duration, Omega,f_rf):
		'''
			Omega -- is a `list` encoded vector whose magnitude represents the field strength \\(-\\mu \\cdot \\vec{B}\\) times the duration.
		'''

		#check to see if pulses are sequential.
		if (t - self.t_last) < 0:
			raise Exception("Rabi Pulses not applied in chronological order. Cannot simulate correctly.")


		#calculate spin preccession since last unitary pulse.
		w = self.f_larmor
		U_free_space = sp.linalg.expm(
				-1j*w/2*(t-self.t_last)*self.pauli_vector[2]
			)

		#evolve atoms until just before we peform interaction.
		self.unitary = U_free_space @ self.unitary 

		#calculate effective unitary in rotating frame 
		delta = 2*pi*(f_rf - self.f_larmor)

		#calculate the interaction part of the effective hamiltonian
		interaction = np.zeros((2,2),dtype=complex)
		for i in range(len(Omega)):
			interaction += Omega[i]/2*self.pauli_vector[i]

		#calculate the interaction hamiltonian
		h0_eff = -delta/2*self.pauli_vector[2]
		u_interaction = sp.linalg.expm(
				-1j*(h0_eff*duration + interaction)
			)

		#evolve under rabi pulse
		self.unitary = u_interaction @ self.unitary

		#evolve back to lab frame.
		self.unitary = sp.linalg.expm(
				-1j*f_rf/2*duration*self.pauli_vector[2]
			) @ self.unitary


		self.t_last = t+duration
		return self.unitary


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

		#calculate intermediate quantities
		identity = np.identity(2,dtype=complex)
		norm = np.linalg.norm(Omega)
		unit_vector = Omega/norm
		
		#calculate dot_product
		dot_product = np.zeros((2,2),dtype=complex)
		for i in range(len(unit_vector)):
			dot_product += unit_vector[i]* self.pauli_vector[i]

		#return unitary
		return identity*np.cos(norm) + 1j*dot_product*np.sin(norm)


class RfRabiDrive:
	'''

	'''

	rabi_channel    	= None
	larmor_frequency	= None
	atom_unitary    	= None

	def __init__(self, rabi_channel, larmor_frequency):
		'''
			rabi_channel - Specify the analog channel for controlling the Rabi Field.
			larmor_frequency - Specify the precession frequency in Hertz.
		'''
		self.rabi_channel    	= rabi_channel
		self.larmor_frequency	= larmor_frequency
		self.atom_unitary    	= Spinor(f_larmor=larmor_frequency)

	def resonant_rabi_pulse(self,t,rabi_area,phase,duration,samplerate,amplitude_correction=0):
		'''
			rabi_area           	- the rotated angle of the spin state in radians.
			phase               	- the phase of the Rabi Drive relative to the Local Oscillator (LO) or Oscillation Phase of the atoms.
			duration            	- how long should the pulse be applied for.
			amplitude_correction	- fractional correction one should apply to the amplitude to accomodate for digitization errors.
		'''

		sine_area_correction = 1
		angfreq = 2*pi*self.larmor_frequency

		#perform theoretical rabi pulse
		self.atom_unitary.rabi_pulse(
			t       	= t,
			duration	= duration,
			Omega   	= [rabi_area*np.cos(phase), rabi_area*np.sin(phase)],
			f_rf    	= self.larmor_frequency
		)

		#perform actual rabi pulse
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
