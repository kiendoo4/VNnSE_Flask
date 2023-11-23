import numpy as np
import requests
from bs4 import BeautifulSoup
import re

urls_t = ["https://laodong.vn/thoi-su?page=",
          "https://laodong.vn/xa-hoi?page=",
          "https://laodong.vn/cong-doan?page=",
          "https://laodong.vn/the-gioi?page=",
          "https://laodong.vn/kinh-doanh?page=",
          "https://laodong.vn/van-hoa-giai-tri?page=",
          "https://laodong.vn/the-thao?page=",
          "https://laodong.vn/ban-doc?page="]
urls = np.array([])
i = np.arange(1, 11).astype(str)
for j in i:
    urls = np.concatenate((urls, np.vectorize(lambda s: s + j)(urls_t)), axis=0)


def get_content(url):
    response = requests.get(url)
    content = response.content
    return content


get_content_vec = np.vectorize(get_content)
contents = get_content_vec(urls)
data_link, data_img = ([], [])

for content in contents:
    soup = BeautifulSoup(content, "html.parser")
    data_link += soup.find_all("a", class_="link-title")
    data_img += soup.find_all("a", class_="link-img")

dl_text, dl_link, dl_img = ([], [], [])
for i in range(0, len(data_link)):
    if len(data_link[i].text.split()) < 5 or data_link[i].text in dl_text: continue
    dl_text.append(data_link[i].text)
    dl_link.append(data_link[i]["href"])
    match = re.search(r'(.*\.\w+)', data_img[i].img['src'])
    dl_img.append(match.group(1))

dl_text = dl_text[1:]
dl_link = dl_link[1:]
dl_img = dl_img[1:]

file = open('data.txt', 'r', encoding="utf-8")
s = file.read().lower().split("\n")

f1 = open('data.txt', 'a', encoding="utf-8")
f2 = open('data_link.txt', 'a', encoding="utf-8")
f3 = open('data_img.txt', 'a', encoding='utf-8')

for i in range (len(dl_text)):
    if dl_text[i].lower() not in s:
        f1.write("\n" + dl_text[i])
        f2.write("\n" + dl_link[i])
        f3.write("\n" + dl_img[i])