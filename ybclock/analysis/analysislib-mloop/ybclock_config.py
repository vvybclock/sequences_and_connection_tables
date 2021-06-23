'''
	A ybclock custom script for defining the settings for MLOOP.

	For different optimization sequences change `get()`.

'''
from .opt_loading import *


def get():
	'''
		
		Returns the `dict()` that contains all the settings for the MLOOP
		controller.

		For a comprehensive list of settings possible to set, see [the MLOOP API](https://m-loop.readthedocs.io/en/stable/api/controllers.html)

	'''
	return opt_loading_config()