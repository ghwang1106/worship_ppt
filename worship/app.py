"""
TODO
"""

__version__ = '0.0.1'

from flask import Flask, request, render_template, send_file, flash, redirect
from flask_cors import CORS
from worship.bible import make_verse_ppt
from worship.jubo import make_main_ppt
from worship.ppt import PPT
from worship.hymn import Hymn
from worship.common import DATA_PATH, log


def create_app():
  log.info('Creating App')
  app = Flask(__name__)
  app.secret_key = 'hello'
  CORS(app)

  @app.route('/', methods=['GET'])
  def index():  # pylint: disable=W0612
    return render_template('index.html', version_str=__version__)

  @app.route('/download_obs', methods=['GET'])
  def download_obs():  # pylint: disable=W0612
    log.info('Download obs')
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
    if not request.files:
      return redirect('index.html')

    doc_file = request.files['jubo_file']
    if '.' not in doc_file.filename:
      flash('주보 파일을 선택하지 않았습니다.', 'warning')
      return render_template('index.html')
    elif doc_file.filename.rsplit('.', 1)[1].upper() in ['DOCX', 'DOC']:
      doc_file.save(DATA_PATH / doc_file.filename)
      path = make_main_ppt(DATA_PATH / doc_file.filename)
      return send_file(path + '.pptx', as_attachment=True)
    else:
      flash('워드 파일이 필요합니다.', 'warning')
      return redirect('/')

  @app.route('/hymn', methods=['GET'])
  def handle_hymn():  # pylint: disable=W0612
    log.info('Handle hymn')
    return redirect('/')
    # request.form

  @app.route('/download_hymn', methods=['GET'])
  def download_hymn():  # pylint: disable=W0612
    hymn_no = request.args['hymn_no'].strip(' ,')
    log.warning('Download hymn %s', str(hymn_no))
    if not hymn_no:
      flash('찬송가 장 수를 입력해주세요.', 'warning')
      return render_template('index.html')
    elif hymn_no.replace(',', '').replace(' ', '').isnumeric():
      hymn = Hymn()
      worship_ppt = PPT()
      worship_ppt.make_hymn(hymn, hymn_no)
      log.info('Sending files')

      path = worship_ppt.to_pptx((DATA_PATH / 'hymn').as_posix())
      log.info(path)
      return send_file(path + '.pptx')
    else:
      flash('입력하신 정보를 처리할 수 없습니다.', 'warning')
      return redirect('/')

  return app
