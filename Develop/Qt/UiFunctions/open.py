##################################################
# Program: open
##################################################

##################################################
# System Module Imports
##################################################
import os
##################################################
# Add-In Module Imports
##################################################
from PyQt5.QtWidgets import QFileDialog
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


def get_file_with_dialogue(get_env='HOME', file_type_args='.*(*.*)') -> str | None:
    app = manager.get_main_window()
    if app is None:
        return
    return app.open_file(get_env, file_type_args)


def get_folder_with_dialogue(get_env='Home') -> str | None:
    app = manager.get_main_window()
    if app is None:
        return
    return app.open_folder(get_env)
