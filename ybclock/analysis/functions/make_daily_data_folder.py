'''
	#WARNING! ALMOST COMPLETELY WRONG IN INTENTION. SAVE FOR SUBROUTINES ONLY!
	
	Run in Lyse, or run on it's own.

	It creates the folder for holding the days experimental shots in the original
	LabView/Boris & Akio Framework.

	It is designed to automatically construct a folder with todays date and
	yesterdays name. It should run if only past, let's say, 6 am. In case anyone wants
	to take data past midnight... This lets it stay in yesterdays folder.

	It will do nothing if a folder with todays date already exists.

	It assumes we've done at least one experiment within the last month up until now.
	If that fails, it will not make a new folder.

'''

import os
import datetime
from os import mkdir
from os.path import isfile, isdir, join

#get the date
now = datetime.datetime.now()

#don't run if it's somewhere from 12 am - 6 am.
#now.hour is in 24h time.
if now.hour < 6:
	print("I'm assuming you're not trying to start a new experiment past\
	midnight. Go to sleep! No folder for you!")
	quit()

#otherwise...
#
#

#declare our variables
exp_data_folder = 'E:/Documents/Experimental data/'
this_months_folder = None
todays_folder = None


def return_months_last_data_folder(year, month, makedirectory=False):
	''' Return the folder name that has data for the given year and month. Create
	said folder if makedirectory==true and that folder doesn't exist.

	Else return None.
	'''

	#generate this_months_folder_name
	this_months_folder = f"{year}_{month:02}"

	#first see if it's a new month. if so, make the folder if desired
	abs_path_of_this_months_folder = join(exp_data_folder, this_months_folder)
	if not isdir(abs_path_of_this_months_folder):
		if makedirectory==True:
			mkdir(abs_path_of_this_months_folder)
		return None

	#check inside this months folder to find last made folder
	(_,this_months_dirs, _) = next(os.walk(abs_path_of_this_months_folder))

	#find all folders with data
	data_folders = [x for x in this_months_dirs if f"{year}" in x]
	if len(data_folders) != 0:
		#return most recent
		return data_folders[-1]
	else:
		return None


#generate this_months_folder_name
this_months_folder = f"{now.year}_{now.month:02}"
todays_prefix = f"{now.year}_{now.month:02}_{now.day:02}_"
abs_path_of_this_months_folder = join(exp_data_folder, this_months_folder)

#check inside this months folder to see if todays date is made
(_,this_months_dirs, _) = next(os.walk(abs_path_of_this_months_folder))
dirs_with_todays_date = [x for x in this_months_dirs if todays_prefix in x]

#if there are no folders with todays date, make a new folder.
data_folders = [x for x in this_months_dirs if f"{now.year}" in x]
if len(dirs_with_todays_date) == 0:
	if len(data_folders) != 0:
		#check to see theres a folder from earlier in the month
		last_working_folder = data_folders[-1]
	else:
		#check last months folder
		last_month = (now.month - 2)%12 + 1
		if now.month == 1:
			last_months_year = now.year - 1
		else:
			last_months_year = now.year
		last_working_folder = return_months_last_data_folder(last_months_year, last_month)
	
	print(last_working_folder)


