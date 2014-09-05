import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QMessageBox, QWidget,\
                            QApplication, QGridLayout, QLayout

from data_correctness import Validations
from classes.sleeping_furniture import SleepingFurniture
from management.room_management import get_all_rooms_number,\
                                       add_sleeping_furniture


class SleepingFurniture_Form(QWidget):
    def __init__( self ):
        super(SleepingFurniture_Form, self).__init__()
        self.setupUi(self)

    def setupUi(self, SleepingFurniture_Form):
        layout = QGridLayout(self)
        self.sleeping_furnitures = []

        if get_all_rooms_number() != []:
            min_room_number = min(get_all_rooms_number())
            max_room_number = max(get_all_rooms_number())
            room_number_label = "Enter room number({0}-{1}):".format(
                                                           str(min_room_number),
                                                           str(max_room_number))
        else:
            room_number_label = ''
        self.room_number_label = QLabel(room_number_label)
        self.room_number_line_edit = QLineEdit()
        self.sleeping_furniture_name_label = QLabel("Name:")
        self.sleeping_furniture_name_line_edit = QLineEdit()
        self.sleeping_seats_label = QLabel("Sleeping Seats")
        self.sleeping_seats_line_edit = QLineEdit()
        self.quality_label = QLabel("Quality")
        self.quality_combo_box = QComboBox()

        self.quality_combo_box.addItem("Excellent")
        self.quality_combo_box.addItem("Good")
        self.quality_combo_box.addItem("Bad")

        layout.addWidget(self.room_number_label, 0, 0)
        layout.addWidget(self.room_number_line_edit, 0, 1)
        layout.addWidget(self.sleeping_furniture_name_label, 1, 0)
        layout.addWidget(self.sleeping_furniture_name_line_edit, 1, 1)
        layout.addWidget(self.sleeping_seats_label, 2, 0)
        layout.addWidget(self.sleeping_seats_line_edit, 2, 1)
        layout.addWidget(self.quality_label, 3, 0)
        layout.addWidget(self.quality_combo_box, 3, 1)

        self.setLayout(layout)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def is_information_invalid(self, name, sleeping_seats, room_number):
        return (not Validations.is_name(name) or
                not Validations.is_positive_integer(sleeping_seats) or
                not Validations.is_positive_integer(room_number) or
                not int(room_number) in get_all_rooms_number())

    def error_message(self, name, sleeping_seats, room_number):
        properties = [Validations.is_name, Validations.is_positive_integer]
        data = [name, sleeping_seats]
        messages = ['name', 'sleeping seats']
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
        name = self.sleeping_furniture_name_line_edit.text()
        sleeping_seats = self.sleeping_seats_line_edit.text()
        quality = self.quality_combo_box.currentText()

        if self.is_information_invalid(name, sleeping_seats, room_number):
            error_message = self.error_message(name, sleeping_seats, room_number) 
            QMessageBox(QMessageBox.Critical, "Error",
                        "Invalid "  + error_message[:len(error_message) - 1] +\
                        ". Correct it!!!").exec_()
            return

        new_sleeping_furniture = SleepingFurniture(name, quality,
                                                    int(sleeping_seats), 
                                                    int(room_number))

        if new_sleeping_furniture in self.sleeping_furnitures:
            notifier = QMessageBox(QMessageBox.Question,
                                   "Add New Sleeping Furniture",
            "You have already added this Sleeping Furniture. Do you want to add it again?", 
                                    QMessageBox.Yes | QMessageBox.No)
            notifier.setDefaultButton(QMessageBox.No)
            choosed_option = notifier.exec_()

            if choosed_option == QMessageBox.No:
                return
            elif choosed_option == QMessageBox.Yes:
                self.sleeping_furnitures.append(new_sleeping_furniture)        
                add_sleeping_furniture(new_sleeping_furniture)
                return

        add_sleeping_furniture(new_sleeping_furniture)
        self.sleeping_furnitures.append(new_sleeping_furniture)
        QMessageBox(QMessageBox.Information, "Add New sleeping furniture",
        "Congratulations. You successful added this sleeping furniture!!!").exec_()
