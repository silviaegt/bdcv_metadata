# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 23:01:18 2017

@author: skar

Notas:
    En alguna distribución linux es posible ver la codificación usando:
        file --mime [archivo]
    y cambiar la codificación usando:
        iconv -f [Encode_original] -t [Encode_nuevo] [Archivo_original] > [Nuevo_Archivo]

"""
from csv import reader,writer,excel
from ClusterManager import ClusterManager
from Fingerprint import Fingerprint
import clusterToFile as c2f


def getWords(filename):
    with open(filename,'r',encoding="iso-8859-1") as f:
        data = f.read()
        data = data.split("\n")
        words = set()
        for i in data:
            words.add(i)
        return words

def aditional(st):
    words = set()
    op = input(st)
    op = op.lower()
    if op.__eq__("s"):
        op = input("ingrese el nombre del archivo con la lista")
        print("Cargando lista")
        words = getWords(op)    
    return words

print("Iniciando proceso, esto puede tardar varios minutos...")
print("Cargando base de datos")
doc = list(reader(open("términos_aceptados.txt",'r',encoding="iso-8859-1"), delimiter='\t'))
dialect = excel
dialect.lineterminator='\n'

wE = aditional("Desea ingresar una lista de palabras a exceptuar? (S/N)")
cE = aditional("Desea ingresar una lista de términos a considerar? (S/N)")

fp = Fingerprint()
print("Calculando clusters y revisando ortografía")
file = open("ClusterReport.csv",'w',encoding="iso-8859-1")
wf = writer(file,dialect)
clusterM = ClusterManager(cE,wE)
clusterM.makeClusters(doc,fp)
print("Generando reporte de clusters")
clusterM.makeClusterReport(wf)
#clusterM.refineCluster()
file.close()

file = open("ortReport.csv",'w',encoding="iso-8859-1")
wf = writer(file,dialect)
print("Generando reporte de ortografía")
clusterM.makeOrtReport(wf)
file.close()

c2f.writeCluster("cluster.p",clusterM.getClusters())

#Limpiamos memoria
del doc
del file
del dialect
del wf
del fp
del clusterM
del wE
del cE