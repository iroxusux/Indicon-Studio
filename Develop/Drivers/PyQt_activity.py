##################################################
# Program: PyQt_activity
# Description: Generic activity base for window applications with PyQt5
# This provides a simple model / view relationship between a code driver and it's view window
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


class BaseActivityWindow(QtWidgets.QWidget):
    def __init__(self,
                 queue_ref: queue.Queue,
                 parent=None):
        super().__init__(parent)
        self._parent = parent
        self._queue_ref = queue_ref
        self.__setup_layout__()

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


class BaseActivity(object):
    @abstractmethod
    def GUI_REF(self):  # over-write this with any inherited class. This is a reference to the TYPE of accompanying window
        return BaseActivityWindow

    def __init__(self, gui_ref: QtWidgets, queue_ref: queue.Queue):
        # generics
        self._exit = False

        # model / view setup
        self._gui_ref = gui_ref
        self._queue_ref = queue_ref

        # main loop thread
        self._main_loop_thread = Thread(target=self.__run__, args=(), daemon=True)
        self._main_loop_thread.start()

    @property
    def gui_ref(self):
        return self._gui_ref

    @property
    def queue_ref(self):
        return self._queue_ref

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
