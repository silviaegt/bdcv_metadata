# -*- coding: utf-8 -*-
"""
Created on Thu May  4 16:04:25 2017

@author: Antonio
"""

import re

class JElement:
    
    def __init__(self,title,dic):
        self.dewey = {}
        self.dic = dic
        self.title=title
        self.topics = []
        self.added = set()
    
    def addTopic(self,lab,cont):
        key = lab+"_"+cont
        if not key in self.added:
            self.added.add(key)
            tmp = {"label":lab,"cont":cont}
            self.topics.append(tmp)
    
    def getFullDewey(self):
        return self.dewey["full"]
    
    def getDewey(self):
        return self.dewey

    def getTitle(self):
        return self.title
    
    def getDictElement(self,key):
        if key in self.dic:
            text = str(self.dic[key])
            text = text.replace("\'","")
            text = text.replace("{","")
            text = text.replace("}","")
            return text
        else:
            return ""
    
    def getTopics(self):
        return self.topics
    
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