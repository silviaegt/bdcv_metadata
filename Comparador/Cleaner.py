# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 19:47:33 2017

@author: Antonio
"""

from ComFunctions import getLists
from csv import reader


def clean(file,cluster):
    print("Procesando "+cluster)
    doc = list(reader(open(cluster,'r',encoding="iso-8859-1"), delimiter=','))
    if len(doc)==0:
        return file
    for i in doc[2:]:
        for j in range(3,len(i),2):
            file.replace(i[j],i[1])
    return file

route = "/Clusters_cont/clusters_cont_reporte/"

l,dire = getLists("ingrese el nombre del directorio ",route)
file = open(dire+".csv",'r',encoding="iso-8859-1").read()

for i in l:
    if i.startswith("Cluster"):
        file = clean(file,dire+route+i)

file2 = open(dire+"_cln.csv","w",encoding="iso-8859-1")
file2.write(file)
file2.close()