##################################################
# Program: program_updater
##################################################

##################################################
# System Module Imports
##################################################
from enum import Enum
import os
import queue
import sys
from threading import Thread
##################################################
# Add-In Module Imports
##################################################
from EngineeringTools.PowerCalculator.PowerCalculator import PowerCalculator
from PyQt5 import QtWidgets, QtCore, QtGui
##################################################
# Local Module Imports
##################################################
from PLC.ab import RockwellProcessor, RockwellMessages
##################################################
# Constant Variable Definitions
##################################################
STUDIO_NAME = 'Indicon Studio'
STUDIO_VERSION = 'v1.00.00'
##################################################
# Global Variable Definitions
##################################################


# messages class to interface between GUI and "engine"
class Messages(Enum):
    IMPORT_L5X = 2
    CALC_CONFIG = 3


class StudioMainWindowForm(QtWidgets.QMainWindow):
    add_activity_to_stack = QtCore.pyqtSignal(type(QtWidgets.QWidget), queue.Queue)  # add new activity to local stack
    remove_activity_from_stack = QtCore.pyqtSignal(QtWidgets.QWidget)  # remove activity from local stack

    def __init__(self, queue_ref: [queue.Queue]):
        super().__init__()
        # set up variables
        self._title = STUDIO_NAME  # window title
        self._version = STUDIO_VERSION  # studio version
        self._queue = queue_ref  # engine interface queue
        self._file_handler = FileHandler()  # file handler - allows thread safe execution from engine threads
        self._built_interface = None

        # set up UI
        self.__setup_ui__()
        self.__bind_connections__()
        # self.__setup_layout__()
        # self.__setup_connections__()
        # self.__setup_action_bar_slots__()
        # self.__setup_dock_slots__()

    def __setup_ui__(self):
        # # # WINDOW GENERICS # # #
        self.setWindowTitle(f'{self._title} {self._version}')
        self.setWindowIcon(QtGui.QIcon('images/_default.png'))
        self.resize(800, 600)
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # # # CENTRAL WIDGET # # #
        self._central_widget = QtWidgets.QStackedWidget(self)  # stacked widget to handle multiple activities
        self.setCentralWidget(self._central_widget)  # set central widget
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # # # MENU BAR # # #
        self._menu_bar = QtWidgets.QMenuBar()  # create menu bar object
        # assign tabs to menu bar
        self._file_menu = self._menu_bar.addMenu("&File")
        self._edit_menu = self._menu_bar.addMenu("&Edit")
        self._view_menu = self._menu_bar.addMenu("&View")
        self._tools_menu = self._menu_bar.addMenu("&Tools")
        self._help_menu = self._menu_bar.addMenu("&Help")
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # # # FILE # # #
        # system exit
        exit_action = QtWidgets.QAction("Exit", parent=self._file_menu)
        exit_action.triggered.connect(_exit)
        # final hooks
        self._file_menu.addAction(exit_action)
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # # # FUNCTIONS # # #
        # sub functions menu AB CONTROLS
        ab_controls = self._tools_menu.addMenu("&AB Controls")
        # l5x import
        import_l5x_action = QtWidgets.QAction("Import L5X", parent=ab_controls)
        import_l5x_action.triggered.connect(lambda: self._queue.put(Messages.IMPORT_L5X))
        # final hooks
        ab_controls.addAction(import_l5x_action)

        # sub functions menu GM CONTROLS
        functions_menu_gm_controls = self._tools_menu.addMenu("&GM Controls")
        # GM Eplan and logix creator tools
        calc_config_action = QtWidgets.QAction("Config Calculator", parent=functions_menu_gm_controls)
        calc_config_action.triggered.connect(lambda: self._queue.put(Messages.CALC_CONFIG))
        calc_to_eplan_action = QtWidgets.QAction("Calc2EPlan", parent=functions_menu_gm_controls)
        calc_to_eplan_action.triggered.connect(self.__debug_method__)
        calc_to_logix_action = QtWidgets.QAction("Calc2Logix", parent=functions_menu_gm_controls)
        calc_to_logix_action.triggered.connect(self.__debug_method__)
        calc_full_build_action = QtWidgets.QAction("Calc Full Build", parent=functions_menu_gm_controls)
        calc_full_build_action.triggered.connect(self.__debug_method__)
        # final hooks
        functions_menu_gm_controls.addAction(calc_config_action)
        functions_menu_gm_controls.addAction(calc_to_eplan_action)
        functions_menu_gm_controls.addAction(calc_to_logix_action)
        functions_menu_gm_controls.addAction(calc_full_build_action)

        # sub functions menu FILE EXPLORER
        functions_menu_file_explorer = self._tools_menu.addMenu("&File Explorer")
        # file content hints tool
        file_content_hints_action = QtWidgets.QAction("Find File w/ Content Hints", parent=functions_menu_file_explorer)
        # file_content_hints_action.triggered.connect()
        # final hooks
        functions_menu_file_explorer.addAction(file_content_hints_action)

        self.setMenuBar(self._menu_bar)  # set menu bar as menu bar to self
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # setup slot - signal connections
    def __bind_connections__(self):
        self.add_activity_to_stack.connect(self.__insert_interface_to_stack__)
        self.remove_activity_from_stack.connect(self.__remove_interface_from_stack__)

    # def __setup_layout__(self):
    #     # Create Dock
    #     self._dock = QtWidgets.QDockWidget("Controllers")
    #
    #     # Create Tree
    #     self.__setup_tree__()
    #     self._dock.setWidget(self._tree)
    #     # self._dock.setTitleBarWidget(self._collapsable_box)
    #
    #     # Add Dock Widget To Main Window
    #     self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self._dock)

    # def __setup_connections__(self):
    #     self._tree.itemDoubleClicked.connect(self.__handle_double_click__)

    # def __setup_tree__(self):
    #     self._tree = ContextualTree()
    #     self._tree.setHeaderLabels(['Name'])
    #
    #     # setup contextual items for this tree
    #     contextual_actions = [ContextualQAction('Add Logix PLC', self, self.__import_l5k__)]
    #     self._tree.contextual_actions = contextual_actions

    # def __setup_action_bar_slots__(self):
    #     self.ui.actionImport_L5K.triggered.connect(self.__import_l5k__)

    # def __import_l5k__(self):
    #     self._queue.put()
    #     progress_report.connect_to_session(obj=self, name='Import L5K')
    #     file_path = get_file_with_dialogue(HOME, L5K_KW)
    #     plc = processor_handler.import_l5k(file_path) if file_path else None
    #     progress_report.destroy_session()
    #     if not processor:
    #         return
    #     self.__new_tree_item__(plc, system_constants.get_image_by_name(PLC_ICON_NAME))

    # def __new_tree_item__(self, var, icon):
    #     new_item = ContextualTreeItem(title=var.name, parent=self._tree, var=var)
    #     new_item.setIcon(0, QtGui.QIcon(icon))
    #     self._tree.addTopLevelItem(new_item)

    # def __handle_double_click__(self, item):
    #     match type(item.var):
    #         case processor.RockwellProcessor:
    #             self.__call_processor_window__(item.var)
    #         case default:
    #             return

    # def __call_processor_window__(self, plc):
    #     processor_window = ProcessorWindow(plc=plc, parent=self)
    #     self._insert_interface_to_stack(processor_window)

    # def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
    #     contextMenu = QMenu(self)

    def open_file(self, get_env, file_type_args):
        return self._file_handler.open_file(get_env, file_type_args)

    def open_folder(self, get_env):
        return self._file_handler.open_folder(get_env)

    def save_file(self, get_env):
        return self._file_handler.save_file(get_env)

    def insert_interface_to_stack(self, interface, queue_ref):
        self._built_interface = None  # clear the built interface buffer
        self.add_activity_to_stack.emit(interface, queue_ref)  # emit the interface to build
        while not self._built_interface:  # wait for interface to be built
            continue
        return self._built_interface  # return the built interface !

    def __insert_interface_to_stack__(self, interface, queue_ref):
        built_interface = interface(queue_ref)  # create the object in this thread
        self._central_widget.insertWidget(0, built_interface)  # append this view to our central stack
        self._central_widget.setCurrentIndex(0)  # set new interface as active view
        # now we create a hook into our view tab
        new_view_action = QtWidgets.QAction(built_interface.windowTitle(), parent=self._view_menu)
        new_view_action.triggered.connect(lambda: self.__set_current_view__(built_interface))
        self._view_menu.addAction(new_view_action)
        self._built_interface = built_interface

    def remove_interface_from_stack(self, interface):
        self.remove_activity_from_stack.emit(interface)

    def __remove_interface_from_stack__(self, interface):
        interface.parent = None  # remove traces for garbage collection
        self._view_menu.removeAction(interface.__getattribute__('QAction'))  # remove object from view menu1

    def __set_current_view__(self, interface):
        self._central_widget.setCurrentWidget(interface)

    @staticmethod
    def __debug_method__():
        print('Whatever you did worked... Good job.')


