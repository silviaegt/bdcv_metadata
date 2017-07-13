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

"""
Clase que se encarga de escribir el archivo JSON
"""    
class JWriter:
    """
    * Constructor de la clase
    * Recibe:
    *    titles: dirección en la que se encuentra el archivo con títulos
    *    cont: dirección en la que se encuentra el archivo con el contenido
    *    n: columna desde la que inician los datos en cont
    *    dewey: ruta donde se encuentra el archivo para la traducción del 
    *           código dewey
    *    labels: Etiquetas válidas
    *    ex: lista con las etiquetas que deben exceptuarse
    """
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
    """
    * Método para obtener el objeto JSON
    """
    def getJBooks(self):
        return self.jBooks
    
    """
    * Método para inicializar el contenido del objeto
    * Recibe:
    *    cont: dirección en la que se encuentra el archivo con el contenido
    *    n: columna desde la que inician los datos en cont
    * Genera:
    *    Archivo con los subs que tuvieron errores
    *    un log del sistema
    """
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
    """
    * Método que se encarga de generar el diccionario para la traducción dewey
    * Recibe:
    *    dewey: Ruta donde se encuentra el archivo con el código dewey
    * Regresa:
    *    dic: diccionario con la interpretación del código dewey
    """
    def initDict(self,dewey):
        tmp = list(reader(open(dewey,'r',encoding=self.encode), delimiter=','))
        dic = defaultdict(str)
        for i in tmp:
            dic[i[0]]=i[1]
        return dic
    """
    * Método que se encarga de iniciar los elementos que se escribirán en un
    * archivo JSON
    * Recibe:
    *    titles: ruta del archivo donde se encuentran los títulos y el código 
    *            dewey de cada registro, así como su número
    * Regresa:
    *    Diccionario con todos los registros agregados
    """
    def initList(self,titles):
        tmp = list(reader(open(titles,'r',encoding=self.encode), delimiter=','))
        l = {}
        for i in tmp[1:]:
            nReg = i[0]
            jElement = JElement(i[5],self.dic)
            jElement.setDewey(i[2])
            l[nReg] = jElement
        return l
    """
    * Método que se encarga de generar el JSON 
    * Regresa:
    *    Diccionario con los datos en formato JSON
    """            
    def initObj(self):
        l = []
        cont = 0
        for k in self.items:
            it = self.items[k]
            l.append({"book_"+str(cont):{"title":it.getTitle(),"dewey":it.getDewey(),"cont":it.getTopics()}})
            cont+=1
        return {"books":l}
    """
    * Método que se encarga de imprimir errores que se encontraron dentro del 
    * archivo de subs
    """        
    def printErrors(self,reg,title,dewey,key):
        print("Error en el registro: "+reg)
        print("Título: "+title)
        print("Dewey: "+dewey)
        print("\""+key+"\""+" no es válida\n")
    """
    * Método que se encarga de escribir a archivo todo el JSON
    """
    def write(self,filename):
        with open(filename,'w',encoding=self.encode) as file:
            json.dump(self.jBooks,file)
            file.close()
        