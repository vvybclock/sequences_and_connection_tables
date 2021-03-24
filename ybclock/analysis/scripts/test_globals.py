from lyse import Run, path, data
from pylab import *


'''
Here is the code to call the globals in the analysis.

'''

run = Run(path)
data_globals = run.get_globals()
print(data_globals)
data_trace_names = run.trace_names()
print(data_trace_names)
print("Updated.")
# run.get_trace(probe_sideband_frequency)