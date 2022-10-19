<template>
  <div
    class="grid"
    v-bind:style="{ 'grid-template-columns': 'repeat(' + columns + ', 1fr)' }"
  >
    <div class="overflow-hidden m-0.5 bg-slate-500 aspect" v-if="isGlobal">
      <ImageItem
        source="http://127.0.0.1:5000/media_low_res/people_ref/liam.jpg"
        alt="image introuvable"
        class="cursor-pointer image-anim"
      />
      <a
        href="/mes_photos"
        class="absolute flex items-center justify-center left-0 right-0 bottom-0 top-0 bg-black bg-opacity-50 transition-all duration-300 hover:bg-opacity-5 hover:text-transparent"
      >
        <h2 class="text-2xl">Mes Photos</h2>
      </a>
    </div>

    <div
      class="overflow-hidden m-0.5 aspect"
      v-for="(media, index) in medias"
      :key="media.path"
      v-bind:class="{ portrait: media.is_portrait }"
    >
      <span
        class="z-10 m-2 text-4xl opacity-80 absolute bottom-0 right-0"
        v-if="media.others != null"
      >
        <font-awesome-icon icon="fa-solid fa-folder" />
      </span>

      <ImageItem
        v-if="media.type == 'pic'"
        :source="'http://127.0.0.1:5000/media_low_res/' + media.path"
        @click="openImage(index)"
        class="cursor-pointer image-anim"
      />

      <div v-else-if="media.type == 'vid'">
        <font-awesome-icon
          icon="fa-solid fa-film"
          class="z-10 m-2 text-4xl opacity-80 absolute bottom-0 right-0"
        />

        <ImageItem
          :source="'http://127.0.0.1:5000/media_low_res/' + media.path"
          alt="image introuvable"
          class="cursor-pointer image-anim"
        />
      </div>

      <div v-if="media.type == 'dir'">
        <ImageItem
          :source="'http://127.0.0.1:5000/media_low_res/' + media.thumbnail"
          alt="image introuvable"
          class="cursor-pointer image-anim"
        />
        <a
          :href="media.path"
          class="absolute flex items-center justify-center left-0 right-0 bottom-0 top-0 bg-black bg-opacity-50 transition-all duration-300 hover:bg-opacity-5 hover:text-transparent"
        >
          <h2 class="text-2xl">
            {{ media.event_name }}
          </h2>
        </a>
      </div>
    </div>
  </div>

  <ImageModal
    :images="modalImages"
    :show="showModal"
    @close="showModal = false"
  />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import ImageItem from "./ImageItem.vue";
import ImageModal from "./ImageModal.vue";

export default defineComponent({
  name: "GalleryViewer",
  components: {
    ImageItem,
    ImageModal,
  },
  data: function () {
    return {
      showModal: false,
      modalImages: [] as Array<string>,
      columns: 1,
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
  },
  created() {
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
