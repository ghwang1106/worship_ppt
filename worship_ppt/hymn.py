"""
TODO
"""
import json

from worship_ppt.common import DATA_PATH, log
from worship_ppt.ppt import PPT


class Hymn():
  """ TODO
  """

  def __init__(self, json_file=DATA_PATH / 'hymn.json'):
    with open(json_file, 'r', encoding='utf-8') as f:
      self.all = json.load(f)

  def lookup(self, song_type='hymn', number=0, title=''):
    try:
      song_received = next(item for item in self.all
                           if item['song_type'] == song_type and
                           item['number'] == number and title in item['title'])
    except StopIteration:
      log.warning('Song not found (%s)', locals()['title'])
      song_received = {
          'song_type': song_type,
          'number': number,
          'title': title,
          'lyrics': ['(가사가 DB에 없습니다)']
      }
    return song_received


def make_hymn_ppt(hymn_no):
  hymn = Hymn()
  worship_ppt = PPT()
  worship_ppt.make_hymn(hymn, hymn_no)

  return worship_ppt.to_pptx((DATA_PATH / 'hymn').as_posix())
