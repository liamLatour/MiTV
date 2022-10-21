import http from "../http-common";

class GetMediaService {
  getMedia(url: string, data?: object) {
    return http.get(url, {
      params: data,
    });
  }
}

export default new GetMediaService();
