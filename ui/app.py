import sys
import os
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QObject, Slot, Signal
from PySide6.QtGui import QIcon, QPixmap
from qt_material import apply_stylesheet
import pandas as pd
from datetime import datetime as dt

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
    
    def saveFrames(self):
        df = pd.DataFrame(columns=self._column_names, data=self._data)
        td = dt.today()
        tt = td.time()
        df.to_csv(f"frames_{td.year}{td.month}{td.day}_{tt.hour}{tt.minute}{tt.second}.csv", index=False)

class UI(QObject):
    busData = Signal(int, int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.loader = QUiLoader()
        self.app = QtWidgets.QApplication(sys.argv)
        apply_stylesheet(self.app, theme="light_blue.xml")
        self.window: QtWidgets.QMainWindow = self.loader.load("ui/app.ui", None)
        self.cBoxInterface: QtWidgets.QComboBox = self.window.findChild(
            QtWidgets.QComboBox, "cBoxInterface"
        )
        self.cBoxChannel: QtWidgets.QComboBox = self.window.findChild(
            QtWidgets.QComboBox, "cBoxChannel"
        )
        self.connectButton: QtWidgets.QPushButton = self.window.findChild(
            QtWidgets.QPushButton, "connectButton"
        )
        self.path = os.path.dirname(__file__)
        pixmapConnect = QPixmap(os.path.join(self.path, "connected.png"))
        pixmapDisconnect = QPixmap(os.path.join(self.path, "disconnected.png"))
        self.iconConnect = QIcon(pixmapConnect)
        self.iconDisconnect = QIcon(pixmapDisconnect)
        self.connectButton.setIcon(self.iconDisconnect)
        self.connectButton.setStyleSheet("border:none; padding-top: 5px;")
        self.connectButton.setCheckable(True)
        self.connectButton.setChecked(False)
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
        self.channels = None
        self.cBoxInterface.currentIndexChanged.connect(self.update_channels)
        self.go_back_to_defauilt_msg = False
        self.connectButton.clicked.connect(self.onConnectClicked)
        self.startBtn.clicked.connect(self.onStartBtnClicked)
        self.statusBar.messageChanged.connect(self.onMessageChanged)
        self.connectButton.toggled.connect(self.onConnectBtnToggled)
        self.initialization()
        self.saveButton.clicked.connect(self.model.saveFrames)

    def initialization(self):
        self.startBtn.setEnabled(False)
        self.connectButton.setEnabled(True)

    def start(self):
        self.window.show()
        self.app.exec()

    def add_new_frame(self, frameID: str, frameData: str) -> None:
        self.model.appendData(frameID, frameData)
        self.frameDataTableView.scrollToBottom()

    def populateFrameNames(self, frameIDList: list):
        row_count = len(frameIDList)
        col_count = len(frameIDList[0]) if row_count > 0 else 0

        self.frameIDTable.setRowCount(row_count)
        self.frameIDTable.setColumnCount(col_count)

        for row in range(row_count):
            for col in range(col_count):
                self.frameIDTable.setItem(
                    row, col, QtWidgets.QTableWidgetItem(str(frameIDList[row][col]))
                )

    @Slot(bool)
    def onConnectBtnToggled(self, checked: bool):
        if checked:
            self.connectButton.setIcon(self.iconConnect)
        else:
            self.connectButton.setIcon(self.iconDisconnect)

    @Slot(int, int)
    def onConnectClicked(self):
        self.busData.emit(
            self.cBoxInterface.currentIndex(), self.cBoxChannel.currentIndex()
        )

    @Slot()
    def onStartBtnClicked(self):
        self.startBtn.setText("Stop")

    @Slot(bool)
    def handle_Device(self, enable: bool):
        self.startBtn.setEnabled(enable)
        self.connectButton.setEnabled(not enable)
        if enable:
            self.go_back_to_defauilt_msg = False
            self.statusBar.showMessage("CAN device connected successfully")
        else:
            self.statusBar.showMessage("CAN device connection failed", timeout=5000)
            self.go_back_to_defauilt_msg = True

    @Slot()
    def onMessageChanged(self):
        if self.go_back_to_defauilt_msg:
            self.statusBar.showMessage("waiting for CAN device...")
            self.go_back_to_defauilt_msg = False

    def add_interfaces(self, interfaces: list[str]):
        self.cBoxInterface.addItems(interfaces)

    def update_channels(self, index=0):
        if self.channels != None:
            self.cBoxChannel.clear()
            self.cBoxChannel.addItems(self.channels[index])

    def get_channel_list(self, channel_list: list[str]):
        self.channels = channel_list


if __name__ == "__main__":
    ui = UI()
    ui.start()
    ui.add_new_frame("0x403", "22.3")
