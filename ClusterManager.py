# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 21:03:33 2017

@author: skar
"""

from collections import defaultdict,Counter
import hunspell
import re

class ClusterManager:
    
    def __init__(self,cEx,wEx):
        self.cnter = Counter()
        self.cEx = cEx
        self.wEx = wEx
        self.clusters = defaultdict(set)
        self.keys = []
        self.detected = Counter()
        self.changes = defaultdict(set)
        self.dic = hunspell.HunSpell("./dicts/es_MX.dic","./dicts/es_MX.aff")
        self.regex = re.compile("[^\w\-]")
        
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
                    tmp = j.replace("_"," ")
                    tmp = self.regex.sub(" ",tmp)
                    for k in tmp.split():
                        if not self.dic.spell(k) and  not k in self.wEx:
                            self.detected[k]+=1
                            l = self.dic.suggest(k)
                            if not k in self.changes:
                                if len(l)>1:
                                    word = l[0].decode("iso-8859-1")
                                elif len(l)==0:
                                    word = k
                                self.changes[k].add(word)
                                j.replace(k,word)
                    self.cnter[j] +=1
                    self.clusters[method.key(j)].add(j)
    
    def makeOrtReport(self,wf):
        wf.writerow(["Palabra Original","Cambio","Ocurrencias"])
        for i in self.detected:
            try:
                wf.writerow([i,self.changes[i],str(self.detected[i])])
            except:
                wf.writerow([i,"  ",str(self.detected[i])])
    
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
            tmp = list(self.clusters[i])
            tmp2 = set()
            for j in tmp:
                if j in self.cEx:
                    tmp2.add(j)
            if len(tmp2)>0:
                self.clusters[i]=tmp2
    