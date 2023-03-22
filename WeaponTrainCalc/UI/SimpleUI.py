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
    QHBoxLayout,
    QWidget,
)

# Import our files
from os.path import dirname, abspath
src_dir_str = dirname(abspath(__file__))
sys.path.append(src_dir_str + '/../src/')
import GenerateGraphs

WINDOW_SIZE = 400
STATUS_BAR_HEIGHT = 35

class MotorCalcWindow(QMainWindow):
    """Motor Calc's main window (GUI or view)."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MotorParamCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.generalLayout = QVBoxLayout()
        self.input_boxes = {}
        centralWidget = QWidget(self)
        self.weaponSys = GenerateGraphs.WeaponSysModel()
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
            ["MoI of Weapon", "kg-m^2", 0.0, 10.0, 1e-7, 0.00056],
            ["Motor Kv", "rpm/V", 0.0, 20000.0, 10, 900],
            ["Max Stall Current", "A", 0.0, 100.0, 0.01, 37],
            ["Max Voltage at Stall", "V", 0.0, 200.0, 0.01, 14.8],
            ["Operational Voltage", "V", 0.0, 200.0, 0.01, 11.1],
            ["Target Gear Ratio", "(out:in)", 0.0, 10.0, 0.01, 0.8],
            ["Target Spin-up Time", "sec", 0.0, 10.0, 0.01, 4.0]
        ]

        for input_i in input_fields:
            self.input_boxes[input_i[0]] = QDoubleSpinBox()
            self.input_boxes[input_i[0]].setSuffix(" " + input_i[1])
            self.input_boxes[input_i[0]].setRange(input_i[2], input_i[3])
            self.input_boxes[input_i[0]].setDecimals(int(max(0, -np.log10(input_i[4]))))
            self.input_boxes[input_i[0]].setSingleStep(input_i[4])
            self.input_boxes[input_i[0]].setValue( input_i[5] )
            inputsLayout.addRow(input_i[0], self.input_boxes[input_i[0]])
        self.generalLayout.addLayout(inputsLayout)


    def _createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QHBoxLayout()
        button_close = QPushButton("Close All Graphs")
        button_calc = QPushButton("Calculate")
        button_close.clicked.connect(self.closeAllGraphs)
        button_calc.clicked.connect(self.calculateCurves)
        buttonsLayout.addWidget(button_close)
        buttonsLayout.addWidget(button_calc)
        self.generalLayout.addLayout(buttonsLayout)

    def setStatusText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def getStatusText(self):
        return self.display.text()
    
    def clearStatus(self):
        self.setStatusText("")

    def calculateCurves(self):
        self.setStatusText("Calculating...")
        print(self.input_boxes["Motor Kv"].value())
        print(self.input_boxes["Max Stall Current"].value())
        print(self.input_boxes["Max Voltage at Stall"].value())
        print(self.input_boxes["Operational Voltage"].value())
        self.weaponSys.initMotorModel(self.input_boxes["Motor Kv"].value(),
                                      self.input_boxes["Max Stall Current"].value(),
                                      self.input_boxes["Max Voltage at Stall"].value(),
                                      self.input_boxes["Operational Voltage"].value())
        print(self.input_boxes["Target Spin-up Time"].value())
        print(self.input_boxes["MoI of Weapon"].value())
        print(self.input_boxes["Target Gear Ratio"].value())
        energy, velocity = self.weaponSys.displayGraphs(self.input_boxes["Target Spin-up Time"].value(),
                                     self.input_boxes["MoI of Weapon"].value(),
                                     self.input_boxes["Target Gear Ratio"].value())
        self.setStatusText("Done! Results: {:.2f}J {:.2f}rad/sec".format(energy, velocity))
        # self.weaponSys.initMotorModel()

    def closeAllGraphs(self):
        # print('Closing all graphs')
        self.weaponSys.closeGraphs()

if __name__ == "__main__":
    """Main function"""
    motorApp = QApplication([])
    motorCalcWindow = MotorCalcWindow()
    motorCalcWindow.show()
    sys.exit(motorApp.exec())

