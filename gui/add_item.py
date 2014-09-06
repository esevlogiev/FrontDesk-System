import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtWidgets import (QStackedWidget, QComboBox, QDialog, QPushButton,
                             QVBoxLayout, QApplication, QLayout)
from PyQt5.QtGui import QIcon, QPixmap

import main
from gui.add_food import Food_Form
from gui.add_furniture import Furniture_Form
from gui.add_bath_items import BathItems_Form
from gui.add_sleeping_furniture import SleepingFurniture_Form


FORMS = [Furniture_Form, SleepingFurniture_Form, BathItems_Form, Food_Form]


class AddItemDialog(QDialog):
    def __init__(self):
        super(AddItemDialog, self).__init__()
        self.setupUi(self)

    def setupUi(self, AddItemDialog):
        self.item_type_picker = QComboBox()

        self.item_properties_switch = QStackedWidget()

        for form in FORMS:
            self.item_type_picker.addItem(form.__name__.split('_')[0],
                                          FORMS.index(form))
            self.item_properties_switch.addWidget(form())

        self.item_type_picker.currentIndexChanged.connect(
            self.item_properties_switch.setCurrentIndex)

        self.add_button = QPushButton("Add")

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.item_type_picker)
        mainLayout.addWidget(self.item_properties_switch, 1)
        mainLayout.addWidget(self.add_button)

        self.add_button.clicked.connect(self.add_item)

        self.setWindowIcon(QIcon(QPixmap('hotel_icon.jpg')))
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        self.setWindowTitle("Add Items")

    def add_item(self):
        self.item_properties_switch.currentWidget().add_button_click()
