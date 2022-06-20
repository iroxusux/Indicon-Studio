##################################################
# Program: plc
##################################################

##################################################
# System Module Imports
##################################################
from enum import Enum
import queue
##################################################
# Add-In Module Imports
##################################################
from Drivers.file_manager import read_file
from Drivers.string_funcs import get_string_from_stream, get_list_from_stream, complex_clear, find_coords, find_variable_ending
from Drivers.PyQt_activity import BaseActivityWindow
from PyQt5 import QtWidgets
from Qt.Objects.ContextualTree import ContextualTree
from Qt.UiFunctions.open import get_file_with_dialogue
##################################################
# Local Module Imports
##################################################
from PLC.plc import PLC
##################################################
# Constant Variable Definitions
##################################################

##################################################
# Global Variable Definitions
##################################################


# enum class to communicate efficiently between gui and "engine"
class RockwellMessages(Enum):
    UI_LOADED = 1
    IMPORT_L5K = 2
    IMPORT_L5X = 3
    CONNECT_TO_PLC = 10


# enum class for Rockwell File Decompression Type
class RockwellFileType(Enum):
    L5K = 1
    L5X = 2


# processor window GUI
class RockwellProcessorWindow(BaseActivityWindow):
    def __init__(self,
                 queue_ref: [queue.Queue],
                 parent=None):
        super().__init__(queue_ref=queue_ref,
                         parent=parent)

    def __setup_layout__(self):
        # setup individual items first
        self.__setup_name_box__()
        self.__setup_ip_table__()
        self.__setup_tag_tree__()
        self.__setup_data_type_tree__()
        # self.__setup_watch_table_tree__()

        # setup layout
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.addWidget(self._plc_name_box)
        self._layout.addWidget(self._plc_ip_box)
        self._layout.addWidget(self._tag_tree)
        self._layout.addWidget(self._data_type_tree)
        # self._layout.addWidget(self._watch_table_tree)

        # bind layout
        self.setLayout(self._layout)

    def __setup_name_box__(self):
        # group box for name
        self._plc_name_box = QtWidgets.QGroupBox('Processor Name')
        self._plc_name_box.setMaximumWidth(200)
        self._plc_name_box.setMaximumHeight(60)
        self.plc_name_label = QtWidgets.QLabel()
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.plc_name_label)
        self._plc_name_box.setLayout(vbox)

    def __setup_ip_table__(self):
        # group box for ip address with button to hot connect to processor
        self._plc_ip_box = QtWidgets.QGroupBox('IP Address')
        self._plc_ip_box.setMaximumWidth(200)
        self._plc_ip_box.setMaximumHeight(60)
        self._plc_ip_label = QtWidgets.QLabel()

        # push-button to hot connect to plc
        self._ip_connect = QtWidgets.QPushButton()
        self._ip_connect.setText('Connect To PLC')
        self._ip_connect.clicked.connect(lambda: self._queue.put(RockwellMessages.CONNECT_TO_PLC))
        # create horizontal layout box for ip stuff
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self._plc_ip_label)
        hbox.addWidget(self._ip_connect)
        self._plc_ip_box.setLayout(hbox)

    def __setup_tag_tree__(self):
        # tree widget for tags
        self._tag_tree = ContextualTree()
        self._tag_tree.setHeaderLabels(['Tags', 'Value', 'Data Type'])
        self._tag_tree.setColumnCount(3)
        # for tag in self._plc.tag_handler.tags:  # add plc tags to tree table
        #     new_item = ContextualTreeItemTag(parent=self._tag_tree, tag=tag)
        #     self._tag_tree.addTopLevelItem(new_item)
        # self._tag_tree.resizeColumnToContents(0)

        # setup contextual items for this tree
        # contextual_actions = [ContextualQAction('Add to watch table', self, self.__add_from_tag_tree_to_watch_table__)]
        # self._tag_tree.contextual_actions = contextual_actions

        # self._tag_tree.view_changed.connect(self.__update_live_plc_feed_table__)  # update what tags are requested from the PLC when on live feed

    def __setup_data_type_tree__(self):
        # tree widget for data_types
        self._data_type_tree = ContextualTree()
        self._data_type_tree.setHeaderLabels(['Data Types'])
        # for data_type in self._plc.data_type_handler.data_types:
        #     new_item = ContextualTreeItem(data_type.name, parent=self._data_type_tree, var=None)
        #     new_item.setIcon(0, QtGui.QIcon(system_constants.get_image_by_name(DATA_ICON_NAME)))
        #     self._data_type_tree.addTopLevelItem(new_item)
    #
    # def __setup_watch_table_tree__(self):
    #     # tree widget for watch table
    #     self._watch_table_tree = ContextualTree()
    #     self._watch_table_tree.setHeaderLabels(['Watch Table', 'Value', 'Data Type'])
    #     self._watch_table_tree.setColumnCount(3)
    #
    # def __update_plc_connection_indicator__(self):
    #     self._ip_connect.setStyleSheet("background-color: green") if self._plc.connection_handler.connected else self._ip_connect.setStyleSheet("background-color: red")
    #
    # def __set_data_points_for_plc_on_connect__(self):
    #     self._plc.send_data_points_to_connection_handler()
    #     self._plc.connection_handler.connect_to_plc()
    #
    # def __add_from_tag_tree_to_watch_table__(self):
    #     selected_items = self._tag_tree.selectedItems()
    #     for item in selected_items:
    #         new_item = ContextualTreeItemTag(parent=self._watch_table_tree, tag=item.var)
    #         new_item.setIcon(0, QtGui.QIcon(system_constants.get_image_by_name(SUNGLASSES_ICON_NAME)))
    #         self._watch_table_tree.addTopLevelItem(new_item)
    #     self._watch_table_tree.sortItems(0, QtCore.Qt.AscendingOrder)
    #     self._watch_table_tree.resizeColumnToContents(0)
    #
    # def __update_live_plc_feed_table__(self, tree_items: [ContextualTreeItemTag]):
    #     tags = [item.var for item in tree_items if type(item is RockwellTag)]
    #     self._plc.connection_handler.visible_tag_items = tags
    #
    # def __test_func__(self):
    #     print('you did it, idiot... Good job....')


