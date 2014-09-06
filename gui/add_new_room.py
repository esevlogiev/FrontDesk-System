import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLabel, QLineEdit, QPushButton, QMessageBox,
                             QDialog, QGridLayout, QApplication, QLayout)
from PyQt5.QtGui import QIcon, QPixmap

import gui.main
from classes.room import Room
from data_correctness import Validations
from management.room_management import add_new_room, get_all_rooms_number


class AddNewRoom_Form(QDialog):
    def __init__(self):
        super(AddNewRoom_Form, self).__init__()
        self.setupUi(self)

    def setupUi(self, AddNewRoom_Form):
        layout = QGridLayout(self)

        self.rooms = []
        self.room_number_label = QLabel("Room Number:")
        self.room_number_line_edit = QLineEdit()
        self.price_per_day_label = QLabel("Price Per Day:")
        self.price_per_day_line_edit = QLineEdit()
        self.capacity_label = QLabel("Capacity:")
        self.capacity_line_edit = QLineEdit()
        self.add_new_room_button = QPushButton("Add New Room")

        layout.addWidget(self.room_number_label, 0, 0)
        layout.addWidget(self.room_number_line_edit, 0, 1)
        layout.addWidget(self.price_per_day_label, 1, 0)
        layout.addWidget(self.price_per_day_line_edit, 1, 1)
        layout.addWidget(self.capacity_label, 2, 0)
        layout.addWidget(self.capacity_line_edit, 2, 1)
        layout.addWidget(self.add_new_room_button, 3, 0, 1, 2, Qt.AlignCenter)
        self.setLayout(layout)

        self.add_new_room_button.clicked.connect(self.add_button_click)
        self.setWindowTitle("Add New Room")
        self.setWindowIcon(QIcon(QPixmap('hotel_icon.jpg')))
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def is_information_invalid(self, room_number, capacity, price_per_day):
        return (not Validations.is_positive_integer(room_number) or
                not Validations.is_positive_integer(capacity) or
                not Validations.is_float_number(price_per_day) or
                int(room_number) in get_all_rooms_number())

    def error_message(self, room_number, capacity, price_per_day):
        properties = [Validations.is_positive_integer,
                      Validations.is_positive_integer,
                      Validations.is_float_number]
        data = [capacity, price_per_day]
        messages = ['capacity', 'price per day']
        result = []
        for i in range(len(data)):
            if not properties[i](data[i]):
                result.append(messages[i] + ',')
        if (not Validations.is_positive_integer(room_number) or
           int(room_number) in get_all_rooms_number()):
            result.append('room number' + ',')
        return ' '.join(result)

    def add_button_click(self):
        room_number = self.room_number_line_edit.text()
        price_per_day = self.price_per_day_line_edit.text()
        capacity = self.capacity_line_edit.text()

        if self.is_information_invalid(room_number, capacity, price_per_day):
            error_message = self.error_message(room_number, capacity,
                                               price_per_day)
            QMessageBox(QMessageBox.Critical, "Error",
                        "Invalid " + error_message[:len(error_message) - 1] +
                        ". Correct it!!!").exec_()
            return

        new_room = Room(int(room_number), float(price_per_day),
                        int(capacity), "False")
        if new_room in self.rooms:
            QMessageBox(QMessageBox.Warning, "Warning",
                        "You have already added this room!!!").exec_()
            return

        self.rooms.append(new_room)
        if add_new_room(new_room):
            QMessageBox(QMessageBox.Information, "Add New Room",
                        "Congratulations. You successfully" +
                        " added this room!!!").exec_()
        else:
            QMessageBox(QMessageBox.Information, "Add New Room",
                        "This room already exists!!!").exec_()
