'''
Define the channels of all the NI DAC cards. They are seperated by device.
Hopefully, this will make learning the lab mechanism easier in the future.
'''
from labscript import AnalogOut, DigitalOut


def define_channels():
	''' Contains all the function calls for declaring all the channels used by
	each device.	
	'''
	blue_laser_channels()
	red_laser_channels()
	green_laser_channels()
	magnetic_field_channels()
	camera()
	photon_counter()

def blue_laser_channels():
	'''
	###`blue_mot_power`

	This controls the power to our 399nm laser. It currently needs no
	distinction, as we only have one blue laser beam path: the MOT beampath.

	###`blue_mot_aom_and_shutter`

	This controls both the RF switch driving the AOM as well as the shutter for
	the MOT beampath.
	
	###`imaging_power_switch`
	Controls the RF switch for the 399nm Imaging Light beampath.

	###`imaging_power_shutter`
	Controls the shutter for the 399nm Imaging Light beampath.

	
	'''
	AnalogOut(
		name         	= 'blue_mot_power',
		parent_device	= ni_pci_6713_dev4,
		connection   	= 'ao0',
		limits       	= None
	)

	DigitalOut(
		name         	= 'blue_mot_aom_and_shutter',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line1'
	)

	DigitalOut(
		name         	= 'imaging_power_switch',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line6'
	)

	DigitalOut(
		name         	= 'imaging_power_shutter',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line7'
	)


def red_laser_channels():
	'''
	## Intensity Controls

	`red_cavity_power`

	Controls the trap light power going into the cavity axis via error offset
	into a (PI) power lockbox.

	`red_transverse_power`
	
	Controls the light power for the transverse trapping beam, which is oriented
	along the y-axis (lab frame).

	'''
	AnalogOut(
		name         	= 'red_cavity_power',
		parent_device	= ni_pci_6723_dev3,
		connection   	= 'ao0',
		limits       	= None
	)
	AnalogOut(
		name         	= 'red_transverse_power',
		parent_device	= ni_pci_6723_dev3,
		connection   	= 'ao5'
	)

def green_laser_channels():
	'''
	Control the power and shutters of the various green beams.
	
	##Beampaths
	
	Polarizations are defined with respect to the magnetic field bias. This is currently pointing up.

	### Probe Beampath
	
	This is beampath for the light going into the cavity **for measurement**.
	It's \\(\\sigma+\\) polarized. 

	#### Probe Sideband

	The Probe carrier frequency is actually a little far off from the atom+cavity
	resonance. The Probe Sideband is what actually interacts with the
	atoms+cavity. One can say the 'Probe Sideband' is the actual probing beam.
	Unfortunately, 'Probe' is more of a name for the ultimate use of the beam path
	rather than it's initial spectral content. 

	This makes things confusing. We can try and help by saying that the naming
	convention in the lab is labeled by its final state. This makes it difficult
	to understand its evolution through the system but that's the way things are.
	
	#### Two Color Probe Sidebands (of the Probe Sideband)

	We have a **phase** measurement technique where we center the probe sideband
	frequency at the center of the atom + cavity resonances, then we apply
	modulation \\(f_m\\) to split this sideband in two. This allows us to drive
	two colors of light into the two modes of the atom + cavity system. Since
	these two beams share the same spatial mode, they interfere at the
	photodetector giving us a signal that, at least somewhat, looks like
	\\(\\cos(f_m t + \\phi\\) where \\(\\phi\\) is the phase shift imparted by
	one of the atom + cavity transmission peaks.



	### Pump Beampath

	This goes into the cavity axis. It's used polarizing the atoms in the up
	state. It's \\(\\sigma+\\) polarized.


	### Cooling Beampath

	This is greenlight coming perpendicular to the cavity axis. It's \\(\\pi\\) polarized.

	### Green MOT Beampath
	
	It has a complicated beam path. Green comes in from all directions.
	
	.. image:: mot_path.png

	##Analog Intensity Controls
	###`probe_sideband_power`

	This controls the **sideband light** power via Mixer + Amplifier into an **EOM**.

	###`two_color_probe_sideband_power`

	The probe sideband is split in two via EOM modulation. See the above section. **We think** that
	this controls the modulation strength and thus the ratio of the probe
	sideband and these two color sidebands, but are not sure.
	
	###`probe_power_lock_error_offset`

	This controls an error offset to the `probe_sideband_power` lock. Typically, this
	constant across a whole experimental run.

	###`pump_power`
	
	This controls the power via Mixer + Amplifier into an **AOM**.
	
	###`cooling_pi_power`

	Currently not connected.

	###`cooling_sigma_plus_power`

	Controls the power of the \\(\\sigma +\\) light feeding into the cavity axis
	for cooling purposes via **EOM**.

	###`green_mot_power`
	Controls the power of the Green MOT via **AOM**.

	
	##Digital Intensity Controls
	All the channels in this section turn off all the RF power to the AOM/EOM via an RF switch.
	###`green_mot_power_switch`
	Controlled via MOT AOM.
	###`probe_power_switch`
	Controlled via AOM. 
	###`probe_sideband_power_switch`
	Controlled via EOM.
	###`pump_switch`
	Controlled via AOM.

	##Shutter Controls

	Aren't these just intensity controls? Yes, but they block the light better
	than turning off the EOM/AOM can. So a shutter helps ensure the light is
	really off. Ofcourse, they are slower so they are used in conjunction with an
	AOM/EOM RF control.

	###`green_mot_shutter`
	###`cooling_pi_shutter`
	###`probe_shutter`
	
	Located almost just before entering the cavity mirror. It's beneath the
	optics table.
	
	###`probe_sideband_cooling_shutters`

	This output actually controls two shutters. For `go_high`, the cooling path
	is open. For `go_low`, the probe sideband path is open.

	## Frequency Control

	###`probe_sideband_frequency`

	Controls the frequency of the EOM modulation, thus letting us control the
	detuning from the atom + cavity system.

	###`two_color_chirp`

	Triggers the SRS to begin the frequency sweep for the phase measurement.

	## FPGA Trigger

	There is an FPGA (Opal Kelly) that controls the frequencies of a Double Pass
	AOM early in the beampath. So it controls all the frequencies of all the
	beampaths. This FPGA controls the PTS synthesizer on top of the canopy of the lab.

	The frequencies are defined in an external program "FrontPanel.exe". There's
	a short cut to it on the desktop.
	
	'''

	#
	# Intensity Controls 
	#
	AnalogOut(
		name         	= 'probe_sideband_power',
		parent_device	= ni_pci_6713_dev5,
		connection   	= 'ao0'
	)

	AnalogOut(
		name         	= 'probe_power_lock_error_offset',
		parent_device	= ni_pci_6713_dev5,
		connection   	= 'ao5'
	)


	DigitalOut(
		name         	= 'probe_sideband_power_switch',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line23'
	)

	DigitalOut(
		name         	= 'probe_power_switch',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line10',
		inverted     	= True
	)

	AnalogOut(
		name         	= 'two_color_probe_sideband_power',
		parent_device	= ni_pci_6713_dev5,
		connection   	= 'ao1'
	)

	DigitalOut(
		name         	= 'probe_shutter',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line12'
	)

	AnalogOut(
		name         	= 'pump_power',
		parent_device	= ni_pci_6713_dev5,
		connection   	= 'ao7',
	)
	DigitalOut(
		name         	= 'pump_switch',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line8'
	)

	AnalogOut(
		name         	= 'cooling_pi_power',
		parent_device	= ni_pci_6713_dev5,
		connection   	= 'ao6',
	)

	AnalogOut(
		name         	= 'cooling_sigma_plus_power',
		parent_device	= ni_pci_6723_dev3,
		connection   	= 'ao4'
	)

	AnalogOut(
		name         	= 'green_mot_power',
		parent_device	= ni_pci_6713_dev4,
		connection   	= 'ao4',
		limits       	= None
	)


	DigitalOut(
		name         	= 'green_mot_power_switch',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line2'
	)

	# 
	# Shutters
	#

	DigitalOut(
		name         	= 'cooling_pi_shutter',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line25'
	)

	DigitalOut(
		name         	= 'green_mot_shutter',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line4'
	)
	DigitalOut(
		name         	= 'green_frequency_fpga_trigger',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line3'
	)

	DigitalOut(
		name         	= 'probe_sideband_cooling_shutters',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line16'
	)
	

	#
	#	Frequency Controls
	#

	AnalogOut(
		name         	= 'probe_sideband_frequency',
		parent_device	= ni_pci_6713_dev4,
		connection   	= 'ao6'
	)

	DigitalOut(
		name         	= 'two_color_chirp',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line5'
	)

