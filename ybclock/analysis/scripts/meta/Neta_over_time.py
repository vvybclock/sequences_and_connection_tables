''' This metanalysis will plot and analyse multiple Neta measured in sequences. It can be used for various applications as, for example:
i) Monitor or study pump efficiency
ii) Cooling efficiency
iii) basis for any Sz measurement (2, 4, 8 -measurements...)

 # To Do 
 	[x] make atoms_in_cavity_helper.py write the Neta 1 value per scan number of fit in lyse parameters
 	[x] read lyse parameters here
 	[] drop Neta based on bad chi^2
 	[x] Multiple Neta fit versus time
 	[] statistics (hist plot, for example) of Neta results

'''

from lyse import *
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
	try:
		#exposes all the variables available in the lyse window
		dataframe = data()

		runtimes = list(dataframe['run time'])
		paths = list(dataframe['filepath'])

		# set the maximal number of scan we can detect in one sequence
		n_max = 101

		# create a new Pandas (a new dataframe) that allows for rapid plotting of multiple traces. Color coding and legend are already built-in!
		Neta_dic = {}
		chi_square_dic = {}
		df=pd.DataFrame()
		j=0
		while j < n_max:
			try:
				newname = "Neta_"+str(j+1)
				chi_newname = "chi_square_"+str(j+1)
				Neta_dic[newname] = list(dataframe['atoms_in_cavity_helper',newname])
				chi_square_dic[newname] = list(dataframe['atoms_in_cavity_helper',chi_newname])
				dfl = pd.DataFrame(np.transpose([list(dataframe['atoms_in_cavity_helper',newname])]),index = runtimes,columns = [newname])
				df = df.append(dfl)
				#df=pd.concat([pd.DataFrame([i], columns=[newname]) for i in Neta_dic[newname]],
					#ignore_index=True)
				j+=1
			except Exception as e:
				if j == 0:
					print("Failed importing data. Error : ",e)
				else:
					print(j ," Rabi splitting scan found.")
				break

		plt.figure(); df.plot();
		plt.title("Fitted Neta" )
		plt.ylabel("Neta")
		plt.xlabel("Time")

		#Calculate and print Good Fit Ratio
		good_chi_for_fit = [0.4,40]

	except Exception as e:
		print("get_keys Error: ", e)