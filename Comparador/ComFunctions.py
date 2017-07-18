# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:37:30 2017
@author: Antonio
Las bibliotecas externas son csv y os
La versión de Python usada es 3.6.0
"""
from csv import reader
import os

"""
* Función que se encarga de comparar dos directorios para determinar cuáles 
* archivos del directorio 1 no se encuentran en el directorio 2
* Recibe:
*    l1: conjunto con los nombres del directorio 1
*    car1: nombre del directorio raíz 1
*    l1: conjunto con los nombres del directorio 2
*    car1: nombre del directorio raíz 2
* Genera:
*    Archivo con el reporte
"""
def compare(l1,car1,l2,car2):
    for i in list(l1):
        tmp = i.replace(".txt",'')
        if i in l2:
            com = getTerms("./"+car1+"/Tablas/"+i)
            ref = getTerms("./"+car2+"/Tablas/"+i)
            file = open("./comparación/"+car1+"vs"+car2+"_"+tmp+".txt",'w',encoding="iso-8859-1")
            dif = list(com.difference(ref))
            for k in dif:
                file.write(k+"\n")
            file.close()

"""
* Función que se encarga de obtener los nombres de los archivos dentro de un
* directorio
* Recibe:
*    msg: mensaje que se muestra para pedir el nombre del directorio principal
*    rte: subdirectorio donde se encuentran los archivos de interes
* Regresa:
*    l: conjunto en el que se encuentran los nombres de los archivos
*    car: nombre del directorio principal
"""
def getLists(msg,rte):
    car = input(msg)
    l = set(os.listdir("./"+car+rte))
    return l,car

"""
* Función que se encarga de generar un diccionario de datos de un archivo csv
* Recibe:
*    filename: nombre del archivo con el que se generará el diccionario
* Regresa:
*    dic: diccionario con los datos
"""
def getTerms(filename):
    file = list(reader(open(filename,'r',encoding="iso-8859-1"), delimiter=','))
    dic = {}
    for i in file:
        dic[i[1]]=i[0]
    return dic
