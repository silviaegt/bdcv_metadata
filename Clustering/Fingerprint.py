# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 21:27:52 2017

@author: skar
"""

import re
from StandarCode import normalize

"""
* Clase que se encarga de ejecutar el algoritmo de fingerprint simple
* para generar llaves de agrupación
"""
class Fingerprint:
    """
    * Constructor de la clase, no requiere argumentos
    """
    def __init__(self):
        self.regex = re.compile("[^\w\s]")
    """
    * Método que se encarga de generar la llave de agrupación
    * Recibe:
    *    s: string al que se le busca obtener la llave
    * Regresa:
    *    s: llave correspondiente al string original
    """    
    def key(self,s):
        s = s.strip()
        s = s.lower()
        s = s.replace("-"," ")
        s = s.replace("—"," ")
        s = s.replace("_"," ")
        s = self.regex.sub('',s)
        toks = list(set(s.split()))
        toks.sort()
        s = ""
        for i in toks:
            s+= normalize(i) +" "
        return s.rstrip()
    
    
"""
* Clase que se encarga de ejecutar el algoritmo de ngram
* para generar llaves de agrupación
"""
class NGram:
    """
    * Constructor de la clase
    * Recibe:
    *    tam: valor de n gramas que se buscará
    """
    def __init__(self,tam):
        self.regex = re.compile("[^\w]")
        self.n = tam
    """
    * Método que se encarga de generar la llave de agrupación
    * Recibe:
    *    s: string al que se le busca obtener la llave
    * Regresa:
    *    s: llave correspondiente al string original
    """  
    def key(self,s):
        s = s.lower()
        s = s.replace("_",'')
        s = self.regex.sub('',s)
        nGrams = self.nGramSplit(s,self.n)
        s = ""
        for i in nGrams:
            s+=normalize(i)
        return s
    """
    * Método que se encarga de obtener lo ngramas diferentes dentro del string
    * Recibe:
    *    s: string al que se le busca obtener los ngrams
    *    n: total de ngramas que se busca
    * Regresa:
    *    nGrams: conjunto de ngrams sin repetidos
    """
    def nGramSplit(self,s,n):
        nGrams = set()
        if n>=len(s):
            nGrams.add(s)
        else:
            for i in range(0,len(s)-(n-1)):
                print(s[i:i+n])
                nGrams.add(s[i:i+n])
        nGrams = list(nGrams)
        nGrams.sort()
        return nGrams
        
        
