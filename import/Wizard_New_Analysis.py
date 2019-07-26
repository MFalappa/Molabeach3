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

TODO:
allow multiple data types
use the info from the first wizard dialog to get infos for the Analysis.npy dicitonary
check add function
check remove functions step by step
          
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
from PyQt5.QtCore import (pyqtSignal)
from inputDlg_creating_input import inputDlg_creating_input
from functionCaller_Generator import (functionCaller_Generator,add_To_Custom_Analysis,
                                      add_To_Plot_Launcher,get_Function_List,remove_Functions)
from deleteDlg import deleteDlg
import numpy as np
from data_type_selection import data_type_selection
from analysis_data_type_class import refreshTypeList

class new_Analysis_Wizard(QDialog):
    editedDictionary = pyqtSignal(dict)
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

        self.alias,self.function_descr = dialog.get_func_info()

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
        # get the list of available funcitons
        list_analysis_func = get_Function_List(os.path.join(lib_dir,self.customAnalysisFile))
        list_plot_func = get_Function_List(os.path.join(lib_dir,self.customPlotsFile))
        # get base names
        an_func = get_Function_List(self.path_analysis)[0]
        plt_func = get_Function_List(self.path_plotting)[0]
        # check if already present
        if an_func in list_analysis_func:
            print('function with the same name already present in: %s'%os.path.join(lib_dir,self.customAnalysisFile))
            self.reject()
            return
        if plt_func in list_plot_func:
            print('function with the same name already present in: %s' % os.path.join(lib_dir, self.customPlotsFile))
            self.reject()
            return
        # import dictionary info
        dictionary = np.load(os.path.join(phenopy_dir, 'Analysis.npy')).all()
        alias_list = list(dictionary.keys())

        if self.alias in  alias_list:
            print('Function label %s already used!'%self.alias)
            self.reject()
            return


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
                    self.reject()
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

        if self.analysisType != 'Integrative':
            dictionary[self.alias] = {'analysis_function' : an_func,
                               'description' : self.function_descr,
                               'type_func' : self.analysisType,
                               'accepted_type_0' : type_list,
                               'is_integrative' : False,
                               'plot_function' : plt_func
                               }
        else:
            dictionary[self.alias] = {'analysis_function': an_func,
                                   'description': self.function_descr,
                                   'type_func': self.analysisType,
                                   'is_integrative': False,
                                   'plot_function': plt_func
                                   }
            ## something like that
            # for kk in range(num_data_types):
            #     dictionary[an_func]['accepted_type_%d'%kk] = type_list[kk]

        np.save(os.path.join(phenopy_dir,'Analysis.npy'),dictionary)
        self.editedDictionary.emit(dictionary)
        self.accept()
#==============================================================================
#   sembra tutto ok... controllare      
#==============================================================================
    def remove_Functions_(self):
        path = lib_dir
        # dialog = Wizard_2()
        # if not dialog.exec_():
        #     return
        # analysisType = dialog.analysisType
        path = str(path)
        dictionary = np.load(os.path.join(phenopy_dir, 'Analysis.npy')).all()
        # get the label for each analysis
        alias_list = list(dictionary.keys())

        dialog = deleteDlg(alias_list,self)
        if not dialog.exec_():
            self.reject()
            return

        deleteList = dialog.get_List()
        print('delete list ',deleteList)
        remove_Functions(path,deleteList,dictionary)

        for func in deleteList:
            dictionary.pop(func)

        
        np.save(os.path.join(phenopy_dir,'Analysis.npy'),dictionary)
        self.editedDictionary.emit(dictionary)
        
        self.accept()

def main():
    app = QApplication(sys.argv)

    form = new_Analysis_Wizard()
    
    form.show()
    
    #print(form.exec_())
    app.exec_()
if __name__=='__main__':
    main()

    