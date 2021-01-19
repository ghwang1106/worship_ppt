import re
import json
import pandas as pd
import os
import pandas as pd
from common import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
from webdriver_manager.chrome import ChromeDriverManager


def takeout_footnote(verse):
  while re.search("\s.\)", verse):
    verse = verse[:verse.find(")")-1] + verse[verse.find(")")+1:]
  while re.search("\d\)", verse):
    verse = verse[:verse.find(")")-1] + verse[verse.find(")")+1:]
  if re.search("^.\)", verse):
    verse = verse[verse.find(")")+1:]
  return verse


def get_chrome_driver():
  chrome_options = Options()
  chrome_options.add_argument("--incognito")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--window-size=1920x1080")
  return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


class Book():
  def __init__(self, kr_name="", kr_abbr="", en_abbr="", total_chapter="", kr_raw=""):
    self.kr_name = kr_name
    self.kr_abbr = kr_abbr
    self.en_abbr = en_abbr
    self.total_chapter = total_chapter
    self.kr_raw = kr_raw

  def __repr__(self):
    return self.en_abbr

  @classmethod
  def get_all_books(cls):
    with open("bible.json", "r") as f:
      books = [cls(**book) for book in json.load(f)]
    return books

  def save_books(books):
    logger.info("save_books")
    try:
      with open("bible.json", "w") as f:
        json.dump([book.__dict__ for book in books], f, ensure_ascii=False)
    except Exception as e:
      logger.warn(str(e))
      return False
    return True

  def update_raw(self):
    logger.info(f"update_raw({self})")
    try:
      driver = get_chrome_driver()
      for chapter in range(self.total_chapter):
        url = f'https://www.bskorea.or.kr/bible/korbibReadpage.php?version=GAE&book={self.en_abbr}&chap={chapter + 1}&sec=1'
        driver.get(url)
        text = driver.find_element_by_class_name("bible_read").text
        self.kr_raw = text
    except Exception as e:
      logger.warn(e)
      return False
    finally:
      driver.close()
    return True

  def update_process(self):
    logger.info("update_process")
    try:
      for line in self.update_raw.split("\n"):
        if re.search(r"^\[.*\]$", line):
          book = line[1:-1]
          i_book = int(bb[bb.Full == book].index[0])
          if bb.Chap[i_book] == 1:
            i_chap = 1
        if re.search(r"제\s\d+\s.", line):
          i_chap = int(line[2:-2])
        if re.search(r"^\d+\s\s\s", line):
          verse = takeout_footnote(line[line.find('   ')+3:])
          self.en_chapter2verses = bible[i_book][i_chap-1].append(verse)
    except Exception as e:
      logger.warn(str(e))
      return False
    return True


if __name__ == "__main__":
  books = Book.get_all_books()

  with ThreadPoolExecutor() as ex:
    futures = [ex.submit(Book.update_raw, book) for book in books]
    all(future.result() for future in as_completed(futures))

  Book.save_books(books)
