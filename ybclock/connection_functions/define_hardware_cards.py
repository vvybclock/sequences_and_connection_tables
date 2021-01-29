from labscript_devices.NI_DAQmx.labscript_devices import NI_PCI_6723, NI_PCI_6713, NI_PCI_6284
from labscript_devices.PineBlaster import PineBlaster
from user_devices.P7888.labscript_devices import P7888
from labscript_devices.AnalogIMAQdxCamera.labscript_devices import AnalogIMAQdxCamera

'''
Here we define the hardware cards.
'''
def define_hardware_cards():
	'''
		We define cards in order of connection.
		The PseudoClock drives the digital card which in turn triggers the
		secondary pseudoclock 'analog_clock', which in turn drives the analog
		or secondary NI cards.
		
	'''
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

	### Cameras
	AnalogIMAQdxCamera(
		name         	= 'cam0',
		parent_device	= '',
		connection   	= '',
		serial_number	= '6BE00895F'
	)

	AnalogIMAQdxCamera(
		name         	= 'cam1',
		parent_device	= '',
		connection   	= '',
		serial_number	= '6BE008960'
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
