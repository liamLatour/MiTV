import http from "../http-common";

class UploadFilesService {
  uploadFiles(
    files: FileList,
    metaData: {
      thumbnail: string;
      exlude_thumbnail: boolean;
      event_name: string;
      association: string;
      login: string;
    },
    uploadProgress: (progressEvent: any) => void
  ) {
    const formData = new FormData();

    formData.append("event_name", metaData.event_name);
    formData.append("association", metaData.association);
    formData.append("login", metaData.login);

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      formData.append("files[" + i + "]", file);
    }

    return http.post("/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      onUploadProgress: uploadProgress,
    });
  }
}

export default new UploadFilesService();
