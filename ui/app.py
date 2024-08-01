import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QObject, Slot
from qt_material import apply_stylesheet

__all__ = ["UI"]


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

    def appendData(self, value1: str, value2: str) -> None:
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append([value1, value2])
        self.endInsertRows()


class UI(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.loader = QUiLoader()
        self.app = QtWidgets.QApplication(sys.argv)
        apply_stylesheet(self.app, theme="light_blue.xml")
        self.window: QtWidgets.QMainWindow = self.loader.load("ui/app.ui", None)
        self.startBtn: QtWidgets.QPushButton = self.window.findChild(
            QtWidgets.QPushButton, "startButton"
        )
        self.clearButton: QtWidgets.QPushButton = self.window.findChild(
            QtWidgets.QPushButton, "clearButton"
        )
        self.saveButton: QtWidgets.QPushButton = self.window.findChild(
            QtWidgets.QPushButton, "saveButton"
        )
        self.frameDataTableView: QtWidgets.QTableView = self.window.findChild(
            QtWidgets.QTableView, "frameDataTableView"
        )
        self.frameDataTableView.setColumnWidth(50, 250)
        self.model = ListModel(
            [["0x502", "Item 1b"], ["0x503", "Item 2b"], ["0x502", "Item 3b"]]
        )
        self.frameDataTableView.setModel(self.model)
        self.statusBar: QtWidgets.QStatusBar = self.window.findChild(
            QtWidgets.QStatusBar, "statusbar"
        )
        self.frameIDTable: QtWidgets.QTableWidget = self.window.findChild(
            QtWidgets.QTableWidget, "frameIDTable"
        )
        self.frameIDTable.setColumnCount(2)
        self.frameIDTable.setRowCount(10)
        self.frameIDTable.setHorizontalHeaderLabels(["Frame ID", "Frame Name"])
        self.statusBar.showMessage("waiting for CAN device...")

    def start(self):
        self.window.show()
        self.app.exec()

    def add_new_frame(self, frameID: str, frameData: str) -> None:
        self.model.appendData(frameID, frameData)
    
    def populateFrameNames(self, frameIDList: list):
        row_count = len(frameIDList)
        col_count = len(frameIDList[0]) if row_count > 0 else 0

        self.frameIDTable.setRowCount(row_count)
        self.frameIDTable.setColumnCount(col_count)

        for row in range(row_count):
            for col in range(col_count):
                self.frameIDTable.setItem(row, col, QtWidgets.QTableWidgetItem(str(frameIDList[row][col])))

    @Slot(bool)
    def enable_start_button(self, enable):
        self.startBtn.setEnabled(enable)
        print(f"{self.startBtn.isEnabled()=}")


if __name__ == "__main__":
    ui = UI()
    ui.start()
    ui.add_new_frame("0x403", "22.3")
