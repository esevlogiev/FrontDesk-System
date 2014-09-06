import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtWidgets import (QLabel, QLineEdit, QPushButton, QMessageBox,
                             QDialog, QGridLayout, QLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

from management.client_management import add_client
from management.room_management import get_all_free_rooms_number
from data_correctness import Validations
from classes.client import Client
import gui.main
import datetime


class AddNewClient_Form(QDialog):
    def __init__(self):
        super(AddNewClient_Form, self).__init__()
        self.setupUi(self)

    def setupUi(self, AddNewClient_Form):
        layout = QGridLayout(self)

        self.clients = []
        min_room_number = min(get_all_free_rooms_number())
        max_room_number = max(get_all_free_rooms_number())
        room_number_label = "Enter room number({0}-{1}):".format(
                            str(min_room_number), str(max_room_number))
        self.room_number_label = QLabel(room_number_label)
        self.room_number_line_edit = QLineEdit()
        self.first_name_label = QLabel("First Name:")
        self.first_name_line_edit = QLineEdit()
        self.last_name_label = QLabel("Last Name:")
        self.last_name_line_edit = QLineEdit()
        self.phone_number_label = QLabel("Phone Number:")
        self.phone_number_line_edit = QLineEdit()
        self.stay_label = QLabel("Stay:")
        self.stay_line_edit = QLineEdit()
        self.add_new_client_button = QPushButton("Add New Client")

        layout.addWidget(self.first_name_label, 0, 0)
        layout.addWidget(self.first_name_line_edit, 0, 1)
        layout.addWidget(self.last_name_label, 1, 0)
        layout.addWidget(self.last_name_line_edit, 1, 1)
        layout.addWidget(self.phone_number_label, 2, 0)
        layout.addWidget(self.phone_number_line_edit, 2, 1)
        layout.addWidget(self.room_number_label, 3, 0)
        layout.addWidget(self.room_number_line_edit, 3, 1)
        layout.addWidget(self.stay_label, 4, 0)
        layout.addWidget(self.stay_line_edit, 4, 1)
        layout.addWidget(self.add_new_client_button, 5, 0, 1, 2,
                         Qt.AlignCenter)

        self.setLayout(layout)
        self.add_new_client_button.clicked.connect(self.add_button_click)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        self.setWindowIcon(QIcon(QPixmap('hotel_icon.jpg')))
        self.setWindowTitle("Add New Client")

    def date_to_string(self, date):
        year = str(date.year)
        month = str(date.month)
        day = str(date.day)
        return year + '-' + month + '-' + day

    def is_information_invalid(self, room_number, stay, phone_number,
                               first_name, last_name):
        return (not Validations.is_positive_integer(room_number) or
                not Validations.is_positive_integer(stay) or
                not Validations.is_phone(phone_number) or
                not Validations.is_name(first_name) or
                not Validations.is_name(last_name) or
                not int(room_number) in get_all_free_rooms_number())

    def error_message(self, room_number, stay, phone_number,
                      first_name, last_name):
        properties = [Validations.is_positive_integer, Validations.is_phone,
                      Validations.is_name, Validations.is_name]
        data = [stay, phone_number, first_name, last_name]
        messages = ['stay', 'phone_number', 'first name', 'last name']
        result = []
        for i in range(len(data)):
            if not properties[i](data[i]):
                result.append(messages[i] + ',')
        if (not Validations.is_positive_integer(room_number) or
           not int(room_number) in get_all_free_rooms_number()):
            result.append('room number' + ',')
        return ' '.join(result)

    def add_button_click(self):
        first_name = self.first_name_line_edit.text()
        last_name = self.last_name_line_edit.text()
        phone_number = self.phone_number_line_edit.text()
        stay = self.stay_line_edit.text()
        room_number = self.room_number_line_edit.text()

        if self.is_information_invalid(room_number, stay, phone_number,
                                       first_name, last_name):
            error_message = self.error_message(room_number, stay,
                                               phone_number, first_name,
                                               last_name)
            QMessageBox(QMessageBox.Critical, "Error",
                        "Invalid " + error_message[:len(error_message) - 1] +
                        ". Correct it!!!").exec_()
            return

        new_client = Client(first_name.capitalize(), last_name.capitalize(),
                            phone_number, int(room_number), int(stay),
                            self.date_to_string(datetime.date.today()))

        if new_client in self.clients:
            QMessageBox(QMessageBox.Warning, "Warning",
                        "You have already added this client!!!").exec_()
            return

        self.clients.append(new_client)
        if add_client(new_client, int(room_number)):
            QMessageBox(QMessageBox.Information, "Add New client",
                        "Congratulations. You successfully" +
                        " added this client!!!").exec_()
        else:
            QMessageBox(QMessageBox.Information, "Add New client",
                        "This client already exists!!!").exec_()
