<!--https://www.bezkoder.com/vue-upload-image-axios/-->

<template>
  <h1 class="text-center mt-10 text-3xl sm:text-6xl sm:mt-16">
    Uploadez vos images
  </h1>
  <upload-image></upload-image>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import UploadImage from "../components/UploadImage.vue";

export default defineComponent({
  name: "UploadView",
  components: {
    UploadImage: UploadImage,
  },
});
</script>
