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
import axios from "axios";

export default defineComponent({
  name: "MyGalleryView",
  components: {
    GalleryViewer: GalleryViewer,
  },
  created() {
    this.getMedias();
  },
  data() {
    return {
      items: {},
      title: "",
      organisation: "",
    };
  },
  methods: {
    async getMedias() {
      try {
        let url = "http://127.0.0.1:5000/get_by_name/munier";

        for (let i in this.$route.params.path as Array<string>) {
          url += this.$route.params.path[i] + "/";
        }

        const response = await axios.get(url);

        this.items = response.data.files;
        this.title = response.data.event_name;
        this.organisation = response.data.association;
      } catch (error) {
        console.log(error);
      }
    },
  },
});
</script>
