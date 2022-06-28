##################################################
# Program: PyQt_activity
# Description: Generic activity base for window applications with PyQt5
# This provides a simple model / view relationship between a code driver and it's view window
##################################################

##################################################
# System Module Imports
##################################################
from abc import abstractmethod
from enum import Enum
import queue
from threading import Thread
##################################################
# Add-In Module Imports
##################################################
from PyQt5 import QtWidgets
##################################################
# Local Module Imports
##################################################

##################################################
# Constant Variable Definitions
##################################################

##################################################
# Global Variable Definitions
##################################################


class BaseMessages(Enum):  # any custom messages must be below "10,000" - System reservations start at 10,000 ...
    # note, underscores don't affect processor readability, use them for large numbers for ease of programming
    SYSTEM_RESERVED = 10_000
    KILL_PROCESS = 10_001


class BaseActivityWindow(QtWidgets.QWidget):
    def __init__(self,
                 queue_ref: queue.Queue,
                 parent=None):
        super().__init__(parent)
        self._parent = parent
        self._queue_ref = queue_ref
        self.setWindowTitle(self.__class__.__name__)
        self.__setup_layout__()
        self.__bind_connections__()

    @abstractmethod
    def __setup_layout__(self):
        # setup layout
        self._layout = QtWidgets.QVBoxLayout(self)

        # create dynamic items
        self._some_item = QtWidgets.QLabel('This is a dynamic item')

        # add items to layout
        self._layout.addWidget(self._some_item)

        # add generic items to layout
        self._layout.addWidget(QtWidgets.QLabel('This is an example of a label on a layout'))
        self._layout.addWidget(QtWidgets.QPushButton('This is an example of a push-button on a layout'))

        # bind layout
        self.setLayout(self._layout)

    @abstractmethod
    def __bind_connections__(self):
        pass


class BaseActivity(object):
    @abstractmethod
    def gui_class(self):  # over-write this with any inherited class. This is a reference to the TYPE of accompanying window
        return BaseActivityWindow

    def __init__(self, gui_ref: QtWidgets, queue_ref: queue.Queue):
        # generics
        self._exit = False

        # model / view setup
        self._gui_ref = gui_ref
        self._queue_ref = queue_ref

        # main loop thread
        self._main_loop_thread = Thread(target=self.__system_loop__, args=(), daemon=True)
        self._main_loop_thread.start()

    @property
    def gui_ref(self):
        return self._gui_ref

    @property
    def queue_ref(self):
        return self._queue_ref

    def __system_loop__(self):  # internal loop, do not override in inherited classes, use __run__
        while not self._exit:
            messages = None
            try:
                messages = self._queue_ref.get(timeout=0.1)
                match messages:
                    case BaseMessages.KILL_PROCESS:
                        self.shutdown()
                        continue
                self.__run__(messages)
            except queue.Empty:
                continue

    @abstractmethod
    def __run__(self, message):
        match message:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass

    def shutdown(self):  # shut down our activity safely
        self._exit = True  # set our bit to shut down
        while self._main_loop_thread.isAlive():  # wait while the thread is still alive
            continue  # stay in loop
        return True  # return True on successful shutdown
