# -*- coding: utf-8 -*-
"""
Created on Thu May  4 16:04:25 2017

@author: Antonio
"""

import re

"""
* Clase que se encarga de encapsular todos los atributos de un objeto json
* para almacenar los datos de un libro
"""
class JElement:
    """
    * Método constructor de la clase
    * Recibe:
    *    title: título del libro
    *    dic: diccionario para hacer la traducción dewey
    """
    def __init__(self,title,dic):
        self.dewey = {}
        self.dic = dic
        self.title=title
        self.topics = []
        self.added = set()
    
    """
    * Método que se encarga de agregar temas dentro de la lista de temas
    * Recibe:
    *    lab: Etiqueta del tema
    *    cont: tema que se agrega
    """
    def addTopic(self,lab,cont):
        key = lab+"_"+cont
        if not key in self.added:
            self.added.add(key)
            tmp = {"label":lab,"cont":cont}
            self.topics.append(tmp)
    
    """
    * Método que se encarga de retornar el código Dewey completo del objeto
    * Regresa:
    *    Código dewey completo del objeto
    """
    def getFullDewey(self):
        return self.dewey["full"]
    """
    * Método que retorna el diccionario donde se almacena el código dewey
    * de forma completa y separada por unidad, decena y centena
    """
    def getDewey(self):
        return self.dewey

    """
    * Método que se encarga de regresar el título asignado al objeto
    """
    def getTitle(self):
        return self.title
    
    """
    * Método que se encarga de regresar el contenido de un elemento del diccionario
    * Recibe:
    *   key: llave del elemento del diccionario
    * Regresa:
    *   "" si la llave no está dentro del diccionario
    *   el contenido del diccionario en caso de que la llave exista
    """
    def getDictElement(self,key):
        if key in self.dic:
            text = str(self.dic[key])
            text = text.replace("\'","")
            text = text.replace("{","")
            text = text.replace("}","")
            return text
        else:
            return ""
    """
    * Método que se encarga de regresar el diccionario donde se encuentran 
    * almacenados los temas
    """
    def getTopics(self):
        return self.topics
    
    """
    * Método que se encarga de agregar el código dewey del libro dentro del 
    * diccionario de datos
    * Recibe:
    *    dew: Código dewey correspondiente
    """
    def setDewey(self,dew):
        if re.fullmatch("\d+\.?\d*",dew):
            tmp = dew.split(".")
            dew = tmp[0]
            while len(dew)<3:
                dew = "0"+dew
            self.dewey["cent"] = dew[0]+"00"
            self.dewey["dec"] = "0"+dew[1]+"0"
            self.dewey["uni"] = "00"+dew[2]
            self.dewey["full"] = dew[0:3]
            #self.dewey["original"] = dew
            self.dewey["name"] = self.getDictElement(dew[0:3])
        else:
            self.dewey = {"cent":"","dec":"","uni":"","full":""}
            if re.match(".*en proceso de.*",dew.lower()):
                self.dewey["name"]="EN PROCESO DE CATALOGACIÓN"
            else:
                self.dewey["name"]=dew