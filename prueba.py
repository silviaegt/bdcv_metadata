# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 21:28:21 2017

@author: skar
"""

from csv import reader,writer
from collections import defaultdict,Counter
from Fingerprint import Fingerprint

"""
* Nota: El archivo que se lee debe ser un archivo de texto separado por
        tabuladores,de esta forma se evita problemas con las comas dentro 
        del texto
"""
doc = list(reader(open('términos_aceptados.txt','r',encoding="iso-8859-1"), delimiter='\t'))
elements = set()
cnter = Counter()
"""
doc = lista de palabras
i = palabra
j = letra?
elements = ??
keys = un diccionario que se va a llenar con instancias únicas (set) de fingerprint
dudas: qué hace fp.key?
"""

for i in doc:
    for j in i:
        if len(j)>0:
            cnter[j] +=1
            elements.add(j)
        
elements = list(elements)
elements.sort()

keys = defaultdict(set)
fp = Fingerprint()

count = 0
for w in elements:
    keys[fp.key(w)].add(count)
    count +=1

report = []
maxE = 0
for w in keys:
    csize = len(keys[w])
    if csize > maxE:
        maxE = csize
    if(csize > 1):
        tmp = []
        tmp.append(str(csize))
        for k in keys[w]:
            tmp.append(elements[k])
            tmp.append(str(cnter[elements[k]]))
        report.append(tmp)

report.sort()
report.reverse()

header = ["Tamaño del cluster"]
for i in range(0,maxE):
    header.append("Palabra")
    header.append("Número de apariciones")

file = open("reporte.csv",'w',encoding="iso-8859-1")
wf = writer(file)
wf.writerow(header)
for i in report:
    wf.writerow(i)
    print(i)
file.close()
