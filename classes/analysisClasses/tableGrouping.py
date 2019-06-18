import sys
import os
from PyQt5.QtCore import (Qt,pyqtSignal,QPersistentModelIndex,QDataStream,
                          QIODevice)
from PyQt5.QtGui import (QIcon, QColor)
from PyQt5.QtWidgets import (QTableWidget, QTableWidgetItem, 
                             QWidget,QVBoxLayout, QInputDialog,
                             QListWidgetItem,QApplication,QMessageBox)

import numpy as np



class TableWidget(QTableWidget):
    
    element_in = pyqtSignal(dict)
#    dragged = pyqtSignal(int)
#    cellExited = pyqtSignal(int, int)
#    itemExited = pyqtSignal(QTableWidgetItem)
    
    def __init__(self, rows, columns,dragAndDropCol=2,tableID='input_table', parent=None):
        QTableWidget.__init__(self, rows, columns, parent)
        self._last_index = QPersistentModelIndex()
       
        self.tableID = tableID
        self.dict_elemenet = {}
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
    
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text")\
                or event.mimeData().hasFormat("%s/x-icon-and-text"%self.tableID)\
                    or event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text")\
                or event.mimeData().hasFormat("%s/x-icon-and-text"%self.tableID)\
                    or event.mimeData().hasFormat("application/x-qabstractitemmodeldatalist"):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
        
    def dropEvent(self, event):
        if event.source() == self:
            try:
                drop_row,drop_col = self.drop_on(event)
                self.setRowCount(self.rowCount()+len(self.selectedItems()))
            
                for item in self.selectedItems():
                    if hasattr(self.item(drop_row,drop_col), 'type'):
                        flag = True
                        while flag:
                            if hasattr(self.item(drop_row,drop_col), 'type'):
                                self.setRowCount(self.rowCount()+1)
                                drop_row += 1
                            else:
                                flag = False

                        self.setItem(drop_row,drop_col,item)
                        drop_row += 1      
                    else:  
                        self.setItem(drop_row,drop_col,item)
                        drop_row += 1
                        
                    newitem = QTableWidgetItem()
                    self.setItem(item.row(), item.column(), newitem)
                    
