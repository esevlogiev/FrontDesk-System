import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtCore import QAbstractItemModel, Qt, QVariant, QModelIndex
from PyQt5.QtWidgets import QTableView, QAbstractScrollArea, QApplication

from classes.client import Client

CLIENT_CHARACTERISTICS = 6

class ClientsModel(QAbstractItemModel):
    def __init__(self,  is_maid=False):
        super(ClientsModel, self).__init__()
        self.clients = []
        self.is_maid = is_maid

    def set_clients(self, clients):
        self.beginResetModel()
        self.clients = clients
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self.clients)

    def columnCount(self, parent=QModelIndex()):
        if self.is_maid:
            return 7
        return CLIENT_CHARACTERISTICS

    def data(self, index, role):
        if (not self.hasIndex(index.row(), index.column()) or
           role != Qt.DisplayRole):
            return QVariant()

        if self.is_maid:
            client = (self.clients[index.row()])[0]   
        else:
            client = self.clients[index.row()] 
        getters = ('get_number_room', 'get_first_name', 'get_last_name',
                   'get_phone_number', 'get_time_stay', 'get_date_registere')
        if not self.is_maid and index.column() < self.columnCount():
            return getattr(client, getters[index.column()])
        elif self.is_maid and index.column() < self.columnCount() - 1:
            return getattr(client, getters[index.column()])
        elif self.is_maid and index.column() == 6:
            return (self.clients[index.row()])[1]

        return QVariant()

    def index(self, row, column, parent=QModelIndex()):
        if self.is_valid_row_index(row) and self.is_valid_column_index(column):
            return self.createIndex(row, column)
        else:
            return QModelIndex()

    def is_valid_row_index(self, row_index):
        return 0 <= row_index and row_index < self.rowCount()

    def is_valid_column_index(self, column_index):
        return 0 <= column_index and column_index < self.columnCount()


    def parent(self, child):
        return QModelIndex()

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Vertical:
            if not self.is_valid_row_index(section):
                return QVariant()
            else:
                return section + 1
        if orientation == Qt.Horizontal:
            if not self.is_valid_column_index(section):
                return QVariant()
            else:
                if section < CLIENT_CHARACTERISTICS:
                    return ('Room Number', 'First Name', 'Last Name',
                            'Phone Number', 'Stay', 'Date Registere')[section]
                elif self.is_maid and section == 6:
                    return "Maid Names"
        return QVariant()