##################################################
# Program: Manager
##################################################

##################################################
# System Module Imports
##################################################

##################################################
# Add-In Module Imports
##################################################
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication
##################################################
# Local Module Imports
##################################################

##################################################
# Constant Variable Definitions
##################################################

##################################################
# Global Variable Definitions
##################################################
main_app = None


def get_main_window() -> QWidget or None:
    global main_app  # grab global var
    if main_app:  # if we did this function before, return the already top level widget
        return main_app
    for widget in QApplication.instance().topLevelWidgets():  # else, filter through widgets to find it
        if isinstance(widget, QMainWindow):
            main_app = widget  # set the global as the main (reserve this memory for faster functionality)
            return main_app
    return None
