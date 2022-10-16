import http from "../http-common";

class UploadFilesService {
  uploadFiles(
    files: FileList,
    metaData: {
      thumbnail: string;
      exlude_thumbnail: boolean;
      event_name: string;
      association: string;
    },
    uploadProgress: (progressEvent: any) => void
  ) {
    const formData = new FormData();

    formData.append("event_name", metaData.event_name);
    formData.append("association", metaData.association);

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

  getFiles() {
    return http.get("/files");
  }
}

export default new UploadFilesService();
