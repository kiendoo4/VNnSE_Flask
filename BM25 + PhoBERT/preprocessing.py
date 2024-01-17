import py_vncorenlp
import json
import numpy as np

rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir= r'C:\Users\Admin\AppData\Local\Programs\Python\Python311\Lib\site-packages\py_vncorenlp')
stopwords= open(r'C:\Users\Admin\Desktop\VNnSE_Flask\data\vietnamese-stopwords-dash.txt','r',encoding='utf-8').read().split("\n")
special_characters = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*',
    '+', ',', '-', '.', '/', ':', ';', '<', '=', '>',
    '?', '@', '[', '\\', ']', '^', '`', '{', '|',
    '}', '~'
]

def remove_stopwords(stopwords, title):
    tokenized_title = title.split(' ')
    fi_title_words = []
    for word in tokenized_title:
        if word not in stopwords:
            fi_title_words.append(word)
    fi_title = ' '.join(fi_title_words)
    return fi_title

def lower_text(text):
    ptext = text.lower()
    return ptext

def segment_text(text):
    text = rdrsegmenter.word_segment(text)
    return str(text)

def remove_stopwords(stopwords, title):
    tokenized_title = title.split(' ')
    fi_title_words = []
    for word in tokenized_title:
        if word not in stopwords:
            fi_title_words.append(word)
    fi_title = ' '.join(fi_title_words)
    return fi_title

def remove_special_characters(title):
    cleaned_title = ''.join(char for char in title if char not in special_characters)
    return cleaned_title

data = json.load(open(r"C:\Users\Admin\Desktop\VNnSE_Flask - Copy\data\ArticlesNewspaper.json", 'r', encoding="utf-8"))
#data = json.load(open(r"C:\Users\Admin\Desktop\VNnSE_Flask - Copy\output2.json", 'r', encoding="utf-8"))

titles = [i['title']for i in data]
abstracts = [i['abstract']for i in data]

pfi = [lower_text(titles[i]) + " " + lower_text(str(abstracts[i])) for i in range(len(titles))]
pfi = [segment_text(word) for word in pfi]
pfi = [remove_stopwords(stopwords, word) for word in pfi]
prpfi = [remove_special_characters(title) for title in pfi]

file=open(r"C:\Users\Admin\Desktop\VNnSE_Flask - Copy\data\preprocessing.txt", "a", encoding="utf-8")
#file = open(r"C:\Users\Admin\Desktop\VNnSE_Flask - Copy\data\pp.txt", 'a', encoding='utf-8')
for i in prpfi:
    file.write("\n" + i)