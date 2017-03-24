# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 20:20:08 2017

@author: Antonio
"""

import os
from ComFunctions import getLists
from ComFunctions import compare

try:
    os.mkdir("Comparación")
except:
    pass
l1,car1 = getLists("Ingrese el nombre de la carpeta con las tablas a comparar: ")
l2,car2 = getLists("Ingrese el nombre de la carpeta con las tablas de referencia: ")
print("Comparando "+car1+" vs "+car2)
compare(l1,car1,l2,car2)