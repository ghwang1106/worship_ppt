import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_driver(url):
  chrome_options = Options()
  chrome_options.add_argument("--incognito")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--window-size=1920x1080")
  return webdriver.Chrome(options=chrome_options, executable_path="./chromedriver.exe")


# Output file
out_file = 'Output.txt'

# Load Index
bb = pd.read_csv('bible_info.csv')

# Bible URL
url = 'https://www.bskorea.or.kr/bible/korbibReadpage.php?version=GAE'  # '&book=num&chap=9&sec=1'

# Loop through Books
f = open(out_file, "w", encoding="utf-8")
driver = get_driver()
try:
  with ThreadPoolExecutor() as ex:
    futures = [ex.submit(Book.update_raw, book) for book in books]
    all(future.result() for future in as_completed(futures))
  for book in range(66):
    f.write('[' + bb.Full[book] + ']\n\n')
    for chap in range(bb.Chap[book]):
      url_full = url + '&book=' + bb.Eng[book] + '&chap=' + str(chap+1) + '&sec=1'
      text_chapter = driver.get(url_full)
      text_chapter = driver.find_element_by_class_name("bible_read").text
      f.write(text_chapter[5:] + '\n\n')
except Exception as e:
  print(e)
finally:
  driver.close()

f.close()
