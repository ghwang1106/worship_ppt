import { Api } from "./api";
import { ApiResponse } from "apisauce";
import { Verse } from "./types";

export type VerseResponse = any

export class BibleAPI extends Api {
  async readVerses(chapter: string, from: Number, to: Number): Promise<VerseResponse>{
    // const response: ApiResponse<any> = await this.apisauce.get(
    //   "/"
    // )
    console.log(chapter)
    console.log(from)
    console.log(to)
  }

}
