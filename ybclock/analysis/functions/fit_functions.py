import numpy as np
from scipy.optimize import minimize, least_squares, differential_evolution, leastsq
import random
from lyse import Run

def square(list):
    return [i ** 2 for i in list]

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

def fit_single_cavity_peak(data,start,end,bin_interval=0.2):
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
	kappa = (right_time-left_time + bin_interval)/2  #in case the peak is one bin wide.
	offset = 0

	bin_centers = bin_edges[:-1]+bin_interval/2
	#format the parameters
	init_guess = [x0, amplitude, kappa, offset]

	#fit
	(best_guess, cov_best_guess) = leastsq(residuals_of_lorentzian, init_guess, args=(bin_centers,hist))
	y_model = [lorentzian(x, best_guess[0], best_guess[1], best_guess[2], best_guess[3],) for x in bin_centers]
	y = hist
	chi_sq = chi_2(y, y_model)


	return {"fcavity" : best_guess[0], "kappa" : best_guess[2], "dark_counts" : best_guess[3],"amplitude": best_guess[1], "covariance matrix":cov_best_guess, "chi_square": chi_sq}


def rabi_splitting_transmission(f, fatom, fcavity, Neta, gamma, kappa, dkcounts = 0):
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

	return ((1+Neta/(1+xa**2))**2+(xc-Neta*xa/(1+xa**2))**2)**(-1)+dkcounts

def residuals_of_rabi_splitting_transmission(params, x_data, y_data):
	'''
	Returns the residuals of rabi_splitting fit
	'''
	#params[6] = amplitude;
	diff = [params[6]*rabi_splitting_transmission(x, params[0], params[1], params[2], params[3], params[4], params[5]) - (y) for x,y in zip(x_data,y_data)]
	return diff

def chi_2(y_data, y_model):
	'''
	Calculates the normalized chi^2 of a fitted model as: , where N is the total amount of data dtectd.

	'''

	try:
		total_chi_2 = [((y-ye)**2)/(y+1) for y,ye in zip(y_data,y_model)]
		return ((len(total_chi_2))**(-1/2))*sum(total_chi_2)
	except Exception as e:
		print("Failed calculating chi_square. Error:",e)

