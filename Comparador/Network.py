# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 19:01:14 2017

@author: Antonio
"""
from csv import writer,excel
from collections import Counter

"""
* Función que se encarga de generar un indice para almacenar el id de cada tema
* diferente y el conteo de ocurrencias
* Recibe:
* forNet: Diccionario en el que se agrupa los temas y etiquetas por registro
*         sin tomar en cuenta los elementos repetidos dentro del mismo registro
* Regresa:
*    cnt: Diccionario donde se tiene el conteo de las ocurrencias conjuntas
*    index: indice con el id de cada tema
"""
def getCounts(forNet):
    cnt = Counter()
    index = {}
    ind = 0
    for i in forNet:
        tmp = list(forNet[i])
        tmp.sort()
        for j in range(len(tmp)-1):
            if not tmp[j] in index:
                index[tmp[j]] = str(ind)
                ind += 1
            for k in range(j+1,len(tmp)):
                if not tmp[k] in index:
                    index[tmp[k]] = str(ind)
                    ind += 1
                if int(index[tmp[j]]) < int(index[tmp[k]]):
                    cnt[index[tmp[j]]+"||"+index[tmp[k]]] += 1
                else:
                    cnt[index[tmp[k]]+"||"+index[tmp[j]]] += 1
    return cnt,index
"""
* Función que se encarga de generar los archivos para la red
* Recibe:
*    route: dirección en la que se almacenarán los archivos
*    cnt: Diccionario donde se tiene el conteo de las ocurrencias conjuntas
*    index: indice con el id de cada tema  
"""
def makeFiles(route,cnt,index):
    dialect = excel
    dialect.lineterminator='\n'
    file = open(route+"Nodes.csv",'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(["id","label","type"])
    for i in index:
        tmp2 = []
        tmp = str(i)
        tmp = tmp.split("||")
        tmp.reverse()
        for j in tmp:
            if len(j)>0:
                tmp2.append(j)
        wf.writerow([index[i]]+tmp2)
    file.close()
    
    file = open(route+"Edges.csv",'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(["Source","Target","Weight","Type"])
    for i in cnt:
        try:
            if(cnt[i]>50):
                tmp = i.split("||")
                l = [tmp[0],tmp[1],str(cnt[i]),"undirected"]
                wf.writerow(l)
        except:
            pass
    file.close()
            