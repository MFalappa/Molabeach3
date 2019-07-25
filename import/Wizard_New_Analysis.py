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
import sys,os
phenopy_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../..')),'mainScripts')
lib_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../..')),'libraries')
import_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../..')),'import')
classes_dir = os.path.join(os.path.abspath(os.path.join(__file__,'../..')),'classes','analysisClasses')
sys.path.append(lib_dir)
sys.path.append(classes_dir)
sys.path.append(import_dir)
from Wizard_1 import Wizard_1
from Wizard_2 import Wizard_2
from dialog_loadfunction import dialog_upload_function
from dialog_loadfunction_integrative import dialog_upload_function_integrative
from Wizard_Input import inputDialog_Wizard

from PyQt5.QtWidgets import (QLabel,QDialog,QApplication,QPushButton,QVBoxLayout,
                             QHBoxLayout,QSpacerItem,QSizePolicy)

from PyQt5.QtGui import (QFont)
#from PyQt5.QtCore import (pyqtSignal)
from inputDlg_creating_input import inputDlg_creating_input
from functionCaller_Generator import (functionCaller_Generator,add_To_Custom_Analysis,
                                      add_To_Plot_Launcher,get_Function_List,remove_Functions)
from deleteDlg import deleteDlg
import numpy as np
from data_type_selection import data_type_selection
from analysis_data_type_class import refreshTypeList

class new_Analysis_Wizard(QDialog):
    def __init__(self,parent = None):
        super(new_Analysis_Wizard,self).__init__(parent)
        print('VERSIONE DA TESTARE, NUOVA ORGANIZZAZIONE ANALISI')
        refreshTypeList(import_dir)
        Label = QLabel('Add a new analysis:  ')
        Start = QPushButton('Add')
        Label_2 = QLabel('Delete analysis:  ')
        Delete = QPushButton('Delete')
        Cancel = QPushButton('Cancel')
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, 
                                 QSizePolicy.Minimum)
        font = QFont()
        font.setBold(True)
        font.setPixelSize(15)
        Label.setFont(font)
        Label_2.setFont(font)
        Hlayout = QHBoxLayout()
        layout = QVBoxLayout()
        Hlayout.addWidget(Label)
        Hlayout.addSpacerItem(spacerItem)
        Hlayout.addWidget(Start)
        layout.addLayout(Hlayout)
        
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, 
                                 QSizePolicy.Minimum)
        Hlayout = QHBoxLayout()
        Hlayout.addWidget(Label_2)
        Hlayout.addSpacerItem(spacerItem)
        Hlayout.addWidget(Delete)
        layout.addLayout(Hlayout)
        
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, 
                                 QSizePolicy.Minimum)
        Hlayout = QHBoxLayout()
        Hlayout.addSpacerItem(spacerItem)
        Hlayout.addWidget(Cancel)
        layout.addLayout(Hlayout)
        
        Cancel.clicked.connect(self.reject)
        Start.clicked.connect(self.startWizard)
        Delete.clicked.connect(self.remove_Functions_)
       
  
        
        self.setLayout(layout)
        
    def startWizard(self):
        dialog = Wizard_1()
        if not dialog.exec_():
            self.reject()
            return
        self.path_analysis = dialog.lineEdit_analysis.text()
        self.path_plotting = dialog.lineEdit_plotting.text()
        self.analysisType = dialog.analysisType
        
        self.customAnalysisFile = 'analysis_functions.py'
        self.customPlotsFile    = 'plots_functions.py'
        self.launcherAnalysis   = 'launcher_all.py'
        self.launcherPlots      = 'plot_Launcher_all.py'
        
        
        if self.analysisType != 'Integrative':
            path_type_list = os.path.join(import_dir,'data_type_list.npy')
            dialog = dialog_upload_function(type_list=list(np.load(path_type_list)),
                                            pathAnalysis=self.path_analysis, 
                                            pathPlotting=self.path_plotting, parent=self)
            dialog.upload_signal.connect(self.check_and_continue)
        else:
            dialog = dialog_upload_function_integrative(pathAnalysis=self.path_analysis, 
                                            pathPlotting=self.path_plotting, parent=self)
            dialog.upload_signal.connect(self.ask_integrative_input)
        dialog.exec_()
        return
    
    def ask_integrative_input(self,input_dict):
        path_type_list = os.path.join(import_dir,'data_type_list.npy')
        type_list = list(np.load(path_type_list))
        dialog = data_type_selection(type_list)        
        if not dialog.exec_():
            return
        self.check_and_continue(dialog.dict_res, input_dict)
    
    def check_and_continue(self,type_list,input_dict):
