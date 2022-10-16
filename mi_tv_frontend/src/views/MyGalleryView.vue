<template>
  <div class="flex flex-col items-center mb-5 mt-10 sm:mt-16">
    <h1 class="text-3xl sm:text-6xl">{{ title }}</h1>
    <h2 class="text-xl sm:text-2xl">{{ organisation }}</h2>
  </div>
  <GalleryViewer :medias="items" :is-global="false" />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import GalleryViewer from "../components/GalleryViewer.vue";
import GetMediaService from "../services/GetMediaService";

export default defineComponent({
  name: "MyGalleryView",
  components: {
    GalleryViewer: GalleryViewer,
  },
  created() {
    let url = "/get_by_name/munier";

    for (let i in this.$route.params.path as Array<string>) {
      url += this.$route.params.path[i] + "/";
    }

    GetMediaService.getMedia(url)
      .then((response) => {
        this.items = response.data.files;
        this.title = response.data.event_name;
        this.organisation = response.data.association;
      })
      .catch((error) => {
        console.log(error);
      });
  },
  data() {
    return {
      items: {},
      title: "",
      organisation: "",
    };
  },
});
</script>
