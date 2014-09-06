import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PyQt5.QtCore import QAbstractItemModel, Qt, QVariant, QModelIndex
from PyQt5.QtWidgets import QTableView, QAbstractScrollArea, QApplication

from classes.sleeping_furniture import SleepingFurniture

SLEEPING_FURNITURE_CHARACTERISTICS = 4


class SleepingFurnituresModel(QAbstractItemModel):
    def __init__(self):
        super(SleepingFurnituresModel, self).__init__()
        self.sleeping_furnitures = []

    def set_sleeping_furnitures(self, sleeping_furnitures):
        self.beginResetModel()
        self.sleeping_furnitures = sleeping_furnitures
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self.sleeping_furnitures)

    def columnCount(self, parent=QModelIndex()):
        return SLEEPING_FURNITURE_CHARACTERISTICS

    def data(self, index, role):
        if (not self.hasIndex(index.row(), index.column()) or
           role != Qt.DisplayRole):
            return QVariant()

        sleeping_furniture = self.sleeping_furnitures[index.row()]

        getters = ('get_room_number', 'get_name', 'get_quality',
                   'get_sleeping_seats')
        if index.column() < self.columnCount():
            return getattr(sleeping_furniture, getters[index.column()])

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
                return ('Room Number', 'Name', 'Quality',
                        'Sleeping Seats')[section]
        return QVariant()
