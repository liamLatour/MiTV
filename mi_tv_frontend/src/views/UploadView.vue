<!--https://www.bezkoder.com/vue-upload-image-axios/-->

<template>
  <h1 class="title">Uploadez vos images</h1>
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

<style lang="scss" scoped>
.title {
  text-align: center;
  padding-top: 70px;
}
</style>
