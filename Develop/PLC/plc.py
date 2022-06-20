##################################################
# Program: plc
##################################################

##################################################
# System Module Imports
##################################################
from abc import abstractmethod
import queue
from threading import Thread
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


# upper most level PLC object
class PLC(object):
    def __init__(self, gui_ref, queue_ref):
        # generics
        self._exit = False

        # model / view setup
        self._gui_ref = gui_ref  # view
        self._queue_ref = queue_ref  # model ( reference of communications between the 2)

        # plc info
        self._name = ''
        self._ip_address = f'{0}.{0}.{0}.{0}'  # placeholder IP, but constructor shows formatting
        self._data_types = []  # all pre-defined & user-defined types
        self._module_templates = []  # module templates inherited by Rockwell Binaries
        self._modules = []  # actual modules
        self._tags = []  # tags (?)

        # create thread to communicate between GUI and this PLC thread
        self._engine_thread = Thread(target=self.__run__, args=(), daemon=True)
        self._engine_thread.start()

    @property
    def gui_ref(self):
        return self._gui_ref

    @property
    def queue_ref(self):
        return self._queue_ref

    @property
    def data_types(self):
        return self._data_types

    @property
    def modules(self):
        return self._modules

    @property
    def tags(self):
        return self._tags

    @abstractmethod
    def __run__(self):
        while not self._exit:
            messages = None
            try:
                messages = self._queue_ref.get(timeout=0.1)
                match messages:
                    case 1:
                        pass
                    case 2:
                        pass
                    case 3:
                        pass
            except queue.Empty:
                pass

    @abstractmethod
    def compile_from_path(self, path: str):
        pass


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
