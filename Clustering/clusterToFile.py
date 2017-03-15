# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 23:36:05 2017

@author: skar
"""
from collections import defaultdict


def writeCluster(name,cluster):
    file = open(name,'w',encoding="iso-8859-1")
    for i in cluster:
        file.write(i)
        for j in cluster[i]:
            file.write("\t"+j)
        file.write("\n")
    file.close()

def readCluster(name):
    file = open(name,'r',encoding="iso-8859-1")
    doc = file.read()
    doc = doc.split("\n")
    dic = defaultdict(set)
    for i in doc:
        l = i.split("\t")
        for j in l[1:]:
            dic[l[0]].add(j)
    return dic