#                super().dropEvent(event)
                
            except:
                
                ret = QMessageBox.question(self,
                                    "Selected items",
                                    "Would you like to create a new group?",
                                    QMessageBox.Yes | QMessageBox.No)

                
                if ret == QMessageBox.Yes:
                    group, okPressed  = QInputDialog.getText(self,'Insert Group Name','Group name:') 
            
                    names = []
                    for colName in range(0,self.columnCount()):
                        names += [self.horizontalHeaderItem((colName)).text()]
                        
                    if not group in names:
                        self.insertColumn(self.columnCount())
                        names += [group]
                        self.setHorizontalHeaderLabels(names)
                        drop_col = self.columnCount()
                        drop_row = 0
                        self.setRowCount(self.rowCount()+len(self.selectedItems()))
            
                        for item in self.selectedItems():
                            self.setItem(drop_row,drop_col,item)
                            drop_row += 1
                                
                            newitem = QTableWidgetItem()
                            self.setItem(item.row(), item.column(), newitem)

                    
                elif ret == QMessageBox.No:
                    ret = QMessageBox.question(self, "Selected items",
                                    "Would you like to delate selected items?",
                                    QMessageBox.Yes | QMessageBox.Cancel)
                    
                    
                    if ret == QMessageBox.Yes:
                        for item in self.selectedItems():
                            newitem = QTableWidgetItem()
                            self.setItem(item.row(), item.column(), newitem)
                        event.accept()
                    
                    else:
                        for item in self.selectedItems():
                            self.setItem(item.row(), item.column(), item)
                        event.accept()
                    
                                                        
            super().dropEvent(event)
            
            row_index = np.zeros(self.rowCount(),dtype = int)
            # tolgo colonne o righe vuote
            for rr in range(self.rowCount()):
                items = np.zeros(self.columnCount(),dtype = int)
                for cc in range(self.columnCount()):
                    if hasattr(self.item(rr, cc), 'text'):
                        if self.item(rr, cc).text() != '':
                            items[cc] = 1
 
                if np.sum(items) == 0:
                    row_index[rr] = 1
                    
            idx = np.where(row_index==1)[0]
            for r_idx in idx:
                self.removeRow(r_idx)
                
            col_index = np.zeros(self.columnCount(),dtype = int)
            
            for cc in range(self.columnCount()):
                items = np.ones(self.rowCount(),dtype = int)
                for rr in range(self.rowCount()):
                    if hasattr(self.item(rr, cc), 'text'):
                        if self.item(rr, cc).text() == '':
                            items[rr] = 0
                    else:
                         items[rr] = 0

                if np.sum(items) == 0:
                    col_index[cc] = 1
                    
            idx = np.where(col_index==1)[0]
            for r_idx in idx:
                tit = self.horizontalHeaderItem((r_idx)).text()
                quest = '%s is an empty group, do you want to remove it?' %tit
                qm = QMessageBox
                ret = qm.question(self,'Message', quest, qm.Yes | qm.No)
                    
                if ret == qm.Yes:
                    self.removeColumn(r_idx)
                    
                    
            list_items = {}
            for cc in range(self.columnCount()):
                gr_mame = self.horizontalHeaderItem((cc)).text()
                print(gr_mame)
                sr_member = []
                for rr in range(self.rowCount()):
                    if hasattr(self.item(rr, cc), 'text'):
                        if self.item(rr, cc).text() != '':
                            sr_member += [self.item(rr, cc).text()]
                
                list_items[gr_mame] = sr_member
            
            self.dict_elemenet = list_items
            self.element_in.emit(list_items)
            
           
        
        elif event.mimeData().hasFormat("application/x-icon-and-text"):
            
            group, okPressed  = QInputDialog.getText(self,'Insert Group Name','Group name:') 
            names = []
            for colName in range(0,self.columnCount()):
                names += [self.horizontalHeaderItem((colName)).text()]
            
            if not group in names:
                self.insertColumn(self.columnCount())
                names += [group]
                self.setHorizontalHeaderLabels(names)
                func = self.columnCount()
            else:
                for nm in range(len(names)):
                    if names[nm] == group:
                        func = nm + 1
            
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            
            num_drag = stream.readInt()
            oldRowNum = self.rowCount()

            self.setRowCount(oldRowNum+num_drag)
                
            for row in range(oldRowNum,oldRowNum+num_drag):
                dataName = stream.readQString()
                dataIcon = QIcon()
                stream >> dataIcon
                item = QTableWidgetItem(dataName)
                item.setIcon(dataIcon)
                if self.columnCount() < 2:
                    self.setItem(row-1,func,item)
                else:
                    self.setItem(row,func-1,item)
                    
        
        list_items = {}
        for cc in range(self.columnCount()):
            gr_mame = self.horizontalHeaderItem((cc)).text()
            sr_member = []
            for rr in range(self.rowCount()):
                if hasattr(self.item(rr, cc), 'text'):
                    if self.item(rr, cc).text() != '':
                        sr_member += [self.item(rr, cc).text()]
            
            list_items[gr_mame] = sr_member
        
        
        self.dict_elemenet = list_items
        self.element_in.emit(list_items)
                    
        super().dropEvent(event)

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.rowCount()

        return (index.row() + 1 if self.is_below(event.pos(), index) else index.row()),index.column()

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
        super(Window, self).__init__()
#        QWidget.__init__(self)
        self.table = TableWidget(rows, columns,'input_table', self)
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
        

#        self.table.itemEntered.connect(self.handleItemEntered)
#        self.table.itemExited.connect(self.handleItemExited)

#    def handleItemEntered(self, item):
#        item.setBackground(QColor('moccasin'))
#
#    def handleItemExited(self, item):
#        item.setBackground(QTableWidgetItem().background())
        

if __name__ == '__main__':
    
    sys.path.append('/Users/Matte/Python_script/Phenopy3/dialogsAndWidget/analysisDlg/')
#    sys.path.append('/Users/edoardo/Work/Code/phenopy/dialogsAndWidget/analysisDlg')
    from MyDnDDialog import MyDnDListWidget
    app = QApplication(sys.argv)
#    window = Window(6, 3)
    window = Window(0, 0)
    window.setGeometry(500, 300, 350, 250)
    window.show()
    sys.exit(app.exec_())