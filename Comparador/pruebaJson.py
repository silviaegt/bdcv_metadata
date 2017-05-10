# -*- coding: utf-8 -*-
"""
Created on Thu May  4 20:56:41 2017

@author: Antonio
"""

from JWriter import JWriter

labels = ["a","b","v","x","y","z","d","c","p","t","l"]
ex = ["2"]
writer = JWriter("./títulos.csv","subs_aceptados.csv",3,"./dewey.csv",labels,ex)
writer.write("result.json")