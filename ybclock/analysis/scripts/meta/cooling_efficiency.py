from lyse import *
import numpy as np
from numpy import array
import matplotlib.pyplot as plt

if __name__ == '__main__':
	try:
		df = data()

		vars = {}
		parameter_str = 'cooling_pi_intensity'
		vars['Neta_2'] = array(df['atoms_in_cavity_helper','Neta_2'])
		vars['Neta_3'] = array(df['atoms_in_cavity_helper','Neta_3'])
		vars[parameter_str] = array(df[parameter_str])
		top = 'Neta_3'
		bot = 'Neta_2'
		cooling_efficency = vars[top]/vars[bot]

		plt.scatter(vars[parameter_str], cooling_efficency)
		plt.title(f'{top}/{bot}')
		plt.ylabel('cooling_efficency')
		plt.xlabel(parameter_str)


	except Exception as e:
		print(e)
		pass