from flask import Flask, request, render_template, url_for, redirect
from flask_paginate import Pagination, get_page_args
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import torch
from transformers import AutoModel, AutoTokenizer
import numpy as np
import py_vncorenlp

phobert = AutoModel.from_pretrained("vinai/phobert-base-v2")
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")

app = Flask(__name__)

NUM_NEWS_PER_PAGE = 10
items = list()
query = ""
similarities=list()

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
def query_input(phoquery):
    cv_query = torch.tensor([tokenizer.encode(str(phoquery))])
    with torch.no_grad():
        cv_query = phobert(cv_query).pooler_output.numpy().flatten()
    return cv_query

def cos_similarity(cv_query, databert):
    global items
    similarities = []
    for i in range(databert.shape[0]):
        similarities.append(databert[i, :].dot(cv_query) / (np.linalg.norm(databert[i, :]) * np.linalg.norm(cv_query)))
    similarities = np.array(similarities)
    sorted_ids=similarities.argsort()[::-1]
    k = 10
    k_idx = sorted_ids[0: k]
    items = k_idx
    return similarities.astype(str)

def get_weighted_query(query, corpus):
  kw_list = query.split(' ')
  s = list()
  w = list()
  w_not_rounded = list()
  for word in kw_list:
    tf = kw_list.count(word) / len(kw_list)
    idf = np.log(len(corpus) / (sum(1 for doc in corpus if word in doc) + 1))
    s.append(tf * idf)
    print(tf, " ", idf, " ", sum(1 for doc in corpus if word in doc) + 1)
  for i in range(len(kw_list)):
    w.append(round((s[i] * len(kw_list)) / sum(s)))
    w_not_rounded.append((s[i] * len(kw_list)) / sum(s))
  print(w, "\n", w_not_rounded)
  weighted_query_words = []
  for i in range(len(w)):
    for j in range(w[i]):
      weighted_query_words.append(kw_list[i])
  weighted_query = ' '.join(weighted_query_words)
  return weighted_query

def phoBERT(content):
    data_ws = list()
    for col in content:
        data_ws.append(str(col))
    input_ids = torch.tensor([tokenizer.encode(data_ws[0])])
    with torch.no_grad():
        databert = phobert(input_ids).pooler_output.numpy()
    for i in range(1, len(data_ws)):
        val_ids = torch.tensor([tokenizer.encode(data_ws[i])])
        with torch.no_grad():
            databert = np.vstack([databert, phobert(val_ids).pooler_output.numpy().flatten()])
    return databert
@app.route("/")
def home():
    return render_template("news/home.html")

@app.route("/search", methods=["POST", "GET"])
def submit():
    global items, query,similarities
    if request.method == "POST":
        query = request.form['search']
        p_query = remove_special_characters(remove_stopwords(stopwords, segment_text(lower_text(query))))
        bm25 = BM25Okapi(tokenized_corpus)
        bm_query = p_query.split(" ")
        doc_scores = bm25.get_scores(bm_query)
        BM25_list50_content = bm25.get_top_n(bm_query, prpfi, n=50)
        content_sorted_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)
        BM25_list50_titles = bm25.get_top_n(bm_query, titles, n=50)
        matrix = phoBERT(BM25_list50_content)

        cv_query = query_input(p_query)
        similarities= cos_similarity(cv_query, matrix)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination = Pagination(page=page, per_page=per_page, total=len(items), css_framework='bootstrap5')
    k_idx_show = items[offset: offset + NUM_NEWS_PER_PAGE]
    return render_template("news/search.html", k_idx = k_idx_show, data=data, similarities=similarities,query = query, pagination=pagination, index = content_sorted_indices)

if __name__ == "__main__":
    data = json.load(open(r"C:\Users\Admin\Desktop\VNnSE_Flask - Copy\data\ArticlesNewspaper.json", 'r', encoding="utf-8"))
    data_text = [i['title']+ " " + i['abstract']for i in data]
    titles = [i['title']for i in data]
    stopwords= open(r"C:\Users\Admin\Desktop\VNnSE_Flask - Copy\data\vietnamese-stopwords-dash.txt",'r',encoding='utf-8').read().split("\n")
    prpfi = open(r"C:\Users\Admin\Desktop\VNnSE_Flask - Copy\data\preprocessing.txt", 'r', encoding='utf-8').read().split("\n")
    tokenized_corpus = [doc.split(" ") for doc in prpfi]
    app.run(debug=True)