# rockwell type PLC handling
class RockwellProcessor(PLC):
    L5K_FILE_TYPE = '.L5K(*.L5K)'
    L5X_FILE_TYPE = '.L5X(*.L5X)'

    L5K_KWORDS = {
        'controller': ['CONTROLLER', 'END_CONTROLLER'],
        'comm_path': ['CommPath := ', '",'],
        'data_type': ['DATATYPE', 'END_DATATYPE'],
        'description': 'Description := ',
        'family': 'FamilyType := ',
        'header': ['(', ')', ',']
    }

    L5X_KWORDS = {
        'add_on_instructions': ('<AddOnInstructionDefinitions>', '</AddOnInstructionDefinitions>'),
        'data_type': ('<DataType ', '</DataType>'),
        'data_types': ('<DataTypes>', '</DataTypes>'),
        'description': ('<Description>', '</Description>'),
        'description_header': ('<![CDATA[', ']]>'),
        'dimension': ('Dimension="', '"'),
        'external_access': ('ExternalAccess="', '"'),
        'family': ('Family="', '"'),
        'hidden': ('Hidden="', '"'),
        'member': ('<Member ', '</Member>'),
        'member_data_type': ('DataType="', '"'),
        'members': ('<Members>', '</Members>'),
        'module': ('<Module ', '</Module>'),
        'modules': ('<Modules>', '</Modules'),
        'name': ('Name="', '"'),
        'programs': ('<Programs>', '</Programs>'),
        'radix': ('Radix="', '"'),
        'tags': ('<Tags>', '</Tags>'),
        'tasks': ('<Tasks>', '</Tasks>'),
        'udt_class': ('Class="', '"'),
    }

    ATTR_BEGIN = 0
    ATTR_END = 1

    EXIT_CODES = {
        'data_type_failure': 12,
        'module_failure': 13,
        'aoi_failure': 14,
        'tag_failure': 15,
        'program_failure': 16,
        'task_failure': 17,
    }

    gui_class = RockwellProcessorWindow

    def __init__(self, gui_ref, queue_ref):
        super().__init__(gui_ref, queue_ref)

    def __run__(self, message):
        match message:
            case RockwellMessages.UI_LOADED:
                print('yeah i get it')
            case RockwellMessages.IMPORT_L5K:
                self.__import_from_L5K__()
            case RockwellMessages.IMPORT_L5X:
                self.__import_from_L5X__()

    def __import_from_L5K__(self):  # this is a less efficient way to grab a processor, L5X is recommended
        # # # GENERICS # # #
        path = get_file_with_dialogue('HOME', self.L5K_FILE_TYPE)  # get path
        if not path:  # do not continue without path
            return
        raw_file = read_file(path)  # read file from path
        valid = get_list_from_stream(self.L5K_KWORDS['controller'][0], self.L5K_KWORDS['controller'][1], raw_file)
        if not valid:  # do not continue if file is not valid
            return
        self._name = get_string_from_stream(self.L5K_KWORDS['controller'][0], '(', raw_file, trim_start=True, trim_end=True)
        if not self._name:  # do not continue without a name (file must be invalid, it seems)
            return
        self._ip_address = get_string_from_stream(self.L5K_KWORDS['comm_path'][0], self.L5K_KWORDS['comm_path'][1], raw_file, trim_start=True, trim_end=True).split('\\')[1]
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # # # DATA TYPE # # #
        self._data_types = [self.__decompress_data_type__(RockwellFileType.L5K, stream) for stream in get_list_from_stream(self.L5K_KWORDS['data_type'][0], self.L5K_KWORDS['data_type'][1], raw_file, trim_start=True, trim_end=True)]
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __import_from_L5X__(self):
        print('not here yet, bud')
        return

    def __decompress_data_type__(self, file_type: [RockwellFileType], stream: str):
        data_type = RockwellProcessor.DataType()
        match file_type:
            case RockwellFileType.L5K:  # decompress data type from L5K

                # clear out white spaces, tabs, new line
                local_stream = complex_clear(stream, self.L5K_KWORDS['data_type'][1], self.L5K_KWORDS['data_type'][0], tabs=True, new_line=True)

                # Separate Header Onto Single Line For Ease Of Parsing
                header_coords = find_coords(self.L5K_KWORDS['header'][0], self.L5K_KWORDS['header'][1], local_stream)
                if not header_coords:  # if the header cannot be found, the data must be corrupted or improper
                    return None

                local_stream = local_stream[:header_coords[1]] + '\n' + local_stream[header_coords[1]:]
                header_stream, child_stream = local_stream.split('\n')  # With the stream formatted properly, split into 2 instances (Header and Child)

                # Search For Name
                name_index = header_stream.find(' ')
                if name_index == -1:
                    return None  # Cannot continue without a proper named to assign
                data_type.name = header_stream[:name_index]

                # attempt to find hidden flag in name - although, i don't think data-types have this...
                hidden_find = data_type.name.find('ZZZZZZZZZZ')
                hidden = True if hidden_find != -1 else False

                # Search For Description
                data_type.description = find_variable_ending(header_stream, self.L5K_KWORDS['description'], self.L5K_KWORDS['header'][2], self.L5K_KWORDS['header'][1], trim_start=True, trim_end=True)

                # Search For Family
                data_type.family = find_variable_ending(header_stream, self.L5K_KWORDS['family'], self.L5K_KWORDS['header'][2], self.L5K_KWORDS['header'][1], trim_start=True, trim_end=True)

                # Split Children To Be Parsed Later
                data_type.members = child_stream.split(';')

                return data_type

            case RockwellFileType.L5X:
                # get name
                data_type.name = get_string_from_stream(begin=self.L5X_KWORDS['name'][0],
                                                                       end=self.L5X_KWORDS['name'][1], stream=stream,
                                                                       trim_start=True, trim_end=True)

                # get family
                data_type.family = get_string_from_stream(begin=self.L5X_KWORDS['family'][0],
                                                                         end=self.L5X_KWORDS['family'][1], stream=stream,
                                                                         trim_start=True, trim_end=True)

                # get udt class
                data_type.udt_class = get_string_from_stream(begin=self.L5X_KWORDS['udt_class'][0],
                                                                            end=self.L5X_KWORDS['udt_class'][1],
                                                                            stream=stream,
                                                                            trim_start=True, trim_end=True)
                # get description
                data_type.description = get_string_from_stream(begin=self.L5X_KWORDS['description'][0],
                                                                              end=self.L5X_KWORDS['description'][1],
                                                                              stream=stream, trim_start=True,
                                                                              trim_end=True)

                data_type.description.replace(self.L5X_KWORDS['description_header'][0], '')  # remove bogus header
                data_type.description.replace(self.L5X_KWORDS['description_header'][1], '')  # remove bogus footer

                # get members
                # data_type.members = [self._get_data_type_members(member_stream) for member_stream in
                #                      string_handler.get_list_from_stream(
                #                          begin=KWORDS['member'][ATTR_BEGIN],
                #                          end=KWORDS['member'][ATTR_END], stream=stream,
                #                          trim_start=True, trim_end=True)]
                return data_type

    class DataType:
        name = ''
        family = ''
        description = ''
        udt_class = ''
        members = []

