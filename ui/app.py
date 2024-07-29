import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from qt_material import apply_stylesheet

class ListModel(QAbstractTableModel):
    def __init__(self, data=None):
        super(ListModel, self).__init__()        
        self._data = data or []
        self._column_names = ["Frame ID", "Frame Data"]

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return 2  # Two columns
    

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._column_names[section]  # Return the column name
            if orientation == Qt.Vertical:
                return str(section + 1)  # Return the row number

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self._data[row][column]

    def appendData(self, value1, value2):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append([value1, value2])
        self.endInsertRows()


loader = QUiLoader()
app = QtWidgets.QApplication(sys.argv)
apply_stylesheet(app, theme='light_blue.xml')

window: QtWidgets.QMainWindow = loader.load("ui/app.ui", None)
# combo_style: str = """
#                             QComboBox {
#                                 border: 0px solid white;
#                                 color: black;
#                                 padding: 10px 0px 0px 50px;
#                             }
#                             QComboBox::drop-down {
#                                 subcontrol-origin: padding;
#                                 subcontrol-position: top right;
#                                 width: 15px;

#                                 border-left-width: 0px;
#                                 border-left-color: darkgray;
#                                 border-left-style: solid; /* just a single line */
#                                 border-top-right-radius: 3px; /* same radius as the QComboBox */
#                                 border-bottom-right-radius: 3px;
#                             }
#                             QComboBox::down-arrow { 
#                                 border:none;image: url(ui/angle-down.png);
#                                 width: 14px;height: 14px;
#                             }"""

# cboxInterface: QtWidgets.QComboBox = window.findChild(QtWidgets.QComboBox, "cboxInterface")
# cboxInterface.setStyleSheet(combo_style)
# cboxChannel: QtWidgets.QComboBox = window.findChild(QtWidgets.QComboBox, "cboxChannel")
# cboxChannel.setStyleSheet(combo_style)

clearButton: QtWidgets.QPushButton = window.findChild(QtWidgets.QPushButton, "clearButton")
saveButton: QtWidgets.QPushButton = window.findChild(QtWidgets.QPushButton, "saveButton")

frameDataTableView: QtWidgets.QTableView = window.findChild(QtWidgets.QTableView, "frameDataTableView")
frameDataTableView.setColumnWidth(50,250)
model = ListModel([["0x502", "Item 1b"], ["0x503", "Item 2b"], ["0x502", "Item 3b"]])
frameDataTableView.setModel(model)

statusBar: QtWidgets.QStatusBar = window.findChild(QtWidgets.QStatusBar, "statusbar")
statusBar.showMessage("waiting for CAN device...")
window.show()
app.exec()