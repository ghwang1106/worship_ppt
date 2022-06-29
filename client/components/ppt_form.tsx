import React, { useState } from "react"
import { PPTApi } from "services";

// export class PPTForm extends Component {
export const PPTForm = () => {
  const [action, setAction] = useState(null);
  const [dateType, setDateType] = useState(null);
  const [sermonTitle, setSermonTitle] = useState(null);
  const [preacher, setPreacher] = useState(null)

  const onSubmit = async e => {
    e.preventDefault();
    const api = new PPTApi();
    api.setup();
    api.download_ppt()
  };
  return (
    <>
      <form className="row" onSubmit={onSubmit}>
        <label htmlFor="date_type" className="col-sm-2 col-form-label">날짜 & 예배</label>
        <select name="cars" id="cars" onChange={setAction}>
          <option value="volvo">Volvo</option>
          <option value="saab">Saab</option>
        </select>

        <div className="col-sm-10">
          <input id="date_type" type="text" name="date_type" className="form-control" size={30}
            placeholder="2022년 2월 2일 주일예배" onChange={e => setDateType(e.target.value)} />
        </div>
        <label htmlFor="sermon_title" className="col-sm-2 col-form-label">설교 제목</label>
        <div className="col-sm-10">
          <input id="sermon_title" type="text" name="sermon_title" className="form-control" size={30}
            placeholder="설교 제목입니다" onChange={e => setSermonTitle} />
        </div>
        <label htmlFor="preacher" className="col-sm-2 col-form-label">설교자</label>
        <div className="col-sm-10">
          <input id="preacher" type="text" name="preacher" className="form-control" size={30} placeholder="이찬우 목사" />
        </div>
        <label htmlFor="main_passage" className="col-sm-2 col-form-label">본문 구절</label>
        <div className="col-sm-10">
          <input id="main_passage" type="text" className="form-control" name="main_passage" size={30}
            placeholder="창세기 1:1-5" />
        </div>
        <label htmlFor="quotes" className="col-sm-2 col-form-label">인용 구절</label>
        <div className="col-sm-10">
          <input id="quotes" type="text" className="form-control" name="quotes" size={30}
            placeholder="창 2:2-3, 롬 11:36-12:2, 요한계시록 22:21 (없을 시 공백)" />
        </div>
        <div className="d-grid gap-2 d-md-flex justify-content-md-end">
          <button className="btn btn-primary" type="submit" name="action">본문 PPT</button>
        </div>
        <hr />
      </form>
    </>
  )
}
