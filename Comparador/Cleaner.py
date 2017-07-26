# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 19:47:33 2017

@author: Antonio
"""

from ComFunctions import getLists
from csv import reader,writer,excel
import sys
sys.path.append("../Clustering")
from Fingerprint import Fingerprint

"""
* Función que se encarga de reemplazar las columnas 3,5,7, etc de los reportes
* de clúster por la columna 1 dentro de un nuevo archivo
* Recibe:
*    file: Archivo en el que se están haciendo todos los cambios (debe ser 
*    convertido a string)
*    cluster: dirección del cluster con el que se hará la limpieza
* Regresa:
*    file: cadena con los cambios del clúster hechos
"""
def getDict(dic,cluster):
    fp = Fingerprint()
    print("Procesando "+cluster)
    doc = list(reader(open(cluster,'r',encoding="iso-8859-1"), delimiter=','))
    if len(doc)==0:
        return dic
    for i in doc[2:]:
        dic[fp.key(i[1])] = i[1]
    return dic.copy()
"""
* Función que se encarga de escribir un archivo nuevo eliminando los subs cuyas
* etiquetas no sean válidas
* Recibe:
*    doc: documento original
*    dire: nombre que se le pondrá al nuevo archivo
*    labs: etiquetas válidas
*    n: columna desde la que empiezan los datos
* Genera:
*    Archivo "limpio" sin etiquetas que no sean válidas
"""
def write(doc,dire,labs,dic,n):
    fp = Fingerprint()
    dialect = excel
    dialect.lineterminator='\n'
    file = open(dire+"_clean.csv",'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(doc[0])
    for i in doc[1:]:
        row = i[0:n-1]
        for j in range(n,len(i),2):
            if len(i[j])>0:
                key = i[j-1]
                if key in labs:
                    if fp.key(i[j]) in dic:
                        row.append(key)
                        row.append(dic[fp.key(i[j])])
                    else:
                        row.append(key)
                        row.append(i[j])
        wf.writerow(row)
    file.close()

"""
* Se generan dos diccionarios para el uso de estos como menú y también se 
* colocan las etiquetas válidas
"""
menu = {'1':"Cluster",'2':"near"}
name = {'1':"fp",'2':"vc"}
route = "/Clusters_cont/clusters_cont_reporte/"
etiquetas = set(["a","b","c","d","e","f","g","h","j","k","l","m","n","o",
                 "p","q","r","s","t","u","v","x","y","z","0","3","4",
                 "6","8"])
"""
* obtenemos la lista de archivos dentro de un directorio proporcionado
* por el usuario y el nombre de dicho directorio (dicho nombre debe ser el
* mismo que el del archivo de subs para poder abrirlo postariormente en la
* limpieza)
"""
l,dire = getLists("ingrese el nombre del directorio ",route)
n = int(input("Ingrese la columna desde donde inician los datos "))+1
op = input("Seleccione una opción:\nFingerprint: 1\nVecinos más cercanos: 2\n> ")
dic = {}

"""
* Cargamos los archivos con los clusters para hacer la limpieza que se 
* seleccionó
"""
for i in l:
    if i.startswith(menu[op]):
        dic = getDict(dic,dire+route+i)

"""
* posteriormente cargamos el archivo anterior y lo utlilizamos para hacer la
* limpieza de etiquetas no válidas
"""
doc = list(reader(open(dire+".csv",'r',encoding="iso-8859-1"), delimiter=','))
write(doc,dire+"_"+name[op],etiquetas,dic,n)

