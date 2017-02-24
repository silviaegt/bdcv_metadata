# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 23:01:18 2017

@author: skar
"""

from csv import reader,writer,excel
from ClusterManager import ClusterManager
from Fingerprint import Fingerprint
from Omanager import Omanager

doc = list(reader(open('términos_aceptados.txt','r',encoding="iso-8859-1"), delimiter='\t'))
file = open("ClusterReport.csv",'w',encoding="iso-8859-1")
dialect = excel
dialect.lineterminator='\n'

wf = writer(file,dialect)
fp = Fingerprint()

clusterM = ClusterManager()
clusterM.makeClusters(doc,fp)
clusterM.makeClusterReport(wf)
clusterM.refineCluster()
#clusterM.toFile()
file.close()

file = open("ortReport.csv",'w',encoding="iso-8859-1")
wf = writer(file,dialect)
om = Omanager(clusterM.getClusters())
om.check()
om.makeReport(wf)
file.close()

"""
TODO: 
    lograr que con pinkle se guarde el cluster
"""