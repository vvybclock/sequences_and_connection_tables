import numpy as np
from scipy.optimize import leastsq

def lorentzian(x, x0, a, gamma, offset):
	'''
	x    	= position,
	x0   	= peak center,
	a    	= amplitude of peak,
	gamma	= Half width half max

	'''
	return a*gamma**2/(gamma**2 + (x-x0)**2) + offset

def residuals_of_lorentzian(params, x_data, y_data):
	''' Calculates the residuals of the fit.'''
	diff = [lorentzian(x, params[0], params[1], params[2], params[3]) - y for x,y in zip(x_data,y_data)]
	return diff

def fit_single_cavity_peak(data,start,end,bin_interval):
	''' Fits a single_cavity_peak using least squares. Assumes unbinned photon
	arrival times for data.

	Returns best_guess and cov_best_guess'''

	#bin the data
	(hist, bin_edges) = np.histogram(
		data,
		bins=np.arange(start,end, bin_interval)
	)

	#estimate initial parameters
	amplitude = np.amax(hist)
	x0_index = np.argmax(hist)
	x0 = bin_edges[x0_index]
	locations_greater_than_half_max = np.where(hist > amplitude/2)[0]
	right_time = bin_edges[locations_greater_than_half_max[-1]]
	left_time = bin_edges[locations_greater_than_half_max[0]]
	gamma = (right_time-left_time + bin_interval)/2  #in case the peak is one bin wide.
	offset = 0

	#format the parameters
	init_guess = [x0, amplitude, gamma, offset]

	#fit
	(best_guess, cov_best_guess) = leastsq(residuals_of_lorentzian, init_guess, args=(bin_edges[:-1]+bin_interval/2,hist))


	return best_guess, cov_best_guess

def rabi_splitting_transmission(f, fatom, fcavity, Neta, gamma, kappa):
	'''
	Returns the transmission through the cavity-atom system.


	f 		= probe frequency (EOM)
	fatom	= atomic frequency (in terms of probe frequency)
	fcavity = empty cavity frequency ("")
	Neta	= total cooperativity (single atom cooperativity eta times the total number of atoms in the up level)
	gamma  	= atomic transition linewidth (184kHz)
	kappa	= empty cavity linewidth (~500kHz)

	'''
	# define some local variables to simplify the writing of the formula

	xa = 2*(f-fatom)/gamma
	xc = 2*(f-fcavity)/kappa

	return ((1+Neta/(1+xa**2))**2+(xc-Neta*xa/(1+xa**2))**2)**(-1)


def logLikelihood_rabi_splitting_transmission(data, fatom, fcavity, Neta):
	'''
	calculates the loglikelihood of a set of data as a function of the other parameters.

	data  			= list of frequencies of detected photons. They are obtained from photons arrival times.
	
	fatom	= atomic frequency (in terms of probe frequency)
	fcavity = empty cavity frequency ("")
	Neta	= total cooperativity (single atom cooperativity eta times the total number of atoms in the up level)

	'''

	# define some fixed value
	kappa_loc = 0.510
	gamma_loc = 0.184
	rabi_splitting_transmission_Integral = 0.59 # for Neta>>1 the Rabi splitting integral formula converges to this value

	loglikelihood=0
	for i in data:
		loglikelihood += np.log(rabi_splitting_transmission(i,fatom,fcavity,Neta,gamma_loc,kappa_loc))

	return loglikelihood/len(data) # loglikelihood normalized to the atom number


	

def fit_rabi_splitting_transmission_MLE(data, params, params_range):

	'''
	Fits the Rabi Splitting in a scan experiment with Maximum Likelihood Estimator (MLE). returns the Neta
	
	data  			= list of frequencies of detected photons. They are obtained from photons arrival times.
	params 			= list of parameters. [fatom, fcavity, Neta]
	params_range 	= fit parameters allowed ranges 

	frequency unit: MHz

	Here we find the parameters for which we maximize the loglikelihood 
	'''
	# guess initial parameters, if not defined/fixed before like Neta
	# TBD