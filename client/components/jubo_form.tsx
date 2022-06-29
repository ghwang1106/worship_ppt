import React, { useState } from "react";
import { Song } from "components/song";
import { JuboApi } from "services/jubo"

export const JuboForm = () => {
  const [file, setFile] = useState(null);

  const onSubmit = async e => {
    e.preventDefault();
    const api = new JuboApi();
    api.setup();
    api.download_jubo(file);
  }

  return (
    <>
      <h3>본당 PPT 만들기 (개발 중)</h3>
      <form className="row" encType='multipart/form-data' onSubmit={onSubmit}>
        <div className="col-12">
          <p>
            'Choose File'로 주보 파일을 선택한 후, 아래 '본당 PPT' 버튼을 눌러주세요
          </p>
        </div>
        <Song></Song>
        <Song></Song>
        <Song></Song>
        <Song></Song>
        <div className="col-2">
          <label> 주보 업로드 (워드 파일): </label>
          <input required type="file" accept=".doc,.docx" id="choose_file" name="filename" className="form-control"
            onChange={(e) => { setFile(e.target.files[0]) }} /><br />
        </div>
        <div className="d-grid gap-2 d-md-flex justify-content-md-end">
          <button className="btn btn-primary" type="submit" name="action">본당 PPT</button>
        </div>
      </form>
    </>
  )
}
