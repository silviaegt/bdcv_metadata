# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 19:47:33 2017
@author: Antonio
Las bibliotecas externas son csv
La versión de Python usada es 3.6.0
"""

from ComFunctions import getLists
from csv import reader,writer,excel

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
def clean(file,cluster):
    print("Procesando "+cluster)
    doc = list(reader(open(cluster,'r',encoding="iso-8859-1"), delimiter=','))
    if len(doc)==0:
        return file
    for i in doc[2:]:
        for j in range(3,len(i),2):
            file = file.replace(i[j],i[1])
    return file
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
def write(doc,dire,labs,n):
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
file = open(dire+".csv",'r',encoding="iso-8859-1").read()

"""
* Cargamos los archivos con los clusters para hacer la limpieza que se 
* seleccionó
"""
for i in l:
    if i.startswith(menu[op]):
        file = clean(file,dire+route+i)
"""
* Generamos el primer archivo limpio, en este sólo se cambió el contenido de 
* los clusters
"""
file2 = open(dire+"_"+name[op]+"_cln.csv","w",encoding="iso-8859-1")
file2.write(file)
file2.close()

"""
* posteriormente cargamos el archivo anterior y lo utlilizamos para hacer la
* limpieza de etiquetas no válidas
"""
doc = list(reader(open(dire+"_"+name[op]+"_cln.csv",'r',encoding="iso-8859-1"), delimiter=','))
write(doc,dire+"_"+name[op],etiquetas,n)

