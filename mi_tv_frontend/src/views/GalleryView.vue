<template>
  <div class="flex flex-col items-center mb-5 mt-10 sm:mt-16" v-if="!modifying">
    <h1 class="text-3xl sm:text-6xl">{{ event_name }}</h1>
    <h2 class="text-xl sm:text-2xl">{{ association }}</h2>
    <font-awesome-icon
      class="absolute text-3xl right-0 m-4 cursor-pointer hover:text-teal-400"
      icon="fa-solid fa-pen"
      @click="modifying = true"
      v-if="$cookies.isKey('login') && isGlobal"
    />
  </div>
  <div class="flex flex-col items-center mb-5 mt-10 sm:mt-16" v-else>
    <input
      class="text-3xl bg-transparent text-center border-b w-1/3 sm:text-6xl"
      type="text"
      id="fname"
      name="fname"
      v-model="event_name"
    />
    <input
      class="text-xl bg-transparent mt-4 text-center border-b w-1/3 sm:text-2xl"
      type="text"
      id="fname"
      name="fname"
      v-model="association"
    />
    <font-awesome-icon
      class="absolute text-3xl right-0 m-4 cursor-pointer hover:text-teal-400"
      icon="fa-solid fa-check"
      @click="modify"
      v-if="$cookies.isKey('login') && isGlobal"
    />
  </div>

  <GalleryViewer
    :medias="items"
    :is-global="isGlobal"
    :thumbnail="thumbnail"
    :exclude_thumbnail="exclude_thumbnail"
    v-if="isGlobal || is_registered"
  />
  <AiRegistration v-else />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import GalleryViewer from "../components/GalleryViewer.vue";
import AiRegistration from "../components/AiRegistration.vue";
import GetMediaService from "../services/GetMediaService";
import UpdateMetaService from "../services/UpdateMetaService";

export default defineComponent({
  name: "GalleryView",
  components: {
    GalleryViewer: GalleryViewer,
    AiRegistration: AiRegistration,
  },
  methods: {
    modify() {
      UpdateMetaService.updateMeta(
        {
          event_name: this.event_name,
          association: this.association,
        },
        this.$cookies.get("login"),
        "/update/" + this.media_url
      );
      this.modifying = false;
    },
  },
  created() {
    // If it is AI
    if (!this.isGlobal) {
      if (this.$cookies.isKey("uuid")) {
        this.is_registered = true;

        GetMediaService.getMedia("/get_by_uuid/" + this.$cookies.get("uuid"))
          .then((response) => {
            console.log(response.data);
            this.items = response.data.files;
            this.event_name = response.data.event_name;
            this.association = response.data.association;
            this.exclude_thumbnail = response.data.exlude_thumbnail == "true";
            this.thumbnail = response.data.thumbnail;
          })
          .catch((error) => {
            console.log(error);
          });
      }

      return;
    }

    for (let i in this.$route.params.path as Array<string>) {
      this.media_url += this.$route.params.path[i] + "/";
    }

    GetMediaService.getMedia(this.url + this.media_url)
      .then((response) => {
        console.log(response.data);
        this.items = response.data.files;
        this.event_name = response.data.event_name;
        this.association = response.data.association;
        this.exclude_thumbnail = response.data.exlude_thumbnail == "true";
        this.thumbnail = response.data.thumbnail;
      })
      .catch((error) => {
        console.log(error);
      });
  },
  props: {
    url: {
      type: String,
      default: "/architecture/",
    },
    isGlobal: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      items: {},
      media_url: "",
      event_name: "",
      association: "",
      exclude_thumbnail: false,
      thumbnail: "",
      modifying: false,
      is_registered: false,
    };
  },
});
</script>
