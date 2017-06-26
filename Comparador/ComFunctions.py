# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:37:30 2017

@author: Antonio
"""
import os
from csv import reader

def getLists(msg,rte):
    car = input(msg)
    l = set(os.listdir("./"+car+rte))
    return l,car

def getTerms(filename):
    file = list(reader(open(filename,'r',encoding="iso-8859-1"), delimiter=','))
    dic = {}
    for i in file:
        dic[i[1]]=i[0]
    return dic

def compare(l1,car1,l2,car2):
    for i in list(l1):
        tmp = i.replace(".txt",'')
        if i in l2:
            com = getTerms("./"+car1+"/Tablas/"+i)
            ref = getTerms("./"+car2+"/Tablas/"+i)
            file = open("./comparación/"+car1+"vs"+car2+"_"+tmp+".txt",'w',encoding="iso-8859-1")
            dif = list(com.difference(ref))
            for k in dif:
                file.write(k+"\n")
            file.close()