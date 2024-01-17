import json

data = json.load(open(r"C:\Users\Admin\Desktop\VNnSE_Flask - Copy\data\ArticlesNewspaper.json", 'r', encoding="utf-8"))
prpfi = open(r"C:\Users\Admin\Desktop\VNnSE_Flask - Copy\data\preprocessing.txt", 'r', encoding='utf-8').read().split("\n")

# data = json.load(open(r"C:\Users\Admin\Desktop\VNnSE_Flask - Copy\output2.json", 'r', encoding="utf-8"))
# prpfi = open(r"C:\Users\Admin\Desktop\VNnSE_Flask - Copy\data\pp.txt", 'r', encoding='utf-8').read().split("\n")
print(len(data))
print(len(prpfi))
import os
print(os.getcwd())