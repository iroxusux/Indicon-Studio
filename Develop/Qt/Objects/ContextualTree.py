##################################################
# Program: qt_contectual_tree
##################################################

##################################################
# System Module Imports
##################################################

##################################################
# Add-In Module Imports
##################################################
import inspect

from PyQt5 import QtCore, QtGui, QtWidgets
##################################################
# Local Module Imports
##################################################

##################################################
# Constant Variable Definitions
##################################################

##################################################
# Global Variable Definitions
##################################################


class ContextualTree(QtWidgets.QTreeWidget):
    view_changed = QtCore.pyqtSignal(object)

    def __init__(self, title='', parent=None, var=None):
        super().__init__(parent)
        self._title = title
        self._visible_items = []
        self._contextual_actions = []
        self.itemExpanded.connect(self.__handle_item_expanded__)

    @property
    def contextual_actions(self):
        return self._contextual_actions

    @contextual_actions.setter
    def contextual_actions(self, val):
        self._contextual_actions = val

    @property
    def visible_items(self):
        return self._visible_items

    @visible_items.setter
    def visible_items(self, val):
        self.view_changed.emit(self._visible_items)
        self._visible_items = val

    def __handle_item_expanded__(self):
        [self.resizeColumnToContents(column) for column in range(self.columnCount())]

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        contextMenu = QtWidgets.QMenu(self)
        for action in self._contextual_actions:
            contextMenu.addAction(action)
        req_action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        for action in self._contextual_actions:
            if req_action == action:
                action.cmd()

    def viewportEvent(self, event: QtCore.QEvent) -> bool:
        return super().viewportEvent(event)

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        self.__get_visible_items()
        return super().wheelEvent(a0)

    def __get_visible_range__(self):
        top = QtCore.QPoint(0, 0)
        bottom = self.viewport().rect().bottomLeft()
        if self.indexAt(top).row() == -1:
            return []
        return range(self.indexAt(top).row(), self.indexAt(bottom).row()+1)

    def __get_visible_items(self):
        visible_range = [i for i in self.__get_visible_range__()]  # added variable to keep this to 1 emit
        visible_items = [self.topLevelItem(row) for row in visible_range if not self.topLevelItem(row) in self._visible_items]  # add each item as long as it isn't already in this list
        self.visible_items = visible_items  # single line update to keep emission to single instance
