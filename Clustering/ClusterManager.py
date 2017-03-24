# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 21:03:33 2017

@author: skar
"""

from collections import defaultdict,Counter
from Levenshtein import Levenshtein as distance

class ClusterManager:
    
    def __init__(self,cEx):
        self.cnter = Counter()
        self.cEx = cEx
        self.clusters = defaultdict(set)
        self.keys = []
        
    def __eq__(self,obj):
        return self.cnter.__eq__(obj.getCounter) and self.clusters.__eq__(obj.getCounter)
        
    def getKeys(self):
        return self.keys
    
    def getClusters(self):
        return self.clusters
        
    def getCounter(self):
        return self.cnter
    
    def makeClusters(self,doc,method):
        for i in doc:
            for j in i:
                if len(j)>0:
                    self.cnter[j] +=1
                    self.clusters[method.key(j)].add(j)
    
    def makeClusters2(self,doc,method):
        for j in doc:
            if len(j)>0:
                self.cnter[j] +=1
                self.clusters[method.key(j)].add(j)
    
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
                    for j in list(self.clusters[i]):
                        tmp.append(j)
                        tmp.append(str(self.cnter[j]))
                    report.append(tmp)
            header = ["Tamaño del cluster"]
            for i in range(0,maxE):
                header.append("Palabra")
                header.append("Número de apariciones")
            wf.writerow(["Total de detecciones:",str(len(report))])
            wf.writerow(header)
            wf.writerows(report)
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

    def nearestNeighborhood(self,tol):
        keys = list(self.clusters.keys())
        flg = 1
        tmp = defaultdict(set)
        for i in keys:
            for k in list(self.clusters[i]):
                tmp[i].add(k)
            for j in keys[flg:]:
                if distance(i,j)<=tol:
                    for k in list(self.clusters[j]):
                        tmp[i].add(k)
            flg+=1
        self.clusters=tmp
   
    def refineCluster(self):
        for i in self.keys:
            tmp = list(self.clusters[i])
            tmp2 = set()
            for j in tmp:
                if j in self.cEx:
                    tmp2.add(j)
            if len(tmp2)>0:
                self.clusters[i]=tmp2
    