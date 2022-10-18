import http from "../http-common";

class UpdateMetaService {
  updateMeta(
    metaData: {
      thumbnail?: string;
      exclude_thumbnail?: boolean;
      event_name?: string;
      association?: string;
    },
    login: string,
    url: string
  ) {
    return http.post(
      url,
      {
        metaData: metaData,
        login: login,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
  }
}

export default new UpdateMetaService();
