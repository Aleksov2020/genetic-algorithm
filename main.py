import evolution_algorithm

import random
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QTextEdit, QCheckBox,
                             QApplication, QLabel, QTableWidget, QTableWidgetItem)


def print_to_file(text):
    file = open('result.txt', 'w')
    file.write(text)


class Gui(QWidget):

    def __init__(self):
        super().__init__()
        self.btna = None
        self.btns = None
        self.res = None
        self.dlab = None
        self.dopf = None
        self.dop = None
        self.result_label = None
        self.table = None
        self.initUI()

    def initUI(self):
        self.setTable()
        self.setButtons()
        # Resut
        self.result_label = QLabel("Result: ", self)
        self.result_label.move(500, 45)

        # Checkbox
        self.dlab = QLabel("View Process", self)
        self.dlab.move(500, 10)
        self.dop = QCheckBox(self)
        self.dop.setChecked(False)
        self.dop.move(600, 10)
        self.dop.stateChanged.connect(self.view_additional)

        # Additional Field
        self.dopf = QTextEdit(self)
        self.dopf.setGeometry(400, 60, 0, 0)

        self.res = QTextEdit(self)
        self.res.setGeometry(400, 60, 580, 420)
        self.res.setAlignment(QtCore.Qt.AlignCenter)

        self.setGeometry(500, 100, 1000, 500)
        self.setWindowTitle('EvolutionAlgorithm')
        self.show()

    def setButtons(self):
        # Button Start
        self.btns = QPushButton('Start', self)
        self.btns.move(20, 20)
        self.btns.clicked.connect(self.start)

        # Button Add
        self.btna = QPushButton('Add Point', self)
        self.btna.move(100, 20)
        self.btna.clicked.connect(self.add_row)

        # Button delete
        self.btna = QPushButton('Delete Point', self)
        self.btna.move(180, 20)
        self.btna.clicked.connect(self.del_row)

        # Button random
        self.btna = QPushButton('Random', self)
        self.btna.move(260, 20)
        self.btna.clicked.connect(self.random)

        # Button default
        self.btna = QPushButton('Default', self)
        self.btna.move(340, 20)
        self.btna.clicked.connect(self.default)

    def setTable(self):
        # define table
        self.table = QTableWidget(self)
        self.table.setGeometry(20, 60, 317, 420)
        self.table.setColumnCount(3)
        self.table.setRowCount(1)

        self.table.setHorizontalHeaderLabels(["X coordinates", "Y coordinates", "Point weight"])

        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)

    def view_additional(self, state):
        if not state:
            self.res.setGeometry(400, 60, 580, 420)
            self.dopf.setGeometry(400, 60, 0, 0)
        else:
            self.res.setGeometry(400, 60, 580, 180)
            self.dopf.setGeometry(400, 270, 580, 210)

    def start(self):
        rows = self.table.rowCount()
        vertexes = []
        flag = False
        for row in range(rows):
            try:
                vertexes.append([
                    int(self.table.item(row, 0).text()),
                    int(self.table.item(row, 1).text()),
                    float(self.table.item(row, 2).text())
                ])
            except:
                flag = True

        if flag:
            result = "Check your input! \nPoint coordinates must be integer."
            self.res.setText(str(result))
        else:
            result = evolution_algorithm.start(vertexes)
            self.res.setText(
                "Minimal route length = " + str(result["min"]) + '\n' +
                "Was found in gen with id = " + str(result["generation"]) + '\n' +
                result['route']
            )
            print_to_file(
                "Minimal route length = " + str(result["min"]) + '\n' +
                "Was found in gen with id - " + str(result["generation"]) + '\n' +
                result['route'])

    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

    def del_row(self):
        row_position = self.table.rowCount() - 1
        self.table.removeRow(row_position)

    def default(self):
        self.table.setItem(0, 0, QTableWidgetItem(str(380)))
        self.table.setItem(0, 1, QTableWidgetItem(str(540)))
        self.table.setItem(0, 2, QTableWidgetItem(str(1.5)))
        self.add_row()

        self.table.setItem(1, 0, QTableWidgetItem(str(390)))
        self.table.setItem(1, 1, QTableWidgetItem(str(200)))
        self.table.setItem(1, 2, QTableWidgetItem(str(2.25)))
        self.add_row()

        self.table.setItem(2, 0, QTableWidgetItem(str(210)))
        self.table.setItem(2, 1, QTableWidgetItem(str(50)))
        self.table.setItem(2, 2, QTableWidgetItem(str(1.75)))
        self.add_row()

        self.table.setItem(3, 0, QTableWidgetItem(str(15)))
        self.table.setItem(3, 1, QTableWidgetItem(str(140)))
        self.table.setItem(3, 2, QTableWidgetItem(str(3)))
        self.add_row()

        self.table.setItem(4, 0, QTableWidgetItem(str(860)))
        self.table.setItem(4, 1, QTableWidgetItem(str(630)))
        self.table.setItem(4, 2, QTableWidgetItem(str(1.25)))
        self.add_row()

        self.table.setItem(5, 0, QTableWidgetItem(str(670)))
        self.table.setItem(5, 1, QTableWidgetItem(str(500)))
        self.table.setItem(5, 2, QTableWidgetItem(str(0.25)))
        self.add_row()

        self.table.setItem(6, 0, QTableWidgetItem(str(600)))
        self.table.setItem(6, 1, QTableWidgetItem(str(730)))
        self.table.setItem(6, 2, QTableWidgetItem(str(1.35)))
        self.add_row()

        self.table.setItem(7, 0, QTableWidgetItem(str(1440)))
        self.table.setItem(7, 1, QTableWidgetItem(str(840)))
        self.table.setItem(7, 2, QTableWidgetItem(str(2.15)))
        self.add_row()

        self.table.setItem(8, 0, QTableWidgetItem(str(1220)))
        self.table.setItem(8, 1, QTableWidgetItem(str(700)))
        self.table.setItem(8, 2, QTableWidgetItem(str(0.5)))
        self.add_row()

        self.table.setItem(9, 0, QTableWidgetItem(str(1380)))
        self.table.setItem(9, 1, QTableWidgetItem(str(60)))
        self.table.setItem(9, 2, QTableWidgetItem(str(2)))

        self.add_row()

        self.table.setItem(10, 0, QTableWidgetItem(str(920)))
        self.table.setItem(10, 1, QTableWidgetItem(str(200)))
        self.table.setItem(10, 2, QTableWidgetItem(str(0.25)))
        self.add_row()

        self.table.setItem(11, 0, QTableWidgetItem(str(1080)))
        self.table.setItem(11, 1, QTableWidgetItem(str(800)))
        self.table.setItem(11, 2, QTableWidgetItem(str(2.5)))
        self.add_row()

        self.table.setItem(12, 0, QTableWidgetItem(str(860)))
        self.table.setItem(12, 1, QTableWidgetItem(str(630)))
        self.table.setItem(12, 2, QTableWidgetItem(str(1.25)))
        self.add_row()

        self.table.setItem(13, 0, QTableWidgetItem(str(480)))
        self.table.setItem(13, 1, QTableWidgetItem(str(400)))
        self.table.setItem(13, 2, QTableWidgetItem(str(1.15)))
        self.add_row()

        self.table.setItem(14, 0, QTableWidgetItem(str(190)))
        self.table.setItem(14, 1, QTableWidgetItem(str(800)))
        self.table.setItem(14, 2, QTableWidgetItem(str(0.75)))

    def random(self):
        for i in range(0, 50):
            self.table.setItem(i, 0, QTableWidgetItem(str(random.randint(10, 1800))))
            self.table.setItem(i, 1, QTableWidgetItem(str(random.randint(10, 680))))
            self.table.setItem(i, 2, QTableWidgetItem(str(random.randint(1, 3))))

            self.add_row()

        self.table.setItem(50, 0, QTableWidgetItem(str(random.randint(10, 1800))))
        self.table.setItem(50, 1, QTableWidgetItem(str(random.randint(10, 680))))
        self.table.setItem(50, 2, QTableWidgetItem(str(random.randint(1, 3))))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())
