##################################################
# Program: plc
##################################################

##################################################
# System Module Imports
##################################################

##################################################
# Add-In Module Imports
##################################################
from Drivers.PyQt_activity import BaseActivity
##################################################
# Local Module Imports
##################################################

##################################################
# Constant Variable Definitions
##################################################

##################################################
# Global Variable Definitions
##################################################


# upper most level PLC object
class PLC(BaseActivity):
    def __init__(self, gui_ref, queue_ref):
        super().__init__(gui_ref, queue_ref)

        # plc info
        self._name = ''
        self._ip_address = f'{0}.{0}.{0}.{0}'  # placeholder IP, but constructor shows formatting
        self._data_types = []  # all pre-defined & user-defined types
        self._module_templates = []  # module templates inherited by Rockwell Binaries
        self._modules = []  # actual modules
        self._tags = []  # tags (?)

    @property
    def data_types(self):
        return self._data_types

    @property
    def modules(self):
        return self._modules

    @property
    def tags(self):
        return self._tags


class AlphaDataType(object):
    class_hi = 1
    class_lo = -1

    def __init__(self, size: int = 1, val: float = 0, signed=True):
        self._size = size
        self._signed = signed
        self._value = self.value(val)

    @property
    def size(self):
        return self._size

    @property
    def signed(self):
        return self._signed

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val if self._get_class_lo() <= val <= self._get_class_hi() else self._value

    @classmethod
    def _get_class_hi(cls):
        return cls.class_hi

    @classmethod
    def _get_class_lo(cls):
        return cls.class_lo


class SINT(AlphaDataType):
    class_hi = 127
    class_lo = -128

    def __init__(self, val=0):
        super().__init__(1, val)


class INT(AlphaDataType):
    class_hi = 32767
    class_lo = -32768

    def __init__(self, val=0):
        super().__init__(2, val)


class DINT(AlphaDataType):
    class_hi = 2147483647
    class_lo = -2147483648

    def __init__(self, val=0):
        super().__init__(4, val)


class REAL(AlphaDataType):
    class_hi = 2147483647.99999999
    class_lo = -2147483648.99999999

    def __init__(self, val=0):
        super().__init__(8, 0.0)


class LINT(AlphaDataType):
    class_hi = 9223372036854775807
    class_lo = -9223372036854775808

    def __init__(self, val=0):
        super().__init__(8, 0)
