from labscript_devices.NI_DAQmx.labscript_devices import NI_PCI_6723, NI_PCI_6713, NI_PCI_6284
from labscript_devices.PineBlaster import PineBlaster
from user_devices.P7888.labscript_devices import P7888
from user_devices.AnalogIMAQdxCamera.labscript_devices import AnalogIMAQdxCamera
from user_devices.HP8648.labscript_devices import HP8648
from user_devices.AnalogInputReader.labscript_devices import AnalogInputReader
from labscriptlib.ybclock.connection_functions  import camera_settings
'''
Here we define the hardware cards and cameras.
'''

def define_hardware_cards():
	'''
		We define cards in order of connection.
		The PseudoClock drives the digital card which in turn triggers the
		secondary pseudoclock 'analog_clock', which in turn drives the analog
		or secondary NI cards.
		
	'''
	print("\tDefining Pseudoclocks, NI Cards, P7888...",end='')
	### Pseudo Clock
	PineBlaster(
		name              	= 'digital_clock',
		trigger_device    	= None,
		trigger_connection	= None,
		usbport           	= 'COM5'
	)

	### Acquisition
	P7888( #photon counting card
		name	= 'photon_counter'
	)

	### NI Cards
	NI_PCI_6284( #digital card
		name            	= 'ni_pci_6284_dev6',
		parent_device   	= digital_clock.clockline,
		clock_terminal  	= 'PFI1',
		MAX_name        	= 'Dev6',
		acquisition_rate	= 1e3
	)

	### Secondary Pseudoclock
	PineBlaster(
		name              	= 'analog_clock',
		trigger_device    	= ni_pci_6284_dev6,
		trigger_connection	= 'port0/line0',
		usbport           	= 'COM7'
	)
	

	### Secondary NI Cards
	NI_PCI_6713( #analog out
		name          	= 'ni_pci_6713_dev5',
		parent_device 	= analog_clock.clockline,
		clock_terminal	= 'PFI2',
		MAX_name      	='Dev5'
	)

	NI_PCI_6723( #analog out
		name          	= 'ni_pci_6723_dev3',
		parent_device 	= analog_clock.clockline,
		clock_terminal	= 'PFI2',
		MAX_name      	='Dev3'
	)

	NI_PCI_6713( #analog out
		name          	= 'ni_pci_6713_dev4',
		parent_device 	= analog_clock.clockline,
		clock_terminal	= 'PFI2',
		MAX_name      	='Dev4'
	)

	print('Done!')

	### Cameras
	print("\tDefining Cameras...",end='')
	AnalogIMAQdxCamera(
		name                         	= 'wide_angle_cam',
		parent_device                	= ni_pci_6713_dev5,
		connection                   	= 'ao3',
		serial_number                	= '6BE00895F',
		voltage                      	= 8,
		trigger_edge_type            	= 'falling',
		camera_attributes            	= camera_settings.seq_camera_attributes,
		manual_mode_camera_attributes	= camera_settings.manual_camera_attributes
	)

	AnalogIMAQdxCamera(
		name                         	= 'isometric_cam',	#See `isometric video game graphics`
		parent_device                	= ni_pci_6713_dev5,
		connection                   	= 'ao2',
		serial_number                	= '6BE008960',
		voltage                      	= 8,
		trigger_edge_type            	= 'falling',
		camera_attributes            	= camera_settings.seq_camera_attributes,
		manual_mode_camera_attributes	= camera_settings.manual_camera_attributes
	)
	print("Done!")

	### Synthesizers

	print("\tDefining HP Synthesizers...",end="")
	HP8648(
		name        	= 'HP8648Cfor759',
		gpib_address	= 'GPIB0::18::INSTR'
	)

	HP8648(
		name        	= 'HP8648B',
		gpib_address	= 'GPIB0::7::INSTR'
	)

	### Analog Input Reader
	# print("\tAdding AnalogInputReader...",end='')
	# AnalogInputReader(
	#  	name    	= 'Light_Monitor', 
	#  	channels	= {
	#  	        	'Green Probe Monitor'      		: 'Dev6/ai5',
	# #	        	'556_nm_ultrastable_cavity'		: 'Dev6/ai0',
	# #	        	'759nm_reference_cavity'   		: 'Dev6/ai2',
	# #	        	'759nm_exp_cavity'         		: 'Dev6/ai3',
	# #	        	'759nm_Lattice_Input'      		: 'Dev6/ai4',
	#  	        	'Cooling Pi Power Monitor' 		: 'Dev6/ai6',
	# #	        	'1157nm_ultrastable_cavity'		: 'Dev6/ai7'
	#  	}
	# )
	# print("Done!")