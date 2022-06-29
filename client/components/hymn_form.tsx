import React, { useState } from "react";
import { SongApi } from "services/song";

export const HymnForm = () => {
  const [song, setSong] = useState("");

  const onSubmit = async e => {
    e.preventDefault();
    const api = new SongApi();
    api.setup();
    api.download_hymn(song);
  }

  return (
    <>
      <h3>찬송가 PPT</h3>
      <form className="row" onSubmit={onSubmit}>
        <label htmlFor="quotes" className="col-sm-2 col-form-label">찬송가 장수</label>
        <div className="col-sm-10">
          <input id="quotes" type="text" className="form-control" name="hymn_no" placeholder="123,353"
            required onChange={e => { setSong(e.target.value) }} />
        </div>

        <div className="d-grid gap-2 d-md-flex justify-content-md-end">
          <button className="btn btn-primary" type="submit" name="action">찬송가 PPT</button>
        </div>
      </form>
    </>
  )
}
