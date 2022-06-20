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


def get_main_window() -> QWidget or None:
    app: [QApplication] = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget
    return None
