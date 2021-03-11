import numpy as np
from scipy.optimize import minimize, leastsq
import random

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
	
	dkcounts= dark-counts per scan This should be implemented.

	'''
	# define some local variables to simplify the writing of the formula

	xa = 2*(f-fatom)/gamma
	xc = 2*(f-fcavity)/kappa

	return ((1+Neta/(1+xa**2))**2+(xc-Neta*xa/(1+xa**2))**2)**(-1)#+dkcounts


def logLikelihood_rabi_splitting_transmission(params, data):
	'''
	calculates the -loglikelihood of a set of data as a function of the other parameters. 
	Minus LL because we maximze the LL using minimize().

	data  			= list of frequencies of detected photons. They are obtained from photons arrival times.
	params 	       	= (fatom, fcavity, Neta)
	
	'''

	# define some fixed value
	kappa_loc = 0.510
	gamma_loc = 0.184
	rabi_splitting_transmission_Integral = 0.59 # for Neta>>1 the Rabi splitting integral formula converges to this value

	loglikelihood=0
	for i in data:
		loglikelihood += np.log(rabi_splitting_transmission(i,params[0],params[1],params[2],gamma_loc,kappa_loc))

	return -loglikelihood/len(data) # loglikelihood normalized to the atom number


def fit_rabi_splitting_transmission_MLE(data, bnds=((0, 25),(0,25),(0, 2000)), param_error = 'off', bs_repetition = 25):

	'''
	Fits the Rabi Splitting in a scan experiment with Maximum Likelihood Estimator (MLE). returns the Neta
	
	data  			= list of frequencies of detected photons. They are obtained from photons arrival times.
	bnds 			= list of bounds/ranges for parameters (fatoms, fcavity, Neta)

	param_error		= if turned on, the function estimates parameters error by bootstrapping the data
	bs_repetition	= specify how many bootstrapped datasample are we analyzing to perform statistics on fit

	frequency unit: MHz

	Here we find the parameters for which we maximize the loglikelihood.
	'''
	# define some fixed value
	kappa_loc = 0.510
	gamma_loc = 0.184

	# extract some parameter
	Neta_range		= bnds[2]
	fatoms_range	= bnds[0]
	fcavity_range	= bnds[1]

	# guess initial parameters, to fix the parameters, set the relative params_range to 0

	fcavity_guess = np.mean(data)
	fatoms_guess  =	fcavity_guess
	Neta_guess = 4*np.var(data)/(gamma_loc * kappa_loc)

	## check if guesses are in the set ranges, if not redefine the guesses
	if fcavity_guess < fcavity_range[0] or fcavity_guess > fcavity_range[1]:
		fcavity_guess = np.mean(fcavity_range)

	if fatoms_guess < fatoms_range[0] or fatoms_guess > fatoms_range[1]:
		fatoms_guess = np.mean(fatoms_range)

	if Neta_guess < Neta_range[0] or Neta_guess > Neta_range[1]:
		Neta_guess = np.mean(Neta_range)

	#format the parameters
	init_guess = (fatoms_guess, fcavity_guess, Neta_guess)

	#fit
	if param_error == 'on':
		# bootstrap the data and perform MLE fit for all databs. Then do statistics of bootstrapped results
		# This method may be slow. It can be improved in speed by implementing Hessian matrix calculations, however it may be tricky becasue of bounds.
		bs_list=[]
		for i in range(bs_repetition):
			data_bs = random.choices(data,k=len(data))
			out=minimize(logLikelihood_rabi_splitting_transmission, init_guess,args=data_bs, bounds=bnds)
			bs_list.append(out.x)
		best_param = np.mean(np.transpose(bs_list),1)
		cov = np.sqrt(np.transpose(bs_list)) # Covariance matrix
		return (best_param, cov) 
	elif param_error == 'off':
		out = minimize(logLikelihood_rabi_splitting_transmission, init_guess,args=data, bounds=bnds)
		best_param = out.x
		return (best_param,)
	else :
		return('incorrect param_error specification')

	
