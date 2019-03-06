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
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui_import_function_integrative import *
#from messageLib import *

from automatic_input_detection import return_input_count, check_analysis_function, check_plot_function


class dialog_upload_function_integrative(QDialog, Ui_Dialog):
    upload_signal = pyqtSignal(dict, name='input_detected')
    def __init__(self, pathAnalysis=None, pathPlotting=None, parent=None):
        super(dialog_upload_function_integrative, self).__init__(parent)
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
        self.dict_inputs = {}
        
        self.addDetectedInput()
        self.controlFunctions()
        
        
        self.connect(self.pushButton_Cancel,SIGNAL('clicked()'),self.close)
        self.connect(self.pushButton_Continue,SIGNAL('clicked()'),self.emit_signal)
        self.connect(self.pushButton_refresh,SIGNAL('clicked()'),self.controlFunctions)
        
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
                return
        self.pushButton_Continue.setEnabled(False)
                
    def emit_signal(self):
        self.upload_signal.emit(self.input_dict)
        self.accept()
    

def main():
    import sys
    fld = '/Users/Matte/Python_script/Phenopy3/future'
    app = QApplication(sys.argv)
    form = dialog_upload_function_integrative(pathAnalysis=s.path.join(fld,'new_switch.py'),pathPlotting=s.path.join(fld,'new_switch_plt.py'))
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
    
