import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


file = json.load(open(r"C:\Users\Admin\Desktop\VNnSE_Flask\output2.json", 'r', encoding="utf-8"))
data_text = [i['title']for i in file]
vectorized = TfidfVectorizer()
X = vectorized.fit_transform(data_text)
XX=X.toarray()
print(XX)

