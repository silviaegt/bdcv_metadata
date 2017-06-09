# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:16:24 2017

@author: Antonio
"""

import sys
import os
import threading
sys.path.append("../Clustering")
from ClusterManager import ClusterManager
import clusterToFile as c2f
from Fingerprint import Fingerprint
from ComFunctions import getLists,getTerms
from csv import writer,excel

def hilo(i):
    dialect = excel
    dialect.lineterminator='\n'
    fp = Fingerprint()
    tmp = i.replace(".csv",'')
    print("Procesando actualmente: "+tmp)
    file = open(car1+"/Clusters_cont/clusters_cont_reporte/ClusterReport_"+tmp+".csv",'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    clusterM = ClusterManager(set())
    clusterM.makeClusters2(getTerms(car1+"/Tablas_count/"+i),fp)
    clusterM.makeClusterReport(wf)
    file.close()
    
    c2f.writeCluster(car1+"/Clusters_cont/clusters_cont_local/cluster_"+tmp+".p",clusterM.getClusters())
    #op = input("Desea checar posibles coincidencias en "+i+"?(S/N) ")
    op = "s"
    #op = op.lower()
    if op.__eq__("s"):
        #op = input("Ingrese la tolerancia: ")
        op = "3"
        clusterM.nearestNeighborhood(int(op))
        file = open(car1+"/Clusters_cont/clusters_cont_reporte/nearReport_"+tmp+".csv",'w',encoding="iso-8859-1")
        wf = writer(file,dialect)
        print("Generando reporte")
        clusterM.makeClusterReport(wf)
        file.close()
        c2f.writeCluster(car1+"/Clusters_cont/clusters_cont_local/clusterN_"+tmp+".p",clusterM.getClusters())
    
    del dialect
    del fp
    del file
    del wf
    del clusterM

l1,car1 = getLists("Ingrese el nombre de la carpeta con las tablas: ")

try:
    os.mkdir(car1+"/Clusters_cont")
    os.mkdir(car1+"/Clusters_cont/clusters_cont_reporte")
    os.mkdir(car1+"/Clusters_cont/clusters_cont_local")
except:
    pass


print("Calculando clusters")
threads = []
for i in l1:
    tmp = threading.Thread(target=hilo,args=(i,))
    tmp.setDaemon(True)
    tmp.start()
    threads.append(tmp)
    
for i in threads:
    i.join()
    