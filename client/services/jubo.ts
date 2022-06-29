import { Api } from "./api";
import { ApiResponse } from "apisauce";

export class JuboApi extends Api {
  async download_jubo(file: FormData): Promise<any> {
    const response: ApiResponse<any> = await this.apisauce.post(
      "/download_jubo",
      {
        file: file
      }
    );
    if (!response.ok) {
      return;
    }
    return response.data
  }
}
