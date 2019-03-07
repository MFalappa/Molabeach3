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

import os,sys
file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
lib_dir = os.path.join(file_path,'libraries')
sys.path.append(lib_dir)
from PyQt5.QtWidgets import (QDialog,QAbstractItemView,QListWidgetItem,
                             QListWidget,QLabel,QSizePolicy,QSpacerItem,QHBoxLayout,
                             QVBoxLayout,QPushButton,QApplication)
from PyQt5.QtGui import QPixmap,QIcon,QImage
from PyQt5.QtCore import pyqtSignal,Qt
from ui_import_function import Ui_Dialog


from automatic_input_detection import (return_input_count, check_analysis_function, 
                                       check_plot_function)


class dialog_upload_function(QDialog, Ui_Dialog):
    upload_signal = pyqtSignal(list, dict, name='sig_dlg')
    def __init__(self, type_list=[], pathAnalysis=None, pathPlotting=None, parent=None):
        super(dialog_upload_function, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.input_dict = None
        refr = QPixmap.fromImage(QImage(os.path.join(file_path,'images','refresh.jpg')))
        icon = QIcon(refr)
        print(os.path.join(file_path,'images','refresh.jpg'))
        self.pushButton_refresh.setIcon(icon)
        self.pushButton_refresh.setText('')
        
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.pathAnalysis = pathAnalysis
        self.pathPlotting = pathPlotting
        self.type_list_available = list(set(type_list))
        self.type_list_selected = []
        self.listWidget_inputType.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.dict_inputs = {}
        self.pushButton_Continue.setEnabled(False)
        
        self.controlFunctions()
        self.addDetectedInput()
        
        self.pushButton_addType.clicked.connect(self.addType)
        self.pushButton_Cancel.clicked.connect(self.close)
        self.pushButton_Continue.clicked.connect(self.emit_signal)
        self.pushButton_remove.clicked.connect(self.removeType)
        self.pushButton_refresh.clicked.connect(self.controlFunctions)
       
        
        
    def addDetectedInput(self):
        if not self.pathAnalysis:
            return
        
        string = ''
        try:
            inp = return_input_count(self.pathAnalysis)
            for key in list(inp.keys()):
                if inp[key] > 0:
                    string += 'Found %d input of type %s\n'%(inp[key],key)
        except NameError as e:
            string += 'NameError, '+ e.message
            print(e.args)
            print(e.__dict__)
            inp = None
        self.textBrowser_inputDetected.setText(string)
        self.input_dict = inp
    
    def removeType(self):
        list_items = self.listWidget_inputType.selectedItems()
        for item in list_items:
            text = item.text()
            self.type_list_available.append(text)
            self.type_list_selected.remove(text)
        self.listWidget_inputType.clear()
        for item in self.type_list_selected:
            qitem = QListWidgetItem(item)
            self.listWidget_inputType.addItem(qitem)
        self.controlFunctions()   
        
    def addType(self):
        print('Adding')
        self.type_list_available += self.type_list_selected
        self.type_list_selected = []
        dialog = listTypeDlg(self.type_list_available,parent=self)
        if dialog.exec_():
            self.listWidget_inputType.clear()
            for item in self.type_list_selected:
                res = self.listWidget_inputType.findItems(item, Qt.MatchExactly)
                if not res:
                    qitem = QListWidgetItem(item)
                    self.listWidget_inputType.addItem(qitem)
        self.controlFunctions()
        
    def controlFunctions(self):
        print( 'control')
        res = check_analysis_function(self.pathAnalysis)
        string = '<b>Check Analysis Function:</b><br>'
        string += res[1]
        self.textBrowser_status.setText(string)
        if res[0]:
            self.dict_inputs.update(res[2])
            string += '<br><br><b>Check Plotting Function:</b><br>'
            res2 = check_plot_function(self.pathPlotting,res[2])
            string += res2[1]
            self.textBrowser_status.setText(string)
            if res2[0] and self.input_dict:
                self.pushButton_Continue.setEnabled(True)
        if self.listWidget_inputType.count() is 0:
            self.pushButton_Continue.setEnabled(False)
                
    def emit_signal(self):
        self.upload_signal.emit(self.type_list_selected,self.input_dict)
        self.accept()
        
class listTypeDlg(QDialog):
    def __init__(self,list_types,parent=None):
        super(listTypeDlg,self).__init__(parent)
        self.parent = parent
        self.list_types = list_types
        self.listWidget = QListWidget()
        for lab in self.list_types:
            item = QListWidgetItem(lab)
            self.listWidget.addItem(item)
#        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        label = QLabel('Input Type List:')
        spaceritem = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        hlayout = QHBoxLayout()
        hlayout.addWidget(label)
        hlayout.addSpacerItem(spaceritem)
        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.listWidget)
        
        spaceritem = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        pushButtonAdd = QPushButton('Add')
        pushButtonCancel = QPushButton('Cancel')
        hlayout = QHBoxLayout()
        hlayout.addSpacerItem(spaceritem)
        hlayout.addWidget(pushButtonCancel)
        hlayout.addWidget(pushButtonAdd)
        vlayout.addLayout(hlayout)
        self.setLayout(vlayout)
        pushButtonAdd.clicked.connect(self.addTypes)
        pushButtonCancel.clicked.connect(self.reject)
      
        
        
    def addTypes(self):
        list_items = self.listWidget.selectedItems()
        for item in list_items:
            text = item.text()
            self.parent.type_list_available.remove(text)
            self.parent.type_list_selected.append(text)
        self.accept()
    

def main():
    import sys
    import os
    fld = '/Users/Matte/Python_script/Phenopy3/future'
    app = QApplication(sys.argv)
    form = dialog_upload_function(pathAnalysis=os.path.join(fld,'new_switch.py'),pathPlotting=os.path.join(fld,'new_switch_plt.py'),
                                  type_list=['siamo troppo fighi','abbasso bk']*40)
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
    
