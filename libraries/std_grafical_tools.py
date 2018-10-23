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

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import show

from matplotlib.font_manager import FontProperties
from matplotlib import rc
from copy import copy
plt.close('all')

rc('font',family='Arial',size=20)
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#rc('text', usetex=True)

def ylabel_std(ax,text,family='Times New Roman',
               weight='normal',style='normal',size=18):
    """
        Parameters description:
        =======================
            - text:
            -------
                string, ylabel text
            - family:
            -------
                string, font type 
            - weight:
            -------
                string, choose 'light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black'
            - styles:
            -------
                string, choose 'oblique','italic','normal'
            - size:
            -------
                int, font size
    """
    font0 = FontProperties()
    font=font0.copy()
    font.set_family(family)
    font.set_style(style)
    font.set_weight(weight)
    font.set_size(size)
    ax.set_ylabel(text,fontproperties=font)

def xlabel_std(ax,text,family='Times New Roman',
               weight='normal',style='normal',size=18):
    """
        Parameters description:
        =======================
            - text:
            -------
                string, ylabel text
            - family:
            -------
                string, font type 
            - weight:
            -------
                string, choose 'light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black'
            - styles:
            -------
                string, choose 'oblique','italic','normal'
            - size:
            -------
                int, font size
    """
    font0 = FontProperties()
    font=font0.copy()
    font.set_family(family)
    font.set_style(style)
    font.set_weight(weight)
    font.set_size(size)
    ax.set_xlabel(text,fontproperties=font)

def xticks_std(ax,tk_pos,tk_lab,family='Times New Roman',
               weight='normal',style='normal',size=14):
    """
        Parameters description:
        =======================
            - text:
            -------
                string, ylabel text
            - family:
            -------
                string, font type 
            - weight:
            -------
                string, choose 'light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black'
            - styles:
            -------
                string, choose 'oblique','italic','normal'
            - size:
            -------
                int, font size
    """
    tk_lab = copy(tk_lab)
    font0 = FontProperties()
    font=font0.copy()
    font.set_family(family)
    font.set_style(style)
    font.set_weight(weight)
    font.set_size(size)
    ax.set_xticks(tk_pos)
    ax.set_xticklabels(tk_lab,fontproperties=font)

def yticks_std(ax,tk_pos,tk_lab,family='Times New Roman',
               weight='normal',style='normal',size=14):
    """
        Parameters description:
        =======================
            - text:
            -------
                string, ylabel text
            - family:
            -------
                string, font type 
            - weight:
            -------
                string, choose 'light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black'
            - styles:
            -------
                string, choose 'oblique','italic','normal'
            - size:
            -------
                int, font size
    """
    tk_lab = copy(tk_lab)
    font0 = FontProperties()
    font=font0.copy()
    font.set_family(family)
    font.set_style(style)
    font.set_weight(weight)
    font.set_size(size)
    ax.set_yticks(tk_pos)
    ax.set_yticklabels(tk_lab,fontproperties=font)

def legend_std(ax, plt_list,lab_list,family='Times New Roman',
               weight='normal',style='normal',size=18,loc=2):
    "must set line before"
    
    font0 = FontProperties()
    font=font0.copy()
    font.set_family(family)
    font.set_style(style)
    font.set_weight(weight)
    font.set_size(size)
    i=0
    for p in plt_list:
        p.set_label(lab_list[i])
        i+=1
    ax.legend(prop=font,loc=loc)
    
def title_std(ax,text,family='Times New Roman',
               weight='bold',style='normal',size=20):
    """
        Parameters description:
        =======================
            - text:
            -------
                string, ylabel text
            - family:
            -------
                string, font type 
            - weight:
            -------
                string, choose 'light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black'
            - styles:
            -------
                string, choose 'oblique','italic','normal'
            - size:
            -------
                int, font size
    """
    font0 = FontProperties()
    font=font0.copy()
    font.set_family(family)
    font.set_style(style)
    font.set_weight(weight)
    font.set_size(size)
    ax.set_title(text,fontproperties=font)
    




def adjust_spines(ax,spines,pos=0):
    for loc, spine in ax.spines.items():
        if loc in spines:
#            spine.set_position(('outward',10)) # outward by 10 points
            spine.set_position(('outward',pos)) # outward by 10 points
        else:
            spine.set_color('none') # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])



if __name__ == '__main__':
    fig = plt.figure()
    
    x = np.linspace(0,2*np.pi,100)
    y = 2*np.sin(x)
    
    ax = fig.add_subplot(2,2,1)
    ax.plot(x,y)
    adjust_spines(ax,['left'])
    
    ax = fig.add_subplot(2,2,2)
    ax.plot(x,y)
    adjust_spines(ax,[])
    
    ax = fig.add_subplot(2,2,3)
    ax.plot(x,y)
    adjust_spines(ax,['left','bottom'],pos=0)
    ylabel_std(ax,'Ciaone')
    
    ax = fig.add_subplot(2,2,4)
    ax.plot(x,y)
    adjust_spines(ax,['bottom'])
    xticks_std(ax,range(8),range(8+10,8+8+10))
    title_std(ax,'Ilariovich rulez')
    show()
