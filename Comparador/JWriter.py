# -*- coding: utf-8 -*-
"""
Created on Thu May  4 15:25:59 2017

@author: Antonio
"""

from collections import defaultdict
from csv import excel,reader,writer
from JElement import JElement 
import json
import re
    
class JWriter:
    
    def __init__(self,titles,cont,n,dewey,labels,ex=[],encoding="iso-8859-1"):
        self.encode = encoding
        self.dialect = excel
        self.dialect.lineterminator='\n'
        self.dic = self.initDict(dewey)
        self.exc = set(ex)
        self.labels = set(labels)
        self.reg = set()
        self.items = self.initList(titles)
        self.initCont(cont,n)
        self.jBooks = self.initObj()
        
    def getJBooks(self):
        return self.jBooks
    
    def initCont(self,cont,n):
        regex = re.compile("[^\w]")
        tmp = list(reader(open(cont,'r',encoding=self.encode), delimiter=','))
        file = open("errors_subs.csv",'w',encoding=self.encode)
        file2 = open("JWriter.log",'w',encoding=self.encode)
        wf = writer(file,self.dialect)
        wf.writerow(["Título","Dewey","Error"])
        for i in tmp[1:]:
            for j in range(n,len(i),2):
                if len(i[j])>0:
                    key = regex.sub('',i[j-1])
                    try:
                        it = self.items[i[0]]
                        if not key in self.labels and not key in self.exc:
                            self.printErrors(i[0],it.getTitle(),it.getFullDewey(),key)
                            wf.writerow([it.getTitle(),it.getFullDewey(),key])
                        elif not key in self.exc:
                            it.addTopic(key,i[j])
                            self.items[i[0]] = it
                    except:
                        file2.write("No se encontró el registro: "+i[0]+" en el archivo de títulos\n")
        file.close()
        file2.close()
    
    def initDict(self,dewey):
        tmp = list(reader(open(dewey,'r',encoding=self.encode), delimiter=','))
        dic = defaultdict(str)
        for i in tmp:
            dic[i[0]]=i[1]
        return dic

    def initList(self,titles):
        tmp = list(reader(open(titles,'r',encoding=self.encode), delimiter=','))
        l = {}
        for i in tmp[1:]:
            nReg = i[0]
            jElement = JElement(i[5],self.dic)
            jElement.setDewey(i[2])
            l[nReg] = jElement
        return l
                
    def initObj(self):
        l = []
        cont = 0
        for k in self.items:
            it = self.items[k]
            l.append({"book_"+str(cont):{"title":it.getTitle(),"dewey":it.getDewey(),"cont":it.getTopics()}})
            cont+=1
        return {"books":l}
            
    def printErrors(self,reg,title,dewey,key):
        print("Error en el registro: "+reg)
        print("Título: "+title)
        print("Dewey: "+dewey)
        print("\""+key+"\""+" no es válida\n")
        
    def write(self,filename):
        with open(filename,'w',encoding=self.encode) as file:
            json.dump(self.jBooks,file)
            file.close()
        