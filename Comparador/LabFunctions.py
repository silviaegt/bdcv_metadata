# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 20:40:05 2017

@author: Antonio
"""
from csv import writer,excel
from collections import defaultdict,Counter
import re

"""
* Función que se encarga de interpretar y homogeneizar el código dewey de los 
* registros
* recibe:
*    st: Código dewey a homogeneizar
* regresa:
*    "EN PROCESO DE CATALOGACIÓN" cuando el código no tiene un dewey definido
*    "pass" cuando el código dewey es un caso especial ej. J/333.333
*    en caso de que el código sea de la forma 333.333 regresa 333
"""
def getClass(st):
    if re.match(".*EN PROCESO.*",st):
        return "EN PROCESO DE CATALOGACIÓN"
    elif re.match("[^\d]/+\d+.?\d*",st):
        return "pass"
    elif re.match("\d+.?\d*",st):
        return number(st)
    else:
        return st
 
"""
* Función que se encarga de obtener primeros 10 elementos de una lista de tuplas
* Recibe:
*    items: lista de tuplas
* Regresa:
*    tmp: lista con las primeras 10 (o menos) tuplas
"""
def getCounts(items):
    tmp = []
    if len(items)>=10:
        lim = 9
    else:
        lim = len(items)
    for i in range(lim):
        it = items[i]
        tmp.append(it[1])
        tmp.append(str(it[0]))
    return tmp
    
"""
* Función que se encarga de generar diccionarios de datos (Dewey y C001)
* Recibe:
*    doc: Lista en la que la columna 1 contendrá la llave y la columna 2 el elemento
* Regresa:
*    dic: Diccionario para que se tenga una búsqueda más rápida
"""
def getDict(doc):
    dic = defaultdict(str)
    for i in doc:
        dic[i[0]]=i[1]
    return dic

"""
* Función que se encarga de obtener los diccionarios en los que se almacenarán
* los Códigos dewey y titulos de cada registro
* Recibe:
*    doc: lista donde se encuentra el título y el código dewey (Archivo de títulos)
*    dic: diccionario donde se encuentra el código dewey y su significado
* Retorna:
*    titles: diccionario con los títulos de cada registro
*    clas:   diccionario con la clasificación de cada registro
"""
def getFlags(doc,dic):
    titles = defaultdict(set)
    clas = defaultdict(set)
    for i in doc[1:]:
        titles[i[0]].add(i[5])
        cl = getClass(i[2])
        if cl in dic:
            clas[i[0]].add(dic[cl])
        else:
            clas[i[0]].add(i[2])
    return titles,clas

"""
* Función que se encarga de obtener el header adecuado para el reporte que se
* está generando
* Recibe:
*    cnt: bandera para determinar el tipo de header
* Retorna:
*    Lista de cadenas con el encabezado del reporte
"""
def getHeader(cnt):
    if cnt == True:
        return ["clas_cent","clas_dec","clas_un","dewey_comp","dewey",
                "Gran Total","Total de Ocurrencias Diferentes"]
    else:
        return ["SH","Total de Ocurrencias en diferentes registros",
                     "Apariciones totales en el documento",
                    "Total de Ocurrencias Diferentes en el documento",
                    "Promedio"]
"""
* Función que se encarga de obtener la llave correspondiente de un valor dentro
* de un diccionario de datos
* Recibe:
*    dic: diccionario de datos en el que se va a búscar el valor
*    value: valor deseado
* Regresa:
*    i: llave correspondiente al valor
*    xxx: en caso de que no se encuentre el valor dentro del diccionario
"""
def getKey(dic,value):
    for i in dic:
        text = getText(str(dic[i]))
        if text.__eq__(value):
            return i
    return "xxx"

"""
* Función que se encarga de calcular: Total de Ocurrencias en diferentes registros,
* Apariciones totales en el documento, Total de Ocurrencias Diferentes en el 
* documento, Promedio y la lista ordenada por frecuencia de elementos
* Recibe:
*    items: lista con diferentes elementos
* Regresa:
*    lista de dos listas
*        1: Ocurrencias y promedio
*        2: Lista de tuplas ordenada por frencuencia de aparición
"""
def getValues(items):
    tot = len(items)
    items = Counter(items)
    tmp = []
    prom = 0
    for i in items:
        prom += items[i]
        tmp.append((items[i],i))
    tmp.sort()
    tmp.reverse()
    den = len(items)
    return [[str(tot),str(den),str(prom/den)],tmp]

"""
* Funcion que se encarga de generar los diccionarios que se estudiarán
* Recibe:
*    doc:    Lista en la cual se tienen cargados los subs
*    keys:   Diccionario con las etiquetas válidas
*    titles: Diccionario en el que se encuentran almacenados los títulos de los
*            libros
*    clas:   Diccionario con el código Dewey de cada registro
*    c001:   Diccionario con el código C001 de cada registro
*    n:      Columna desde la que empiezan los subs en doc
*    route:  Ruta en la que se generará el archivo erros_subs.csv
* Regresa:
*    tables: Diccionario en el que se agrupa todos los temas por etiquetas sin 
*            importar que esten repetidos o no
*    reg2:   Diccionario en el que se agrupan todas las etiquetas por registro
*            sin importar si las etiquetas se repiten o no
*    reg3:   Diccionario en el que se agrupan todos los temas por clasificación
*            Dewey sin importar si se repiten o no
*    forNet: Diccionario en el que se agrupa los temas y etiquetas por registro
*            sin tomar en cuenta los elementos repetidos dentro del mismo registro
* Genera:
*    errors_subs.csv: Archivo en el que se registran las etiquetas que no eran
*                     válidas y su contenido
"""
def getTables(doc,keys,titles,clas,c001,n,route):
    regex = re.compile("[^\w]")
    errors = Counter()
    tables = defaultdict(list)
    reg2 = defaultdict(list)
    reg3 = defaultdict(list)
    forNet = defaultdict(set)
    dialect = excel
    dialect.lineterminator='\n'
    file = open(route+"errors_subs.csv",'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(["Título","C001","Error"])
    for i in doc[1:]:
        tmp = getText(str(titles[i[0]]))
        for j in range(n,len(i),2):
            if len(i[j])>0:
                key = regex.sub('',i[j-1])
                if not key in keys and not key.__eq__("2"):
                    errors[key]+=1
                    print("Error en el registro: "+i[0])
                    print("Título: "+tmp)
                    print("C001: "+c001[i[0]])
                    print("\""+key+"\""+" no es válida\n")
                    wf.writerow([tmp,c001[i[0]],key])
                elif not key.__eq__("2"):
                    tables[key].append(i[j])
                    reg2[str(i[0])].append(key)
                    reg3[getText(str(clas[i[0]]))].append(i[j])
                    sTmp=key+"||"+i[j]#+"_"+txt[:2]
                    forNet[str(i[0])].add(sTmp)
    file.close()
    return tables,reg2,reg3,forNet

"""
* Función que se encarga de eliminar los siguientes caracteres de una cadena:
*    ' { }
* Recibe:
*    titles: cadena a limpiar
* Regresa:
*    tmp: cadena limpia
"""
def getText(title):
    tmp = title.replace("\'","")
    tmp = tmp.replace("{","")
    tmp = tmp.replace("}","")
    return tmp

"""
* Función que se encarga de hacer el conteo de apariciones de etiquetas en
* diferentes registros
* Recibe:
*    sh: Diccionario en el que se agrupan todas las etiquetas por registro
*    sin importar si las etiquetas se repiten o no
* Regresa:
*    cnt: contador con la ocurrencia de cada etiqueta en diferentes registros
"""
def keyCount(sh):
    cnt = Counter()
    for i in sh:
        tmp = set(list(sh[i]))
        for j in tmp:
            cnt[j]+=1
    return cnt

"""
* Función que se encarga de generar una lista ordenada por etiquetas para que
* pueda ser escrita de forma columnar en un reporte (no se usa)
* Recibe:
*    items: diccionario en el que se tienen etiquetas con su frecuencia
* Regresa:
*    tmp: lista ordenada por etiqueta para escritura mediante csv.writer
"""
def listToReport(items):
    dic = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7,"j":8,"k":9,
    "l":10,"m":11,"n":12,"o":13,"p":14,"q":15,"r":16,"s":17,"t":18,"u":19,
    "v":20,"x":21,"y":22,"z":23,"0":24,"2":25,"3":26,"4":27,"6":28,"8":29}
    tmp = []
    for i in range(len(dic)+1):
        tmp.append("")
    for i in items:
        tmp.pop(dic[i[1]])
        tmp.insert(dic[i[1]],str(i[0]))
    return tmp

"""
* Función que se encarga de generar el archivo cont_por_clas.csv
* Recibe:
*    route: dirección en la que se almacenará el archivo
*    sh: Diccionario en el que se agrupan todos los temas por clasificación
*       Dewey sin importar si se repiten o no
*    cnt: Bandera para determinar el header
*    dicc: diccionario para la traducción del codígo dewey
*    clas: diccionario con la clasificación de cada registro
*    c001: diccionario para la traducción del codígo c001
"""
def makeCntClas(route,sh,cnt,dicc,clas,c001):
    print("Generando: "+route+"\n")
    dialect = excel
    dialect.lineterminator='\n'
    file = open(route,'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(getHeader(cnt))
    dire = route.replace("cont_por_clas","dewey_errors")
    file2 = open(dire,'w',encoding="iso-8859-1")
    wf2 = writer(file2,dialect)
    wf2.writerow(["Num_reg","c001","Error"]+getHeader(cnt)[5:])
    for i in sh:
        l = getValues(list(sh[i]))
        dewey = getKey(dicc,i)
        if dewey.__eq__("xxx"):
            if re.match("[^\d]{1,8}/?\d+\.?\d*",i):
                wf.writerow(["","","","",i]+l[0][0:-1]+getCounts(l[1]))
            else:
                reg = getKey(clas,i)
                wf2.writerow([reg,c001[reg],i]+l[0][0:-1]+getCounts(l[1]))
        else:
            val = [dewey[0]+"00","0"+dewey[1]+"0","00"+dewey[2],dewey]
            wf.writerow(val+[i]+l[0][0:-1]+getCounts(l[1]))
    file2.close()
    file.close()

"""
* Función que se encarga de generar el archivo subs_reporte_gral.csv
* Recibe:
*    route: dirección en la que se almacenará el archivo
*    sh: Diccionario en el que se agrupa todos los temas por etiquetas sin 
*       importar que esten repetidos o no
*    cnt: contador con la ocurrencia de cada etiqueta en diferentes registros   
"""
def makeGralReport(route,sh,cnt):
    print("Generando: "+route+"\n")
    dialect = excel
    dialect.lineterminator='\n'
    file = open(route,'w',encoding="iso-8859-1")
    wf = writer(file,dialect)
    wf.writerow(getHeader(cnt))
    for i in sh:
        l = getValues(list(sh[i]))
        prom = float(l[0].pop(2))
        prom *= float(l[0][1])
        prom = prom/float(cnt[i])
        prom = str(prom)
        l[0].insert(2,prom)
        wf.writerow([i,str(cnt[i])]+l[0]+getCounts(l[1]))
        dire = re.sub("Subs_reporte/.*","Tablas_count/",route)
        file2 = open(dire+i+".csv",'w',encoding="iso-8859-1")
        wf2 = writer(file2,dialect)
        wf2.writerow(["Frecuencia","Elemento"])
        for j in l[1]:
            wf2.writerow([str(j[0]),j[1]])
        file2.close()
    file.close()

"""
* Función que se encarga de hacer coincidir el codigo dewey de los libros con 
* el que se tiene en el diccionario de datos. Ej: 1 -> 001
* recibe:
*    st: Código dewey que se adecuará
* regresa:
*    st: Código dewey adecuado
"""
def number(st):
    st = st.split(".")
    st = st[0]
    if len(st)<3:
        for i in range(3-len(st)):
            st = "0"+st
        return st
    else:
        return st[:3]

"""
* Función que se encarga de generar los archivos de tablas dentro del directorio
* Tablas
* Recibe:
*    tables: lista con todo el contenido de la tabla
*    route:  ruta y nombre del archivo que se generará
* Genera:
*    Archivo de texto plano con el contenido de cada etiqueta eliminando repetidos
"""
def toFile(tables,route):
    tables = list(set(tables))
    tables.sort()
    with open(route+".txt",'w',encoding="iso-8859-1") as file:
        for i in tables:
            file.write(i+"\n")
        file.close()
