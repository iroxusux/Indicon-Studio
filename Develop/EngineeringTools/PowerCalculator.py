##################################################
# Program: PowerCalculator
##################################################

##################################################
# System Module Imports
##################################################
from enum import Enum
import queue
##################################################
# Add-In Module Imports
##################################################
from Drivers.PyQt_activity import BaseActivity, BaseActivityWindow
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


class Messages(Enum):  # enum classes exist as a "template" of sorts to allow easy-to-implement / read code.
    EXAMPLE_MESSAGE = 1
    SECOND_EXAMPLE = 2


class PowerCalculatorWindow(BaseActivityWindow):
    def __init__(self,
                 queue_ref: [queue.Queue],
                 parent=None):
        super().__init__(queue_ref=queue_ref,
                         parent=parent)

    def __setup_layout__(self):
        # setup layout
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setContentsMargins(5, 5, 5, 5)

        # explicit definitions
        # Quick lambda example
        self._some_push_button = QtWidgets.QPushButton()
        self._some_push_button.setText('push me!')
        self._some_push_button.clicked.connect(lambda: print('you pushed me!'))

        # Another reference to bind to a local def
        self._another_push_button = QtWidgets.QPushButton('Hello!')
        self._another_push_button.clicked.connect(self.example_public_method)  # we only pass method references to slots, do not call the method here (e.g. this is a bad signal call: xxx.connect(self.example_public_method() <- where the "()" should be omitted).

        # Another reference to bind to a local def
        self._private_pb = QtWidgets.QPushButton('I call a private method (function)!')
        self._private_pb.clicked.connect(self.__example_private_method__)  # we only pass method references to slots, do not call the method here (e.g. this is a bad signal call: xxx.connect(self.example_public_method() <- where the "()" should be omitted).

        # last example, with messages to our queue which will communicate with the "engine" thread (general code thread, NOT gui thread)
        self._message_push_button = QtWidgets.QPushButton('I communicate to a different thread!')
        self._message_push_button.clicked.connect(lambda: self._queue_ref.put(Messages.EXAMPLE_MESSAGE))  # this will queue up a message and safety give it to the other thread to process

        # implicit definitions
        self._layout.addWidget(QtWidgets.QLabel('this is a label'))
        self._layout.addWidget(QtWidgets.QLabel('this is a label, again'))
        self._layout.addWidget(QtWidgets.QLabel('this is a label, for the third time'))
        self._layout.addWidget(QtWidgets.QLabel('this is a label, as you may have guessed'))

        # bind explicit definitions
        self._layout.addWidget(self._some_push_button)
        self._layout.addWidget(self._another_push_button)
        self._layout.addWidget(self._private_pb)
        self._layout.addWidget(self._message_push_button)

        # bind layout
        self.setLayout(self._layout)

    @staticmethod
    def example_public_method():  # note: static method means "self" is not used (an instance of this class is not required to use this function, just the "type" of the class is required for this call)
        print('anyone can call me! I do not have an "_" (underscore)')

    def __example_private_method__(self):  # note: this is NOT a static method because we're calling attributes to an EXISTING object.
        print('only my class should be calling me...')  # example of printing to the console (print())
        print(f'my class is {self.__class__.__name__}!')  # example of an "f" string, use curly brackets to insert variables, as shown


class PowerCalculator(BaseActivity):
    GUI_REF = PowerCalculatorWindow

    def __init__(self, gui_ref, queue_ref):
        super().__init__(gui_ref, queue_ref)

    def __run__(self):
        while not self._exit:
            messages = None
            try:
                messages = self._queue_ref.get(timeout=0.1)
                match messages:
                    case Messages.EXAMPLE_MESSAGE:
                        print('you made it to me! This is a different thread than the GUI!')
                        print(f'btw, my class is {self.__class__.__name__}!')
                    case 1:
                        pass
                    case 2:
                        pass
                    case 3:
                        pass
            except queue.Empty:
                pass

