import re
import json
import pandas as pd


class Book():
    def __init__(self, title, text_all):
        self.title = title
        self.text_all = text_all


def takeout_footnote(verse):
    while re.search("\s.\)", verse):
        verse = verse[:verse.find(")")-1] + verse[verse.find(")")+1:]
    while re.search("\d\)", verse):
        verse = verse[:verse.find(")")-1] + verse[verse.find(")")+1:]
    if re.search("^.\)", verse):
        verse = verse[verse.find(")")+1:]
    return verse


def bible2dict(bible, titles):
    for i in range(len(bible)):
        bible[i] = Book(titles[i], bible[i]).__dict__
    return bible


# Specify text file
bible_text_file = 'BIBLE_ALL_GAE.txt'

# Load file
with open(bible_text_file, "r", encoding="utf-8") as f:
    bible_str = f.read()

bb = pd.read_csv('bible_info.csv')

# Create empty Bible
bible = [[] for i in range(66)]
for i in range(66):
    bible[i] = [[] for i in range(bb.Chap[i])]

# Read by line
by_line = bible_str.split("\n")

for i in by_line:

    if re.search("^\[.*\]$", i):
        book = i[1:-1]
        print(book)
        i_book = int(bb[bb.Full == book].index[0])
        if bb.Chap[i_book] == 1:
            i_chap = 1

    if re.search("제\s\d+\s.", i):
        i_chap = int(i[2:-2])

    if re.search("^\d+\s\s\s", i):
        verse = takeout_footnote(i[i.find('   ')+3:])
        bible[i_book][i_chap-1].append(verse)

bible = bible2dict(bible, bb.Full)

with open("./bible.json", "w", encoding='utf-8') as f:
    json.dump(bible, f, ensure_ascii=False, indent=4)
