import sys

import sqlite3
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.result = [1]
        self.pixmap = QPixmap('data/coffee.jpg')
        self.image_l.setPixmap(self.pixmap)
        self.con = sqlite3.connect("data/coffee.db")
        self.btn_poisk.clicked.connect(self.poisk)
        self.btn_add.clicked.connect(self.add)
        self.btn_redakt.clicked.connect(self.creat)

    def poisk(self):
        id = self.input_id.text()
        cur = self.con.cursor()
        if id:
            self.result = cur.execute(f"SELECT * FROM kofe WHERE id = {id}").fetchall()[0]
            self.print_id.setText(str(self.result[0]))
            self.print_name.setText(str(self.result[1]))
            self.print_stepeni.setText(str(self.result[2]))
            self.print_zerna.setText(str(self.result[3]))
            self.print_info.setText(str(self.result[4]))
            self.print_price.setText(str(self.result[5]))
            self.print_v.setText(str(self.result[6]))

    def add(self):
        self.add_k = AddEditCoffeeForm(self)
        self.add_k.show()

    def creat(self):
        self.add_c = CreatEditCoffeeForm(self, self.result[0])
        self.add_c.show()

class CreatEditCoffeeForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('creatEditCoffeeForm.ui', self)
        self.r_id = args[-1]
        self.print_id.setText(str(self.r_id))
        self.con = sqlite3.connect("data/coffee.db")
        self.btn_add.clicked.connect(self.add)
        cur = self.con.cursor()
        self.result = cur.execute(f"SELECT * FROM kofe WHERE id = {self.r_id}").fetchall()[0]
        self.input_name.setText(str(self.result[1]))
        self.input_stepeni.setCurrentText(str(self.result[2]))
        self.input_zerna.setCurrentText(str(self.result[3]))
        self.input_info.setText(str(self.result[4]))
        self.input_price.setValue(self.result[5])
        self.input_v.setValue(self.result[6])

    def add(self):
        name, stepeni = self.input_name.text(), self.input_stepeni.currentText()
        zerna, info = self.input_zerna.currentText(), self.input_info.text()
        price, v = self.input_price.text(), self.input_v.text()
        cur = self.con.cursor()
        cur.execute(f"UPDATE kofe "
                    f"SET name = '{name}', stepeni = '{stepeni}', "
                    f"zerna = '{zerna}', info = '{info}', "
                    f"price = {price}, v = {v} WHERE id = {self.r_id}")
        self.con.commit()


class AddEditCoffeeForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect("data/coffee.db")
        self.btn_add.clicked.connect(self.add)

    def add(self):
        name, stepeni = self.input_name.text(), self.input_stepeni.currentText()
        zerna, info = self.input_zerna.currentText(), self.input_info.text()
        price, v = self.input_price.text(), self.input_v.text()
        cur = self.con.cursor()
        cur.execute(f"INSERT INTO kofe(name, stepeni, zerna, info, price, v) "
                    f"VALUES('{name}', '{stepeni}', '{zerna}', '{info}', {price}, {v})")
        self.con.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())