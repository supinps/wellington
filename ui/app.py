import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader

loader = QUiLoader()
app = QtWidgets.QApplication(sys.argv)
window: QtWidgets.QMainWindow = loader.load("ui/app.ui", None)
combo_style: str = """
                            QComboBox {
                                border: 0px solid white;
                                border-bottom: 2px solid rgba(0, 0, 0, 60);
                                color: black;
                                padding: 10px 0px 0px 50px;
                            }
                            QComboBox::drop-down {
                                subcontrol-origin: padding;
                                subcontrol-position: top right;
                                width: 15px;

                                border-left-width: 0px;
                                border-left-color: darkgray;
                                border-left-style: solid; /* just a single line */
                                border-top-right-radius: 3px; /* same radius as the QComboBox */
                                border-bottom-right-radius: 3px;
                            }
                            QComboBox::down-arrow { 
                                border:none;image: url(ui/angle-down.png);
                                width: 14px;height: 14px;
                            }"""
cboxInterface: QtWidgets.QComboBox = window.findChild(QtWidgets.QComboBox, "cboxInterface")
cboxInterface.setStyleSheet(combo_style)
cboxChannel: QtWidgets.QComboBox = window.findChild(QtWidgets.QComboBox, "cboxChannel")
cboxChannel.setStyleSheet(combo_style)
window.show()
app.exec()