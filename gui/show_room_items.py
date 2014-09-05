import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLabel, QLineEdit, QPushButton, QMessageBox,
                             QDialog, QGridLayout, QLayout, QComboBox,
                             QTableView, QAbstractScrollArea)

from management.client_management import show_client 
from data_correctness import Validations
from classes.client import Client
import gui.main
from PyQt5.QtGui import QIcon, QPixmap
from management.room_management import (furnitures_in_room, bath_items_in_room,
                             food_in_room, sleeping_furnitures_in_room,
                             get_all_rooms_number)
from models.food_model import FoodModel
from models.bath_item_model import BathItemsModel
from models.furniture_model import FurnituresModel
from models.sleeping_furniture_model import SleepingFurnituresModel

ITEMS = ["Furnitures", "Sleeping Furnitures", "Bath Items", "Food"]

class ShowItems_Form(QDialog):
    def __init__( self ):
        super(ShowItems_Form, self).__init__()
        self.setupUi(self)

    def setupUi(self, ShowItems_Form):
        layout = QGridLayout(self)

        self.room_number_label = QLabel("Room Number:")
        self.room_number_line_edit = QLineEdit()
        self.item_label = QLabel("Choose Item:")
        self.item_combo_box = QComboBox()
        self.show_items = QPushButton("Show Items")

        #for i in range(0, len(ITEMS)):
        self.item_combo_box.addItems(ITEMS)

        layout.addWidget(self.room_number_label, 0, 0)
        layout.addWidget(self.room_number_line_edit, 0, 1)
        layout.addWidget(self.item_label, 1, 0)
        layout.addWidget(self.item_combo_box, 1, 1)
        layout.addWidget(self.show_items, 2, 0, 1, 2, Qt.AlignCenter)

        self.setLayout(layout)
        self.show_items.clicked.connect(self.show_button_click)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        self.setWindowIcon(QIcon(QPixmap('hotel_icon.jpg')))
        self.setWindowTitle("Show Items")

    def show_table(self, items, model):
        self.table = QTableView()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.model = model
        if type(model) == type(FurnituresModel()):
            self.model.set_furnitures(items)
            self.table.setWindowTitle("Furnitures")
        elif type(model) == type(BathItemsModel()):
            self.model.set_bath_items(items)
            self.table.setWindowTitle("Bath Items")
        elif type(model) == type(FoodModel()):
            self.model.set_food(items)
            self.table.setWindowTitle("Food")
        elif type(model) == type(SleepingFurnituresModel()):
            self.model.set_sleeping_furnitures(items)
            self.table.setWindowTitle("Sleeping Furnitures")
        self.table.setWindowIcon(QIcon(QPixmap(':/images/hotel_icon.jpg')))
        self.table.setModel(model)
        self.table.show()

    def show_button_click(self):
        room_number = self.room_number_line_edit.text()
        item = self.item_combo_box.currentText()

        if not Validations.is_positive_integer(room_number):
            QMessageBox(QMessageBox.Critical, "Error",
                        "Invalid room number. Correct it!!!").exec_()
            return

        if not int(room_number) in get_all_rooms_number():
            QMessageBox(QMessageBox.Critical, "Error",
                     "There is no room with such number. Correct it!!!").exec_()
            return

        if item == 'Furnitures':
            self.show_table(furnitures_in_room(int(room_number)),
                                               FurnituresModel())
        elif item == 'Bath Items':
            self.show_table(bath_items_in_room(int(room_number)),
                                               BathItemsModel())
        elif item == 'Food':
            self.show_table(food_in_room(int(room_number)),
                                         FoodModel())
        elif item == 'Sleeping Furnitures':
            self.show_table(sleeping_furnitures_in_room(int(room_number)),
                                               SleepingFurnituresModel())

        