# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:32:28 2017

@author: Antonio
"""

from csv import reader
from LabFunctions import getTables
from LabFunctions import getFlags
from LabFunctions import toFile
from LabFunctions import makeReport
import os


etiquetas = set(["a","b","v","x","y","z","d","c","p","t","l","2"])
file = input("ingrese el nombre del archivo con los títulos: ")
tit = list(reader(open(file,'r',encoding="iso-8859-1"), delimiter=','))
file = input("ingrese el nombre del archivo con los subs: ")
doc = list(reader(open(file,'r',encoding="iso-8859-1"), delimiter=','))
titles,clas = getFlags(tit)
name = file.replace(".csv","")
try:
    os.mkdir(name)
    os.mkdir(name+"/Reportes")
    os.mkdir(name+"/Tablas")
except:
    pass
n = int(input("Ingrese la columna desde la que empiezan los datos: "))+1
tmp = "./"+name+"/Reportes/"
tables,reg,reg2,reg3,reg4 = getTables(doc,etiquetas,titles,clas,n,tmp)
for i in tables:
    toFile(list(tables[i]),"./"+name+"/Tablas/"+i)
makeReport("./"+name+"/Reportes/Reporte_General.csv",tables)
makeReport("./"+name+"/Reportes/Subject_headings.csv",reg2)
makeReport("./"+name+"/Reportes/Valores.csv",reg)
makeReport("./"+name+"/Reportes/Subs_class.csv",reg4)
makeReport("./"+name+"/Reportes/Valores_class.csv",reg3)
