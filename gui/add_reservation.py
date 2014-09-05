import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QLabel, QLineEdit, QPushButton, QDateEdit,
                             QMessageBox, QDialog, QApplication, QGridLayout,
                             QLayout)

import gui.main
from classes.client import Client
from data_correctness import Validations
from management.reservation_management import make_reservation
from management.room_management import get_all_rooms_number,\
                                       get_all_free_rooms_number





class AddReservation_Form(QDialog):
    def __init__( self ):
        super(AddReservation_Form, self).__init__()
        self.setupUi(self)

    def setupUi(self, AddReservation_Form):
        layout = QGridLayout(self)

        self.clients = []

        #ako nqma svobodni stai
        min_room_number = min(get_all_rooms_number())
        max_room_number = max(get_all_rooms_number())
        room_number_label = "Enter room number({0}-{1}):".format(
                                                          str(min_room_number),
                                                          str(max_room_number))
        self.room_number_label = QLabel(room_number_label)
        self.room_number_line_edit = QLineEdit()
        self.first_name_label = QLabel("First Name:")
        self.first_name_line_edit = QLineEdit()
        self.last_name_label = QLabel("Last Name:")
        self.last_name_line_edit = QLineEdit()
        self.phone_number_label = QLabel("Phone Number:")
        self.phone_number_line_edit = QLineEdit()
        self.date_registere_label = QLabel("Date Registere:")
        self.date_registere_edit = QDateEdit(QDate.currentDate())
        self.stay_label = QLabel("Stay")
        self.stay_line_edit = QLineEdit()
        self.add_new_reservation_button = QPushButton("Add New Reservation")

        layout.addWidget(self.first_name_label, 0, 0)
        layout.addWidget(self.first_name_line_edit, 0, 1)
        layout.addWidget(self.last_name_label, 1, 0)
        layout.addWidget(self.last_name_line_edit, 1, 1)
        layout.addWidget(self.phone_number_label, 2, 0)
        layout.addWidget(self.phone_number_line_edit, 2, 1)
        layout.addWidget(self.room_number_label, 3, 0)
        layout.addWidget(self.room_number_line_edit, 3, 1)
        layout.addWidget(self.date_registere_label, 4, 0)
        layout.addWidget(self.date_registere_edit, 4, 1)
        layout.addWidget(self.stay_label, 5, 0)
        layout.addWidget(self.stay_line_edit, 5, 1)
        layout.addWidget(self.add_new_reservation_button, 6, 0, 1, 2,
                         Qt.AlignCenter)
        
        self.setLayout(layout)
        self.add_new_reservation_button.clicked.connect(self.add_button_click)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        self.setWindowIcon(QIcon(QPixmap('hotel_icon.jpg')))
        self.setWindowTitle("Add New Reservation")

    def date_to_string(self, date):
        year = str(date.year())
        month = str(date.month())
        day = str(date.day())
        return year + '-' + month + '-' + day

    def is_information_invalid(self, room_number, stay, phone_number,
                               first_name, last_name, date_registere):
        return (not Validations.is_positive_integer(room_number) or
               not Validations.is_positive_integer(stay) or
               not Validations.is_phone(phone_number) or
               not Validations.is_name(first_name) or
               not Validations.is_name(last_name) or
               date_registere < QDate.currentDate() or
               not int(room_number) in get_all_rooms_number())

    def error_message(self, room_number, stay, phone_number,
                      first_name, last_name):
        properties = [Validations.is_positive_integer, Validations.is_phone,
                      Validations.is_name, Validations.is_name]
        data = [stay, phone_number, first_name, last_name]
        messages = ['stay', 'phone number', 'first name', 'last name']
        result = []
        for i in range(len(data)):
            if not properties[i](data[i]):
                result.append(messages[i] + ',')
        if (not Validations.is_positive_integer(room_number) or 
            not int(room_number) in get_all_rooms_number()):
            result.append('room number' + ',')
        return ' '.join(result)

    def add_button_click(self):
        first_name = self.first_name_line_edit.text()
        last_name = self.last_name_line_edit.text()
        phone_number = self.phone_number_line_edit.text()
        date_registere = self.date_registere_edit.date()
        stay = self.stay_line_edit.text()
        room_number = self.room_number_line_edit.text()


        if self.is_information_invalid(room_number, stay, phone_number,
                                       first_name, last_name, date_registere):
            error_message = self.error_message(room_number, stay, phone_number,
                                               first_name, last_name) 
            QMessageBox(QMessageBox.Critical, "Error",
                        "Invalid "  + error_message[:len(error_message) - 1] +\
                        ". Correct it!!!").exec_()
            return

        new_client = Client(first_name.capitalize(), last_name.capitalize(),
                            phone_number, int(room_number), int(stay),
                            self.date_to_string(date_registere))

        if new_client in self.clients:
            QMessageBox(QMessageBox.Warning, "Warning",
                        "You have already added this reservation!!!").exec_()
            return

        self.clients.append(new_client)
        if make_reservation(int(room_number), new_client):
            QMessageBox(QMessageBox.Information, "Add New Reservation",
            "Congratulations. You successful added this reservation!!!").exec_()
        else:
            QMessageBox(QMessageBox.Information, "Add New Reservation",
                        "There is overbooking!!!").exec_()
