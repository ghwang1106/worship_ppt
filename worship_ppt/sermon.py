""" TODO
"""

import pandas as pd
from worship_ppt.common import log


class Sermon:
  """
  TODO
  """

  def __init__(self, bible: pd.DataFrame, raw_inputs):
    self.bible = bible

    if len(raw_inputs) > 4 and (raw_inputs[4].isspace() or
                                raw_inputs[4] == ''):  # Remove extra lines
      raw_inputs = raw_inputs[:4]

    # assign to variables (order must match!)
    self.date_type, self.title, self.preacher, passage = raw_inputs[:4]

    try:
      if int(self.date_type[:3]) != 202 or sum(x.isdigit()
                                               for x in self.date_type) < 6:
        log.warning('Check dates')
    except ValueError:
      log.warning('Check dates')
    passages_raw = [x.strip() for x in passage.split(',')]
    self.passages_raw, self.passages_ind = self.passages_raw2ind(passages_raw)

    if len(self.passages_raw
          ) > 1:  # if there are multiple blocks of text within the main passage
      if len({a.split(' ')[0] for a in self.passages_raw}) == 1:
        if len({a.split(' ')[-1].split(':')[0] for a in self.passages_raw
               }) == 1:
          self.passages_raw[1:] = [
              a.split(':')[-1] for a in self.passages_raw[1:]
          ]
        else:
          self.passages_raw[1:] = [
              a.split(' ')[-1] for a in self.passages_raw[1:]
          ]
      self.passages_raw = [', '.join(self.passages_raw)]

    if len(raw_inputs
          ) == 5:  # if there are quotes to include other than the main passage
      quotes_raw = [x.strip() for x in raw_inputs[4].split(',')]
      self.quotes_raw, self.quotes_ind = self.passages_raw2ind(quotes_raw)
    else:
      self.quotes_ind = []

  def passages_raw2ind(self, passages_raw):
    passages_ind = []

    for i, passage_raw in enumerate(passages_raw):
      assert passage_raw.count(
          ' ') == 1, 'Passage Format Error: Each passage should have one blank'
      [book, verses] = passages_raw[i].split()
      if book in list(
          self.bible.Abbr
      ):  # if only abbreviation of the book is given, turn it into full name
        passages_raw[i] = self.bible.Full[int(
            self.bible[self.bible.Abbr == book].index[0])] + ' ' + verses
      passages_ind.append(self.parse_passage(passages_raw[i]))

    return passages_raw, passages_ind

  def parse_passage(self, passage):
    try:
      book, verse_range = passage.split()
      book_ind = self.bible.Eng[int(
          self.bible[self.bible.Full == book].index[0])]
    except (ValueError, IndexError) as e:
      raise f'Bible book not recognizable ({passage})' from e

    try:
      if '-' in verse_range:
        verses = verse_range.split('-')
        if ':' not in verses[1]:
          verses[1] = verses[0].split(':')[0] + ':' + verses[1]
        verses[0] = [int(i) for i in verses[0].split(':')]
        verses[1] = [int(i) for i in verses[1].split(':')]
      else:
        verses = [[int(i) for i in verse_range.split(':')] for _ in range(2)]
    except (ValueError, IndexError) as e:
      raise 'Incorrect verse (check line 4-5 in prep file for typos)' from e

    return [book_ind, *verses]
