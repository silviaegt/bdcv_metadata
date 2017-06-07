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

def getTables(doc,keys,titles,clas,cClas,c001,n,route):
    regex = re.compile("[^\w]")
    errors = Counter()
    tables = defaultdict(list)
    reg2 = defaultdict(list)
    reg3 = defaultdict(list)
    forNet = defaultdict(set)
    dialect = excel
    dialect.lineterminator='\n'
    file = open(route+"errors_subs.csv",'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(["Título","C001","Error"])
    for i in doc[1:]:
        #txt = getText(str(cClas[i[0]]))
        tmp = getText(str(titles[i[0]]))
        for j in range(n,len(i),2):
            if len(i[j])>0:
                key = regex.sub('',i[j-1])
                if not key in keys and not key.__eq__("2"):
                    errors[key]+=1
                    print("Error en el registro: "+i[0])
                    print("Título: "+tmp)
                    print("C001: "+c001[i[0]])
                    print("\""+key+"\""+" no es válida\n")
                    wf.writerow([tmp,c001[i[0]],key])
                elif not key.__eq__("2"):
                    tables[key].append(i[j])
                    reg2[str(i[0])].append(key)
                    reg3[getText(str(clas[i[0]]))].append(i[j])
                    sTmp=key+"_"+i[j]#+"_"+txt[:2]
                    forNet[str(i[0])].add(sTmp)
    file.close()
    return tables,reg2,reg3,forNet

def getDict(doc):
    dic = defaultdict(str)
    for i in doc:
        dic[i[0]]=i[1]
    return dic

def number(st):
    st = st.split(".")
    st = st[0]
    if len(st)<3:
        for i in range(3-len(st)):
            st = "0"+st
        return st
    else:
        return st[:3]


#REdefinir las explersiones
def getClass(st):
    if re.match(".*EN PROCESO.*",st):
        return "EN PROCESO DE CATALOGACIÓN"
    elif re.match("[^\d]/+\d+.?\d*",st):
        return "pass"
    elif re.match("\d+.?\d*",st):
        return number(st)
    else:
        return st

def getFlags(doc,dic):
    titles = defaultdict(set)
    clas = defaultdict(set)
    cClas = defaultdict(str)
    for i in doc[1:]:
        titles[i[0]].add(i[5])
        cl = getClass(i[2])
        cClas[i[0]]=i[2]
        if cl in dic:
            clas[i[0]].add(dic[cl])
        else:
            clas[i[0]].add(i[2])
    return titles,clas,cClas

def toFile(tables,route):
    tables = list(set(tables))
    tables.sort()
    with open(route+".txt",'w',encoding="iso-8859-1") as file:
        for i in tables:
            file.write(i+"\n")
        file.close()

def getValues(items):
    tot = len(items)
    items = Counter(items)
    tmp = []
    prom = 0
    for i in items:
        prom += items[i]
        tmp.append((items[i],i))
    tmp.sort()
    tmp.reverse()
    den = len(items)
    return [[str(tot),str(den),str(prom/den)],tmp]

def getCounts(items):
    tmp = []
    if len(items)>=10:
        lim = 9
    else:
        lim = len(items)
    for i in range(lim):
        it = items[i]
        tmp.append(it[1])
        tmp.append(str(it[0]))
    return tmp

def keyCount(sh):
    cnt = Counter()
    for i in sh:
        tmp = set(list(sh[i]))
        for j in tmp:
            cnt[j]+=1
    return cnt

def listToReport(items):
    dic = {"a":0,"b":1,"v":2,"x":3,"y":4,"z":5,"d":6,"c":7,"p":8,"t":9,"l":10,"2":11}
    tmp = ["","","","","","","","","","","",""]
    for i in items:
        tmp.pop(dic[i[1]])
        tmp.insert(dic[i[1]],str(i[0]))
    return tmp

def getHeader(cnt):
    if cnt == True:
        return ["clas_cent","clas_dec","clas_un","dewey_comp","dewey",
                "Gran Total","Total de Ocurrencias Diferentes"]
    else:
        return ["SH","Total de Ocurrencias en diferentes registros",
                     "Apariciones totales en el documento",
                    "Total de Ocurrencias Diferentes en el documento",
                    "Promedio"]

def getKey(dic,value):
    for i in dic:
        text = getText(str(dic[i]))
        if text.__eq__(value):
            return i
    return "xxx"

def makeReport(route,sh,cnt,dicc,clas):
    print("Generando: "+route+"\n")
    dialect = excel
    dialect.lineterminator='\n'
    file = open(route,'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(getHeader(cnt))
    if cnt==True:
        dire = route.replace("cont_por_clas","dewey_errors")
        file2 = open(dire,'w',encoding="iso-8859-1")
        wf2 = writer(file2,dialect)
        wf2.writerow(["Núm_reg","Error"]+getHeader(cnt)[5:])
    for i in sh:
        l = getValues(list(sh[i]))
        if cnt == True:
            dewey = getKey(dicc,i)
            if dewey.__eq__("xxx"):
                if re.match("[^\d]{1,8}/?\d+\.?\d*",i):
                    wf.writerow(["","","","",i]+l[0][0:-1]+getCounts(l[1]))
                else:
                    reg = getKey(clas,i)
                    wf2.writerow([reg,i]+l[0][0:-1]+getCounts(l[1]))
            else:
                val = [dewey[0]+"00","0"+dewey[1]+"0","00"+dewey[2],dewey]
                wf.writerow(val+[i]+l[0][0:-1]+getCounts(l[1]))
        else:
            wf.writerow([i,str(cnt[i])]+l[0]+getCounts(l[1]))
            dire = re.sub("Subs_reporte/.*","Tablas_count/",route)
            file2 = open(dire+i+".csv",'w',encoding="iso-8859-1")
            wf2 = writer(file2,dialect)
            wf2.writerow(["Frecuencia","Elemento"])
            for j in l[1]:
                wf2.writerow([str(j[0]),j[1]])
            file2.close()
    if cnt==True:
        file2.close()
    file.close()