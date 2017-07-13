# -*- coding: utf-8 -*-
"""
Created on Thu May  4 20:56:41 2017

@author: Antonio
"""

from JWriter import JWriter

"""
* Se definen las etiquetas váilidas y las que son exepciones
"""
labels = ["a","b","v","x","y","z","d","c","p","t","l"]
ex = ["2"]

"""
* Se inicializa el objeto con las rutas adecuadas y la columna desde la que 
* inician los datos.
* Posteriormente se indica el nombre con el que serán escritos los datos
"""
writer = JWriter("./títulos_prueba.csv","subs_pruebas.csv",4,"./dewey.csv",labels,ex)
writer.write("subs_prueba.json")
