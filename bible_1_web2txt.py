import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def grab_chapter(url):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=chrome_options, executable_path="./chromedriver.exe")
    driver.get(url)
    text_chapter = driver.find_element_by_class_name("bible_read").text
    driver.close()

    return text_chapter


# Output file
out_file = 'Output.txt'

# Load Index
bb = pd.read_csv('bible_info.csv')

# Bible URL
url = 'https://www.bskorea.or.kr/bible/korbibReadpage.php?version=GAE'  # '&book=num&chap=9&sec=1'

# Check if file exists
if os.path.exists(out_file):
    print('WARNING: FILE ALREADY EXISTS!')
    exit()

# Loop through Books
f = open(out_file, "a", encoding="utf-8")

for book in range(66):
    f.write('[' + bb.Full[book] + ']\n\n')

    for chap in range(bb.Chap[book]):
        url_full = url + '&book=' + bb.Eng[book] + '&chap=' + str(chap+1) + '&sec=1'
        text_chapter = grab_chapter(url_full)

        f.write(text_chapter[5:] + '\n\n')

f.close()
