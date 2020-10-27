"""
	#ybclock
	
	Where we store our connection tables and sequences for our
	current version of hardware. 

	## Versioning

	The idea for the version number is to separate mutually exclusive hardware
	wirings. For example when we use something that was driving the mot now drives
	an AOM, we should change version number so as not to run (old AOM) code that
	could break our MOT by over-driving it.

	Documentation as to what changed shall go into HW_VERSIONING.md

	If however we are installing new channels without disconnecting old channels
	, then the hardware version shall remain the same, and the git shall account
	for improvements and new connections.

"""