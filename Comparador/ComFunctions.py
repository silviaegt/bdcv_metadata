# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:37:30 2017

@author: Antonio
"""
import os

def getLists(msg):
    car = input(msg)
    l = set(os.listdir("./"+car+"/Tablas"))
    return l,car

def getTerms(filename):
    file = open(filename,'r',encoding="iso-8859-1").read()
    return set(file.split("\n"))

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