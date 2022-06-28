##################################################
# Program: list_funcs
##################################################

##################################################
# System Module Imports
##################################################

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


def find(obj_attribute, obj_value, list_to_search: list):  # set to overload to set value directly to object for list comprehension capabilities
    for i in list_to_search:
        try:
            if obj_value == (getattr(i, obj_attribute)):
                return i
        except AttributeError:
            pass
    return None