def fit_rabi_splitting_transmission(data,bnds={"fatom_range":(0,50), "fcavity_range":(0,50), "Neta_range":(0,20000)}, bin_interval=0.2, path=None):

	''' Fits a rabi_splitting_data using least squares. Assumes unbinned photon
	arrival times for data.

	Returns best_guess and cov_best_guess
	# To dos

	[] Try a parameter grid scan to find the region of global minima

	'''


	# get globals

	try:
		run = Run(path)
		data_globals = run.get_globals() # path should be called inside the function. 
		print("Globals Imported Successfully during lstsq fit.")
	except:
		print("Failed Importing Globals during lstsq fit!")

	
		# define some fixed value. 
	# Try to get values from globals. If globals is missing, it will use some preset value.
	try:
		kappa_loc = data_globals['exp_cavity_kappa']*0.001 # 0.001 becasue in globals this is specified in kHz
	except:
		kappa_loc = 0.530
		print("Failed getting kappa from globals.")
	try:
		gamma_loc = data_globals['green_gamma']*0.001  # 0.001 becasue in globals this is specified in kHz
	except:
		gamma_loc = 0.184
	try:
		dark_counts = data_globals['dark_counts']*data_globals['empty_cavity_sweep_duration']*0.001
	except:
		dark_counts = 120*0.03

	# extract some parameter
	Neta_range   	= bnds["Neta_range"]
	fatom_range 	= bnds["fatom_range"]
	fcavity_range	= bnds["fcavity_range"]


	#bin the data
	(hist, bin_edges) = np.histogram(
		data,
		bins=np.arange(data[0]-1,data[-1]+1, bin_interval)
	)
	

	#estimate initial parameters

	fcavity_guess = np.mean(data)
	Neta_guess = 4.*np.var(data)/(gamma_loc * kappa_loc)
	# guess initial parameters, to fix the parameters, set the relative params_range to 0
	## check if guesses are in the set ranges, if not redefine the guesses
	try:
		if fcavity_guess < fcavity_range[0] or fcavity_guess > fcavity_range[1]:
			fcavity_guess = np.mean(fcavity_range)
	except:
		pass
	print("Initial Neta_guess : ",Neta_guess)
	fatoms_guess =	fcavity_guess
	try:
		if fatoms_guess < fatom_range[0] or fatoms_guess > fatom_range[1]:
			fatoms_guess = np.mean(fatom_range)
	except Exception as e:
		print("fatoms_guess failed. Error:", e)
	try:
		if Neta_guess < Neta_range[0] or Neta_guess > Neta_range[1]:
			Neta_guess = np.mean(Neta_range)
	except:
		pass

	bin_centers=bin_edges[:-1]+bin_interval/2;
	if Neta_guess > 50:
		amplitude = sum(hist)/0.6*bin_interval
		grid_scan=1e9
		for Neta_grid in np.arange(Neta_guess*0.4, Neta_guess*1.4+1, Neta_guess/10):
			for fcav_grid in np.arange(fcavity_guess, fcavity_guess+4, .5):
				for fatoms_grid in np.arange(fatoms_guess-2, fatoms_guess+2, .5):
					try:
						init_guess_loc = (fatoms_grid,fcav_grid, Neta_grid, gamma_loc, kappa_loc, dark_counts, amplitude)
						residuals_tot_local=sum(square(residuals_of_rabi_splitting_transmission(init_guess_loc, bin_centers,hist)))/len(bin_centers)
						if grid_scan>residuals_tot_local:
							print("Temporary Min of residuals:", residuals_tot_local)
							grid_scan = residuals_tot_local
							init_guess = init_guess_loc
					except Exception as e:
						init_guess = (fatoms_guess, fcavity_guess, Neta_guess, gamma_loc, kappa_loc, dark_counts, amplitude)
						print("----- Fucked up getting init_guess from grid. Error :",e)
		bnds_list = ((init_guess[0]-.5, init_guess[1]-.5, init_guess[2]*(1-1/10), gamma_loc-0.004, kappa_loc-0.05, 0,.25*amplitude),(init_guess[0]+.5, init_guess[1]+.5, init_guess[2]*(1+1/10), gamma_loc+0.001, kappa_loc+0.2, 10*dark_counts,4*amplitude))
	else:
		amplitude = sum(hist)/0.85*bin_interval
		init_guess = (fatoms_guess, fcavity_guess, Neta_guess, gamma_loc, kappa_loc, dark_counts, amplitude)
		bnds_list = ((fatom_range[0], fcavity_range[0], Neta_range[0], gamma_loc-0.004, kappa_loc-0.05, 0,.25*amplitude),(fatom_range[1], fcavity_range[1], Neta_range[1], gamma_loc+0.001, kappa_loc+0.2, 10*dark_counts,4*amplitude))

	#fit

	for s in range(len(init_guess)):
		if (init_guess[s]-bnds_list[0][s])<0:
			print("Initial value failed Element : ", s)
		if (init_guess[s]-bnds_list[1][s])>0:
			print("Initial value failed. Element : ", s)
	print("fcavity_guess: ", init_guess[1])
	print("fcavity_range: ", fcavity_range)

	out = least_squares(
		residuals_of_rabi_splitting_transmission, 
		init_guess, 
		args=(bin_centers,hist), 
		bounds =bnds_list
		)
	best_param=out.x
	#best_param=init_guess
	jac_best_guess=out.jac
	#jac_best_guess=1
	y_model = [best_param[6]*rabi_splitting_transmission(x, best_param[0], best_param[1], best_param[2], best_param[3], best_param[4], best_param[5]) for x in bin_centers]
	y = hist
	chi_sq = chi_2(y, y_model)


	return {"fatom": best_param[0], "fcavity" : best_param[1], "Neta": best_param[2], "gamma" : best_param[3], "kappa" : best_param[4], "dark_counts" : dark_counts,"amplitude": best_param[6], "jacobian":jac_best_guess, "chi_square": chi_sq}