class FileHandler(QtCore.QObject):  # pseudo context manager - allows separate threads to interface with our main thread safely (to get contextual GUI stuff, like use windows explorer to open files / folders)
    open_file_req = QtCore.pyqtSignal(str, str)
    open_folder_req = QtCore.pyqtSignal(str)
    save_file_req = QtCore.pyqtSignal(str)
    file_opened = QtCore.pyqtSignal(str)
    folder_opened = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._file_path = None
        self._folder_path = None
        self.open_file_req.connect(self.__open_file__)
        self.open_folder_req.connect(self.__open_folder__)
        self.save_file_req.connect(self.__save_file__)

    def open_file(self, get_env, file_type_args):
        self._file_path = None  # clear out memory before attempting to loop
        self.open_file_req.emit(get_env, file_type_args)
        while True:
            if not self._file_path:
                continue
            return self._file_path[0] if self._file_path[0] else None

    def save_file(self, get_env):
        self._file_path = None  # clear out memory before attempting to loop
        self.save_file_req.emit(get_env)
        while True:
            if not self._file_path:
                continue
            return self._file_path[0] if self._file_path[0] else None

    def open_folder(self, get_env):
        self._folder_path = None  # clear out memory before attempting to loop
        self.open_folder_req.emit(get_env)
        while True:
            if not self._folder_path:
                continue
            return self._folder_path if self._folder_path[0] else None

    def __open_file__(self, get_env, file_type_args):
        self._file_path = QtWidgets.QFileDialog.getOpenFileName(None, "Open File", os.getenv(get_env), file_type_args)

    def __save_file__(self, get_env):
        self._file_path = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", get_env)

    def __open_folder__(self, get_env):
        self._folder_path = QtWidgets.QFileDialog.getExistingDirectory(None, 'Open Directory', os.getenv(get_env))


