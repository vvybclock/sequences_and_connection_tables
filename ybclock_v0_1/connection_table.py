from labscript import start, stop, add_time_marker, AnalogOut, DigitalOut
from labscript_devices.NI_DAQmx.labscript_devices import NI_PCI_6723, NI_PCI_6713, NI_PCI_6284
from labscript_devices.DummyPseudoclock.labscript_devices import DummyPseudoclock

def define_connection_table():
	### Pseudo Clock
	DummyPseudoclock(name='pseudoclock')
	
	### NI Cards
	NI_PCI_6723(
		name          	= 'ni_pci_6723_dev3',
		parent_device 	= pseudoclock.clockline,
		clock_terminal	= '',
		MAX_name      	='Dev3'
	)

	NI_PCI_6713(
		name          	= 'ni_pci_6713_dev4',
		parent_device 	= pseudoclock.clockline,
		clock_terminal	= '',
		MAX_name      	='Dev4'
	)

	NI_PCI_6713(
		name          	= 'ni_pci_6713_dev5',
		parent_device 	= pseudoclock.clockline,
		clock_terminal	= '',
		MAX_name      	='Dev5'
	)

	NI_PCI_6284(
		name            	= 'ni_pci_6284_dev6',
		parent_device   	= pseudoclock.clockline,
		clock_terminal  	= '',
		MAX_name        	= 'Dev6',
		acquisition_rate	=1e3
	)


	#====================
	# Dev 3 Connections
	#====================
	#	This card has a lot of Analog Output Ramps

	#====================
	# Dev 4 Connections
	#====================
	#	This card has a lot of Analog Output Ramps
	

	#====================
	# Dev 5 Connections
	#====================
	#	This card has a lot of Analog Outputs.
	

	#====================
	# Dev 6 Connections
	#====================
	#	This card has a lot of Digital Outputs

	#the DO NOT USE digital outs
	DigitalOut(
		name         	= 'trigger_for_p7888_start_DONOTUSE',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line11'
	)

	DigitalOut(
		name         	= 'p7888_flushing_channel_DONOTUSE',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line15'
	)

	# green mot controls
	DigitalOut(
		name         	= 'green_mot_shutter',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line4'
	)

	DigitalOut(
		name         	= 'green_mot_aom',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line2'
	)

	# blue mot controls
	DigitalOut(
		name         	= 'blue_mot_aom_and_shutter',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line1'
	)

	#cooling light controls
	DigitalOut(
		name         	= 'cooling_shutter',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line25'
	)






if __name__ == '__main__':

	define_connection_table()
	
	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()

	# Stop the experiment shot with stop()
	stop(1.0)
