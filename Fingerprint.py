# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 21:27:52 2017

@author: skar
"""

import re
from StandarCode import normalize

class Fingerprint:
    
    def __init__(self):
        self.regex = re.compile("[^\w\s]")
        
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
    
    

class NGram:
    
    def __init__(self,tam):
        self.regex = re.compile("[^\w]")
        self.n = tam
    
    def key(self,s):
        s = s.lower()
        s = s.replace("_",'')
        s = self.regex.sub('',s)
        nGrams = self.nGramSplit(s,self.n)
        s = ""
        for i in nGrams:
            s+=normalize(i)
        return s
    
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
        
        