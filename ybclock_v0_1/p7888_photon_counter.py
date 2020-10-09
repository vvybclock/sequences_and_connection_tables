
from p7888_c_definitions import *
import ctypes


# Test 1: Load the COMCTL.DLL, this is the DLL specified in figure 5.9 of the
# P7888 manual. It appears that its actually "comctl32.dll" as a window search
# revealed.

# Here we load the Dynamic Linked Library that allows sending commands to the
# P7888 card provided we have enabled remote mode in the P7888 server. See
# section 5.2 (p. 5-9) in the p7888 docs.
comtec_dll = ctypes.windll.LoadLibrary("comctl32.dll")

# In section 5.4, they instead reference "dp7888.dll"! This is what is used
# for controlling the server.
dp7888_dll = ctypes.windll.LoadLibrary("dp7888.dll")


#Specify the functions in CTYPES

#StoreSettingData
StoreSettingData = dp7888_dll.StoreSettingData

#GetSettingData
GetSettingData = dp7888_dll.GetSettingData
GetSettingData.restype = c_int
GetSettingData.argtypes = [POINTER(ACQSETTING), c_int]


if __name__ == '__main__':
	settings = ACQSETTING()
	nDisplay = 1

	print(settings.range)
	print(GetSettingData(settings,nDisplay))
	print(settings.range)
