# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 21:03:33 2017

@author: skar
"""

from collections import defaultdict,Counter

class ClusterManager:
    
    def __init__(self):
        self.cnter = Counter()
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
            
    def refineCluster(self):
        for i in self.keys:
            try:
                tmp = list(self.clusters[i])
                index = 0
                print("¿Cuál término dese tomar como válido?")
                for j in tmp:
                    print(str(index)+" : "+j)
                    index += 1
                print("-1: conservar todos")
                print("q: salir")
                op = input(">> ")
                if op.__eq__("q"):
                    return
                elif int(op) >= 0:
                    self.clusters[i] = set([tmp[int(op)]])
            except:
                print("Opción no válida")
            print("\n")            
    