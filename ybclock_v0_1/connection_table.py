from labscript import start, stop, add_time_marker, AnalogOut, DigitalOut

from labscriptlib.ybclock_v0_1.connection_functions import define_connection_table

def define_connection_table():

	define_hardware_cards()
	
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

	DigitalOut(
		name         	= 'green_frequency_fpga_trigger',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line3'
	)


	print("Time Markers:")



if __name__ == '__main__':

	define_connection_table()
	
	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()

	# Stop the experiment shot with stop()
	stop(1.0)
