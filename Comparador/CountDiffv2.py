# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 10:52:39 2017

@author: Antonio
"""
from difflib import ndiff
from collections import defaultdict,Counter
from csv import reader

def purgeString(st1,st2):
    tmp = st2
    for i in st1.split(" "):
        st2 = st2.replace(i,"")
    for i in tmp.split(" "):
        st1 = st1.replace(i,"")
    return st1,st2

def findDiferences(file):
    adds = []
    dels = []
    vals = {}
    addsdic = defaultdict(list)
    deldic = defaultdict(list)
    for i in file[2:]:
        for j in range(3,len(i),2):
            if(len(i[j])>0):
                st1,st2 = purgeString(i[1],i[j])
                vals[st1] = i[2]
                vals[st2] = i[j+1]
                for k, s in enumerate(ndiff(st1,st2)):
                    if s[0] == ' ':
                        continue
                    elif s[0] == '-':
                        #print(k, s)
                        #adds = []
                        #print(u'Delete "{}" from position {}'.format(s[-1], i))
                        dels.append(s[-1])
                        deldic[(st1,st2)].append(s[-1])
                        #print(len(adds))
                    elif s[0] == '+':
                        #print(u'Add "{}" to position {}'.format(s[-1], i))
                        adds.append(s[-1])
                        addsdic[(st1,st2)].append(s[-1])
    return adds,addsdic,dels,deldic,vals

def getDiff(deldic):
    #### Diccionario con los errores que sólo dependen de eliminar un caracter
    diffonedic = {}
    diffone = []
    for termstuple, errorlist in deldic.items():
        if len(errorlist) < 2:
            #print(termstuple[0], termstuple[1], errorlist[0])
            diffone.append(errorlist[0])
            diffonedic[(termstuple[0], termstuple[1])] = errorlist[0]
            #onediffdel[(termstuple[0], termstuple[1])] =
    #print(len(diffone))
    diffonecount = Counter(diffone).most_common()
    #csv_from_tuplelist("diffone_delscount.csv", diffonecount)
    return diffonedic,diffone,diffonecount

def getWwithE (string, dictio,vals):
    """
    Permite ver los términos en los que se encuentra un determinado error y las palabras más comunes dentro de los términos correctos y los incorrectos
    :param string:
    :param dictio:
    :return:
    """
    correcto = []
    incorrecto = []
    corr_incorr = {}
    for termstuple, errorlist in dictio.items():
        if string in errorlist:
            correcto.append(termstuple[1])
            incorrecto.append(termstuple[0])
            v1 = vals[termstuple[1]]
            v2 = vals[termstuple[0]]
            print("correcto %s [%s] || error %s [%s]" % (termstuple[1],v1, termstuple[0],v2))
            corr_incorr[termstuple[1]] = termstuple[0]
    correct_string = ' '.join(correcto).split()
    wrong_string = ' '.join(incorrecto).split()
    #print("Palabras más comunes en térm. correctos: ", Counter(correct_string).most_common())
    #print("Palabras más comunes en térm. errados: ", Counter(wrong_string).most_common())
    return corr_incorr

##cambiar por la ruta donde se tenga el archivo de cluster
di = "/subs_completos/Clusters_cont/clusters_cont_reporte/ClusterReport_a.csv"
file = list(reader(open(di,'r',encoding="iso-8859-1"), delimiter=','))
adds,addsdic,dels,deldic,vals = findDiferences(file)
diffonedic,diffone,diffonecount = getDiff(deldic)
oes = getWwithE("o", diffonedic,vals)
    