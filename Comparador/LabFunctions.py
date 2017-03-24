# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:40:05 2017

@author: Antonio
"""
from csv import writer,excel
from collections import defaultdict,Counter
import re

def getText(title):
    tmp = title.replace("\'","")
    tmp = tmp.replace("{","")
    tmp = tmp.replace("}","")
    return tmp

def getTables(doc,keys,titles,clas,n,route):
    regex = re.compile("[^\w]")
    cnt = Counter()
    errors = Counter()
    tables = defaultdict(list)
    reg = defaultdict(list)
    reg2 = defaultdict(list)
    reg3 = defaultdict(list)
    reg4 = defaultdict(list)
    dialect = excel
    dialect.lineterminator='\n'
    file = open(route+"Errors.csv",'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(["No. Registro","Sub","Título"])
    for i in doc[1:]:
        for j in range(n,len(i),2):
            if len(i[j])>0:
                key = regex.sub('',i[j-1])
                if not key in keys:
                    errors[key]+=1
                    tmp = getText(str(titles[i[0]]))
                    print("Error en el registro: "+i[0])
                    print("Título: "+tmp)
                    print("\""+key+"\""+" no es válida\n")
                    wf.writerow([i[0],key,tmp])
                else:
                    tables[key].append(i[j])
                    cnt[i[j]]+=1
                    reg[getText(str(titles[i[0]]))].append(i[j])
                    reg2[getText(str(titles[i[0]]))].append(key)
                    reg3[getText(str(clas[i[0]]))].append(i[j])
                    reg4[getText(str(clas[i[0]]))].append(key)
    file.close()
    return tables,reg,reg2,reg3,reg4

def getFlags(doc):
    titles = defaultdict(set)
    clas = defaultdict(set)
    for i in doc[1:]:
        titles[i[0]].add(i[5])
        clas[i[0]].add(i[2])
    return titles,clas

def toFile(tables,route):
    tables = list(set(tables))
    tables.sort()
    with open(route+".txt",'w',encoding="iso-8859-1") as file:
        for i in tables:
            file.write(i+"\n")
        file.close()

def getMaxMin(items):
    tot = len(items)
    items = Counter(items)
    maxx = 0
    minn = 100000
    tmpm = "NA"
    tmpl = "NA"
    for i in items:
        if items[i]>maxx:
            maxx = items[i]
            tmpm = i
        if items[i]<=minn:
            minn = items[i]
            tmpl = i
    return [tmpm,str(maxx),tmpl,str(minn),str(tot)]

def makeReport(route,sh):
    dialect = excel
    dialect.lineterminator='\n'
    file = open(route,'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(["Elemento/Título","Máximo","Ocurrencias","Mínimo","Ocurrencias","Total"])
    for i in sh:
        wf.writerow([i]+getMaxMin(list(sh[i])))
    file.close()