#        print('CHECK AND CONTINUE')
#        print(input_dict)
#        print(type_list)
#        Includo funzione in custom analysis
        tot_num = sum(input_dict.values())
        ind = 0
        dictionaryInput = {}
        for inputName in list(input_dict.keys()):
            if inputName == 'PhaseSel' and input_dict['PhaseSel'] == 1:
                dictionaryInput['PhaseSel'] = []
                continue
            string = '['
            for num in range(1,input_dict[inputName]+1):
                if ind == tot_num-1:
                    ButtonText = 'Apply'
                else:
                    ButtonText = 'Continue'
                dialog = inputDialog_Wizard(inputName,num, ButtonText = ButtonText,parent=self)
                if not dialog.exec_():
                    return
                string += dialog.input + ','
                ind += 1
            string = string[:-1] +  ']'
            if string != ']':
                dictionaryInput[inputName] = string
        

        funcName = add_To_Custom_Analysis(lib_dir,self.path_analysis,
                                          AddTo = self.customAnalysisFile)
        
#        Rigenero il file che chiama le funzioni

        path = os.path.join(lib_dir,self.customAnalysisFile)
        functionCaller_Generator(path,
                                 self.launcherAnalysis,
                                 classes_dir,self.analysisType)
        
        inputDlg_creating_input(classes_dir,dictionaryInput,funcName)
#        check if it works from here
        plotFun = add_To_Custom_Analysis(lib_dir,self.path_plotting,
                                         AddTo = self.customPlotsFile)                             
        add_To_Plot_Launcher(classes_dir,plotFun,funcName,
                             AddTo = self.launcherPlots)
 
        dictionary = np.load(os.path.join(phenopy_dir,'Analysis.npy')).all()
        
        dictionary[self.analysisType][funcName] = type_list
        np.save(os.path.join(phenopy_dir,'Analysis.npy'),dictionary)
        self.accept()
#==============================================================================
#   sembra tutto ok... controllare      
#==============================================================================
    def remove_Functions_(self):
        path = lib_dir
        dialog = Wizard_2()
        if not dialog.exec_():
            return
        analysisType = dialog.analysisType
        path = str(path) 
        
        if analysisType == 'Single':
            String = ''
        else:
            String = '_Gr'
        funcList_1 = get_Function_List(os.path.join(path, 'custom_Analysis%s.py'%String))
        funcList = funcList_1 + get_Function_List(os.path.join(path , 'custom_Plots%s.py'%String))
        dialog = deleteDlg(funcList,self)
        if not dialog.exec_():
            self.reject()
            return
        deleteList = dialog.get_List()
        print('delete list ',deleteList)
        remove_Functions(path,deleteList,String)
        dictionary = np.load(os.path.join(phenopy_dir,'Analysis.npy')).all()
        if analysisType == 'Single':
            for func in deleteList:
                if func in funcList_1:
                   dictionary['Single'].pop(func)
        else:
            for func in deleteList:
                if func in funcList_1:
                    try:
                        dictionary['Group'].pop(func)
                    except:
                        dictionary['Integrative'].pop(func)
        
        np.save(os.path.join(phenopy_dir,'Analysis.npy'),dictionary)
        
        
        self.accept()
def main():
    app = QApplication(sys.argv)

    form = new_Analysis_Wizard()
    
    form.show()
    
    #print(form.exec_())
    app.exec_()
if __name__=='__main__':
    main()

    