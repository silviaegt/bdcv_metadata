# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 20:20:08 2017

@author: Antonio
"""

import os

def getLists(msg):
    car = input(msg)
    l = set(os.listdir("./"+car))
    l.remove("Errors.csv")
    return l,car

def getTerms(filename):
    file = open(filename,'r',encoding="iso-8859-1").read()
    return set(file.split("\n"))

def compare(l1,car1,l2,car2):
    for i in list(l1):
        tmp = i.replace(".txt",'')
        if i in l2:
            com = getTerms("./"+car1+"/"+i)
            ref = getTerms("./"+car2+"/"+i)
            file = open("./comparación/"+car1+"vs"+car2+"_"+tmp+".txt",'w',encoding="iso-8859-1")
            dif = list(com.difference(ref))
            for k in dif:
                file.write(k+"\n")
            file.close()
try:
    os.mkdir("comparación")
except:
    pass
l1,car1 = getLists("Ingrese el nombre de la carpeta con las tablas a comparar: ")
l2,car2 = getLists("Ingrese el nombre de la carpeta con las tablas de referencia: ")
print("Comparando "+car1+" vs "+car2)
compare(l1,car1,l2,car2)