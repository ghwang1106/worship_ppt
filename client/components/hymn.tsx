import React, { Component } from "react";

export class Hymn extends Component {
  render() {
    return (
      <>
        <h3>찬송가 PPT</h3>
        <form method="POST" action="/download_hymn" class="row">
          <label for="quotes" name="hymn_no" class="col-sm-2 col-form-label">찬송가 장 수</label>
          <div class="col-sm-10">
            <input id="quotes" type="text" class="form-control" name="hymn_no" size="30" placeholder="123,353" />
          </div>
          <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <button class="btn btn-primary" type="submit" name="action">찬송가 PPT</button>
          </div>
        </form>
      </>
    )
  }
}
