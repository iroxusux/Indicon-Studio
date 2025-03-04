##################################################
# Program: status_bar.py
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
import Qt.Manager as manager
##################################################
# Constant Variable Definitions
##################################################

##################################################
# Global Variable Definitions
##################################################


def set_status_bar(text: str):  # set status bar of main window
    app = manager.get_main_window()
    if app is None:
        return
    app.set_status_bar_text(text)
