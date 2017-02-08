# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 21:28:21 2017

@author: skar
"""

from csv import reader
from collections import defaultdict,Counter
from Fingerprint import Fingerprint


doc = list(reader(open('términos_aceptados.txt','r',encoding="iso-8859-1"), delimiter='\t'))
elements = set()
cnter = Counter()

for i in doc:
    for j in i:
        if len(j)>0:
            cnter[j] +=1
            elements.add(j)
        
elements = list(elements)
elements.sort()

keys = defaultdict(set)
fp = Fingerprint()

count = 0
for w in elements:
    keys[fp.key(w)].add(count)
    count +=1

for w in keys:
    num = 0
    for k in keys[w]:
        tmp = cnter[elements[k]]
        print(elements[k])
        num += tmp
    if(num > 1):
        print("total: "+str(num))

#Nota, pensar cómo usar k medias
