"""
TODO
"""

__version__ = '0.0.1'

from flask import Flask, request, render_template, send_file, flash
import logging
from livereload import Server
from worship_ppt.bible import make_verse_ppt
from worship_ppt.jubo import make_main_ppt
from worship_ppt.hymn import make_hymn_ppt
from worship_ppt.common import DATA_PATH, log


def create_app():
  log.info('Creating App')
  app = Flask(__name__)
  app.secret_key = 'hello'

  @app.route('/', methods=['GET'])
  def index():  # pylint: disable=W0612
    return render_template('index.html', version_str=__version__)

  @app.route('/download_obs', methods=['POST'])
  def download_obs():  # pylint: disable=W0612
    log.info('Download obs')
    if request.method != 'POST':
      return

    ppt_inputs = [
        request.form['date_type'], request.form['sermon_title'],
        request.form['preacher'], request.form['main_passage'],
        request.form['quotes']
    ]

    try:
      path = make_verse_ppt(ppt_inputs, request.form['action'] == '자막 PPT')
      return send_file(path + '.pptx', as_attachment=True)
    except (TypeError, IndexError, AssertionError) as _:
      return ('', 204)

  @app.route('/download_jubo', methods=['POST'])
  def download_jubo():  # pylint: disable=W0612
    log.info('Download jubo')
    if request.method != 'POST' or not request.files:
      return

    doc_file = request.files['filename']
    if '.' not in doc_file.filename:
      flash('주보 파일을 선택하지 않았습니다.', 'warning')
      return render_template('index.html')
    elif doc_file.filename.rsplit('.', 1)[1].upper() in ['DOCX', 'DOC']:
      doc_file.save(DATA_PATH / doc_file.filename)
      path = make_main_ppt(DATA_PATH / doc_file.filename)
      return send_file(path + '.pptx', as_attachment=True)
    else:
      flash('워드 파일이 필요합니다.', 'warning')
      return render_template('index.html')

  @app.route('/download_hymn', methods=['POST'])
  def download_hymn():  # pylint: disable=W0612
    log.info('Download hymn')
    if request.method != 'POST':
      return

    hymn_no = request.form['hymn_no'].strip(' ,')
    if not hymn_no:
      flash('찬송가 장 수를 입력해주세요.', 'warning')
      return render_template('index.html')
    elif hymn_no.replace(',', '').replace(' ', '').isnumeric():
      path = make_hymn_ppt(hymn_no)
      return send_file(path + '.pptx', as_attachment=True)
    else:
      flash('입력하신 정보를 처리할 수 없습니다.', 'warning')
      return render_template('index.html')

  return app


if __name__ == '__main__':
  logging.basicConfig(level='DEBUG')
  my_app = create_app()
  server = Server(my_app.wsgi_app)
  server.serve(port=8080, debug=True)
