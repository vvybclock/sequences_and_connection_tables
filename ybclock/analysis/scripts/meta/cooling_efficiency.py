from lyse import *
import numpy as np
from numpy import array
import matplotlib.pyplot as plt

if __name__ == '__main__':
	try:
		df = data()

		vars         	= {}
		parameter_str	= 'cooling_pump_intensity'
		mask_str     	= 'use_cooling_pump'


		vars['Neta_2'] = array(df['atoms_in_cavity_helper','Neta_2'])
		vars['Neta_3'] = array(df['atoms_in_cavity_helper','Neta_3'])
		vars[parameter_str] = array(df[parameter_str])
		vars[mask_str] = list(df[mask_str])
		top = 'Neta_3'
		bot = 'Neta_2'
		cooling_efficency = vars[top]/vars[bot]

		mask = array([1 if x else 0 for x in vars[mask_str]])
		plt.scatter(vars[parameter_str]*mask, cooling_efficency,s=10)
		plt.title(f'{top}/{bot}')
		plt.ylabel('cooling_efficency')
		plt.xlabel(parameter_str)
		plt.ylim(0 ,1.5)
		plt.grid()



	except Exception as e:
		print(e)
		pass