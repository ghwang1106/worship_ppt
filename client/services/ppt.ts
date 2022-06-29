import { Api } from "./api";
import { ApiResponse } from "apisauce"

export class PPTApi extends Api {
  async mainPPT(action, date_type, sermon_title, preacher, main_passage, quotes) {
    const response: ApiResponse<any> = await this.apisauce.get(
      "/download_obs",
      {
        action, date_type, sermon_title, preacher, main_passage, quotes
      }
    )

    if (!response.ok) {
      return;
    }
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'ppt.pptx'); //or any other extension
    document.body.appendChild(link);
    return link.click();
  }
}
