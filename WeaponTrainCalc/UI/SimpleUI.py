#
# Lucas Xu-Hill
# March 9, 2023
# https://realpython.com/python-pyqt-gui-calculator/

import sys
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

WINDOW_SIZE = 400
STATUS_BAR_HEIGHT = 35

class MotorCalcWindow(QMainWindow):
    """Motor Calc's main window (GUI or view)."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MotorParamCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createStatus()
        self._createInputFields()
        self._createButtons()

    def _createStatus(self):
        """Status bar"""
        self.display = QLineEdit()
        self.display.setFixedHeight(STATUS_BAR_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createInputFields(self):
        """"""
        inputsLayout = QFormLayout()
        input_fields = [
            ["MoI of Weapon", "kg-m^2", 0.0, 10.0, 1e-7],
            ["Motor Kv", "rpm/V", 0.0, 20000.0, 10],
            ["Max Stall Current", "A", 0.0, 100.0, 0.01],
            ["Max Voltage at Stall", "V", 0.0, 200.0, 0.01],
            ["Operational Voltage", "V", 0.0, 200.0, 0.01]
        ]

        for input_i in input_fields:
            tmpbox = QDoubleSpinBox()
            tmpbox.setSuffix(" " + input_i[1])
            tmpbox.setRange(input_i[2], input_i[3])
            tmpbox.setDecimals(int(max(0, -np.log10(input_i[4]))))
            inputsLayout.addRow(input_i[0], tmpbox)
        self.generalLayout.addLayout(inputsLayout)


    def _createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QVBoxLayout()
        buttonsLayout.addWidget(QPushButton("Calculate"))
        self.generalLayout.addLayout(buttonsLayout)

    def setStatusText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def getStatusText(self):
        return self.display.text()
    
    def clearStatus(self):
        self.setStatusText("")

if __name__ == "__main__":
    """Main function"""
    motorApp = QApplication([])
    motorCalcWindow = MotorCalcWindow()
    motorCalcWindow.show()
    sys.exit(motorApp.exec())

