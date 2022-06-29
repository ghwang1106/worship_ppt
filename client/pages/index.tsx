import React, { Component } from "react";
import { Layout } from "components/layout";
import { PPTForm } from "components/ppt_form";
import { JuboForm } from "components/jubo_form";
import { HymnForm } from "components/hymn_form";

export default class Index extends Component {
  render() {
    return (
      <Layout className="row">
        <PPTForm></PPTForm>
        <br />
        <JuboForm></JuboForm>

        <hr />
        <HymnForm></HymnForm>
      </Layout>
    );
  }
}
