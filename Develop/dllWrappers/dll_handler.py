##################################################
# Program: dll_handler
##################################################

##################################################
# System Module Imports
##################################################
import ctypes
import time
##################################################
# Add-In Module Imports
##################################################

##################################################
# Local Module Imports
##################################################

##################################################
# Constant Variable Definitions
##################################################

##################################################
# Global Variable Definitions
##################################################


# load dll into memory
generics_dll = ctypes.WinDLL("D:\Personal\PyCharmProjects\Indicon Studio\Indicon-Studio\Develop\lib\\Generics.dll")

# set up prototype and parameters for function call
genericsAPI_add_proto = ctypes.WINFUNCTYPE(ctypes.c_int,  # return type
                                           ctypes.c_int,  # parameter 1
                                           ctypes.c_int)  # parameter 2
genericsAPI_add_params = (1, "a", 0), (1, "b", 0)

genericsAPI_sub_proto = ctypes.WINFUNCTYPE(ctypes.c_int,  # return type
                                           ctypes.c_int,  # parameter 1
                                           ctypes.c_int)  # parameter 2
genericsAPI_sub_params = (1, "a", 0), (1, "b", 0)

addApi = genericsAPI_add_proto(("add", generics_dll), genericsAPI_add_params)
subApi = genericsAPI_sub_proto(("sub", generics_dll), genericsAPI_sub_params)


# stress test


# check generic python function timing
start_time = time.time()
for _ in range(1_000_000):
    x = 1 + 2
end_time = time.time()
delta = end_time - start_time
print(f'Python took {delta} seconds to complete.')

# check dll API function timing
start_time = time.time()
for _ in range(1_000_000):
    x = addApi(1, 2)
end_time = time.time()
delta = end_time - start_time
print(f'DLL took {delta} seconds to complete.')
