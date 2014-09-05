import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from classes.food import Food
from management.room_management import release_room, get_all_rooms_number,\
                                       get_all_free_rooms_number
from data_correctness import Validations

import gui.add_furniture


class ReleaseRoom_Form(QDialog):
    def __init__(self):
        super(ReleaseRoom_Form, self).__init__()
        self.setupUi(self)

    def setupUi(self, ReleaseRoom_Form):
        self.release_rooms = []

        layout = QGridLayout()
        self.room_number_label = QLabel("Room Number:")
        self.room_number_combo_box = QComboBox()
        self.release_room_button = QPushButton("Release Room")

        layout.addWidget(self.room_number_label, 0, 0)
        layout.addWidget(self.room_number_combo_box, 0, 1)
        layout.addWidget(self.release_room_button, 1, 0, 1, 2)

        self.add_all_rooms()

        self.release_room_button.clicked.connect(self.release_button_click)
        self.setLayout(layout)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        self.setWindowTitle("Release Room")

    def close_form(self):
        self.main_form = menu.MainWindow()
        self.main.show()
        self.close()

    def add_all_rooms(self):
        all_rooms = get_all_rooms_number()
        for room in all_rooms:
            self.room_number_combo_box.addItem(str(room))

    def release_button_click(self):
        room_number = self.room_number_combo_box.currentText()
        
        if not int(room_number) in get_all_rooms_number():
            QMessageBox(QMessageBox.Critical, "Error",
                        "This room doesn't exist. Correct it!!!").exec()
            return

        if int(room_number) in get_all_free_rooms_number():
            QMessageBox(QMessageBox.Critical, "Error",
                        "This room isn't rent. Correct it!!!").exec()
            return        

        if int(room_number) in self.release_rooms:
            notifier = QMessageBox(QMessageBox.Warning,
                                   "Release Room",
                                   "You have already released this room!!!")
            choosed_option = notifier.exec()
            return


        release_room(int(room_number))

        self.release_rooms.append(int(room_number))
        QMessageBox(QMessageBox.Information, "Release Room",
            "Congratulations. You successfully released this room!!!").exec()
