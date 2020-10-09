### Test 1: Load the COMCTL.DLL, this is the DLL specified in figure 5.9 of the P7888 manual.
###		It appears that its actually "comctl32.dll" as a window search revealed.
import ctypes

#comtec_dll = ctypes.cdll.LoadLibrary("COMCTL.DLL")
comtec_dll = ctypes.cdll.LoadLibrary("comctl32.dll")

print(comtec_dll)