'''
	Running an experiment consists mostly using smaller subsequences in chain.

	Since this is incredibly natural to remove complexity, as well as is obvious
	in coding, this module is used for containing subsequences. 

	#Adding your own subsequences.

	Simply store your custom subsequences in a file like `dummy_filename.py`. 

	If you want your functions to be accessible from `ybclock.subsequences`
	then add a `from .dummy_filename import *` line to the `__init__.py`. If 
	however, you want to group a large number of functions then don't add this 
	line.

	In the first case, the imports will look like 
	`import labscriptlib.ybclock.subsequences.dummy_subsequence as ds`
	and in the second like
	`import labscriptlib.ybclock.subsequences.dummy_filename.dummy_subsequence as ds`

'''

print("Importing Subsequences...")
from .dummy_filename import *
from .loading_subsequences import *
from .camera_helper import *
print("Finished importing Subsequences!")
print()