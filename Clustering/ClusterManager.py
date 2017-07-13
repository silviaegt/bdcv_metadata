# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 21:03:33 2017

@author: skar
"""

from collections import defaultdict,Counter
from Levenshtein import Levenshtein as distance

"""
* Clase que se encarga de hacer los clústers y sus respectivos reportes
"""
class ClusterManager:
    """
    * Constructor de la clase
    * Recibe:
    *    cEx: diccionario en el que se almacenarán exepciones que no se deben 
    *         tomar en cuenta al momento de hacer el clúster
    """
    def __init__(self,cEx):
        self.cnter = Counter()
        self.cEx = cEx
        self.clusters = defaultdict(set)
        self.keys = []
    """
    * Método que se encarga de comparar el clúster actual con otro considerando
    * los clústers y su conteo de frecuencia
    * Recibe:
    *    obj: Objeto con el que será comparado
    """
    def __eq__(self,obj):
        return self.cnter.__eq__(obj.getCounter) and self.clusters.__eq__(obj.getCounter)
    
    """
    * Método que se encarga de regresar las llaves del clúster
    * Regresa:
    *    keys: Llaves del diccionario de datos
    """    
    def getKeys(self):
        return self.keys
    """
    * Método que se encarga de regresar el diccionario donde se encuentra
    * almacenado el clúster
    """
    def getClusters(self):
        return self.clusters
    """
    * Método que se encarga de regresar el diccionario donde se encuentran
    * almacenados el conteo de frecuencias
    """
    def getCounter(self):
        return self.cnter
    
    """
    * Método que se encarga de hacer el cluster en caso de que doc sea una
    * lista de listas (renglones)
    * Doc: Lista de renglones en los que se encuentra la información
    * method: forma en la que se calcularán las llaves
    """
    def makeClusters(self,doc,method):
        for i in doc:
            for j in i:
                if len(j)>0:
                    self.cnter[j] +=1
                    self.clusters[method.key(j)].add(j)
    """
    * Método que se encarga de hacer el cluster en caso de que doc sea una
    * lista simple
    * Doc: Lista en la que se encuentra la información
    * method: forma en la que se calcularán las llaves
    """
    def makeClusters2(self,doc,method):
        self.cnter = doc
        for j in doc:
            if len(j)>0:
                self.clusters[method.key(j)].add(j)
    """
    * Método que se encarga de hacer el reporte con el cluster actual
    * Recibe:
    *    wf: objeto csv.writer en el que será escrito el culster
    * Genera:
    *    Reporte de agrupación del cluster
    """
    def makeClusterReport(self,wf):
        try:
            report = []
            maxE = 0
            for i in self.clusters:
                csize = len(self.clusters[i])
                if maxE < csize:
                    maxE = csize
                if csize > 1:
                    self.keys.append(i)
                    tmp = [csize]
                    tmp2 = []
                    for j in list(self.clusters[i]):
                        tmp2.append((int(self.cnter[j]),j))
                    tmp2.sort()
                    tmp2.reverse()
                    for j in tmp2:
                        tmp.append(j[1])
                        tmp.append(str(j[0]))
                    report.append(tmp)
            header = ["Tamaño del cluster"]
            for i in range(0,maxE):
                header.append("Palabra")
                header.append("Número de apariciones")
            if len(report)>0:
                wf.writerow(["Total de detecciones:",str(len(report))])
                wf.writerow(header)
                wf.writerows(report)
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
    """
    * Método que se encarga de verificar el cluster actual para encontrar 
    * posibles coincidencias con términos no agrupados
    * Recibe:
    *    tol: distancia máxima entre terminos para determinar si es o no
    *         vecino
    """
    def nearestNeighborhood(self,tol):
        try:
            keys = list(self.clusters.keys())
            keys.sort()
            keys2 = keys.copy()
            flg = 0
            tmp = defaultdict(set)
            for i in keys:
                flg+=1
                keys = keys2.copy()
                for k in list(self.clusters[i]):
                    tmp[i].add(k)
                for j in keys[flg:]:
                    if(len(j)>0):
                        if i[0]==j[0]:
                            if distance(i,j)<=tol:
                                for k in list(self.clusters[j]):
                                    tmp[i].add(k)
                                keys2.remove(j)
                        else:
                            break
            self.clusters=tmp
        except:
            pass
   
    