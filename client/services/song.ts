import { Api } from "./api";
import { ApiResponse } from "apisauce";

export class SongApi extends Api {
  async download_hymn(songs: String): Promise<any> {
    console.log("Downloading hymn", songs)
    const response: ApiResponse<any> = await this.apisauce.get(
      "/download_hymn",
      {
        hymn_no: songs,
      },
      { responseType: 'arraybuffer' }
    );

    if (!response.ok) {
      return;
    }
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'hymn.pptx'); //or any other extension
    document.body.appendChild(link);
    return link.click();
  }
}
