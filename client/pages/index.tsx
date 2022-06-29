import React, { Component } from "react";
import { Layout } from "components/layout";
import { Song } from "components/song";
import { Hymn } from "components/hymn";

export default class Index extends Component {
  render() {
    return (
      <Layout>
        <body class="container">
          <br />
          <form method="POST" action="/download_obs" class="row">
            <label for="date_type" class="col-sm-2 col-form-label">날짜 & 예배</label>
            <div class="col-sm-10">
              <input id="date_type" type="text" name="date_type" class="form-control" size="30"
                placeholder="2022년 2월 2일 주일예배" />
            </div>
            <label for="sermon_title" class="col-sm-2 col-form-label">설교 제목</label>
            <div class="col-sm-10">
              <input id="sermon_title" type="text" name="sermon_title" class="form-control" size="30"
                placeholder="설교 제목입니다" />
            </div>
            <label for="preacher" class="col-sm-2 col-form-label">설교자</label>
            <div class="col-sm-10">
              <input id="preacher" type="text" name="preacher" class="form-control" size="30" placeholder="이찬우 목사" />
            </div>
            <label for="main_passage" class="col-sm-2 col-form-label">본문 구절</label>
            <div class="col-sm-10">
              <input id="main_passage" type="text" class="form-control" name="main_passage" size="30"
                placeholder="창세기 1:1-5" />
            </div>
            <label for="quotes" class="col-sm-2 col-form-label">인용 구절</label>
            <div class="col-sm-10">
              <input id="quotes" type="text" class="form-control" name="quotes" size="30"
                placeholder="창 2:2-3, 롬 11:36-12:2, 요한계시록 22:21 (없을 시 공백)" />
            </div>
            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
              <button class="btn btn-primary" type="submit" name="action">본문 PPT</button>
              <button class="btn btn-primary" type="submit" name="action">자막 PPT</button>
            </div>
            <hr />
          </form>

          <h3>본당 PPT 만들기 (개발 중)</h3>
          <form method="POST" action="/download_jubo" class="row" enctype='multipart/form-data'>
            <div class="col-12">
              <p>
                'Choose File'로 주보 파일을 선택한 후, 아래 '본당 PPT' 버튼을 눌러주세요
              </p>
            </div>
            <Song></Song>
            <Song></Song>
            <Song></Song>
            <Song></Song>
            <div class="col-2">
              <label> 주보 업로드 (워드 파일): </label>
              <input type="file" id="choose_file" name="filename" class="form-control" /><br />
            </div>
            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
              <button class="btn btn-primary" type="submit" name="action">본당 PPT</button>
            </div>
          </form>
          <hr />
          <Hymn></Hymn>

        </body>

      </Layout>
    );
  }
}
