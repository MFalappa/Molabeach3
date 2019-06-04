import sys
import os
from PyQt5.QtCore import (Qt,pyqtSignal,QPersistentModelIndex,QDataStream,
                          QIODevice,QMimeData,QByteArray,QPoint)
from PyQt5.QtGui import (QIcon, QColor,QDrag)
from PyQt5.QtWidgets import (QTableWidget, QAbstractItemView, QTableWidgetItem, 
                             QWidget,QVBoxLayout, QInputDialog,
                             QListWidgetItem,QApplication)


class TableWidget(QTableWidget):
    
    dropped = pyqtSignal(int)
    dragged = pyqtSignal(int)
    cellExited = pyqtSignal(int, int)
    itemExited = pyqtSignal(QTableWidgetItem)
    
    def __init__(self, rows, columns,dragAndDropCol=2,tableID='input_table', parent=None):
        QTableWidget.__init__(self, rows, columns, parent)
        self._last_index = QPersistentModelIndex()
       
        self.tableID = tableID
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text")\
                or event.mimeData().hasFormat("%s/x-icon-and-text"%self.tableID):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text")\
                or event.mimeData().hasFormat("%s/x-icon-and-text"%self.tableID):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
            
    def startDrag(self, dropActions):
        list_items = self.selectedItems()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeInt(len(list_items))

        for item in list_items:

            rowDrag = item.row()
            stream.writeInt(rowDrag)

        mimeData = QMimeData()
        mimeData.setData("%s/x-icon-and-text"%self.tableID, data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = item.icon().pixmap(24, 24)
        drag.setHotSpot(QPoint(12, 12))
        drag.setPixmap(pixmap)
        drag.exec_(Qt.CopyAction) #== QtCore.Qt.CopyAction:
        self.dragged.emit(len(list_items))

#    def dropEvent(self, event: QDropEvent):
    def dropEvent(self, event):
        if event.mimeData().hasFormat("%s/x-icon-and-text"%self.tableID):
#        if not event.isAccepted() and event.source() == self:
            drop_row = self.drop_on(event)

            rows = sorted(set(item.row() for item in self.selectedItems()))
            rows_to_move = [[QTableWidgetItem(self.item(row_index, column_index)) for column_index in range(self.columnCount())]
                            for row_index in rows]
            for row_index in reversed(rows):
                self.removeRow(row_index)
                if row_index < drop_row:
                    drop_row -= 1

            for row_index, data in enumerate(rows_to_move):
                row_index += drop_row
                self.insertRow(row_index)
                for column_index, column_data in enumerate(data):
                    self.setItem(row_index, column_index, column_data)
            event.accept()
            for row_index in range(len(rows_to_move)):
                self.item(drop_row + row_index, 0).setSelected(True)
                self.item(drop_row + row_index, 1).setSelected(True)
                
        
        elif event.mimeData().hasFormat("application/x-icon-and-text"):
            group, okPressed  = QInputDialog.getText(self,'Insert Group Name','Group name:')
            
            data = event.mimeData().data("application/x-icon-and-text" )
            stream = QDataStream(data, QIODevice.ReadOnly)

            num_drag = stream.readInt()
            oldRowNum = self.rowCount()

            self.setRowCount(oldRowNum+num_drag)
            

            for row in range(oldRowNum,oldRowNum+num_drag):
                item = QTableWidgetItem(group)
                self.setItem(row,0,item)
                dataName = stream.readQString()
                dataIcon = QIcon()
                stream >> dataIcon

                item = QTableWidgetItem(dataName)
                item.setIcon(dataIcon)
                self.setItem(row,1,item)
                
        super().dropEvent(event)

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.rowCount()

        return index.row() + 1 if self.is_below(event.pos(), index) else index.row()

    def is_below(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        # noinspection PyTypeChecker
        return rect.contains(pos, True) and not (int(self.model().flags(index)) & Qt.ItemIsDropEnabled) and pos.y() >= rect.center().y()


class Window(QWidget):
    def __init__(self, rows, columns):
        QWidget.__init__(self)
        self.table = TableWidget(rows, columns,2,'input_table', self)
        dndListWidget = MyDnDListWidget()
        for column in range(columns):
            for row in range(rows):
                item = QTableWidgetItem('Text%d' % row)
                self.table.setItem(row, column, item)
        
        layout = QVBoxLayout(self)

        path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
#        path = '/Users/Matte/Python_script/Phenopy3/'
        i = 0
        for image in sorted(os.listdir(os.path.join(path, "images"))):
            if image.endswith(".png") or image.endswith(".ico"):
                item = QListWidgetItem(image.split(".")[0].capitalize())
                if i in [0, 2, 3]:
                    item.setIcon(QIcon(os.path.join(path,
                                                    "images/{0}".format(image))))
                i += 1
                dndListWidget.addItem(item)


        layout.addWidget(self.table)
        layout.addWidget(dndListWidget)


        self.table.itemEntered.connect(self.handleItemEntered)
        self.table.itemExited.connect(self.handleItemExited)

    def handleItemEntered(self, item):
        item.setBackground(QColor('moccasin'))

    def handleItemExited(self, item):
        item.setBackground(QTableWidgetItem().background())
        

if __name__ == '__main__':
    
    sys.path.append('/Users/Matte/Python_script/Phenopy3/dialogsAndWidget/analysisDlg/')
#    sys.path.append('/Users/edoardo/Work/Code/phenopy/dialogsAndWidget/analysisDlg')
    from MyDnDDialog import MyDnDListWidget
    app = QApplication(sys.argv)
    window = Window(6, 3)
    window.setGeometry(500, 300, 350, 250)
    window.show()
    sys.exit(app.exec_())