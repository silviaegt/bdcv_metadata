# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 21:28:21 2017

@author: skar
"""

from csv import reader,writer,excel
from collections import defaultdict,Counter
from Fingerprint import Fingerprint

"""
* Nota: El archivo que se lee debe ser un archivo de texto separado por
        tabuladores,de esta forma se evita problemas con las comas dentro 
        del texto
"""

#1. Leer el archivo con la lista de los términos aceptados
doc = list(reader(open('términos_aceptados.txt','r',encoding="iso-8859-1"), delimiter='\t'))

#2. Crear una tabla hash con todas las ocurrencias únicas a través de filas y colummnas

elements = set()

#3. Crear un diccionario con el número de ocurrencias por término
cnter = Counter()


#4. For-loop para crear 2 y 3
"""
doc = Todo el documento
i = Fila
j = Celda
"""

for i in doc:
    for j in i:
        if len(j)>0:
            cnter[j] +=1
            elements.add(j)

#5. elements = Términos aceptados eliminando duplicados y ordenados alfabéticamente
                
elements = list(elements)
elements.sort()




keys = defaultdict(set)
fp = Fingerprint()

#6. For-loop para alimentar keys donde las llaves son los términos fingerprinteados (Ciudad de México = ciudad de mexico) 
#y su contenido sus índices (es decir en qué posición ocurren)
count = 0
for w in elements:
    keys[fp.key(w)].add(count)
    count +=1

#7. For-loop para saber el tamaño del cluster y guardarlo en csize(ciudad de mexico: 1, 6, 9 -> 3)
#identificar el tamaño máximo de clúster (maxE)
#report = tamaño de cluster, termino 1, número de ocurrencias, término 2, número ocurrencias, etc
report = []
maxE = 0
for w in keys:
    csize = len(keys[w])
    if csize > maxE:
        maxE = csize
    if(csize > 1):
        tmp = []
        tmp.append(str(csize))
        for k in keys[w]:
            tmp.append(elements[k])
            tmp.append(str(cnter[elements[k]]))
        report.append(tmp)

report.sort()
report.reverse()
#8. Generar el encabezdo de la tabla
header = ["Tamaño del cluster"]
for i in range(0,maxE):
    header.append("Palabra")
    header.append("Número de apariciones")

#9. Crear tabla

file = open("reporte.csv",'w',encoding="iso-8859-1")
dialect = excel
dialect.lineterminator='\n'
wf = writer(file,dialect)
wf.writerow(["Total de detecciones:",str(len(report))])
wf.writerow(header)
wf.writerows(report)
for i in report:
    print(i)
file.close()
