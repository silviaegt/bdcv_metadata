# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 21:28:21 2017

@author: skar
"""

from csv import reader

doc = list(reader(open('prueba.csv','r',encoding="iso-8859-1"), delimiter=';'))
firstFilter = set()

for i in doc:
    if len(i)>0:
        firstFilter.add(i[0])
        
print(len(firstFilter))