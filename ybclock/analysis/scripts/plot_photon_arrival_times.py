from lyse import *
import numpy as np
import matplotlib.pyplot as plt

run = Run(path)


photon_arrival_times = run.get_result(group='extract_photon_arrival_times',name='processed_arrivals_ch_1')

plt.hist(photon_arrival_times)
print(photon_arrival_times)