# Load and Modify Existing Rockwell Processor Programs
class IndiconStudio(object):
    def __init__(self):
        self._exit: bool = False
        self._window: StudioMainWindowForm
        self._queue: queue.Queue
        self._activities: list = []

    def run(self):
        self.__init_systems__()

    def __init_systems__(self):
        # Create queue to communicate between GUI thread and engine thread
        _queue = queue.Queue()
        # create QT application
        app = QtWidgets.QApplication(sys.argv)
        # Create main window for application
        _window = StudioMainWindowForm(_queue)
        _window.show()
        _engine_thread = Thread(target=self.__program_loop__, args=(_window, _queue), daemon=True)
        _engine_thread.start()
        app.exec_()

    def __program_loop__(self, _window, _queue):
        while not self._exit:
            message = None
            try:
                message = _queue.get(timeout=0.1)
                match message:

                    case Messages.IMPORT_L5X:  # import an L5X into a logical processor
                        activity = self.__generic_activity_launch__(_window, RockwellProcessor)
                        activity.queue_ref.put(RockwellMessages.IMPORT_L5X)  # cast our command to our new object
                        self._activities.append(activity)  # create and append to memory stack (protect from garbage collection)

                    case Messages.CALC_CONFIG:  # configure a power calculator ( -> Excel Workbook)
                        activity = self.__generic_activity_launch__(_window, PowerCalculator)
                        self._activities.append(activity)

            except queue.Empty:
                pass

    @staticmethod
    def __generic_activity_launch__(_window, activity):
        g, q = activity.gui_class, queue.Queue()
        bg = _window.insert_interface_to_stack(g, q)
        return activity(bg, q)


# exit program
def _exit(self):
    exit(2)
