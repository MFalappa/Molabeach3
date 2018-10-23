# -*- coding: utf-8 -*-
"""
Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

Copyright (C) 2017 FONDAZIONE ISTITUTO ITALIANO DI TECNOLOGIA
                   E. Balzani, M. Falappa - All rights reserved

@author: edoardo.balzani87@gmail.com; mfalappa@outlook.it

                                Publication:
         An approach to monitoring home-cage behavior in mice that 
                          facilitates data sharing
                          
        DOI: 10.1038/nprot.2018.031
          
"""
#import os
#import sys
#from PyQt4.QtCore import (QByteArray, QDataStream, QIODevice, QMimeData,
#        QPoint, Qt)
#from PyQt4.QtGui import (QApplication, QDialog, QDrag, 
#        QGridLayout, QIcon, QListWidget,QListWidgetItem)
#
import sys
import os
from PyQt4.QtCore import (QByteArray, QDataStream, QIODevice, QMimeData,
        QPoint, Qt,SIGNAL)
from PyQt4.QtGui import ( QDrag, QIcon, QListWidget,QListWidgetItem,QDialog,QApplication,QGridLayout,QAbstractItemView)



class MyDnDListWidget(QListWidget):
    def __init__(self, parent=None):
        super(MyDnDListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
            #event.ignore()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(Qt.MoveAction)
            event.accept()
            
            #event.ignore()
        else:
            event.ignore()


    def dropEvent(self, event):
        
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            num_drag = stream.readInt()
            for k in xrange(num_drag):
                text = stream.readQString()
                icon = QIcon()
                stream >> icon
                item = QListWidgetItem(text)
                item.setIcon(icon)
                items=self.findItems(text,Qt.MatchExactly)
                if len(items)>0:
                    event.setDropAction(Qt.CopyAction)
                    #self.takeItem(self.row(items[0]))
                    event.ignore()
                   
                    
                else:
                    self.addItem(item) 
                    event.setDropAction(Qt.MoveAction)
                    event.accept()
                    self.emit(SIGNAL('dropped()'))
                
        else:
            event.ignore()
            

    def startDrag(self, dropActions):
        list_items = self.selectedItems()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeInt(len(list_items))
        for item in list_items:
            icon = item.icon()
            stream.writeQString(item.text())
            stream << icon
        mimeData = QMimeData()
        mimeData.setData("application/x-icon-and-text", data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QPoint(12, 12))
        drag.setPixmap(pixmap)
        if drag.start(Qt.MoveAction) == Qt.MoveAction:
            for item in list_items:
                self.takeItem(self.row(item))
            self.emit(SIGNAL('dragged()'))
            
class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        dndListWidget = MyDnDListWidget()
        if os.path.exists('C:\Users\ebalzani\Desktop\TMP'):
            path = 'C:\Users\ebalzani\Desktop\TMP\\'
        else:
            path = os.path.dirname(__file__)
        i=0
        for image in sorted(os.listdir(os.path.join(path, "images"))):
            if image.endswith(".png") or image.endswith(".ico"):
                item = QListWidgetItem(image.split(".")[0].capitalize())
                if i in [0,2,3]:
                    item.setIcon(QIcon(os.path.join(path,
                                   "images/{0}".format(image))))
                i+=1
                dndListWidget.addItem(item)
        dndIconListWidget = MyDnDListWidget()
        dndIconListWidget.setViewMode(QListWidget.IconMode)
        

        layout = QGridLayout()
        layout.addWidget(dndListWidget, 0, 0)
        layout.addWidget(dndIconListWidget, 0, 1)
        
        
        self.setLayout(layout)

        self.setWindowTitle("Custom Drag and Drop")

def main():
    from deleteDlg import deleteDlg
    app = QApplication(sys.argv)
    form = deleteDlg(['ciao','cacao'])
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
