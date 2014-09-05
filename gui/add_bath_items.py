from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QLayout, QLabel, QLineEdit, QDateEdit, QMessageBox,\
                            QApplication, QWidget, QGridLayout

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classes.bath_items import BathItems
from data_correctness import Validations
from management.room_management import add_bath_item, get_all_rooms_number


class BathItems_Form(QWidget):
    def __init__( self ):
        super(BathItems_Form, self).__init__()
        self.setupUi(self)

    def setupUi(self, BathItems_Form):
        layout = QGridLayout(self)
        self.bath_items = []

        if get_all_rooms_number() != []:
            min_room_number = min(get_all_rooms_number())
            max_room_number = max(get_all_rooms_number())
            room_number_label = "Enter room number({0}-{1}):".\
                              format(str(min_room_number), str(max_room_number))
        else:
            room_number_label = ''
        self.room_number_label = QLabel(room_number_label)
        self.room_number_line_edit = QLineEdit()
        self.bath_item_name_label = QLabel("Name:")
        self.bath_item_name_line_edit = QLineEdit()
        self.last_replace_date_label = QLabel("Last Replace Date:")
        self.last_replace_date_edit = QDateEdit(QDate.currentDate())
        self.replace_period_label = QLabel("Replace Period:")
        self.replace_period_line_edit = QLineEdit()

        layout.addWidget(self.room_number_label, 0, 0)
        layout.addWidget(self.room_number_line_edit, 0, 1)
        layout.addWidget(self.bath_item_name_label, 1, 0)
        layout.addWidget(self.bath_item_name_line_edit, 1, 1)
        layout.addWidget(self.last_replace_date_label, 2, 0)
        layout.addWidget(self.last_replace_date_edit, 2, 1)
        layout.addWidget(self.replace_period_label, 3, 0)
        layout.addWidget(self.replace_period_line_edit, 3, 1)

        self.setLayout(layout)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def date_to_string(self, date):
        year = str(date.year())
        month = str(date.month())
        day = str(date.day())
        return year + '-' + month + '-' + day

    def is_information_invalid(self, name, replace_period, room_number,
                               last_replace_date):
        return (not Validations.is_name(name) or
                not Validations.is_positive_integer(replace_period) or
                last_replace_date.addDays(int(replace_period)) <=\
                                          QDate.currentDate() or
                not int(room_number) in get_all_rooms_number())

    def error_message(self, name, replace_period, room_number):
        properties = [Validations.is_name, Validations.is_positive_integer]
        data = [name, replace_period]
        messages = ['name', 'replace period']
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
        name = self.bath_item_name_line_edit.text()
        last_replace_date = self.last_replace_date_edit.date()
        replace_period = self.replace_period_line_edit.text()

        if self.is_information_invalid(name, replace_period, room_number,
                                       last_replace_date):
            error_message = self.error_message(name, replace_period,
                                               room_number) 
            QMessageBox(QMessageBox.Critical, "Error",
                        "Invalid "  + error_message[:len(error_message) - 1] +\
                        ". Correct it!!!").exec_()
            return

        new_bath_item = BathItems(str(name),
                                  self.date_to_string(last_replace_date),
                                  int(replace_period), int(room_number))

        if new_bath_item in self.bath_items:
            notifier = QMessageBox(QMessageBox.Question,
                                   "Add New Bath Item",
          "You have already added this Bath Item. Do you want to add it again?", 
                                    QMessageBox.Yes | QMessageBox.No)
            notifier.setDefaultButton(QMessageBox.No)
            choosed_option = notifier.exec_()

            if choosed_option == QMessageBox.No:
                return
            elif choosed_option == QMessageBox.Yes:
                self.bath_items.append(new_bath_item)        
                add_bath_item(new_bath_item)
                return

        add_bath_item(new_bath_item)
        self.bath_items.append(new_bath_item)
        QMessageBox(QMessageBox.Information, "Add New Bath Item",
              "Congratulations. You successful added this Bath Item!!!").exec_()
