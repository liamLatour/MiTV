import http from "../http-common";

class GetMediaService {
  getMedia(url: string) {
    return http.get(url);
  }
}

export default new GetMediaService();
