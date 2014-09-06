import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QLabel, QLineEdit, QPushButton, QMessageBox,
                             QDialog, QGridLayout, QLayout, QTableView,
                             QAbstractScrollArea)

from management.client_management import show_client
from data_correctness import Validations
from classes.client import Client
import gui.main
from models.client_model import ClientsModel
from management.client_management import show_client


class ShowClient_Form(QDialog):
    def __init__(self):
        super(ShowClient_Form, self).__init__()
        self.setupUi(self)

    def setupUi(self, ShowClient_Form):
        layout = QGridLayout(self)

        self.first_name_label = QLabel("First Name:")
        self.first_name_line_edit = QLineEdit()
        self.last_name_label = QLabel("Last Name:")
        self.last_name_line_edit = QLineEdit()
        self.show_client = QPushButton("Show Client")

        layout.addWidget(self.first_name_label, 0, 0)
        layout.addWidget(self.first_name_line_edit, 0, 1)
        layout.addWidget(self.last_name_label, 1, 0)
        layout.addWidget(self.last_name_line_edit, 1, 1)
        layout.addWidget(self.show_client, 2, 0, 1, 2, Qt.AlignCenter)

        self.setLayout(layout)
        self.show_client.clicked.connect(self.show_button_click)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        self.setWindowIcon(QIcon(QPixmap('hotel_icon.jpg')))
        self.setWindowTitle("Show Client")

    def show_clients_model(self, clients, is_maid=False):
        self.table = QTableView()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.model = ClientsModel(is_maid)
        self.model.set_clients(clients)
        self.table.setModel(self.model)
        self.table.setWindowTitle('Show Client')
        self.table.setWindowIcon(QIcon(QPixmap(':/images/hotel_icon.jpg')))
        self.table.show()

    def is_information_invalid(self, first_name, last_name):
        return (not Validations.is_name(first_name) or
                not Validations.is_name(last_name))

    def error_message(self, first_name, last_name):
        properties = [Validations.is_name, Validations.is_name]
        data = [first_name, last_name]
        messages = ['first name', 'last name']
        result = []
        for i in range(len(data)):
            if not properties[i](data[i]):
                result.append(messages[i] + ',')
        return ' '.join(result)

    def show_button_click(self):
        first_name = self.first_name_line_edit.text()
        last_name = self.last_name_line_edit.text()

        if self.is_information_invalid(first_name, last_name):
            error_message = self.error_message(first_name, last_name)
            QMessageBox(QMessageBox.Critical, "Error",
                        "Invalid " + error_message[:len(error_message) - 1] +
                        ". Correct it!!!").exec_()
            return
        if not show_client(first_name.capitalize(), last_name.capitalize()):
            QMessageBox(QMessageBox.Warning, "Warning",
                        "This person is not a Client!!!").exec_()
            return
        self.show_clients_model(show_client(first_name.capitalize(),
                                            last_name.capitalize()), True)
