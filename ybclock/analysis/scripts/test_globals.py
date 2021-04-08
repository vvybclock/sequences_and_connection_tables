from lyse import Run, path, data
from pylab import *


'''
Here is the code to call the globals in the analysis.

'''

run = Run(path)
data_globals = run.get_globals()

print(data_globals['VCO_polynomial_interp'])

print(data_globals)
# run.get_trace(probe_sideband_frequency)