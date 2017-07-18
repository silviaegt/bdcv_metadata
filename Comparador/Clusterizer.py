# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:16:24 2017
@author: Antonio
Las bibliotecas externas son csv, threading, os y sys
La versión de Python usada es 3.6.0
"""

import os
import sys
import threading
sys.path.append("../Clustering")
from ClusterManager import ClusterManager
from ComFunctions import getLists,getTerms
from csv import writer,excel
from Fingerprint import Fingerprint

"""
* Función que se encarga de generar los reportes de los clústers mediante 
* Fingerprint y Vecinos más cercanos
* Recibe:
*    i: archivo csv con los datos a procesar
*    op: bandera para determinar si se harán vecinos más cercanos
*    tol: tolerancia en caso de que se hagan vecinos más cercanos
* Genera:
*    Archivo con el reporte de los clusters
"""
def hilo(i,op,tol):
    dialect = excel
    dialect.lineterminator='\n'
    fp = Fingerprint()
    tmp = i.replace(".csv",'')
    print("\nSe inicia el proceso en: "+tmp)
    file = open(car1+"/Clusters_cont/clusters_cont_reporte/ClusterReport_"+tmp+".csv",'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    clusterM = ClusterManager(set())
    clusterM.makeClusters2(getTerms(car1+"/Tablas_count/"+i),fp)
    clusterM.makeClusterReport(wf)
    file.close()
    print("\nClusterReport_"+tmp+" terminado satisfactoriamente")
    if op.__eq__("s"):
        clusterM.nearestNeighborhood(tol)
        file = open(car1+"/Clusters_cont/clusters_cont_reporte/nearReport_"+tmp+".csv",'w',encoding="iso-8859-1")
        wf = writer(file,dialect)
        print("\nnearReport_"+tmp+" terminado satisfactoriamente")
        clusterM.makeClusterReport(wf)
        file.close()
    
    del dialect
    del fp
    del file
    del wf
    del clusterM

"""
* Se solicita el nombre del directorio donde se tienen los datos
"""
l1,car1 = getLists("Ingrese el nombre de la carpeta con las tablas: ","/Tablas_count")

"""
* Completamos la estructura de directorios
"""
try:
    os.mkdir(car1+"/Clusters_cont")
    os.mkdir(car1+"/Clusters_cont/clusters_cont_reporte")
except:
    pass
"""
* Se pregunta si se quiere hacer vecinos más cercanos y se inicializa la tolerancia
"""
op = input("Desea checar vecinos más cercanos? (S/N) ")
op = op.lower()
tol = 0
if op.__eq__("s"):
    tol = int(input("Ingrese la tolerancia: "))
print("Calculando clusters")
"""
* se genera una lista de hilos en la que se irán almacenando los hilos de
* ejecución en segundo plano y se inicializan dichos hilos
"""
threads = []
for i in l1:
    tmp = threading.Thread(target=hilo,args=(i,op,tol,))
    tmp.setDaemon(True)
    tmp.start()
    threads.append(tmp)

"""
* se espera a que todos los hilos en segundo plano temrinen su ejecución
"""
for i in threads:
    i.join()
    
