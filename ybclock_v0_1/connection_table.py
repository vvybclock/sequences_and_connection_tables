from labscript import start, stop, add_time_marker, AnalogOut, DigitalOut
from labscript_devices.NI_DAQmx.labscript_devices import NI_PCI_6723, NI_PCI_6713, NI_PCI_6284

def define_connection_table():
	### Pseudo Clock
	PineBlaster(
		name              	= 'digital_clock',
		trigger_device    	= None,
		trigger_connection	= None,
		usbport           	= 'COM5'
	)
	

	### NI Cards
	NI_PCI_6284( #digital card
		name            	= 'ni_pci_6284_dev6',
		parent_device   	= digital_clock.clockline,
		clock_terminal  	= '',
		MAX_name        	= 'Dev6',
		acquisition_rate	= 1e3
	)
	

	### Secondary Pseudoclock
	PineBlaster(
		name              	= 'analog_clock',
		trigger_device    	= ni_pci_6284_dev6,
		trigger_connection	= None,
		usbport           	= 'COM7'
	)
	

	### Secondary NI Cards
	NI_PCI_6713( #analog out
		name          	= 'ni_pci_6713_dev5',
		parent_device 	= analog_clock.clockline,
		clock_terminal	= '',
		MAX_name      	='Dev5'
	)

	NI_PCI_6723( #analog out
		name          	= 'ni_pci_6723_dev3',
		parent_device 	= analog_clock.clockline,
		clock_terminal	= '',
		MAX_name      	='Dev3'
	)

	NI_PCI_6713( #analog out
		name          	= 'ni_pci_6713_dev4',
		parent_device 	= analog_clock.clockline,
		clock_terminal	= '',
		MAX_name      	='Dev4'
	)

	#====================
	# Dev 3 Connections
	#====================
	#	This card has a lot of Analog Output Ramps
	AnalogOut(
		name         	= 'mot_voltage_setting_do_not_use',
		parent_device	= ni_pci_6723_dev3,
		connection   	= 'ao3',
		limits       	= None
	)

	AnalogOut(
		name         	= 'red_power',
		parent_device	= ni_pci_6723_dev3,
		connection   	= 'ao0',
		limits       	= None
	)



	#====================
	# Dev 4 Connections
	#====================
	#	This card has a lot of Analog Output Ramps

	AnalogOut(
		name         	= 'blue_power',
		parent_device	= ni_pci_6713_dev4,
		connection   	= 'ao0',
		limits       	= None
	)

	AnalogOut(
		name         	= 'x_bias_field',
		parent_device	= ni_pci_6713_dev4,
		connection   	= 'ao1',
		limits       	= None
	)

	AnalogOut(
		name         	= 'y_bias_field',
		parent_device	= ni_pci_6713_dev4,
		connection   	= 'ao2',
		limits       	= None
	)

	AnalogOut(
		name         	= 'z_bias_field',
		parent_device	= ni_pci_6713_dev4,
		connection   	= 'ao3',
		limits       	= None
	)

	AnalogOut(
		name         	= 'green_power',
		parent_device	= ni_pci_6713_dev4,
		connection   	= 'ao4',
		limits       	= None
	)

	AnalogOut(
		name         	= 'mot_coil_current',
		parent_device	= ni_pci_6713_dev4,
		connection   	= 'ao5',
		limits       	= None
	)


	#====================
	# Dev 5 Connections
	#====================
	#	This card has a lot of Analog Outputs.
	AnalogOut(
		name         	= 'wide_range_camera_trigger',
		parent_device	= ni_pci_6713_dev5,
		connection   	= 'ao2',
		limits       	= (0, 8)
	)

	AnalogOut(
		name         	= 'one_to_one_camera_trigger',
		parent_device	= ni_pci_6713_dev5,
		connection   	= 'ao3',
		limits       	= (0,8)
	)
	

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
