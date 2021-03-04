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

