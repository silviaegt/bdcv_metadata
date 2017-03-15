# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:32:28 2017

@author: Antonio
"""

from csv import reader
from collections import defaultdict
import re
import os

def getTables(doc,keys,n,name):
    regex = re.compile("[^\w]")
    tables = defaultdict(set)
    file = open("./"+name+"/errors.log",'w',encoding="iso-8859-1")
    for i in doc[1:]:
        for j in range(n,len(i),2):
            if len(i[j])>0:
                key = regex.sub('',i[j-1])
                if not key in keys:
                    print("Error en el registro: "+i[0])
                    print("\""+key+"\""+" no es válida")
                    file.write("Error en el registro: "+i[0])
                    file.write(" \""+key+"\""+" no es válida"+"\n")
                else:
                    tables[key].add(i[j])
    file.close()
    return tables

def toFile(tables,name):
    for i in tables:
        with open("./"+name+"/"+i+".txt",'w',encoding="iso-8859-1") as file:
            for j in list(tables[i]):
                file.write(j+"\n")
            file.close()
    
etiquetas = set(["a","b","v","x","y","z","d","c","p","t","l","2"])
file = input("ingrese el nombre del archivo: ")
doc = list(reader(open(file,'r',encoding="iso-8859-1"), delimiter=','))
name = file.replace(".csv","")
os.mkdir(name)
n = int(input("Ingrese la columna desde la que empiezan los datos: "))+1
toFile(getTables(doc,etiquetas,n,name),name)