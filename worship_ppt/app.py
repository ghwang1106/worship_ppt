"""
TODO
"""

from flask import Flask, request, render_template, send_file, flash
import logging
from livereload import Server
from worship_ppt.bible2pptx_web import make_verse_ppt
from worship_ppt.jubo2pptx import make_main_ppt
from worship_ppt.hymn2pptx import make_hymn_ppt
from worship_ppt.common import DATA_PATH


def create_app():
  app = Flask(__name__)
  app.secret_key = 'hello'

  @app.route('/', methods=['GET'])
  def index():  # pylint: disable=W0612
    return render_template('index.html')

  @app.route('/download_obs', methods=['GET', 'POST'])
  def download_obs():  # pylint: disable=W0612
    if request.method == 'POST':
      ppt_inputs = [
          request.form['date_type'], request.form['sermon_title'],
          request.form['preacher'], request.form['main_passage'],
          request.form['quotes']
      ]

      try:
        if request.form['action'] == '본문 PPT':
          path = make_verse_ppt(ppt_inputs)
        elif request.form['action'] == '자막 PPT':
          path = make_verse_ppt(ppt_inputs, 1)
        return send_file(path + '.pptx', as_attachment=True)
      except (TypeError, IndexError, AssertionError) as _:
        return ('', 204)

  @app.route('/download_jubo', methods=['GET', 'POST'])
  def download_jubo():  # pylint: disable=W0612
    if request.method == 'POST':
      if request.files:
        doc_file = request.files['filename']
        if '.' in doc_file.filename:
          if doc_file.filename.rsplit('.', 1)[1].upper() in ['DOCX', 'DOC']:
            doc_file.save(DATA_PATH / doc_file.filename)
            path = make_main_ppt(DATA_PATH / doc_file.filename)
            return send_file(path + '.pptx', as_attachment=True)
          else:
            flash('워드 파일이 필요합니다.', 'warning')
            return render_template('index.html')

        flash('주보 파일을 선택하지 않았습니다.', 'warning')
        return render_template('index.html')

  @app.route('/download_hymn', methods=['GET', 'POST'])
  def download_hymn():  # pylint: disable=W0612
    if request.method == 'POST':
      hymn_no = request.form['hymn_no'].strip(' ,')
      if hymn_no:
        if hymn_no.replace(',', '').replace(' ', '').isnumeric():
          path = make_hymn_ppt(hymn_no)
          return send_file(path + '.pptx', as_attachment=True)
        else:
          flash('입력하신 정보를 처리할 수 없습니다.', 'warning')
          return render_template('index.html')
      else:
        flash('찬송가 장 수를 입력해주세요.', 'warning')
        return render_template('index.html')

  return app


if __name__ == '__main__':
  my_app = create_app()
  logging.basicConfig(level='DEBUG')
  server = Server(my_app.wsgi_app)
  server.serve(debug=True)
