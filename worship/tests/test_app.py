# pylint: disable=redefined-outer-name
"""
API test for worship_ppt
"""

import pytest
from worship.app import create_app
from worship.common import log, DATA_PATH


@pytest.fixture()
def app():
  log.warning('Creating app')
  app = create_app()
  app.config.update({})

  yield app


@pytest.fixture()
def client(app):
  return app.test_client()


@pytest.fixture()
def runner(app):
  return app.test_cli_runner()


def test_download_obs(client):
  response = client.post('/download_obs',
                         data={
                             'action': '본문 PPT',
                             'date_type': '2021년 1월 1일 주일예배',
                             'sermon_title': '설교 제목입니다',
                             'preacher': '이찬우 목사',
                             'main_passage': '창세기 1:1-5',
                             'quotes': ''
                         })
  assert response.status_code == 200
  response = client.post('/download_obs',
                         data={
                             'action': '자막 PPT',
                             'date_type': '2021년 1월 1일 주일예배',
                             'sermon_title': '설교 제목입니다',
                             'preacher': '이찬우 목사',
                             'main_passage': '창세기 1:1-5',
                             'quotes': ''
                         })
  assert response.status_code == 200


def test_jubo(client):
  response = client.post(
      '/download_jubo',
      data={'filename': (DATA_PATH / '6-26-22.docx').open('rb')})
  assert response.status_code == 200


def test_download_hymn(client):
  log.info('Downloading jubo')
  response = client.post('/download_hymn', data={'hymn_no': '123'})
  assert response.status_code == 200
