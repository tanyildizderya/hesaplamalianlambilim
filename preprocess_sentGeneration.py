import turkishnlp
from turkishnlp import detector
import pandas as pd
from difflib import SequenceMatcher

with open("isimler", encoding='utf-8') as f:
    nouns = f.readlines()

with open("fiiller", encoding="utf-8") as f:
    verbs = f.readlines()


obj = detector.TurkishNLP()
obj.download()
obj.create_word_set()

#%% spell correction func
def autoCorrect(text):
    text = obj.list_words(text)
    corrected_text = obj.auto_correct(text)
    corrected_text = " ".join(corrected_text)
    return corrected_text

#%% text cleaning func
def cleanText(text):
    
    import re
    pattern = re.compile("iliski")
    pattern2 = re.compile("\n")
    punc = '''!()-[]{};:""''\<>.@#$%^&*_?''' # ?/
    
    for element in text:
        if element in punc:
            text = text.replace(element,"")
            text = text.replace("�","ğ")
            text = text.replace("/"," ")
            text = re.sub(pattern,'',text)
            text = re.sub(pattern2,'',text)
            text = text.lstrip()
            text = text.lower()
            
    #text = obj.auto_correct(text)
    return text

#%% creating noun df
for i in range(len(nouns)):
    sample = nouns[i]
    nouns[i] = cleanText(sample)

df_noun = pd.DataFrame(nouns, columns = ["kelime"])
df_noun[['kelime', 'ilişki_türü','ilişki_değeri']] = df_noun["kelime"].str.split(',',3,expand=True)
df_noun.sort_values(by = ["kelime"], ascending = True, inplace = True, ignore_index = True)
#print(df_noun["ilişki_türü"].unique())

#%% creating verb df
for i in range(len(verbs)):
    sample = verbs[i]
    verbs[i] = cleanText(sample)

df_verbs = pd.DataFrame(verbs, columns = ["kelime"])
df_verbs[['kelime', 'ilişki_türü','ilişki_değeri']] = df_verbs["kelime"].str.split(',',3,expand=True)
#print(df_noun.tail()) # her sütunda bozukluk var, spell checker uygula
df_verbs.sort_values(by = ["kelime"], ascending = True, inplace = True, ignore_index = True)
#print(df_verbs["ilişki_türü"].unique())

#%% auto correct the annotators data
def correctAnnots(df):
    for word in range(len(df)):
        relation_value = df["ilişki_değeri"].values[word]
        corrected = autoCorrect(relation_value)
        df["ilişki_değeri"].values[word] = corrected
#%%

correctAnnots(df_noun)
correctAnnots(df_verbs)

#%% data singularity
df_noun = pd.DataFrame(df_noun.groupby(["kelime","ilişki_türü"])["ilişki_değeri"].agg(list))
df_verbs = pd.DataFrame(df_verbs.groupby(["kelime","ilişki_türü"])["ilişki_değeri"].agg(list))

#%% turn index into columns after agg
df_noun = df_noun.reset_index(level=1)
df_noun = df_noun.reset_index(level=0)

df_verbs = df_verbs.reset_index(level=1)
df_verbs = df_verbs.reset_index(level=0)
#%% all columns

all_cols = ['neyi kimi yapılır',
 'ağırlık gr kg',
 'nerede yapılır',
 'ne işe yarar',
 'sıfatları',
 'nasıl yapılır',
 'niçin yapılır',
 'yapınca ne olur',
 'kim ne ile yapılır',
 'rengi',
 'hammaddesi nedir',
 'canlı cansız',
 'ne olunca yapılır',
 'kim ne yapar',
 'fiziksel zihinsel',
 'kim kullanır',
 'hacmi cm3 m3',
 'üst kavramı nedir',
 'içinde neler bulunur',
 'neye kime yapılır',
 'şekli nasıl',
 'tanımı nedir',
 'yanında neler bulunur',
 'nerede bulunur']


#%% necessary columns for sentence generation

noun_cols = ['kelime','tanımı nedir','ne işe yarar','nerede bulunur',
        'yanında neler bulunur','içinde neler bulunur',
        'hammaddesi nedir','üst kavramı nedir',
        'kim kullanır','sıfatları','rengi',
        'şekli nasıl','canlı cansız']

verb_cols = ['kelime','tanımı nedir','nasıl yapılır','niçin yapılır',
        'ne olunca yapılır','yapınca ne olur',
        'neyi kimi yapılır','kim ne ile yapılır',
        'neye kime yapılır','nerede yapılır',
        'kim ne yapar','fiziksel zihinsel']

#%% concat cols and data
data = pd.DataFrame(columns=all_cols)
df_noun= pd.concat([df_noun,data], axis = 1)
df_verbs= pd.concat([df_verbs,data], axis = 1)

#%% correcting typos for relation types

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def correctRelations(df):
    for record in range(len(df)):
        relation = df["ilişki_türü"].values[record]
        relation = str.lower(relation)
        if(relation not in all_cols): # yanlış yazılmışsa
            max_sim = 0
            true_rel = relation
            for r in all_cols:
                ratio = similar(relation,r)
            #print(ratio,r,relation)
                if(ratio > max_sim):
                    max_sim = ratio
                    true_rel = r
                
            print(true_rel, "düzeltilen : ", relation, max_sim)
            df["ilişki_türü"].values[record] = true_rel
        else:
            df["ilişki_türü"].values[record] = relation
       
#%%
correctRelations(df_noun)
#%%
correctRelations(df_verbs)
#%%
#print(df_noun["ilişki_türü"].unique())
#print(df_noun["ilişki_türü"].nunique())
#%%
#print(df_verbs["ilişki_türü"].unique())
#print(df_verbs["ilişki_türü"].nunique())
#%% ilişki türü '' empty olanları siler
df_verbs.drop(df_verbs[df_verbs['ilişki_türü'] == ''].index, inplace = True)
#%% relation type infos to relation columns

def createTable(df):
    for i in range(len(df)): # satırlar arası dolaşır, başlangıç kelimesi seçer
        values = set()
        word = df["kelime"].values[i]
        relation_type = df["ilişki_türü"].values[i]
        relation_value = df["ilişki_değeri"].values[i]
        for v in relation_value:
            values.add(v)
        for j in range(len(df)): # karşılaştırılacak kayıtları gezer
            if(j>i): # kendinden sonra gelen kayıtlara bakar
                word2 = df["kelime"].values[j]
                relation_type2 = df["ilişki_türü"].values[j]
                if(word == word2 and relation_type == relation_type2):
                    relation_value2 = df["ilişki_değeri"].values[j]
                    for v2 in relation_value:
                        values.add(v2)
        #print(word, relation_type, "", values)
        df[relation_type].values[i] = list(values)
            

#%%
createTable(df_noun)
createTable(df_verbs)
#%% creating data for sentence generation

df_noun = pd.DataFrame(data=df_noun, columns = noun_cols)
df_verbs = pd.DataFrame(data=df_verbs, columns = verb_cols)
#%% creating data singularity
df_noun = df_noun.groupby(["kelime"]).first() 
df_verbs = df_verbs.groupby(["kelime"]).first()

#%% resetting index
df_noun = df_noun.reset_index(level=0)
df_verbs = df_verbs.reset_index(level=0)

#%% save the general data 
df_noun.to_csv("nouns.csv", index = False)
df_verbs.to_csv("verbs.csv", index = False)

