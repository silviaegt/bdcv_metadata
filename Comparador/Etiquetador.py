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
import threading
import os


etiquetas = set(["a","b","c","d","e","f","g","h","j","k","l","m","n","o",
                 "p","q","r","s","t","u","v","x","y","z","0","2","3","4",
                 "6","8"])
doc = list(reader(open("dewey.csv",'r',encoding="iso-8859-1"), delimiter=','))
dic = getDict(doc)
del doc
doc1 = list(reader(open("c001_1.csv",'r',encoding="iso-8859-1"), delimiter=','))
doc2 = list(reader(open("c001_2.csv",'r',encoding="iso-8859-1"), delimiter=','))
c001 = getDict(doc1+doc2)
del doc1
del doc2
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
tables,reg2,reg3,forNet = getTables(doc,etiquetas,titles,clas,cClas,c001,n,tmp)
for i in tables:
    toFile(list(tables[i]),"./"+name+"/Tablas/"+i)

cnt = keyCount(reg2)
print("Generando reportes")
t1 = ("./"+name+"/Subs_reporte/subs_reporte_gral.csv",tables,cnt,None,None,)
t2 = ("./"+name+"/Subs_reporte/cont_por_clas.csv",reg3,True,dic,clas,)
srg = threading.Thread(target=makeReport,args=t1)
srg.setDaemon(True)
srg.start()
#makeReport("./"+name+"/Subs_reporte/subs_reporte_gral.csv",tables,cnt=cnt)
#makeReport("./"+name+"/Subs_reporte/cont_por_clas.csv",reg3,cnt=True,dicc=dic,clas=clas)
cpc = threading.Thread(target=makeReport,args=t2)
cpc.setDaemon(True)
cpc.start()


print("\nGenerando archivos para la red\n")
cnt,index = getCounts(forNet,dic)
makeFiles("./"+name+"/Network/",cnt,index,dic)

srg.join()
cpc.join()
