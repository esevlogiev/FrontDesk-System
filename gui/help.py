import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtWidgets import (QApplication, QLayout, QListWidget, QWidget,
                             QHBoxLayout, QListWidgetItem, QTextEdit, QFrame)
from PyQt5.QtGui import QIcon, QPixmap
import gui.main
import resource_file

class Help(QWidget):
    def __init__( self ):
        super(Help, self).__init__()
        self.setupUi(self)

    def setupUi(self, Help):
        self.option_picker = QListWidget()
        self.option_picker.setStyleSheet("background-color:transparent")
        self.option_picker.addItem(QListWidgetItem("FrontDesk System Description"))
        self.option_picker.addItem(QListWidgetItem("Requirements for Clients data"))
        self.option_picker.addItem(QListWidgetItem("Menus"))
        self.option_picker.setFrameStyle(QFrame.NoFrame)
        self.information_shower = QTextEdit()
        self.information_shower.setReadOnly(True)

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.option_picker)
        main_layout.addWidget(self.information_shower)

        self.option_picker.setCurrentRow(0)
        self.option_picker.itemPressed.connect(self.choose_option)
        description = open("C:/Users/Asus/Desktop/project_final/\
                           description_files/program_description.txt","r")
        self.information_shower.setText(description.read())

        self.setWindowIcon(QIcon(QPixmap(':/images/hotel_icon.jpg')))
        self.setWindowTitle("Help")

    def choose_option(self):
        if self.option_picker.currentRow() == 0:
            description = open('C:/Users/Asus/Desktop/project_final/\
                               description_files/program_description.txt',"r")
            self.information_shower.setText(description.read())
        elif self.option_picker.currentRow() == 1:
            requirements = open("C:/Users/Asus/Desktop/project_final/\
                                description_files/requirements_for_client_data.txt", "r")
            self.information_shower.setText(requirements.read())
        elif self.option_picker.currentRow() == 2:
            menus = open("C:/Users/Asus/Desktop/project_final/\
                         description_files/menus.txt", "r")
            self.information_shower.setText(menus.read())

