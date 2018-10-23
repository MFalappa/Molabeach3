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
import pandas as pd
import numpy as np
import sys
import os

phenopy_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(phenopy_dir,'libraries')))
sys.path.append(phenopy_dir)

from Modify_Dataset_GUI import *

def export_EEG_DataStruct(path,data_eeg,txt_delimiter=';'):
    data_eeg = data_eeg.reconstructDataMatrix()
    if path.endswith(('xls','xslx')):
        writer = pd.ExcelWriter(path)
        df = pd.DataFrame(data_eeg)
        df.to_excel(writer,index=False)
        writer.save()
        return True, 'Data %s succesfully saved as excel file'%os.path.basename(path)
    elif path.endswith(('csv','txt')):
        header = txt_delimiter.join(data_eeg.dtype.names)
        fmt = ['%i','%s','%s'] + ['%f']*(len(data_eeg.dtype.names)-3)
        np.savetxt(path,data_eeg,comments='',header=header,fmt=fmt,delimiter=txt_delimiter)
        return True, 'Data %s succesfully saved as text file'%os.path.basename(path)
    else:
        return False, 'Could not export with the indicated exention'

def export_numpy_array(path, array, delimiter=';'):
    if path.endswith(('xls','xslx')):
        try:
            writer = pd.ExcelWriter(path)
            df = pd.DataFrame(array)
            df.to_excel(writer,index=False)
            writer.save()
            return True, 'Data %s succesfully saved as excel file'%os.path.basename(path)
        except Exception, e:
            return False,'Couldn\'t save to excel with the following exception \"%s\"'%e
    elif path.endswith(('csv','txt')):
        fmt = []
        if array.dtype.names:
            type_list = array.dtype.descr
            header = delimiter.join(array.dtype.names)
        else:
            type_list = [('',array.dtype)]
            header = ''
        for STR,TYPE in type_list:
            if np.dtype(TYPE) == float:
                fmt += ['%f']
            elif np.dtype(TYPE) == int or np.dtype(TYPE) == long:
                fmt += ['%d']
            elif np.dtype(TYPE) == complex:
                fmt+= ['%s']
            elif np.dtype(TYPE).char == 'S':
                fmt += ['%s']
            else:
                return False, 'Unable to understand format %s'%TYPE
        if len(fmt) is 1:
            fmt = fmt[0]
        np.savetxt(path,array,delimiter=delimiter,header=header,comments='',
                   fmt=fmt)
        return True, 'Data %s succesfully saved as text file'%os.path.basename(path)

def save_a_Dataset_GUI(dataGUI, path_file):
    if '.' in path_file:
        path_file = '.'.join(path_file.split('.')[:-1]) + '.npz'
    else:
        path_file += '.npz'
    np.savez_compressed(path_file ,dataGUI)
    os.rename(path_file, path_file.split('.')[0] + '.phz')
    return True, 'Data %s succesfully saved'%(path_file.split('.')[0] + '.phz')
                        
def select_export(data_exp, path, delimiter=';'):
    print(type(data_exp))
    if type(data_exp) == EEG_Data_Struct:
        return export_EEG_DataStruct(path,data_exp,txt_delimiter=delimiter)
    elif type(data_exp) == Dataset_GUI:
        return save_a_Dataset_GUI(data_exp,path)
    elif type(data_exp) == np.ndarray or type(data_exp) == np.recarray:
        return export_numpy_array(path,data_exp,delimiter=delimiter)
    else:
        return False, 'Unable to export data of type %s'%(type(data_exp))
        




def main():
    test_data=np.random.uniform(size=(10,4))
    path1 = 'C:\Users\ebalzani\Desktop\TMP\\test.xls'
    path2 = 'C:\Users\ebalzani\Desktop\TMP\\test.csv'
    print export_numpy_array(path1,test_data)
    print export_numpy_array(path2,test_data)
    test_data=np.zeros(10,dtype={'names':('a','b','c','d','e'),
                                 'formats':('S10','f8',long,int,complex)})
    path1 = 'C:\Users\ebalzani\Desktop\TMP\\test1.xls'
    path2 = 'C:\Users\ebalzani\Desktop\TMP\\test1.csv'
    print export_numpy_array(path1,test_data)
    print export_numpy_array(path2,test_data)
    
if __name__ == '__main__':
    main()