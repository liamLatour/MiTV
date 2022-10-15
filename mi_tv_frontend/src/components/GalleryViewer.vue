<template>
  <div
    class="grid"
    v-bind:style="{ 'grid-template-columns': 'repeat(' + columns + ', 1fr)' }"
  >
    <div class="overflow-hidden m-0.5 bg-slate-500" v-if="isGlobal">
      <ImageItem
        source="http://127.0.0.1:5000/media_low_res/people_ref/liam.jpg"
        alt="image introuvable"
        class="cursor-pointer image-anim portrait"
      />
      <a
        href="/mes_photos"
        class="absolute flex items-center justify-center left-0 right-0 bottom-0 top-0 bg-black bg-opacity-50 transition-all duration-300 hover:bg-opacity-5 hover:text-transparent"
      >
        <h2 class="text-2xl">Mes Photos</h2>
      </a>
    </div>

    <div
      class="overflow-hidden m-0.5"
      v-for="(media, index) in medias"
      :key="media.path"
      v-bind:class="{ portrait: media.is_portrait }"
    >
      <span
        class="z-10 m-2 text-4xl opacity-60 absolute bottom-0 right-0"
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

  <div
    class="modal fixed flex flex-col z-30 left-0 top-0 w-full h-screen overflow-auto bg-black bg-opacity-70"
    v-if="showModal"
    @click="showModal = false"
    :class="{ small: medias[currentImg].others == null }"
  >
    <div class="h-12">
      <div class="absolute right-2 m-1 text-white text-3xl">
        <a
          :href="'http://127.0.0.1:5000/download/' + getModalImg()"
          class=""
          download
        >
          <font-awesome-icon
            icon="fa-solid fa-download"
            class="m-1 mr-4 hover:text-gray-300"
            v-on:click.stop
          />
        </a>
        <font-awesome-icon
          icon="fa-solid fa-times"
          class="m-1 mr-4 hover:text-gray-300 cursor-pointer"
          @click="showModal = false"
        />
      </div>
    </div>

    <div class="modal-content flex m-auto">
      <div class="imgContainer max-w-full max-h-full m-auto">
        <img
          :src="'http://127.0.0.1:5000/media/' + getModalImg()"
          alt="image introuvable"
          v-on:click.stop
          class="object-cover max-h-full max-w-full"
        />
      </div>
    </div>

    <div :class="{ 'h-5': medias[currentImg].others == null }" class="max-h-36">
      <div
        class="flex justify-center h-36"
        v-if="medias[currentImg].others != null"
      >
        <img
          v-for="path in medias[currentImg].others"
          :key="path"
          :src="'http://127.0.0.1:5000/media_low_res/' + path"
          class="h-full p-1 cursor-pointer image-anim"
          alt="image introuvable"
          @click="changeModalImage(path)"
          v-on:click.stop
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import ImageItem from "./ImageItem.vue";

export default defineComponent({
  name: "GalleryViewer",
  components: {
    ImageItem,
  },
  data: function () {
    return {
      showModal: false,
      currentImg: 0,
      modalImg: "",
      columns: 36,
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
      this.currentImg = index;
      this.showModal = true;
      this.modalImg = this.medias[index].path;
    },
    changeModalImage(path: string) {
      this.modalImg = path;
    },
    getModalImg() {
      return this.modalImg;
    },
    windowSizeChange() {
      console.log(window.innerWidth);
      let nb_columns = (window.innerWidth / 300) >> 0;
      this.columns = nb_columns;
    },
  },
});
</script>

<style scoped lang="scss">
.image-anim {
  transition: transform 0.4s;

  &:hover {
    -ms-transform: scale(1.1); /* IE 9 */
    -webkit-transform: scale(1.1); /* Safari 3-8 */
    transform: scale(1.1);
  }
}

.portrait {
  padding-left: 28%;
  padding-right: 28%;
}

.modal {
  .modal-content {
    height: calc(100% - 48px - 144px);

    .imgContainer {
      aspect-ratio: 3/2; //TODO: change that for portrait
    }
  }
}

.small {
  .modal-content {
    height: calc(100% - 48px - 20px);
  }
}
</style>
