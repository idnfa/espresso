import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication, QTableWidgetItem, QHeaderView, QVBoxLayout


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.con = None
        self.tableWidget = None
        uic.loadUi('main.ui', self)

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Название сорта', 'обжарка', 'помол', 'вкусовые характеристики', 'цена', 'объем упаковки']
        )
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        self.con = sqlite3.connect('coffee.sqlite')
        cur = self.con.cursor()
        cur.execute("""
            SELECT ID, name, roasting, grinding, taste, price, volume FROM coffee
        """)
        rows = cur.fetchall()
        self.tableWidget.setRowCount(0)
        for row in rows:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for col, item in enumerate(row):
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, col, QTableWidgetItem(str(item)))
                if col == 0:
                    self.tableWidget.item(self.tableWidget.rowCount() - 1, col).setFlags(Qt.ItemFlag.ItemIsEditable)

        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
