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
from Network import getCounts
from Network import makeFiles
import os


etiquetas = set(["a","b","v","x","y","z","d","c","p","t","l"])
doc = list(reader(open("dewey.csv",'r',encoding="iso-8859-1"), delimiter=','))
dic = getDict(doc)
file = input("ingrese el nombre del archivo con los títulos: ")
tit = list(reader(open(file,'r',encoding="iso-8859-1"), delimiter=','))
file = input("ingrese el nombre del archivo con los subs: ")
doc = list(reader(open(file,'r',encoding="iso-8859-1"), delimiter=','))
titles,clas,cClas = getFlags(tit,dic)
name = file.replace(".csv","")
print("Generando directorios")
try:
    os.mkdir(name)
    os.mkdir(name+"/Subs_reporte")
    os.mkdir(name+"/Tablas_count")
    os.mkdir(name+"/Tablas")
    os.mkdir(name+"/Network")
except:
    pass
n = int(input("Ingrese la columna desde la que empiezan los datos: "))+1
tmp = "./"+name+"/Subs_reporte/"
print("Generando tablas")
tables,reg2,reg3,forNet = getTables(doc,etiquetas,titles,clas,cClas,n,tmp)
for i in tables:
    toFile(list(tables[i]),"./"+name+"/Tablas/"+i)

cnt = keyCount(reg2)
print("Generando reportes")
makeReport("./"+name+"/Subs_reporte/subs_reporte_gral.csv",tables,cnt=cnt)
makeReport("./"+name+"/Subs_reporte/cont_por_clas.csv",reg3,cnt=True,dicc=dic,clas=clas)

print("Generando archivos para la red")
cnt,index = getCounts(forNet,dic)
makeFiles("./"+name+"/Network/",cnt,index,dic)