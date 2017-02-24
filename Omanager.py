# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 08:58:07 2017

@author: skar
"""

import hunspell
import re
from collections import defaultdict,Counter

class Omanager:

    def __init__(self,cluster):
        self.cluster = cluster
        self.cnter = Counter()
        self.detected = set()
        self.correctWord = defaultdict(list)
        self.dic = hunspell.HunSpell("./dicts/es_MX.dic","./dicts/es_MX.aff")
        self.regex = re.compile("[^\w\-]")

    def getCluster(self):
        return self.cluster
    
    def getDectected(self):
        return self.detected
        
    def check(self):
        print("Iniciando análisis ortográfico presione :quit para salr")
        for i in self.cluster:
            for j in list(self.cluster[i]):
                stTmp = j
                print("\nFrase: "+j)
                print("Detecciones: ")
                lTmp = []
                st = j.replace("_"," ")
                st = self.regex.sub(" ",st)
                tmp = list(set(st.split()))
                for k in tmp:
                    if k in self.detected:
                        self.cnter[k]+=1
                        value = self.correctWord[k]
                        stTmp.replace(k,value[0])
                    elif(not self.dic.spell(k)):
                        self.detected.add(k)
                        self.cnter[k]+=1
                        print(k+" no se encuentra en el diccionario")
                        print("Algunas sugerencias: ")
                        print(self.dic.suggest(k))
                        word = input("Ingrese la palabra deseada: ")
                        if word.__eq__(":quit"):
                            return
                        word = self.regex.sub("",word)
                        self.dic.add(word)
                        self.correctWord[k]=[word]
                        stTmp.replace(k,word)
                lTmp.append(stTmp)
            self.cluster[i]=set(lTmp)
    
    def makeReport(self,wf):
        wf.writerow(["Total de detecciones",str(len(self.detected))])
        wf.writerow(["Palabra","Número de ocurrencias"])
        for i in self.cnter:
            wf.writerow([i,str(self.cnter[i])])