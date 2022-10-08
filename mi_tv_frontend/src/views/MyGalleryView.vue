<template>
  <div class="header">
    <h1 class="eventname">{{ title }}</h1>
    <h2 class="organisation">{{ organisation }}</h2>
  </div>
  <GalleryViewer :medias="items" :isglobal="false" />
</template>

<script lang="ts">
import GalleryViewer from "../components/GalleryViewer.vue";
import axios from "axios";

export default {
  name: "GalleryView",
  components: {
    GalleryViewer: GalleryViewer,
  },
  created() {
    this.getMedias();
  },
  methods: {
    async getMedias() {
      try {
        let url = "http://127.0.0.1:5000/get_by_name/";

        for (let i in this.$route.params.path) {
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
  data() {
    return {
      items: {},
      title: "",
      organisation: "",
    };
  },
};
</script>

<style lang="scss">
.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;

  .eventname {
    font-size: 70px;
  }
}
</style>
