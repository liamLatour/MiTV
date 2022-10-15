<template>
  <div class="flex flex-col mt-11 h-2/4">
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

    <div
      class="flex w-11/12 sm:w-2/3 max-w-screen-lg h-full m-auto rounded-xl mb-5 border-dashed border-gray-500 border-2 justify-center items-center"
    >
      <input type="file" multiple @change="selectFile" />
      <label class="font-semibold text-xl sm:text-2xl"
        >Déposer vos images ici</label
      >
    </div>

    <button
      class="text-green-400 text-4xl"
      :disabled="!selectedFiles"
      @click="uploadFiles"
    >
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
#app {
  height: 100vh;
}
</style>
