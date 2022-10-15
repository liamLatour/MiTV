<template>
  <div class="wrapper">
    <div v-if="progressInfos">
      <div class="" v-for="(progressInfo, index) in progressInfos" :key="index">
        <span>{{ progressInfo.fileName }}</span>
        <div class="">
          <div
            class=""
            role="progressbar"
            :aria-valuenow="progressInfo.percentage"
            aria-valuemin="0"
            aria-valuemax="100"
            :style="{ width: progressInfo.percentage + '%' }"
          >
            {{ progressInfo.percentage }}%
          </div>
        </div>
      </div>
    </div>

    <div class="files">
      <input type="file" multiple @change="selectFile" />
      <label>Déposer vos images ici</label>
    </div>

    <button class="upload" :disabled="!selectedFiles" @click="uploadFiles">
      <font-awesome-icon icon="fa-solid fa-upload" />
    </button>

    <div v-if="message" class="">
      <ul>
        <li v-for="(ms, i) in message.split('\n')" :key="i">
          {{ ms }}
        </li>
      </ul>
    </div>
    <!--
    <div class="">
      <div class="">List of Files</div>
      <ul class="">
        <li class="" v-for="(file, index) in fileInfos" :key="index">
          <a :href="file.url">{{ file.name }}</a>
        </li>
      </ul>
    </div>
  --></div>
</template>

<script lang="ts">
import UploadService from "../services/UploadFilesService";
import { defineComponent } from "vue";

export default defineComponent({
  name: "UploadFiles",
  data() {
    return {
      selectedFiles: undefined,
      progressInfos: [],
      message: "",

      fileInfos: [],
    };
  },
  methods: {
    selectFile() {
      this.progressInfos = [];
      this.selectedFiles = event.target.files;
    },
    uploadFiles() {
      this.message = "";

      for (let i = 0; i < this.selectedFiles.length; i++) {
        this.upload(i, this.selectedFiles[i]);
      }
    },
    upload(idx, file) {
      this.progressInfos[idx] = { percentage: 0, fileName: file.name };

      UploadService.upload(file, (event) => {
        this.progressInfos[idx].percentage = Math.round(
          (100 * event.loaded) / event.total
        );
      })
        .then((response) => {
          let prevMessage = this.message ? this.message + "\n" : "";
          this.message = prevMessage + response.data.message;

          return UploadService.getFiles();
        })
        .then((files) => {
          this.fileInfos = files.data;
        })
        .catch(() => {
          this.progressInfos[idx].percentage = 0;
          this.message = "Could not upload the file:" + file.name;
        });
    },
  },
  mounted() {
    UploadService.getFiles().then((response) => {
      this.fileInfos = response.data;
    });
  },
});
</script>

<style lang="scss">
.wrapper {
  display: flex;
  flex-direction: column;
  margin-top: 50px;
  height: 50%;

  .files {
    display: block;
    width: 70%;
    height: 100%;
    margin: auto;
    border: 2px dashed grey;
    border-radius: 10px;
    margin-bottom: 20px;

    label {
      position: absolute;
      transform: translate(-50%, -50%);
      left: 50%;
      top: 50%;
      font-weight: 700;
      font-size: large;
    }
  }
  .upload {
    color: rgb(84, 223, 107);
    font-size: 2.3em;
  }
}

#app {
  height: 100vh;
}
</style>
