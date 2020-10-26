from labscript_devices.NI_DAQmx.labscript_devices import NI_PCI_6723, NI_PCI_6713, NI_PCI_6284
from labscript_devices.PineBlaster import PineBlaster


def define_hardware_cards():
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
