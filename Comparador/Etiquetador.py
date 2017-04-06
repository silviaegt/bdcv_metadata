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
from LabFunctions import keyCount
from LabFunctions import getDict
import os


etiquetas = set(["a","b","v","x","y","z","d","c","p","t","l","2"])
doc = list(reader(open("dewey.csv",'r',encoding="iso-8859-1"), delimiter=','))
dic = getDict(doc)
file = input("ingrese el nombre del archivo con los títulos: ")
tit = list(reader(open(file,'r',encoding="iso-8859-1"), delimiter=','))
file = input("ingrese el nombre del archivo con los subs: ")
doc = list(reader(open(file,'r',encoding="iso-8859-1"), delimiter=','))
titles,clas = getFlags(tit,dic)
name = file.replace(".csv","")
try:
    os.mkdir(name)
    os.mkdir(name+"/Subs_reporte")
    os.mkdir(name+"/Tablas_count")
    os.mkdir(name+"/Tablas")
except:
    pass
n = int(input("Ingrese la columna desde la que empiezan los datos: "))+1
tmp = "./"+name+"/Subs_reporte/"
tables,reg2,reg3,reg4 = getTables(doc,etiquetas,titles,clas,n,tmp)
for i in tables:
    toFile(list(tables[i]),"./"+name+"/Tablas/"+i)

makeReport("./"+name+"/Subs_reporte/subs_por_sh.csv",reg2,tit=titles,cl=clas)
cnt = keyCount(reg2)
makeReport("./"+name+"/Subs_reporte/subs_reporte_gral.csv",tables,cnt=cnt)
makeReport("./"+name+"/Subs_reporte/subs_por_clas.csv",reg4,dicc=dic)
makeReport("./"+name+"/Subs_reporte/cont_por_clas.csv",reg3,cnt=True,dicc=dic)