def logLikelihood_rabi_splitting_transmission(params, data,):
	'''
	calculates the -loglikelihood of a set of data as a function of the other parameters. 
	Minus LL because we maximze the LL using minimize().

	data  			= list of frequencies of detected photons. They are obtained from photons arrival times.
	params		= (fatom, fcavity, Neta, gamma, kappa, dkcounts)
	
	'''
	rabi_splitting_transmission_Integral = 0.59 # for Neta>>1 the Rabi splitting integral formula converges to this value

	#loglikelihood=0
	#for i in data:
	#	loglikelihood += np.log(rabi_splitting_transmission(i,params[0],params[1],params[2],params[3],params[4],params[5]))

	#return -loglikelihood/len(data) # loglikelihood normalized to the atom number

	i = data

	LL_perpoint = - np.log(rabi_splitting_transmission(i,params[0],params[1],params[2],params[3],params[4],params[5]))
	
	return sum(LL_perpoint)/len(data)


def fit_rabi_splitting_transmission_MLE(data, bnds={"fatom_range":(0,25), "fcavity_range":(0,25), "Neta_range":(0,2000)}, param_error = 'off', bs_repetition = 25, path=None):

	'''
	Fits the Rabi Splitting in a scan experiment with Maximum Likelihood Estimator (MLE). Returns the Neta.
	
	output = fit_rabi_splitting_transmission_MLE(data,bnds,param_error,bs_repetition)


	data  			: list of frequencies of detected photons. They are obtained from photons arrival times.
	bnds 			: dictionary specifying parameters's ranges (fatoms, fcavity, Neta)

	param_error		: if turned on, the function estimates parameters error by bootstrapping the data
	bs_repetition	: specify how many bootstrapped datasample are we analyzing to perform statistics on fit

	output			: tuple with a MLE result as first element; it is a 3 elements ndarray reporting (fatoms, fcavity, Neta). 
					  When param_error='on' the output tuple contains the covariance matrix of the fitted parameters as second element. The second element is absent if param_error='off'.


	frequency unit: MHz

	We first perform a `least_square fit` to the data binned into histograms. We use this parameter guess as a starting point for `maximize` the loglikelihood function.


	## Why we used bootstrapping method 
	
	The presence of bounds in fit parameters significantly increments the complexity in estimating uncertainties and correlations. This is due to the fact that it bacomes hard (if not impossible) to correctly calculate the Hessian matrix in the presence of bounds.
	Therefore, to estimate the covariance matrix of the fitted parameters, we bootstrap the data (bootsrapping method). This allows us to estimate fit parameters and the experimental covariance matrix without computing Hessians or Jacobian.

	
	
	### What is bootstrapping?
	
	Bootstrapping is a method widely used in statistics. Bootstrapping is any test or metric that uses random sampling with replacement (e.g. mimicking the sampling process). This technique allows estimation of the sampling distribution of almost any statistic using random sampling methods.

	The idea is to create a set of n "measurements" sampled from data with the same statistical properties as the data itself. We then perform the MLE fit to each of these n resampled data. Finally, we can extract mean values for the fit parameters and the experimental covariance matrix.

	For deatails, see : https://en.wikipedia.org/wiki/Bootstrapping_%28statistics%29

	'''
	try:
		run = Run(path)
		data_globals = run.get_globals() # path should be called inside the function.
		print("Globals imported successfully during MLE Fit") 
	except:
		print("Failed Importing Globals during MLE fit ")

	# define some fixed value. 
	# Try to get values from globals. If globals is missing, it will use some preset value.
	try:
		kappa_loc = data_globals['exp_cavity_kappa']*0.001 # 0.001 becasue in globals this is specified in kHz
	except:
		kappa_loc = 0.510
		print("Failed getting kappa from globals.")
	try:
		gamma_loc = data_globals['green_gamma']*0.001  # 0.001 becasue in globals this is specified in kHz
	except:
		gamma_loc = 0.180
	try:
		dark_counts = data_globals['dark_counts']*data_globals['empty_cavity_sweep_duration']*0.001
	except:
		dark_counts = 120*0.03 

	#remove data from wings very far away. This photons are either dark counts or carry very low Fisher information.
	data =  data[round(len(data)*0.05) : round(len(data)*0.95)]

	# guess initial parameters, to fix the parameters, set the relative params_range to 0

	preFit = fit_rabi_splitting_transmission(data,bnds=bnds, bin_interval=0.2, path=path)
	init_guess = (preFit["fatom"], preFit["fcavity"], preFit["Neta"], preFit["gamma"], preFit["kappa"], preFit["dark_counts"]);

	fatoms_range 	= (preFit["fatom"]-0.3, preFit["fatom"]+0.3)
	fcavity_range 	= (preFit["fcavity"]-0.3, preFit["fcavity"]+0.3)
	# Calculate some amount of freedom in Neta range. It should depend on Neta and total number of photons. From theory, with an eta~ 1, e have 1 SQL per ~ 20 photons. We use this as weight factor.
	# This can be further optimized and studied.
	try:
		range_factor = 0.05 + 1/sqrt(preFit["Neta"])*20/(len(data)-preFit['dark_counts'])
	except:
		range_factor = 1
	Neta_range		= (preFit["Neta"]*(1-range_factor), preFit["Neta"]*(1+range_factor))

	bnds_list = (fatoms_range, fcavity_range, Neta_range, (gamma_loc-0.001, gamma_loc), (kappa_loc-0.05, kappa_loc+.1), (0*dark_counts, 10*dark_counts)) # this is a tuple defining boundaries. Contants defined in globals need to be treated as a parameter with near dimensionless range.


	#fit
	if param_error == 'on':
		# bootstrap the data and perform MLE fit for all databs. Then do statistics of bootstrapped results
		# This method may be slow. It can be improved in speed by implementing Hessian matrix calculations, however it may be tricky because of bounds.
		bs_list=[]
		for i in np.arange(bs_repetition):
			data_bs = random.choices(data,k=len(data))
			out=minimize(logLikelihood_rabi_splitting_transmission, init_guess,args=data_bs, bounds=bnds_list, tol=0.001)
			bs_list.append(out.x)
		fit_result= np.mean(np.transpose(bs_list),1)
		cov = np.sqrt(np.transpose(bs_list)) # Covariance matrix
		# Get the chi_2
		#bin the data
		bin_interval=0.2
		(hist, bin_edges) = np.histogram(
		data,
		bins=np.arange(data[0]-1,data[-1]+1, bin_interval)
		)
		
		bin_centers=bin_edges[:-1]+bin_interval/2
		amplitude = sum(hist)*bin_interval
		y_model = [rabi_splitting_transmission(x, fit_result[0], fit_result[1], fit_result[2], fit_result[3], fit_result[4], fit_result[5]) for x in bin_centers]
		y_model = y_model/sum(y_model)*sum(hist);
		y = hist
		chi_sq = chi_2(y, y_model)

		best_param = {"fatom" : fit_result[0], "fcavity" : fit_result[1], "Neta": fit_result[2],  "gamma" : fit_result[3], "kappa" : fit_result[4], "dark_counts" : fit_result[5],'covariance' : cov,"chi_square" : chi_sq} # gamma and kappa are not fit parameters!
		return best_param
	elif param_error == 'off':
		out = minimize(logLikelihood_rabi_splitting_transmission, init_guess,args=data,bounds=bnds_list, tol=0.001)
		best_param = out.x
		# Get the chi_2
		#bin the data
		bin_interval=0.2
		(hist, bin_edges) = np.histogram(
		data,
		bins=np.arange(data[0]-1,data[-1]+1, bin_interval)
		)
		bin_centers=bin_edges[:-1]+bin_interval/2
		y_model = [rabi_splitting_transmission(x, best_param[0], best_param[1], best_param[2], best_param[3], best_param[4], best_param[5]) for x in bin_centers]
		y_model = y_model/sum(y_model)*sum(hist);
		
		y = hist
		chi_sq = chi_2(y, y_model)

		return {"fatom": best_param[0], "fcavity" : best_param[1], "Neta": best_param[2], "gamma" : best_param[3], "kappa" : best_param[4], "dark_counts" : best_param[5],"chi_square" : chi_sq}
	else :
		return('incorrect param_error specification')

