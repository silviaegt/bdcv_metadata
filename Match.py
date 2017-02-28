# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 21:45:48 2017

@author: skar
"""

import clusterToFile as c2f
from collections import Counter
from csv import DictReader,writer,excel
from Fingerprint import Fingerprint

dic = c2f.readCluster("cluster.p")
name = input("Ingresa el nombre de la base de datos: ")
col = input("ingresa el nombre de la columna a refinar: ")
fp = Fingerprint()
print("Cargando la base de datos...")
try:
    doc = list(DictReader(open(name,'r',encoding="utf-16"), delimiter='\t'))
    doc2 = open(name,'r',encoding="utf-16").read()
except:
    doc = list(DictReader(open(name,'r',encoding="iso-8859-1"), delimiter='\t'))
    doc2 = open(name,'r',encoding="iso-8859-1").read()

changed = set()
cnter = Counter()

print("Proceso iniciado...")
for i in doc:
    text = i[col]
    text = text.replace("--"," ")
    for term in text.split(";"):
        key = fp.key(term)
        cnter[key]+=1
        if key in dic:
            if (not term in dic[key])and(not term in changed):
                print(term+" no es entándar, posibles opciones: ")
                num = 0
                l = list(dic[key])
                for j in l:
                    print(str(num)+": "+j)
                print(":quit para salir")
                op = input(">> ")
                if op.__eq__(":quit"):
                    exit(0)
                else:
                    doc2.replace(term,l[int(op)])
                changed.add(term)
        elif len(term)>0:
            print(term+" ha generado una detección")
            print("Ingrese el término adecuado o alguna de las siguientes opciones")
            print("\":add\" para agregar el término al diccionario sin corregir")
            print("\":ignore\" para descartar")
            print("\":quit\" para salir")
            op = input(">> ")
            if op.__eq__(":add"):
                dic[key].add(term)
            elif op.__eq__(":quit"):
                exit(0)
            elif not op.__eq__(":ignore"):
                dic[fp.key(op)].add(op)
                doc2.replace(term,op)
            changed.add(term)

c2f.writeCluster("cluster.p",dic)
dialect = excel
dialect.lineterminator='\n'
file = open("new_db.csv",'w',encoding="utf-16")
wf = writer(file,dialect)

for i in doc2.split("\n"):
    wf.writerow(i.split("\t"))

file.close()
file = open("changes.csv","w",encoding="iso-8859-1")
wf = writer(file,dialect)
wf.writerow(["Palabra","Número de apariciones"])
for i in changed:
    wf.writerow([str(cnter[i]),i])
file.close()
    