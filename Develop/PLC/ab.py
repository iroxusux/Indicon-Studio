##################################################
# Program: plc
##################################################

##################################################
# System Module Imports
##################################################
from dataclasses import dataclass
from enum import Enum
import queue
##################################################
# Add-In Module Imports
##################################################
from Drivers.file_manager import read_file
from Drivers.list_funcs import find
from Drivers.object_manager import copy_instance
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
    IMPORT_L5X = 3
    CONNECT_TO_PLC = 10


# enum class for Rockwell File Decompression Type
class RockwellFileType(Enum):
    L5X = 2


# Rockwell specific data type class
class DataType:
    name = ''
    family = ''
    description = ''
    udt_class = ''
    members = []


# Dataclass for complex data types to allow easy-to-read deconstruction of typing as the file is decompressed
@dataclass
class DataTypeMember:
    name = None
    data_type = None
    dimension = None
    radix = None
    hidden = False
    ext_access = None
    description = ''


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
    L5X_FILE_TYPE = '.L5X(*.L5X)'

    PRE_DEFINED_TYPE_PATH = 'PLC/L5X Files/raPreDefinedDataTypes.L5X'

    L5X_KWORDS = {
        'add_on_instructions': ('<AddOnInstructionDefinitions>', '</AddOnInstructionDefinitions>'),
        'content_header': ('<RSLogix5000Content', '\n'),
        'controller': ('<Controller ', '>'),
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
        'processor_type': ('ProcessorType="', '" '),
        'programs': ('<Programs>', '</Programs>'),
        'radix': ('Radix="', '"'),
        'sw_major': ('MajorRev="', '" '),
        'sw_minor': ('MinorRev="', '" '),
        'tags': ('<Tags>', '</Tags>'),
        'target_type': ('TargetType="', '" '),
        'tasks': ('<Tasks>', '</Tasks>'),
        'udt_class': ('Class="', '"'),
    }

    EXIT_CODES = {
        'data_type_failure': 12,
        'module_failure': 13,
        'aoi_failure': 14,
        'tag_failure': 15,
        'program_failure': 16,
        'task_failure': 17,
    }

    gui_class = RockwellProcessorWindow

    class ExtractionType(Enum):
        Controller = 1
        Program = 2

    def __init__(self, gui_ref, queue_ref):
        super().__init__(gui_ref, queue_ref)
        self.data_types.extend(self.__compile_data_type_stream__(read_file(self.PRE_DEFINED_TYPE_PATH)))  # get pre defined data types before decompiling or creating anything
        self._hw_type = ''
        self._maj_sw_rev = 0
        self._minor_sw_rev = 0

    def __run__(self, message):
        match message:
            case RockwellMessages.IMPORT_L5X:
                self.__import_from_L5X__()

    def __import_from_L5X__(self):
        # # # GENERICS # # #
        path = get_file_with_dialogue('HOME', self.L5X_FILE_TYPE)  # get path
        if not path:  # do not continue without path
            return
        stream = read_file(path)
        contents_header = get_string_from_stream(begin=self.L5X_KWORDS['content_header'][0], end=self.L5X_KWORDS['content_header'][1], stream=stream)  # get header from L5X file (if it exists, that is)
        if not contents_header:  # do not continue without finding header
            return
        target_type = get_string_from_stream(begin=self.L5X_KWORDS['target_type'][0], end=self.L5X_KWORDS['target_type'][1], stream=contents_header, trim_start=True, trim_end=True)
        if not target_type:  # do not continue without a known target type
            return
        match target_type:
            case 'Controller':
                self.__extract_controller__(stream)
                return
            case 'Program':
                print('i found a program!')
                return
            case _:  # default argument
                print('i found nothing!')
                return
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # # # DATA TYPE # # #

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __extract_controller__(self, stream):
        # # # CONTROLLER INFO # # #
        controller_info = get_string_from_stream(begin=self.L5X_KWORDS['controller'][0], end=self.L5X_KWORDS['controller'][1], stream=stream)  # get header
        self._name = get_string_from_stream(begin=self.L5X_KWORDS['name'][0], end=self.L5X_KWORDS['name'][1], stream=controller_info, trim_start=True, trim_end=True)  # find name
        self._hw_type = get_string_from_stream(begin=self.L5X_KWORDS['processor_type'][0], end=self.L5X_KWORDS['processor_type'][1], stream=controller_info, trim_start=True, trim_end=True)  # find processor hardware type
        self._maj_sw_rev = int(get_string_from_stream(begin=self.L5X_KWORDS['sw_major'][0], end=self.L5X_KWORDS['sw_major'][1], stream=controller_info, trim_start=True, trim_end=True))  # find processor software major revision
        self._min_sw_rev = int(get_string_from_stream(begin=self.L5X_KWORDS['sw_minor'][0], end=self.L5X_KWORDS['sw_minor'][1], stream=controller_info, trim_start=True, trim_end=True))  # find processor software minor revision
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # # # USER DATA TYPES # # #
        self._user_data_types.extend(udt for udt in self.__compile_data_type_stream__(stream))
        print('waiting')
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __compile_data_type_stream__(self, udt_stream: str):
        udt_list = [self.__decompress_data_type__(s) for s in get_list_from_stream(begin=self.L5X_KWORDS['data_type'][0], end=self.L5X_KWORDS['data_type'][1], stream=udt_stream, trim_start=True, trim_end=True)]
        return self.__bind_members__(udt_list)

    def __decompress_data_type__(self, stream: str) -> DataType or None:
        # get information from stream
        name = get_string_from_stream(begin=self.L5X_KWORDS['name'][0], end=self.L5X_KWORDS['name'][1], stream=stream, trim_start=True, trim_end=True)
        family = get_string_from_stream(begin=self.L5X_KWORDS['family'][0], end=self.L5X_KWORDS['family'][1], stream=stream, trim_start=True, trim_end=True)
        udt_class = get_string_from_stream(begin=self.L5X_KWORDS['udt_class'][0], end=self.L5X_KWORDS['udt_class'][1], stream=stream, trim_start=True, trim_end=True)
        description = get_string_from_stream(begin=self.L5X_KWORDS['description'][0], end=self.L5X_KWORDS['description'][1], stream=stream, trim_start=True, trim_end=True)
        members = [self.__get_data_type_members__(stream) for stream in get_list_from_stream(begin=self.L5X_KWORDS['member'][0], end=self.L5X_KWORDS['member'][1], stream=stream, trim_start=True, trim_end=True)]

        if not name:  # if no name is found, return None
            return None

        # create new data type
        data_type = DataType()
        data_type.name = name
        data_type.family = family if family else None
        data_type.udt_class = udt_class if udt_class else None
        data_type.description = description if description else None
        data_type.members = members

        return data_type

    def __get_data_type_members__(self, stream) -> [DataTypeMember]:

        name = get_string_from_stream(begin=self.L5X_KWORDS['name'][0], end=self.L5X_KWORDS['name'][1], stream=stream, trim_start=True, trim_end=True)
        data_type = get_string_from_stream(begin=self.L5X_KWORDS['member_data_type'][0], end=self.L5X_KWORDS['member_data_type'][1], stream=stream, trim_start=True, trim_end=True)
        array_found = get_string_from_stream(begin='[', end=']', stream=data_type, trim_start=True, trim_end=True)
        dimension = get_string_from_stream(begin=self.L5X_KWORDS['dimension'][0], end=self.L5X_KWORDS['dimension'][1], stream=stream, trim_start=True, trim_end=True)
        radix = get_string_from_stream(begin=self.L5X_KWORDS['radix'][0], end=self.L5X_KWORDS['radix'][1], stream=stream, trim_start=True, trim_end=True)
        hidden = get_string_from_stream(begin=self.L5X_KWORDS['hidden'][0], end=self.L5X_KWORDS['hidden'][1], stream=stream, trim_start=True, trim_end=True)
        ext_access = get_string_from_stream(begin=self.L5X_KWORDS['external_access'][0], end=self.L5X_KWORDS['external_access'][1], stream=stream, trim_start=True, trim_end=True)
        description = get_string_from_stream(begin=self.L5X_KWORDS['description'][0], end=self.L5X_KWORDS['description'][1], stream=stream, trim_start=True, trim_end=True)

        temp_member = DataTypeMember()
        temp_member.name = name
        temp_member.data_type = data_type
        temp_member.dimension = dimension
        temp_member.radix = radix
        temp_member.hidden = hidden
        temp_member.ext_access = ext_access
        temp_member.description = description

        if not array_found:
            return temp_member

        if array_found:
            member_list = []
            array_location = temp_member.data_type.find('[')
            array_size = int(array_found)
            for _ in range(array_size):
                new_member = copy_instance(DataTypeMember(), temp_member)
                new_member.name = f'{new_member.name}[{_}]'
                new_member.data_type = new_member.data_type[:array_location]
                member_list.append(new_member)
            return member_list

    def __bind_members__(self, udt_list):
        for udt in udt_list:
            for member in udt.members:
                if type(member) is list:  # if the member is an array...
                    for x in member:
                        self.__find_existing_data_type__(x, udt_list)
                if type(member) is DataTypeMember:  # if the member is not an array...
                    self.__find_existing_data_type__(member, udt_list)
        return udt_list

    def __find_existing_data_type__(self, member, user_data_type_list):
        data_type = find('name', member.data_type, self._data_types)  # search pre defines
        if data_type:
            member.data_type = data_type
            return
        data_type = find('name', member.data_type, user_data_type_list)  # search run-time defines
        if data_type:
            member.data_type = data_type
            return
        print(f'No existing data type found for : {member}')
        print(f'Member name : {member.name}')
        print(f'Member data type : {member.data_type}')

