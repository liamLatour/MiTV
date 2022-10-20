<template>
  <div class="flex flex-col mt-11 h-2/4 justify-center items-center">
    <div
      class="flex justify-center items-center w-10/12"
      v-if="progressInfo != 0"
    >
      <span>{{ progressInfo }}%</span>
      <hr class="m-2 border-green-500" :style="{ width: progressInfo + '%' }" />
    </div>

    <div
      class="aspect overflow-clip flex w-11/12 sm:w-2/3 max-w-screen-lg m-auto rounded-xl mb-5 border-dashed border-gray-500 border-2 justify-center items-center"
    >
      <input
        type="file"
        name="test"
        accept="image/*"
        @change="selectFile"
        class="h-full w-full opacity-0 cursor-pointer z-10"
      />

      <label
        class="absolute font-semibold text-xl p-5 sm:text-2xl cursor-pointer hover:text-3xl duration-200"
        v-if="!selectedFiles"
      >
        Déposer votre photo ici
      </label>

      <div
        class="grid absolute left-0 right-0 top-0 bottom-0 p-1"
        :style="{ 'grid-template-columns': 'repeat(' + columns + ', 1fr)' }"
        v-if="selectedFiles"
      >
        <div
          v-for="(file, index) in selectedFiles"
          :key="file"
          class="overflow-clip m-0.5 aspect max-h-full max-w-full"
        >
          <template v-if="index < 25">
            <ImageItem :source="imageUrl(file)" />
          </template>
        </div>
      </div>
    </div>

    <div class="flex justify-center items-center mb-12">
      <button
        class="text-green-400 text-4xl cursor-pointer p-2 border-2 border-green-400 border-solid rounded-lg duration-300 hover:text-white hover:border-white disabled:text-gray-500 disabled:border-gray-500 disabled:cursor-default"
        @click="uploadFile"
        :disabled="!selectedFiles"
      >
        <font-awesome-icon icon="fa-solid fa-upload" />
        Envoyer
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import UploadService from "../services/UploadFilesService";
import ImageItem from "./ImageItem.vue";

export default defineComponent({
  name: "UploadFiles",
  components: {
    ImageItem,
  },
  data() {
    return {
      selectedFiles: undefined as any,
      progressInfos: [] as Array<number>,
      progressInfo: 0,

      columns: 6,
      association: "",
      event_name: "",
    };
  },
  methods: {
    selectFile(event: Event) {
      this.progressInfos = [];

      const files = (event.target as HTMLInputElement).files;
      if (files != null) {
        this.columns = Math.sqrt(Math.min(25, files.length)) >> 0;
      }
      this.selectedFiles = files;
    },
    uploadFile() {
      let uuid = this.$uuid.v4();

      UploadService.uploadRef(this.selectedFiles, uuid, (event: any) => {
        this.progressInfo = Math.round((100 * event.loaded) / event.total);
      })
        .then((response) => {
          alert(response.data);
          this.$cookies.set("uuid", uuid, Infinity);
        })
        .catch(() => {
          this.progressInfo = 0;
        });
    },
    imageUrl(file: File) {
      return URL.createObjectURL(file);
    },
    globalProgress() {
      if (this.progressInfos.length == 0) return 0;
      return Math.round(
        this.progressInfos.reduce((partialSum, a) => partialSum + a, 0) /
          this.progressInfos.length
      );
    },
  },
});
</script>

<style scoped lang="scss">
.aspect {
  aspect-ratio: 3/2;
}
</style>
