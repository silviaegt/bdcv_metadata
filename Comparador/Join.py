# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 23:08:59 2017

@author: Antonio
"""

from csv import reader,writer,excel

doc1 = list(reader(open("temas_1.csv",'r',encoding="iso-8859-1"), delimiter=','))
doc2 = list(reader(open("temas_2.csv",'r',encoding="iso-8859-1"), delimiter=','))
dialect = excel
dialect.lineterminator='\n'
file = open("subs_juntos.csv","w",encoding="iso-8859-1")
wf = writer(file,dialect)
wf.writerows(doc1+doc2[1:])
file.close()