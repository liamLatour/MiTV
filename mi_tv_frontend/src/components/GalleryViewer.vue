<template>
  <h2 v-if="medias.length == 0" class="text-center text-4xl m-36 text-gray-500">
    Aucune Photos
  </h2>
  <div
    class="grid"
    v-bind:style="{ 'grid-template-columns': 'repeat(' + columns + ', 1fr)' }"
  >
    <div class="overflow-hidden m-0.5 bg-slate-500 aspect" v-if="isGlobal">
      <img
        src="../assets/camera.jpg"
        alt="image introuvable"
        class="object-cover h-full max-w-full cursor-pointer image-anim"
      />
      <router-link
        :to="'/mes_photos/' + media_url"
        class="absolute flex items-center justify-center left-0 right-0 bottom-0 top-0 bg-black bg-opacity-50 transition-all duration-300 hover:bg-opacity-5 hover:text-transparent"
      >
        <h2 class="text-2xl">Mes Photos</h2>
      </router-link>
    </div>

    <div
      class="overflow-hidden m-0.5 aspect"
      v-for="(media, index) in medias"
      :key="media.path"
      :id="media.path"
      v-bind:class="{
        portrait: media.is_portrait,
        hidden: exclude_thumbnail && media.path == thumbnail,
      }"
    >
      <span
        class="z-10 m-2 text-4xl opacity-80 absolute bottom-0 right-0"
        v-if="media.others != null"
      >
        <font-awesome-icon icon="fa-solid fa-folder" />
      </span>

      <ImageItem
        v-if="media.type == 'pic'"
        :source="'http://backend:5000/media_low_res/' + media.path"
        @click="openImage(index)"
        class="cursor-pointer image-anim"
      />

      <div v-else-if="media.type == 'vid'">
        <font-awesome-icon
          icon="fa-solid fa-film"
          class="z-10 m-2 text-4xl opacity-80 absolute bottom-0 right-0"
        />

        <ImageItem
          :source="'http://backend:5000/media_low_res/' + media.path"
          alt="image introuvable"
          @click="openVideo(index)"
          class="cursor-pointer image-anim"
        />
      </div>

      <div v-if="media.type == 'dir'">
        <ImageItem
          :source="'http://backend:5000/media_low_res/' + media.thumbnail"
          alt="image introuvable"
          class="cursor-pointer image-anim"
        />
        <router-link
          :to="'/photos/' + media.path"
          class="absolute flex items-center justify-center left-0 right-0 bottom-0 top-0 bg-black bg-opacity-50 transition-all duration-300 hover:bg-opacity-5 hover:text-transparent"
        >
          <h2 class="text-2xl">
            {{ media.event_name }}
          </h2>
        </router-link>
      </div>
    </div>
  </div>

  <ImageModal
    :images="modalImages"
    :show="showModal"
    @close="showModal = false"
  />
  <VideoModal
    :video="modalVideo"
    :show="showVModal"
    @close="showVModal = false"
  />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import ImageItem from "./ImageItem.vue";
import ImageModal from "./ImageModal.vue";
import VideoModal from "./VideoModal.vue";

export default defineComponent({
  name: "GalleryViewer",
  components: {
    ImageItem,
    ImageModal,
    VideoModal,
  },
  data: function () {
    return {
      showModal: false,
      modalImages: [] as Array<string>,
      showVModal: false,
      modalVideo: "",
      columns: 1,
      media_url: "",
    };
  },
  props: {
    medias: {
      type: Object,
      required: true,
    },
    isGlobal: {
      type: Boolean,
      default: false,
    },
    exclude_thumbnail: {
      type: Boolean,
      default: false,
    },
    thumbnail: {
      type: String,
      default: "",
    },
  },
  created() {
    for (let i in this.$route.params.path as Array<string>) {
      this.media_url += this.$route.params.path[i] + "/";
    }

    window.addEventListener("resize", this.windowSizeChange);
    this.windowSizeChange();
  },
  unmounted() {
    window.removeEventListener("resize", this.windowSizeChange);
  },
  methods: {
    openImage(i: string) {
      let index: number = parseInt(i);
      this.showModal = true;

      if (this.medias[index].others == null) {
        this.modalImages = [this.medias[index].path];
      } else {
        this.modalImages = this.medias[index].others;
      }
    },
    openVideo(i: string) {
      let index: number = parseInt(i);

      this.showVModal = true;
      this.modalVideo = this.medias[index].path;
    },
    windowSizeChange() {
      this.columns = (window.innerWidth / 300) >> 0;
    },
  },
});
</script>

<style lang="scss">
.aspect {
  aspect-ratio: 3/2;
}

.image-anim {
  transition: transform 0.4s;

  &:hover {
    -ms-transform: scale(1.1); /* IE 9 */
    -webkit-transform: scale(1.1); /* Safari 3-8 */
    transform: scale(1.1);
  }
}
</style>
