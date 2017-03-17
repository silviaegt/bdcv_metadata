# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:32:28 2017

@author: Antonio
"""

from csv import reader,writer,excel
from collections import defaultdict
import re
import os

def getTables(doc,keys,titles,n,name):
    regex = re.compile("[^\w]")
    tables = defaultdict(set)
    dialect = excel
    dialect.lineterminator='\n'
    file = open("./"+name+"/Errors.csv",'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(["No. Registro","Sub","Título"])
    for i in doc[1:]:
        for j in range(n,len(i),2):
            if len(i[j])>0:
                key = regex.sub('',i[j-1])
                if not key in keys:
                    tmp = str(titles[i[0]]).replace("\'","")
                    tmp = tmp.replace("{","")
                    tmp = tmp.replace("}","")
                    print("Error en el registro: "+i[0])
                    print("Título: "+tmp)
                    print("\""+key+"\""+" no es válida\n")
                    wf.writerow([i[0],key,tmp])
                else:
                    tables[key].add(i[j])
    file.close()
    return tables

def getTitles(doc):
    titles = defaultdict(set)
    for i in doc[1:]:
        titles[i[0]].add(i[5])
    return titles

def toFile(tables,name):
    for i in tables:
        with open("./"+name+"/"+i+".txt",'w',encoding="iso-8859-1") as file:
            for j in list(tables[i]):
                file.write(j+"\n")
            file.close()
    
etiquetas = set(["a","b","v","x","y","z","d","c","p","t","l","2"])
file = input("ingrese el nombre del archivo con los títulos: ")
tit = list(reader(open(file,'r',encoding="iso-8859-1"), delimiter=','))
file = input("ingrese el nombre del archivo con los subs: ")
doc = list(reader(open(file,'r',encoding="iso-8859-1"), delimiter=','))
titles = getTitles(tit)
name = file.replace(".csv","")
try:
    os.mkdir(name)
except:
    pass
n = int(input("Ingrese la columna desde la que empiezan los datos: "))+1
toFile(getTables(doc,etiquetas,titles,n,name),name)