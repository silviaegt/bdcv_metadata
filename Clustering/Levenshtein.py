# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 19:44:26 2017

@author: skar
"""

import numpy
"""
* Función que se encarga de evaluar la distancia entre dos cadenas
* mediante el algoritmo de Levenshtein
* Recibe:
*    s: primer cadena de interes
*    t: segunda cadena de interes
* Regresa:
*    distancia entre ambas cadenas
"""
def Levenshtein(s,t):
    m = len(s)+1
    n = len(t)+1
    d = numpy.zeros([m,n])
    for i in range(1,m):
        d[i][0] = i
    for i in range(1,n):
        d[0][i] = i
    
    for j in range(1,n):
        for i in range(1,m):
            if s[i-1]==t[j-1]:
                const = 0
            else:
                const = 1
            d[i][j] = min([d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+const])
        
    return d[m-1][n-1]
    