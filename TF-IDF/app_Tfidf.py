from flask import Flask, request, render_template, url_for, redirect
from flask_paginate import Pagination, get_page_args
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

NUM_NEWS_PER_PAGE = 5
items = list()
query = ""
similarities=list()

def query_input(query):
    query_vector = vectorizer.transform([query])
    return query_vector

def cos_similarity(query_vector):
    global items
    similarities = cosine_similarity(query_vector, Tf_idf_matrix).flatten()
    sorted_ids=similarities.argsort()[::-1]
    k = 100
    k_idx = sorted_ids[0: k]
    items = k_idx
    return similarities.astype(str)

@app.route("/")
def home():
    return render_template("news/home.html")

@app.route("/search", methods=["POST", "GET"])
def submit():
    global items, query,similarities
    if request.method == "POST":
        query = request.form['search']
        cv_query = query_input(query)
        similarities= cos_similarity(cv_query)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination = Pagination(page=page, per_page=per_page, total=len(items), css_framework='bootstrap5')
    k_idx_show = items[offset: offset + NUM_NEWS_PER_PAGE]
    return render_template("news/search.html", k_idx = k_idx_show, data=data,similarities=similarities,query = query, pagination=pagination)

if __name__ == "__main__":
    data = json.load(open('.app/static/ArticlesNewspaper.json', 'r', encoding="utf-8"))
    data_text = [i['title']+ " " + i['abstract']for i in data]
    stopwords= open('data/vietnamese-stopwords.txt','r',encoding='utf-8').read().split("\n")
    vectorizer = TfidfVectorizer(stop_words=stopwords)
    Tf_idf_matrix = vectorizer.fit_transform(data_text)
    app.run(debug=True)
