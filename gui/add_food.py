import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (QLabel, QLineEdit, QDateEdit, QDialog,
                             QMessageBox, QGridLayout, QApplication,
                             QLayout, QWidget)

import gui.add_furniture
from classes.food import Food
from data_correctness import Validations
from management.room_management import add_food, get_all_rooms_number


class Food_Form(QWidget):
    def __init__(self):
        super(Food_Form, self).__init__()
        self.setupUi(self)

    def setupUi(self, Food_Form):
        layout = QGridLayout()
        self.foods = []

        if get_all_rooms_number() != []:
            min_room_number = min(get_all_rooms_number())
            max_room_number = max(get_all_rooms_number())
            room_number_label = "Enter room number({0}-{1}):".format(
                                str(min_room_number), str(max_room_number))
        else:
            room_number_label = ''
        self.room_number_label = QLabel(room_number_label)
        self.room_number_line_edit = QLineEdit()
        self.food_name_label = QLabel("Name:")
        self.food_name_line_edit = QLineEdit()
        self.food_quantity_label = QLabel("Quantity:")
        self.food_quantity_line_edit = QLineEdit()
        self.manufacture_date_label = QLabel("Manufacture Date:")
        self.manufacture_date_edit = QDateEdit(QDate.currentDate())
        self.expire_date_label = QLabel("Expire Date:")
        self.expire_date_edit = QDateEdit(QDate.currentDate())
        self.setWindowTitle("Add Food Item")

        layout.addWidget(self.room_number_label, 0, 0)
        layout.addWidget(self.room_number_line_edit, 0, 1)
        layout.addWidget(self.food_name_label, 1, 0)
        layout.addWidget(self.food_name_line_edit, 1, 1)
        layout.addWidget(self.food_quantity_label, 2, 0)
        layout.addWidget(self.food_quantity_line_edit, 2, 1)
        layout.addWidget(self.manufacture_date_label, 3, 0)
        layout.addWidget(self.manufacture_date_edit, 3, 1)
        layout.addWidget(self.expire_date_label, 4, 0)
        layout.addWidget(self.expire_date_edit, 4, 1)

        self.setLayout(layout)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def close_form(self):
        self.furniture = add_furniture.Furniture_Form()
        self.furniture.show()
        self.close()

    def date_to_string(self, date):
        year = str(date.year())
        month = str(date.month())
        day = str(date.day())
        return year + '-' + month + '-' + day

    def is_information_invalid(self, room_number, name, quantity):
        return (not Validations.is_name(name) or
                not Validations.is_float_number(quantity) or
                QDate.currentDate() >= self.expire_date_edit.date() or
                self.expire_date_edit.date() <=
                self.manufacture_date_edit.date() or
                not int(room_number) in get_all_rooms_number())

    def error_message(self, name, quantity, room_number):
        properties = [Validations.is_name, Validations.is_float_number]
        data = [name, quantity]
        messages = ['name', 'quantity']
        result = []
        for i in range(len(data)):
            if not properties[i](data[i]):
                result.append(messages[i] + ',')
        if (not Validations.is_positive_integer(room_number) or
           not int(room_number) in get_all_rooms_number()):
            result.append('room number' + ',')
        return ' '.join(result)

    def add_button_click(self):
        room_number = self.room_number_line_edit.text()
        name = self.food_name_line_edit.text()
        quantity = self.food_quantity_line_edit.text()
        manufacture_date = (self.date_to_string(
                            self.manufacture_date_edit.date()))
        expire_date = self.date_to_string(self.expire_date_edit.date())

        if self.is_information_invalid(room_number, name, quantity):
            error_message = self.error_message(name, quantity, room_number)
            QMessageBox(QMessageBox.Critical, "Error",
                        "Invalid " + error_message[:len(error_message) - 1] +
                        ". Correct it!!!").exec_()
            return

        new_food = Food(str(name.lower()),
                        float(quantity), manufacture_date,
                        expire_date, int(room_number))

        if new_food in self.foods:
            notifier = QMessageBox(QMessageBox.Question,
                                   "Add New Food",
                                   ("You have already added this food." +
                                    " Do you want to add it again?"),
                                   QMessageBox.Yes | QMessageBox.No)
            notifier.setDefaultButton(QMessageBox.No)
            choosed_option = notifier.exec_()

            if choosed_option == QMessageBox.No:
                return
            elif choosed_option == QMessageBox.Yes:
                self.foods.append(new_food)
                add_food(new_food)
                return

        add_food(new_food)
        self.foods.append(new_food)
        QMessageBox(QMessageBox.Information, "Add New Food",
                    ("Congratulations. You successfully" +
                     " added this food!!!")).exec_()
