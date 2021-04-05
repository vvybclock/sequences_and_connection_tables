from lyse import Run, path, data
from pylab import *


'''
Here is the code to call the globals in the analysis.

'''

run = Run(path)
data_globals = run.get_globals()
<<<<<<< HEAD
print(data_globals['VCO_polynomial_interp'])

=======
print(data_globals)
data_trace_names = run.trace_names()
print(data_trace_names)
print("Updated.")
>>>>>>> fc8658fcb41cb2ef75082167e3a9455718f2578e
# run.get_trace(probe_sideband_frequency)