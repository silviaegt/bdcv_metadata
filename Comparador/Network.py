# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 19:01:14 2017

@author: Antonio
"""

from csv import writer,excel
from collections import Counter


def getCounts(forNet,dic):
    cnt = Counter()
    dewey = set()
    lab = set()
    index = {}
    for i in forNet:
        for j in list(forNet[i]):
            cnt[j]+=1
            if j[-2:]+"0" in dic:
                dewey.add(dic[j[-2:]+"0"]+"_"+j[-2:]+"X")
                lab.add(j[:-3])
    ind = 0
    for i in dewey:
        index[i] = ind
        ind += 1
    for i in lab:
        index[i] = ind
        ind += 1
    return cnt,index

def makeFiles(route,cnt,index,dic):
    dialect = excel
    dialect.lineterminator='\n'
    file = open(route+"Nodes.csv",'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(["id","label","clas"])
    for i in index:
        wf.writerow([str(index[i])]+i.split("_"))
    file.close()
    
    file = open(route+"Relations.csv",'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(["Source","Target","Weight"])
    for i in cnt:
        try:
            source = i[:-3]
            target = dic[i[-2:]+"0"]+"_"+i[-2:]+"X"
            l = [str(index[source]),str(index[target]),str(cnt[i])]
            wf.writerow(l)
        except:
            pass
    file.close()
            
    
    