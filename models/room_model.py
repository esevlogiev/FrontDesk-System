import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtCore import QAbstractItemModel, Qt, QVariant, QModelIndex
from PyQt5.QtWidgets import QTableView, QAbstractScrollArea, QApplication

from classes.room import Room

ROOM_CHARACTERISTICS = 4


class RoomModel(QAbstractItemModel):
    def __init__(self):
        super(RoomModel, self).__init__()
        self.room = []

    def set_rooms(self, rooms):
        self.beginResetModel()
        self.rooms = rooms
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self.rooms)

    def columnCount(self, parent=QModelIndex()):
        return ROOM_CHARACTERISTICS

    def data(self, index, role):
        if (not self.hasIndex(index.row(), index.column()) or
           role != Qt.DisplayRole):
            return QVariant()

        room = self.rooms[index.row()]

        getters = ('get_number', 'get_price_per_day', 'get_capacity',
                   'get_is_rent')
        if index.column() < self.columnCount():
            return getattr(room, getters[index.column()])

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
                return ('Room Number', 'Price Per Day', 'Capacity',
                        'Rent')[section]
        return QVariant()
