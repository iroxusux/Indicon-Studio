##################################################
# Program: dll_handler
##################################################

##################################################
# System Module Imports
##################################################
import ctypes
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


# simple generic DLL for functionality testing between python module and DLL objects
class GenericsDLL:
    # create object of DLL
    dll = ctypes.WinDLL("D:\Personal\PyCharmProjects\Indicon Studio\Indicon-Studio\Develop\lib\\Generics.dll")

    # set up prototype and parameters for function call
    genericsAPI_add_proto = ctypes.WINFUNCTYPE(ctypes.c_int,  # return type
                                               ctypes.c_int,  # parameter 1
                                               ctypes.c_int)  # parameter 2
    genericsAPI_add_params = (1, "a", 0), (1, "b", 0)

    # set up prototype and parameters for function call
    genericsAPI_sub_proto = ctypes.WINFUNCTYPE(ctypes.c_int,  # return type
                                               ctypes.c_int,  # parameter 1
                                               ctypes.c_int)  # parameter 2
    genericsAPI_sub_params = (1, "a", 0), (1, "b", 0)

    # bind functions to prototypes
    addAPI = genericsAPI_add_proto(("add", dll), genericsAPI_add_params)
    subAPI = genericsAPI_sub_proto(("sub", dll), genericsAPI_sub_params)

    @classmethod
    def add(cls, a, b):
        return cls.addAPI(a, b)

    @classmethod
    def sub(cls, a, b):
        return cls.subAPI(a, b)
