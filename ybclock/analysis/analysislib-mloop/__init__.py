'''
	This is the Labscript-MLOOP API. 
		
	#Upgrading this API

	## To Do
	* I wish to rewrite it so it takes in programmatically defined parameters
	instead of resorting to the .ini file.
	
	## How MLOOP interfaces with Python

	It already has an API, so I'm curious what this analysis-mloop api introduces.

	### Native MLOOP API

	One needs to define a Custom Interface and an instance of MLOOP controller.
	Then tells the controller to start.
	
	#### Interface
	The *interface* pulls the cost from the experiment (as every python experiment
	can have a possibly different programming paradigm.)

	#### Controller
	The *controller* is the MLOOP class that does all the looping for you, you need
	to just pass the interface, and the parameters.
	
	The settings sent to the controller actually replaces the .ini file. So why
	did the designed Labscript API rely on it? Dumb design choice.

	## How it Works Currently

 '''