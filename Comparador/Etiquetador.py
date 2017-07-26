# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:32:28 2017

@author: Antonio
"""
from csv import reader
from LabFunctions import getDict
from LabFunctions import getFlags
from LabFunctions import getTables
from LabFunctions import keyCount
from LabFunctions import makeCntClas
from LabFunctions import makeGralReport
from LabFunctions import toFile
from Network import getCounts
from Network import makeFiles
import threading
import os

#Etiquetas válidas
etiquetas = set(["a","b","c","d","e","f","g","h","j","k","l","m","n","o",
                 "p","q","r","s","t","u","v","x","y","z","0","2","3","4",
                 "6","8"])
"""
* Se procede a cargar el archivo dewey.csv, en caso de que no se encuentre
* en el mismo directorio que este código se deberá poner la ruta correspondiente
"""
file = input("ingrese el nombre del archivo con el código dewey: ")
doc = list(reader(open(file,'r',encoding="iso-8859-1"), delimiter=','))
"""
* Se genera diccionario para la traducción del codígo dewey
* La función getDict está definida en LabFunctions.py
"""
dic = getDict(doc)
del doc
"""
* Se cargan los archivos con el código c001 para generar el diccionario de datos
* posteriormente se eliminan las listas en las que se cargaron los documentos
* para evitar saturar la RAM
"""
file = input("ingrese el nombre del archivo con el 001: ")
doc1 = list(reader(open(file,'r',encoding="iso-8859-1"), delimiter=','))
doc2 = list(reader(open("c001_2.csv",'r',encoding="iso-8859-1"), delimiter=','))
c001 = getDict(doc1+doc2)
del doc1
del doc2
"""
* Cargamos el archivo con los títulos y la clasificación dewey de cada
* registro
"""
file = input("ingrese el nombre del archivo con los títulos: ")
tit = list(reader(open(file,'r',encoding="iso-8859-1"), delimiter=','))
"""
* Se carga el archivo que contiene los subs
"""
file = input("ingrese el nombre del archivo con los subs: ")
doc = list(reader(open(file,'r',encoding="iso-8859-1"), delimiter=','))
"""
* Generamos los diccionarios con los títulos de cada registro
* y la clasificación de cada registro
"""
titles,clas = getFlags(tit,dic)
"""
* Se obtiene el nombre que va a tener el directorio raíz (el mismo nombre que
* el archivo con los subs), y se procede a crear la estructura de directorios
"""
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
"""
* Se obtienen los diccionarios para generar los reportes y la red
* tables: Diccionario en el que se agrupa todos los temas por etiquetas sin 
*         importar que estén repetidos o no
* reg2:   Diccionario en el que se agrupan todas las etiquetas por registro
*         sin importar si las etiquetas se repiten o no
* reg3:   Diccionario en el que se agrupan todos los temas por clasificación
 *        Dewey sin importar si se repiten o no
* forNet: Diccionario en el que se agrupa los temas y etiquetas por registro
*         sin tomar en cuenta los elementos repetidos dentro del mismo registro
"""
tables,reg2,reg3,forNet = getTables(doc,etiquetas,titles,clas,c001,n,tmp)
"""
* Escribimos las tablas en texto plano (eliminando repetidos)
"""
for i in tables:
    toFile(list(tables[i]),"./"+name+"/Tablas/"+i)
"""
* hacemos el conteo de apariciones de etiquetas en diferentes registros
"""
cnt = keyCount(reg2)
print("Generando reportes")
"""
* Generamos las tuplas con los parámetros que se le pasarán a cada hilo de
* ejecución
"""
t1 = ("./"+name+"/Subs_reporte/subs_reporte_gral.csv",tables,cnt,)
t2 = ("./"+name+"/Subs_reporte/cont_por_clas.csv",reg3,True,dic,clas,c001,)
"""
* Se inicia la ejecución del primer hilo y se manda a segundo plano
"""
srg = threading.Thread(target=makeGralReport,args=t1)
srg.setDaemon(True)
srg.start()
"""
* Se inica la ejecución del segundo hilo y también se manda a segundo plano
"""
cpc = threading.Thread(target=makeCntClas,args=t2)
cpc.setDaemon(True)
cpc.start()
"""
* El programa principal empieza a generar los archivos para la red
"""
print("\nGenerando archivos para la red\n")
cnt,index = getCounts(forNet)
makeFiles("./"+name+"/Network/",cnt,index)
"""
* Esperamos a que los hilos en segundo plano terminen de ejecutarse para que 
* el programa termine
"""
srg.join()
cpc.join()
