import os,sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QLabel, 
                            QWidget, QAction, QDesktopWidget, QInputDialog,
                            QMessageBox, QTableView, QAbstractScrollArea)

import gui.add_new_room, gui.cancel_reservation, gui.show_client
import gui.add_food, gui.add_reservation, gui.add_new_client, gui.add_item,\
       gui.cancel_reservation, gui.show_room_items
from management.room_management import (release_room, change_bath_item, change_food,
                                        get_all_rooms_number, get_all_rooms,
                                        get_all_free_rooms_number)
from management.reservation_management import get_all_reservations
from management.client_management import get_all_clients, accomodate_clients
from models.client_model import ClientsModel
from gui.help import Help
import resource_file

from gui.add_maid import MaidForm
from management.maid_management import get_all_maids
from models.maid_model import MaidModel
from models.room_model import RoomModel
from create_database_tables import create_tables


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
         
    def initUI(self):
        self.is_bath_items_replace = False
        self.is_food_replace = False

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        myImage = QImage()
        myImage.load(":/images/project_logo_resize.jpg")

        myLabel = QLabel()
        myLabel.setScaledContents(True) 
        myLabel.setGeometry(200,200,200,200)
        myLabel.setPixmap(QPixmap.fromImage(myImage))
        layout.addWidget(myLabel)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)
        self.setWindowIcon(QIcon(QPixmap(':/images/hotel_icon.jpg')))

        menubar = self.menuBar()
        main_menu = menubar.addMenu('&Main')

        room_management_menu = main_menu.addMenu('&Room Management')
        client_management_menu = main_menu.addMenu('&Client Management')
        reservation_management_menu = main_menu.addMenu('&Reservation Management')
        maid_management_menu = main_menu.addMenu('&Maid Management')

        items_menu = room_management_menu.addMenu('&Items Menu')
        add_room_action = QAction('Add New Room', self)
        add_room_action.triggered.connect(self.add_new_room_form_load)
        room_management_menu.addAction(add_room_action)
        
        release_rooms_action = QAction('Release Room', self)
        release_rooms_action.triggered.connect(self.release_room_load)
        room_management_menu.addAction(release_rooms_action)

        show_rooms_action = QAction('Show Rooms', self)
        show_rooms_action.triggered.connect(self.show_rooms)
        room_management_menu.addAction(show_rooms_action)

        add_maid_action = QAction('Add Maid', self)
        add_maid_action.triggered.connect(self.add_maid)
        maid_management_menu.addAction(add_maid_action)


        show_maid_action = QAction('Show All Maids', self)
        show_maid_action.triggered.connect(self.show_maid_model)
        maid_management_menu.addAction(show_maid_action)

        add_item_action = QAction('Add New Item', self)
        add_item_action.triggered.connect(self.add_item_form_load)
        items_menu.addAction(add_item_action)

                

        show_items_action = QAction('Show Items in Room', self)
        show_items_action.triggered.connect(self.show_items_load)
        items_menu.addAction(show_items_action)


        add_client_action = QAction('Add New Client', self)
        add_client_action.triggered.connect(self.add_new_client_form_load)
        client_management_menu.addAction(add_client_action)
        show_client_action = QAction('Show Client', self)
        show_client_action.triggered.connect(self.show_client_load)
        client_management_menu.addAction(show_client_action)
        show_all_clients_action = QAction('Show All Clients', self)
        show_all_clients_action.triggered.connect(self.show_clients)
        client_management_menu.addAction(show_all_clients_action)


        make_reservation_action = QAction('Make Reservation', self)
        make_reservation_action.triggered.connect(self.make_reservation_form_load)
        reservation_management_menu.addAction(make_reservation_action)
        cancel_reservation_action = QAction('Cancel Reservation', self)
        cancel_reservation_action.triggered.connect(self.cancel_reservation_form_load)
        reservation_management_menu.addAction(cancel_reservation_action)

        show_reservation_action = QAction('Show All Reservations', self)
        show_reservation_action.triggered.connect(self.show_reservations)
        reservation_management_menu.addAction(show_reservation_action)


        help_menu = menubar.addMenu('&Help')

        help_action = QAction('About Front Desk System', self)
        help_action.triggered.connect(self.help)

        about_action = QAction('About Author', self)
        about_action.triggered.connect(self.about)

        help_menu.addAction(help_action)
        help_menu.addAction(about_action)

        self.setFixedSize(self.sizeHint())
        self.setWindowTitle("Front Desk System")
        self.move(QDesktopWidget().availableGeometry().center() -\
                  self.frameGeometry().center())

    def add_new_client_form_load(self):
        if get_all_free_rooms_number() == []:
            self.no_free_rooms()
            return

        self.add_client_form = gui.add_new_client.AddNewClient_Form()
        self.add_client_form.show()
        #self.close()

    def add_new_room_form_load(self):
        self.add_new_room_form = gui.add_new_room.AddNewRoom_Form()
        self.add_new_room_form.show()
        #self.close()

    def add_maid(self):
        self.add_maid_form = MaidForm()
        self.add_maid_form.show()

    
    def make_reservation_form_load(self):
        if get_all_rooms_number() == []:
            self.no_rooms()
            return

        self.make_reservation_form = gui.add_reservation.AddReservation_Form()
        self.make_reservation_form.show()    

    def cancel_reservation_form_load(self):
        if get_all_rooms_number() == []:
            self.no_rooms()
            return

        self.cancel_reservation_form = gui.cancel_reservation.CancelReservation_Form()
        self.cancel_reservation_form.show()
        #self.close()     

    def add_item_form_load(self):
        if get_all_rooms_number() == []:
            self.no_rooms()
            return
        self.add_item_load = gui.add_item.AddItemDialog()
        self.add_item_load.show()
        #self.close() 

    def show_client_load(self):
        if get_all_rooms_number() == []:
            self.no_rooms()
            return
        self.show_client_form = gui.show_client.ShowClient_Form()
        self.show_client_form.show()
        #self.close()

    def show_items_load(self):
        if get_all_rooms_number() == []:
            self.no_rooms()
            return
        self.show_items_form = gui.show_room_items.ShowItems_Form()
        self.show_items_form.show()
        #self.close()

    def room_number_input_dialog(self):
        self.room = 0
        if get_all_rooms_number() == []:
            self.no_rooms()
            return

        min_room_number = min(get_all_rooms_number())
        max_room_number = max(get_all_rooms_number())
        return QInputDialog.getInt(self, "Release",
                    "Enter room number({0}-{1})".format(str(min_room_number),
                                                        str(max_room_number)), 
                             self.room, min_room_number, max_room_number)

    def release_room_load(self):
        if get_all_rooms_number() == []:
            self.no_rooms()
            return

        room_number, ok = self.room_number_input_dialog() 
        if ok:
            if not room_number in get_all_rooms_number():
               notifier = QMessageBox(QMessageBox.Critical, "Release Room",
                        "This room does not exist!!!")
               notifier.setWindowIcon(QIcon(QPixmap(':/images/hotel_icon.jpg')))
               notifier.exec_()
               self.release_room_load()
            elif  room_number in get_all_free_rooms_number():
                notifier = QMessageBox(QMessageBox.Warning, "Release Room",
                        "This room is free!!!")
                notifier.setWindowIcon(QIcon(QPixmap(':/images/hotel_icon.jpg')))
                notifier.exec_()
                self.release_room_load()
            else:
                release_room(room_number)
                QMessageBox(QMessageBox.Information, "Release Room",
                'Congratulations!!! You successfully released this room.').exec_()
                self.release_room_load()

    def set_table(self, table_name):
        table = getattr(self, table_name + '_table')
        table.setModel(self.proxy_model)
        table.setSortingEnabled(True)
        table.setWindowTitle('Show ' + table_name.capitalize())
        table.setWindowIcon(QIcon(QPixmap(':/images/hotel_icon.jpg')))
        table.move(self.frameGeometry().center() -\
                   table.frameGeometry().center())
        table.show()

    def show_maid_model(self):
        maids = get_all_maids()
        if maids == []:
            QMessageBox(QMessageBox.Warning, "Show Maids",
                        "There is no added maids!!!").exec_()
            return
        self.maids_table = QTableView()
        self.maids_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.model = MaidModel()
        self.model.set_maids(maids)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.set_table('maids')


    def show_reservations(self):
        reservations = get_all_reservations()
        if reservations == []:
            QMessageBox(QMessageBox.Warning, "Show Reservations",
                        "There is no reservations made!!!").exec_()
            return
        self.reservations_table = QTableView()
        self.reservations_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.model = ClientsModel()
        self.model.set_clients(reservations)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.set_table('reservations')

    def show_rooms(self):
        rooms = get_all_rooms()
        if rooms == []:
            QMessageBox(QMessageBox.Warning, "Show Rooms",
                        "There is no room!!!").exec_()
            return
        self.rooms_table = QTableView()
        self.rooms_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.model = RoomModel()
        self.model.set_rooms(rooms)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.set_table('rooms')  

    def show_clients(self):
        clients = get_all_clients()
        if clients == []:
            QMessageBox(QMessageBox.Warning, "Show Clients",
                        "There is no client!!!").exec_()
            return
        self.clients_table = QTableView()
        self.clients_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.model = ClientsModel()
        self.model.set_clients(clients)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.set_table('clients')      

    def about(self):
         QMessageBox.about(self, "About",
         "<p><b>Front Desk System</b></p><p> Version 2.5.3</p>\
        <p>Registered to Evgeny Evlogiev</p><p>Email: evgenistefchov@abv.bg</p>")

    def no_free_rooms(self):
        notifier = QMessageBox(QMessageBox.Warning, "Warning",
                        "There is no free room!!!")
        notifier.setWindowIcon(QIcon(QPixmap(':/images/hotel_icon.jpg')))
        notifier.exec_()

    def no_rooms(self):
        QMessageBox(QMessageBox.Warning, "Warning",
                        "There is no room!!!").exec_()

    def help(self):
        self.help = Help()
        self.help.show()



def main():
    create_tables()
    change_food()
    change_bath_item()
    accomodate_clients()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()