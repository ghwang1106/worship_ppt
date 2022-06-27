"""
TODO
"""
from itertools import groupby
from docx import Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import Table
from docx.text.paragraph import Paragraph
from worship_ppt.common import DATA_PATH
from worship_ppt.hymn import Hymn
from worship_ppt.ppt import PPT


class Jubo:
  """ TODO
  """

  def __init__(self, jubo_file):
    jubo_raw = Document(jubo_file)
    all_text = []
    for block in self.iter_block_items(jubo_raw):
      if not isinstance(block, Table):
        continue
      for row in block.rows:
        row_data = [cell.text for cell in row.cells]
        if not row_data:
          continue
        for item in set(row_data):
          all_text.append(item)
    self.all_text = [x[0] for x in groupby(all_text)]

  def iter_block_items(self, jubo_raw):
    for content in jubo_raw.element.body.iterchildren():
      if isinstance(content, CT_P):
        yield Paragraph(content, jubo_raw)
      elif isinstance(content, CT_Tbl):
        yield Table(content, jubo_raw)

  def grab_section(self, s_start, s_finish):
    if isinstance(s_finish, int):
      return self.all_text[self.find_index(self.all_text, s_start)[0]:self.
                           find_index(self.all_text, s_start)[0] + s_finish]
    else:
      return self.all_text[self.find_index(self.all_text, s_start)[0]:self.
                           find_index(self.all_text, s_finish)[0]]

  def find_index(self, l, s):
    return [i for i, ll in enumerate(l) if s in ll]


def make_main_ppt(jubo_path):
  hymn = Hymn()
  jubo = Jubo(jubo_path)
  jubo.sermon = jubo.grab_section('년 표어', 2)[1].strip('\n')
  jubo.announcement = jubo.grab_section('우리 교회에 처음 오신 성도님들을', 3)[2].split('\n')
  jubo.worship_order = jubo.grab_section('입례송', '성경봉독')

  worship_ppt = PPT()
  worship_ppt.add_slide()
  worship_ppt.make_announcement(jubo.announcement)
  worship_ppt.make_worship1(jubo.worship_order, hymn)
  worship_ppt.make_worship2(jubo.sermon)

  return worship_ppt.to_pptx((DATA_PATH / 'worship').as_posix())
