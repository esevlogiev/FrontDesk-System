from PyQt5.QtWidgets import (QLabel, QLineEdit, QComboBox, QLayout,
                             QGridLayout, QWidget, QMessageBox, QApplication)
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import gui.add_food
from classes.sleeping_furniture import Furniture
from data_correctness import Validations
from management.room_management import get_all_rooms_number, add_furniture


class Furniture_Form(QWidget):
    def __init__( self ):
        super(Furniture_Form, self).__init__()
        self.setupUi(self)

    def setupUi(self, Furniture_Form):
        layout = QGridLayout(self)
        self.furnitures = []

        if get_all_rooms_number() != []:
            min_room_number = min(get_all_rooms_number())
            max_room_number = max(get_all_rooms_number())
            room_number_label = "Enter room number({0}-{1}):".\
            format(str(min_room_number), str(max_room_number))
        else:
            room_number_label = ''
        self.room_number_label = QLabel(room_number_label)
        self.room_number_line_edit = QLineEdit()
        self.furniture_name_label = QLabel("Name:")
        self.furniture_name_line_edit = QLineEdit()
        self.quality_label = QLabel("Quality")
        self.quality_combo_box = QComboBox()
        self.quality_combo_box.addItem("Excellent")
        self.quality_combo_box.addItem("Good")
        self.quality_combo_box.addItem("Bad")

        layout.addWidget(self.room_number_label, 0, 0)
        layout.addWidget(self.room_number_line_edit, 0, 1)
        layout.addWidget(self.furniture_name_label, 1, 0)
        layout.addWidget(self.furniture_name_line_edit, 1, 1)
        layout.addWidget(self.quality_label, 2, 0)
        layout.addWidget(self.quality_combo_box, 2, 1)

        self.setLayout(layout)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def is_information_invalid(self, name, room_number):
        return (not Validations.is_name(name) or
                not int(room_number) in get_all_rooms_number())

    def error_message(self, name, room_number):
        result = []
        if not Validations.is_name(name):
            result.append('name, ')
        if (not Validations.is_positive_integer(room_number) or 
            not int(room_number) in get_all_rooms_number()):
            result.append('room number' + ',')
        return ' '.join(result)

    def add_button_click(self):
        room_number = self.room_number_line_edit.text()
        name = self.furniture_name_line_edit.text()
        quality = self.quality_combo_box.currentText()

        if self.is_information_invalid(name, room_number):
            error_message = self.error_message(name, room_number) 
            QMessageBox(QMessageBox.Critical, "Error",
                        "Invalid "  + error_message[:len(error_message) - 1] +\
                        ". Correct it!!!").exec_()
            return

        new_furniture = Furniture(name, quality, int(room_number))

        if new_furniture in self.furnitures:
            notifier = QMessageBox(QMessageBox.Question,
                                   "Add New Furniture",
          "You have already added this Furniture. Do you want to add it again?", 
                                    QMessageBox.Yes | QMessageBox.No)
            notifier.setDefaultButton(QMessageBox.No)
            choosed_option = notifier.exec_()

            if choosed_option == QMessageBox.No:
                return
            elif choosed_option == QMessageBox.Yes:
                self.furnitures.append(new_furniture)        
                add_furniture(new_furniture)
                return

        add_furniture(new_furniture)
        self.furnitures.append(new_furniture)
        QMessageBox(QMessageBox.Information, "Add New Furniture",
        "Congratulations. You successful added this Furniture!!!").exec_()
