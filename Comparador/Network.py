# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 19:01:14 2017

@author: Antonio
"""

from csv import writer,excel
from collections import Counter


def getCounts(forNet,dic):
    cnt = Counter()
    index = {}
    ind = 0
    for i in forNet:
        tmp = list(forNet[i])
        tmp.sort()
        for j in range(len(tmp)-1):
            if not tmp[j] in index:
                index[tmp[j]] = str(ind)
                ind += 1
            for k in range(j+1,len(tmp)):
                if not tmp[k] in index:
                    index[tmp[k]] = str(ind)
                    ind += 1
                cnt[index[tmp[j]]+"_"+index[tmp[k]]] += 1
    return cnt,index

def makeFiles(route,cnt,index,dic):
    dialect = excel
    dialect.lineterminator='\n'
    file = open(route+"Nodes.csv",'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(["id","data","type"])
    for i in index:
        tmp = str(i)
        tmp = tmp.split("_")
        tmp.reverse()
        wf.writerow([index[i]]+tmp)
    file.close()
    
    file = open(route+"Relations.csv",'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(["Source","Target","Weight"])
    for i in cnt:
        try:
            tmp = i.split("_")
            l = [tmp[0],tmp[1],str(cnt[i])]
            wf.writerow(l)
        except:
            pass
    file.close()
            
    
    