def test_fit_rabi_splitting_transmission_MLE(data, bnds={"fatom_range":(0,50), "fcavity_range":(0,50), "Neta_range":(0,20000)}, param_error = 'off', bs_repetition = 25, path=None):

	'''
	I am testing here a fit that does not involve least_square method. Just a coarse grid scan, and then MLE method
	'''
	try:
		run = Run(path)
		data_globals = run.get_globals() # path should be called inside the function.
		print("Globals imported successfully during MLE Fit") 
	except:
		print("Failed Importing Globals during MLE fit ")

	# define some fixed value. 
	# Try to get values from globals. If globals is missing, it will use some preset value.
	try:
		kappa_loc = data_globals['exp_cavity_kappa']*0.001 # 0.001 becasue in globals this is specified in kHz
	except:
		kappa_loc = 0.530
		print("Failed getting kappa from globals.")
	try:
		gamma_loc = data_globals['green_gamma']*0.001  # 0.001 becasue in globals this is specified in kHz
	except:
		gamma_loc = 0.180
	try:
		dark_counts = data_globals['dark_counts']*data_globals['empty_cavity_sweep_duration']*0.001
	except:
		dark_counts = 120*0.03 

	# extract some parameter
	Neta_range   	= bnds["Neta_range"]
	fatom_range 	= bnds["fatom_range"]
	fcavity_range	= bnds["fcavity_range"]
	#remove data from wings very far away. This photons are either dark counts or carry very low Fisher information.
	data =  data[round(len(data)*0.05) : round(len(data)*0.95)]

	# guess initial parameters, to fix the parameters, set the relative params_range to 0
	#estimate initial parameters

	fcavity_guess = np.mean(data)
	Neta_guess = 4.*np.var(data)/(gamma_loc * kappa_loc)
	# guess initial parameters, to fix the parameters, set the relative params_range to 0
	## check if guesses are in the set ranges, if not redefine the guesses
	try:
		if fcavity_guess < fcavity_range[0] or fcavity_guess > fcavity_range[1]:
			fcavity_guess = np.mean(fcavity_range)
	except:
		pass
	print("Initial Neta_guess : ",Neta_guess)
	fatoms_guess =	fcavity_guess
	try:
		if fatoms_guess < fatom_range[0] or fatoms_guess > fatom_range[1]:
			fatoms_guess = np.mean(fatom_range)
	except Exception as e:
		print("fatoms_guess failed. Error:", e)
	try:
		if Neta_guess < Neta_range[0] or Neta_guess > Neta_range[1]:
			Neta_guess = np.mean(Neta_range)
	except:
		pass

	if Neta_guess > 50:
		grid_scan=0
		for Neta_grid in np.arange(Neta_guess*0.4, Neta_guess*1.4+1, Neta_guess/20):
			for fcav_grid in np.arange(fcavity_guess, fcavity_guess+4, .2):
				for fatoms_grid in np.arange(fatoms_guess-2, fatoms_guess+2, .2):
					try:
						init_guess_loc = (fatoms_grid,fcav_grid, Neta_grid, gamma_loc, kappa_loc, dark_counts)
						LL_tot_loc=logLikelihood_rabi_splitting_transmission(init_guess_loc, data)
						if grid_scan>LL_tot_loc:
							print("Temporary Min of -LL:", LL_tot_loc)
							grid_scan = LL_tot_loc
							init_guess = init_guess_loc
					except Exception as e:
						init_guess = (fatoms_guess, fcavity_guess, Neta_guess, gamma_loc, kappa_loc, dark_counts)
						print("----- Fucked up getting init_guess from grid. Error :",e)
		bnds_list = ((init_guess[0]-.5, init_guess[0]+.5), (init_guess[1]-.5,init_guess[1]+.5), (init_guess[2]*(1-1/5),init_guess[2]*(1+1/5)), (gamma_loc-0.004,gamma_loc+0.004),( kappa_loc-0.1, kappa_loc+0.15), (0, 5*dark_counts))
	else:
		init_guess = (fatoms_guess, fcavity_guess, Neta_guess, gamma_loc, kappa_loc, dark_counts)
		bnds_list = (fatom_range, fcavity_range, Neta_range, (gamma_loc-0.004,gamma_loc+0.004),( kappa_loc-0.1, kappa_loc+0.15), (0, 5*dark_counts))
	#fit

	if param_error == 'on':
		# bootstrap the data and perform MLE fit for all databs. Then do statistics of bootstrapped results
		# This method may be slow. It can be improved in speed by implementing Hessian matrix calculations, however it may be tricky because of bounds.
		bs_list=[]
		for i in np.arange(bs_repetition):
			data_bs = random.choices(data,k=len(data))
			out=minimize(logLikelihood_rabi_splitting_transmission, init_guess,args=data_bs, bounds=bnds_list, tol=0.001)
			bs_list.append(out.x)
		fit_result= np.mean(np.transpose(bs_list),1)
		cov = np.sqrt(np.transpose(bs_list)) # Covariance matrix
		# Get the chi_2
		#bin the data
		bin_interval=0.2
		(hist, bin_edges) = np.histogram(
		data,
		bins=np.arange(data[0]-1,data[-1]+1, bin_interval)
		)
		
		bin_centers=bin_edges[:-1]+bin_interval/2
		amplitude = sum(hist)*bin_interval
		y_model = [rabi_splitting_transmission(x, fit_result[0], fit_result[1], fit_result[2], fit_result[3], fit_result[4], fit_result[5]) for x in bin_centers]
		y_model = y_model/sum(y_model)*sum(hist);
		y = hist
		chi_sq = chi_2(y, y_model)

		best_param = {"fatom" : fit_result[0], "fcavity" : fit_result[1], "Neta": fit_result[2],  "gamma" : fit_result[3], "kappa" : fit_result[4], "dark_counts" : fit_result[5],'covariance' : cov,"chi_square" : chi_sq} # gamma and kappa are not fit parameters!
		return best_param
	elif param_error == 'off':
		out = minimize(logLikelihood_rabi_splitting_transmission, init_guess,args=data,bounds=bnds_list, tol=0.00000001)
		best_param = out.x
		# Get the chi_2
		#bin the data
		bin_interval=0.2
		(hist, bin_edges) = np.histogram(
		data,
		bins=np.arange(data[0]-1,data[-1]+1, bin_interval)
		)
		bin_centers=bin_edges[:-1]+bin_interval/2
		y_model = [bin_interval/0.6*rabi_splitting_transmission(x, best_param[0], best_param[1], best_param[2], best_param[3], best_param[4], best_param[5]) for x in bin_centers]
		y_model = y_model*sum(hist);
		
		y = hist
		chi_sq = chi_2(y, y_model)

		return {"fatom": best_param[0], "fcavity" : best_param[1], "Neta": best_param[2], "gamma" : best_param[3], "kappa" : best_param[4], "dark_counts" : best_param[5],"chi_square" : chi_sq}
	else :
		return('incorrect param_error specification')