def magnetic_field_channels():
	'''
	## Bias Fields
	
	These are the magnetic fields that are intended to be uniform across the atoms.

	## MOT Coil

	This creates the large quadrupole field for trapping and cooling the atoms.

	## Rabi Coil

	This drives AC fields along the x-direction (lab frame). This is for driving
	nuclear spin flips.

	The Rabi Coil was designed in a idiosyncratic manner. Given our difficulties
	in creating bipolar current controllers, we came up with a method for driving
	AC fields with unipolar current controllers. We have two coils wound
	together, and we drive currents in opposite directions. This causes zero
	magnetic field. We then modulate each current in opposite amounts causing a
	net AC field.

	###`rabi_coil_dc_offset`
	controls that DC offset.

	###`rabi_coil_field'
	
	controls that differential offset, and thus magnetic field that the atoms do
	see.

	'''
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


	#sets the voltage on the mot coil current controller.
	#for constant current mode, voltage needs to be larger than actual,
	#for constant voltage mode, current needs to be larger than actual.
	AnalogOut(
		name         	= 'mot_coil_current',
		parent_device	= ni_pci_6713_dev4,
		connection   	= 'ao5',
		limits       	= None
	)
	AnalogOut(
		name         	= 'mot_coil_voltage',
		parent_device	= ni_pci_6723_dev3,
		connection   	= 'ao3',
		limits       	= None
	)

	#
	# Rabi Coil
	#

	AnalogOut(
		name         	= 'rabi_coil_dc_offset',
		parent_device	= ni_pci_6713_dev5,
		connection   	= 'ao4'
	)

	AnalogOut(
		name         	= 'rabi_coil_field',
		parent_device	= ni_pci_6713_dev4,
		connection   	= 'ao7'
	)

def camera():
	'''
	The camera triggers are analog out's as they require 8V pulses to trigger.
	The channels will actually be defined in `define_hardware_cards.py`
	'''
	# AnalogOut(
	#	name         	= 'wide_range_camera_trigger',
	#	parent_device	= ni_pci_6713_dev5,
	#	connection   	= 'ao2',
	#	limits       	= (0, 8)
	# )

	# AnalogOut(
	#	name         	= 'one_to_one_camera_trigger',
	#	parent_device	= ni_pci_6713_dev5,
	#	connection   	= 'ao3',
	#	limits       	= (0,8)
	# )

def photon_counter():
	DigitalOut(
		name         	= 'p7888_start_trigger',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line11'
	)

	DigitalOut(
		name         	= 'p7888_flushing_trigger',
		parent_device	= ni_pci_6284_dev6,
		connection   	= 'port0/line15'
	)

