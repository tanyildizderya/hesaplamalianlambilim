import pandas as pd
from ast import literal_eval
import random

verbs = pd.read_csv("verbs.csv")
nouns = pd.read_csv("nouns.csv")

verbs.fillna("empty", inplace = True)
cols = verbs.iloc[:,1:].columns

for i in range(len(verbs)):
    for j in cols:
        cell = verbs[j].values[i]
        if(cell == "empty"):
            verbs[j].values[i] = [""]
        else:
            cell = literal_eval(cell)
            verbs[j].values[i] = cell

nouns.fillna("empty", inplace = True)
cols = nouns.iloc[:,1:].columns

for i in range(len(nouns)):
    for j in cols:
        cell = nouns[j].values[i]
        if(cell == "empty"):
            nouns[j].values[i] = [""]
        else:
            cell = literal_eval(cell)
            nouns[j].values[i] = cell

#create verb list
verb_list = []
for i in verbs["kelime"]:
    verb_list.append(i)

while '' in verb_list:
    verb_list.remove('')

#create subject list
subject_list = []
for i in verbs["kim ne yapar"]:
    subject_list.extend(i)

for i in nouns["kim kullanır"]:
    subject_list.extend(i)

while '' in subject_list:
    subject_list.remove('')

#create object list
object_list = []
for i in nouns["kelime"]:
    object_list.append(i)

while '' in object_list:
    object_list.remove('')

#create adjective list
adjective_list = []
for i in nouns["sıfatları"]:
    adjective_list.extend(i)

for i in nouns["rengi"]:
    adjective_list.extend(i)

while '' in adjective_list:
    adjective_list.remove('')

#create adverbial list
adverbial_list = []
for i in verbs["nasıl yapılır"]:
    adverbial_list.extend(i)

while '' in adverbial_list:
    adverbial_list.remove('')

#create indirect object list
indirect_object_list = []
for i in nouns["nerede bulunur"]:
    indirect_object_list.extend(i)

for i in verbs["nerede yapılır"]:
    indirect_object_list.extend(i)

for i in verbs["neye kime yapılır"]:
    indirect_object_list.extend(i)

while '' in indirect_object_list:
    indirect_object_list.remove('')

#create preposition list
preposition_list = []
for i in verbs["kim ne ile yapılır"]:
    preposition_list.extend(i)

while '' in preposition_list:
    preposition_list.remove('')

"""
Türkçe Cümle Yapısı

Özne + Sıfat + Nesne + Dolaylı Tümleç + Zarf +Yüklem

- Öğrenciler kalın kitaplarıyla birlikte kütüphaneye gitti
- Çocuklar büyük ağaçların etrafında el ele koşuyorlar

"""

def sentenceGenerate():
    sentence_generator = random.choice(subject_list) + " " \
                         + random.choice(adjective_list) + " " \
                         + random.choice(object_list) + " " \
                         + random.choice(indirect_object_list) + " " \
                         + random.choice(verb_list)
    return sentence_generator


print(sentenceGenerate())