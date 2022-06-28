##################################################
# Program: Calculator Selection
##################################################

##################################################
# System Module Imports
##################################################
from enum import Enum
import queue
##################################################
# Add-In Module Imports
##################################################
from PyQt5 import QtCore, QtGui, QtWidgets
##################################################
# Local Module Imports
##################################################

##################################################
# Constant Variable Definitions
##################################################
CALC_DICT_KW_ECS_NUM = 0
CALC_DICT_KW_DESC = 1
CALC_DICT_KW_480_CIRCUITS = 2
CALC_DICT_KW_120_ABOVE_TRANSFORMER_CIRCUITS = 3
CALC_DICT_KW_120_BELOW_TRANSFORMER1_CIRCUITS = 4
CALC_DICT_KW_120_BELOW_TRANSFORMER2_CIRCUITS = 5
CALC_DICT_KW_24_ABOVE_CIRCUITS = 6
CALC_DICT_KW_24_BELOW_CIRCUITS = 7
CALC_DICT_KW_FILE_NAME = 8
CALC_DICT_KW_REV = 9

##################################################
# Global Variable Definitions
##################################################
Calculator_dict = {
    'ECS-4335': ['ECS-4335-TT', '3KVA Remote Power Panel', '0', '0', '5', '0', '0', '0', 'ECS-4335-TT_RevI(2021-09-28)', 'I'],
    'ECS-4336': ['ECS-4336-TT', '5KVA Remote Power Panel', '0', '0', '7', '0', '0', '0', 'ECS-4336-TT_RevH(2021-09-23)', 'H'],
    'ECS-4830': ['ECS-4830', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'ECS-4830_RevF(2020-08-27)', 'F'],
    'ECS-5100': ['ECS-5100-TT', '30AMP PDP', '3', '4', '4', '0', '0', '0', 'ECS-5100-TT_RevB(2021-09-23)', 'B'],
    'ECS-5101': ['ECS-5101-BB-AA-TT', '60AMP PDP', '4', '4', '4', '0', '0', '0', 'ECS-5101-BB-AA-TT_RevB(2021-09-24)', 'B'],
    'ECS-5103': ['ECS-5103-CC-BB-AA-TT', '100AMP PDP', '11', '4', '4', '0', '0', '0', 'ECS-5103-CC-BB-AA-TT_RevB(2021-09-24)', 'B'],
    'ECS-5105': ['ECS-5105-DD-CC-BB-AA-TT', '200AMP PDP', '17', '6', '9', '0', '0', '0', 'ECS-5105-DD-CC-BB-AA-TT_RevB(2021-09-24)', 'B'],
    'ECS-5106': ['ECS-5106-BB-AA-TT', '200AMP PDP', '18', '6', '9', '0', '0', '0', 'ECS-5106-BB-AA-TT_RevB(2021-09-24)', 'B'],
    'ECS-5107': ['ECS-5107-DD-CC-BB-AA-TT', '400AMP PDP', '16', '6', '9', '0', '0', '0', 'ECS-5107-DD-CC-BB-AA-TT_RevB(2021-09-24)', 'B'],
    'ECS-5108': ['ECS-5108-DD-CC-BB-AA-TT', '400AMP PDP', '17', '6', '9', '0', '0', '0', 'ECS-5108-DD-CC-BB-AA-TT_RevB(2021-09-24)', 'B'],
    'ECS-5109': ['ECS-5109-BB-AA-TT', '400AMP PDP', '18', '6', '9', '0', '0', '0', 'ECS-5109-BB-AA-TT_RevB(2021-09-24)', 'B'],
    'ECS-5110': ['ECS-5110-UU-VV', '400AMP Weld PDP', '5', '0', '0', '0', '0', '0', 'ECS-5110-UU-VV_RevB(2021-09-30)', 'B'],
    'ECS-5115': ['ECS-5115-UU-VV', '400AMP Weld PDP', '15', '0', '0', '0', '0', '0', 'ECS-5115-UU-VV_RevB(2021-09-28)', 'B'],
    'ECS-5119': ['ECS-5119-CC-BB-AA', '100AMP CONTROL POWER DISTRIBUTION SUB PANEL', '27', '0', '0', '0', '0', '0', 'ECS-5119-CC-BB-AA_Rel(2022-04-27)', 'Rel'],
    'ECS-5120': ['ECS-5120-BB-AA-MM-TT', '60AMP COMBO MCP AND PDP', '4', '2', '2', '0', '3', '6', 'ECS-5120-BB-AA-MM-TT_RevB(2021-09-24)', 'B'],
    'ECS-5121': ['ECS-5121-BB-AA-TT', '60AMP COMBO MCP AND PDP', '4', '2', '2', '0', '3', '6', 'ECS-5121-BB-AA-TT_RevB(2021-09-24)', 'B'],
    'ECS-5123': ['ECS-5123-CC-BB-AA-TT', '100AMP COMBO MCP AND PDP', '4', '2', '2', '0', '3', '6', 'ECS-5123-CC-BB-AA-TT_RevB(2021-09-24)', 'B'],
    'ECS-5137': ['ECS-5137-TT', 'PDP 3KVA 120V CONTROL POWER / 24V PLC POWER', '0', '0', '3', '0', '3', '0', 'ECS-5137-TT_RevA(2021-09-24)', 'A'],
    'ECS-5138': ['ECS-5138-TT', 'PDP 5KVA 120V CONTROL POWER / 24V PLC POWER', '0', '0', '6', '0', '3', '0', 'ECS-5138-TT_Rel(2021-10-14)', 'Rel'],
}
for key in Calculator_dict['ECS-4335']:
    print(key)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1037, 574)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(660, 520, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(420, 350, 175, 95))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.formLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.formLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.pushButton)
        self.pushButton_3 = QtWidgets.QPushButton(self.formLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.pushButton_3)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(390, 260, 231, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_2.setText(_translate("Dialog", "Open .PDF"))
        self.pushButton.setText(_translate("Dialog", "Create Calculator"))
        self.pushButton_3.setText(_translate("Dialog", "Panel Info"))
        self.comboBox.setItemText(0, _translate("Dialog", "New Item"))
        self.comboBox.setItemText(1, _translate("Dialog", "New Item"))
        self.comboBox.setItemText(2, _translate("Dialog", "New Item"))
        self.comboBox.setItemText(3, _translate("Dialog", "New Item"))
        self.comboBox.setItemText(4, _translate("Dialog", "New Item"))
        self.comboBox.setItemText(5, _translate("Dialog", "New Item"))
