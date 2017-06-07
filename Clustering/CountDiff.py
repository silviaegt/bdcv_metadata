__author__ = 'silvia'

import difflib
from collections import Counter, defaultdict
#from nltk.tokenize import word_tokenize
import csv

def csv_from_tuplelist(csvfile, tuplelist):
    """
    create a csv file from a dictionary with a tuple list
    """
    csv_name = open(csvfile, 'w', encoding='latin1', newline='')
    csv_writer = csv.writer(csv_name, dialect='excel', lineterminator='\n')
    for x in tuplelist:
        csv_writer.writerow([x[0], x[1]])


### Comparar los términos del cluster que son menos frecuentes (st, tt, qt) contra el más frecuente (pt)

# pt = Primer término (más frecuente)
pt = []
# st = Segundo término (segundo más frecuente)
st = []
tt = []
qt = []
with open('words.csv', "r", encoding="latin1") as fin:
    next(fin)
    for l in fin:
        #print(l)
        line = l.split('"')
        g = l.split('"')
        pt.append(g[1])
        st.append(g[3])
        tt.append(g[5])
        qt.append(g[7])
        #print(type(st))

onevstwo = list(zip(pt, st))
#print(onevstwo)
onevsthree = list(zip(pt, tt))
onevsfour = list(zip(pt, qt))
#print(len(onevsfour))


sumof = onevstwo + onevsthree + onevsfour

adds = []
dels = []

addsdic = defaultdict(list)
deldic = defaultdict(list)

for a, b in onevstwo:
    if len(b) != 0:
        #print('{} => {}'.format(a, b))
        for i, s in enumerate(difflib.ndiff(b, a)):
            if s[0] == ' ':
                continue
            elif s[0] == '-':
                print(i, s)
                #adds = []
                #print(u'Delete "{}" from position {}'.format(s[-1], i))
                dels.append(s[-1])
                deldic[(b,a)].append(s[-1])
                print(len(adds))
            elif s[0] == '+':
                #print(u'Add "{}" to position {}'.format(s[-1], i))
                adds.append(s[-1])
                addsdic[(b,a)].append(s[-1])


delscount = Counter(dels).most_common()
addscount = Counter(adds).most_common()



#csv_from_tuplelist("dels_count.csv", delscount)
#csv_from_tuplelist("adds_count.csv", addscount)

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


def getWwithE (string, dictio):
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
            print("correcto %s  || error %s" % (termstuple[1], termstuple[0]))
            corr_incorr[termstuple[1]] = termstuple[0]
    correct_string = ' '.join(correcto).split()
    wrong_string = ' '.join(incorrecto).split()
    print("Palabras más comunes en térm. correctos: ", Counter(correct_string).most_common())
    print("Palabras más comunes en térm. errados: ", Counter(wrong_string).most_common())
    return corr_incorr

###Se prueba encontrar las palabras con error único (i, ",", o, a)

#ies = getWwithE("i", diffonedic)
##Conclusión: errores gramaticales en Poesía, Política, Judíos, Río, María, agrícolas, Filosofía, Ingeniería, Compañía, indígenas, Sociología

#commas = getWwithE(",", diffonedic)
##Conclusión: muchas palabras que terminan con , / en los correctos se escriben países entre paréntesis; en los errados se separa por coma

oes = getWwithE("o", diffonedic)
##Conclusión: errores gramaticales en Administración, Filósofos, Discriminación, Población (ción-words!)
