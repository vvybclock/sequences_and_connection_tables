from lyse import *
import numpy as np
import matplotlib.pyplot as plt
from labscriptlib.ybclock.analysis.functions.metadata import extract_sequence_repetition_numbers, extract_date,extract_sequence_name

run = Run(path)

(sequence_number, repetition_number)	= extract_sequence_repetition_numbers(path)
date                                	= extract_date(path)
sequence_name                       	= extract_sequence_name(path)

photon_arrival_times = run.get_result(group='extract_photon_arrival_times',name='processed_arrivals_ch_1')

plt.hist(
	photon_arrival_times,
	bins=np.arange(0,30e-3, 200e-6)
)

plt.title(f"({date}) #{sequence_number}_r{repetition_number}\n{sequence_name}")

plt.ylabel("Photon Counts, (200us Bin)")
plt.xlabel("Time (s)")
print(photon_arrival_times)